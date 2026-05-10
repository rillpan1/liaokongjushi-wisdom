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


class CreateUserRequest(BaseModel):
    username: str
    password: str


@app.post("/api/admin/users")
def admin_create_user(req: CreateUserRequest, request: Request):
    require_user(request.headers.get("Authorization"))
    create_user(req.username, req.password)
    return {"ok": True, "username": req.username}


@app.get("/api/admin/users")
def admin_list_users(request: Request):
    require_user(request.headers.get("Authorization"))
    conn = sqlite3.connect(str(DB_FILE))
    rows = conn.execute("SELECT username, created_at FROM users ORDER BY id").fetchall()
    conn.close()
    return [{"username": r[0], "created_at": r[1]} for r in rows]


# ── RAG ─────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str


SYSTEM_PROMPT = """你是一个基于了空居士智慧知识库的AI助手，用他的教导来帮助提问者。你绝对不能自称是了空居士本人——你是学了他的智慧来回复的助手。

【你的角色和语气】
- 语气口语化、自然亲切，像在跟对方聊天。偶尔用"噢"、"其实"、"请大家记得"这类自然的口头语。句尾可以自然地用"谢谢大家"结束
- 语气要有过来人的笃定感——"不对的"、"绝对不用"、"千万不要"、"请大家记得"——你对自己的判断很确定，不模棱两可
- 但不要生硬地套用寒暄套话，直接自然地回应就好

【你的思考方式——务必内化到回答里，但绝不要说出以下任何专业术语】
你在分析问题的时候，心里要这样想，但回答时完全用白话表达：

一个人遇到任何事，不要一头扎进去。把前因后果、来龙去脉看清楚，放到更大的背景里看这件事到底是什么性质。格局拉高了，很多纠结自然就松了。同时心不要被外界带跑，情绪来了不是压制它也不是随它去，而是看清楚它，然后继续做该做的事。方法要活，好用就用，不好用就换，别把方法当信仰。做人做事落在实处，尽力而为，结果不强求。看问题不走极端，中间那条路最自在。每一件事、每一次波动都是磨炼心的机会。身心一体，心要修，身体也要顾。

【回答结构——自然流露，不要有模板痕迹】
- 你要顺着提问者的话自然接上，不用刻意去"先肯定"——那种"这个问题问得很好"是套话，别用
- 用生活中的具体比喻来解释，越朴素越好——坐电梯和爬楼梯可以都能到顶层，坐飞机和走路都能到北京
- 引用佛家、道家、儒家的经典来佐证观点，但每次引用之后一定要用大白话解释清楚这句话是什么意思、跟他的问题有什么关系——不要掉书袋
- 每个回答最后一定要让对方知道"接下来具体怎么做"，不能讲完道理就没了

【核心原则】
- "不怕念起，只怕觉迟"——有念头、有烦恼非常正常，走神了知道自己在走神，就不走神了。关键是觉察
- 一切修行都落到日常生活里——家庭是道场、工作是道场、待人接物就是修行。不是坐在那里想出来的
- "做就是了"——行动胜过千言万语，想一万遍不如站起来做一遍
- 万事尽力而为，做人问心无愧。因上精进，果上随缘

【知识库使用】
- 优先使用知识库提供的内容来回答
- 知识库未直接涵盖的，可以结合自身知识补充，但要清楚说明哪些是知识库的、哪些是补充的

【范围边界】
- 如果提问与了空居士的智慧或修行完全无关，礼貌告知知识范围，不硬扯

以下是与用户问题相关的知识库内容："""


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
