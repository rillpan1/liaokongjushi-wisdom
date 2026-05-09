#!/usr/bin/env python3
"""FastAPI server for 了空居士 AI 助手 — RAG + DeepSeek + Auth."""
from __future__ import annotations

import os
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

import numpy as np
import httpx
import jwt
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# ── Config ──────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"
CHUNKS_FILE = DATA_DIR / "chunks.json"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.npy"
DB_FILE = DATA_DIR / "users.db"

JWT_SECRET = os.environ.get("JWT_SECRET", "liaokongjushi-2026-ai-secret")
JWT_ALGO = "HS256"
JWT_EXPIRY_HOURS = 24

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# ── Globals (singletons) ───────────────────────────────────────────────
_chunks: list | None = None
_embeddings: np.ndarray | None = None
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def load_data():
    global _chunks, _embeddings
    if _chunks is None:
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            _chunks = json.load(f)
        _embeddings = np.load(EMBEDDINGS_FILE)
    return _chunks, _embeddings


# ── Database ────────────────────────────────────────────────────────────
def init_db():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_FILE))
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )"""
    )
    conn.commit()
    conn.close()


def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(str(DB_FILE))
    row = conn.execute(
        "SELECT password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return row is not None and row[0] == hash_pw(password)


def create_user(username: str, password: str):
    conn = sqlite3.connect(str(DB_FILE))
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_pw(password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(400, "用户已存在")
    finally:
        conn.close()


def user_count() -> int:
    conn = sqlite3.connect(str(DB_FILE))
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return count


# ── Auth helpers ────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


def make_token(username: str) -> str:
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        },
        JWT_SECRET,
        algorithm=JWT_ALGO,
    )


def require_user(authorization: str | None = None) -> str:
    if not authorization:
        raise HTTPException(401, "未登录")
    try:
        payload = jwt.decode(
            authorization.replace("Bearer ", ""), JWT_SECRET, algorithms=[JWT_ALGO]
        )
        return payload["username"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "登录已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "无效的登录凭证")


# ── FastAPI app ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    try:
        load_data()
        print(f"Loaded {len(_chunks)} chunks")
    except FileNotFoundError:
        print("WARNING: chunks.json or embeddings.npy not found — run preprocess.py")
    if user_count() == 0:
        create_user("admin", "password123")
        print("Created default admin user (admin / password123)")
    yield


app = FastAPI(title="了空居士AI助手", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Auth endpoints ──────────────────────────────────────────────────────
@app.post("/api/auth/login")
def login(req: LoginRequest):
    if verify_user(req.username, req.password):
        return {"token": make_token(req.username), "username": req.username}
    raise HTTPException(401, "用户名或密码错误")


@app.get("/api/auth/check")
def check_auth(request: Request):
    username = require_user(request.headers.get("Authorization"))
    return {"username": username, "ok": True}


# ── RAG ─────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str


SYSTEM_PROMPT = """你是一个基于"了空居士智慧"知识库的AI助手。你的回答风格：

1. 优先根据提供的知识库内容回答；如果知识库未涵盖，可以结合自身知识补充
2. 引用知识库内容时注明来源（如"来源：xxx"）；自身补充部分请明确说明
3. 回答简洁有层次，使用中文
4. 如果问题与了空居士或修行完全无关，礼貌告知知识范围
5. 了空居士体系融合佛家、道家、儒家、丹道四家

以下是知识库中与用户问题相关的内容："""


def search_context(query: str, top_k: int = 5):
    """Vector search — return (results_list, context_string)."""
    chunks, embeddings = load_data()
    model = get_model()

    query_vec = model.encode([query], normalize_embeddings=True)
    scores = np.dot(embeddings, query_vec.T).squeeze()
    top_idx = np.argsort(scores)[-top_k:][::-1]

    results = []
    context_parts = []
    for i, idx in enumerate(top_idx):
        score = float(scores[idx])
        if score < 0.2:
            continue
        chunk = chunks[idx]
        source = chunk.get("source", "未知来源")
        text = chunk["text"][:1000]
        context_parts.append(f"[{i+1}] 来源: {source}\n{text}")
        results.append({**chunk, "score": score})

    if not context_parts:
        return [], "知识库中未找到直接相关的引用内容。请结合自身知识回答。"

    return results, "\n\n---\n\n".join(context_parts)


async def stream_deepseek(messages: list):
    """SSE stream from DeepSeek."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "stream": True,
                "temperature": 0.7,
                "max_tokens": 2048,
            },
        ) as resp:
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                    content = (
                        obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    )
                    if content:
                        yield f"data: {json.dumps({'content': content})}\n\n"
                except json.JSONDecodeError:
                    continue
    yield "data: [DONE]\n\n"


@app.post("/api/chat")
async def chat(req: ChatRequest, request: Request):
    require_user(request.headers.get("Authorization"))

    results, context = search_context(req.message)
    system_msg = SYSTEM_PROMPT + "\n\n" + context

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": req.message},
    ]

    return StreamingResponse(
        stream_deepseek(messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3001)
