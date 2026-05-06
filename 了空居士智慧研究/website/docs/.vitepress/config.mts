// @ts-check
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '了空居士智慧',
  description: '了空居士智慧知识库 —— 系统性结构化智慧体系',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'icon', href: '/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#2c3e50' }],
  ],

  themeConfig: {
    logo: '/favicon.svg',

    nav: [
      { text: '首页', link: '/' },
      { text: '核心模型', link: '/10-核心模型/' },
      { text: '专题研究', link: '/20-专题研究/' },
      { text: '学习路径', link: '/30-学习路径/' },
      { text: '原话金句', link: '/40-原话金句/' },
      { text: '概念词典', link: '/50-概念资料/' },
    ],

    sidebar: {
      '/10-核心模型/': [
        {
          text: '核心心智模型',
          items: [
            { text: '🌍 天人合一', link: '/10-核心模型/model-天人合一' },
            { text: '🧘 对境不住', link: '/10-核心模型/model-对境不住' },
            { text: '👐 对法不执', link: '/10-核心模型/model-对法不执' },
            { text: '⚡ 自然务实', link: '/10-核心模型/model-自然务实' },
            { text: '🌊 圆融中和', link: '/10-核心模型/model-圆融中和' },
            { text: '🔥 历境炼心', link: '/10-核心模型/model-历境炼心' },
            { text: '💪 性命双修', link: '/10-核心模型/model-性命双修' },
          ],
        },
      ],

      '/20-专题研究/': [
        {
          text: '问题分析',
          items: [
            { text: '如何面对焦虑', link: '/20-专题研究/topic-焦虑' },
            { text: '如何处理情绪', link: '/20-专题研究/topic-情绪' },
            { text: '如何处理人际关系', link: '/20-专题研究/topic-人际关系' },
            { text: '如何做出选择', link: '/20-专题研究/topic-选择' },
            { text: '如何面对疾病与健康', link: '/20-专题研究/topic-疾病与健康' },
            { text: '如何看待财富与布施', link: '/20-专题研究/topic-财富与布施' },
            { text: '如何面对忍辱与原谅', link: '/20-专题研究/topic-忍辱与原谅' },
            { text: '如何面对生死', link: '/20-专题研究/topic-生死观' },
            { text: '如何教育子女', link: '/20-专题研究/topic-亲子教育' },
          ],
        },
        {
          text: '实践指导',
          items: [
            { text: '如何开始实修', link: '/20-专题研究/topic-入门实修' },
            { text: '在工作中修行', link: '/20-专题研究/topic-工作修行' },
            { text: '修行进阶', link: '/20-专题研究/topic-修行进阶' },
          ],
        },
        {
          text: '体系构建',
          items: [
            { text: '🏠 家庭教育体系', link: '/20-专题研究/topic-家庭教育体系' },
          ],
        },
      ],

      '/30-学习路径/': [
        {
          text: '学习路线',
          items: [
            { text: '认知路径', link: '/30-学习路径/path-认知路径' },
            { text: '问题路径', link: '/30-学习路径/path-问题路径' },
            { text: '新手入门', link: '/30-学习路径/path-新手入门' },
          ],
        },
      ],

      '/40-原话金句/': [
        {
          text: '按经典索引',
          items: [
            { text: '金刚经', link: '/40-原话金句/quote-金刚经' },
            { text: '道德经', link: '/40-原话金句/quote-道德经' },
            { text: '心经', link: '/40-原话金句/quote-心经' },
            { text: '中论丹道', link: '/40-原话金句/quote-中论丹道' },
            { text: '答疑精选', link: '/40-原话金句/quote-答疑精选' },
          ],
        },
        {
          text: '按模型索引',
          items: [
            { text: '7大模型金句索引', link: '/40-原话金句/quote-按模型索引' },
          ],
        },
      ],

      '/50-概念资料/': [
        {
          text: '佛学概念',
          items: [
            { text: '清净心', link: '/50-概念资料/dict-清净心' },
            { text: '顽空', link: '/50-概念资料/dict-顽空' },
            { text: '我执', link: '/50-概念资料/dict-我执' },
            { text: '法执', link: '/50-概念资料/dict-法执' },
            { text: '无明', link: '/50-概念资料/dict-无明' },
            { text: '烦恼', link: '/50-概念资料/dict-烦恼' },
            { text: '菩提', link: '/50-概念资料/dict-菩提' },
            { text: '涅槃', link: '/50-概念资料/dict-涅槃' },
            { text: '观照', link: '/50-概念资料/dict-观照' },
            { text: '止观', link: '/50-概念资料/dict-止观' },
          ],
        },
        {
          text: '丹道概念',
          items: [
            { text: '小周天', link: '/50-概念资料/dict-小周天' },
            { text: '大周天', link: '/50-概念资料/dict-大周天' },
            { text: '任脉', link: '/50-概念资料/dict-任脉' },
            { text: '督脉', link: '/50-概念资料/dict-督脉' },
            { text: '丹田', link: '/50-概念资料/dict-丹田' },
            { text: '炼精化气', link: '/50-概念资料/dict-炼精化气' },
            { text: '炼气化神', link: '/50-概念资料/dict-炼气化神' },
            { text: '炼神还虚', link: '/50-概念资料/dict-炼神还虚' },
            { text: '形神俱妙', link: '/50-概念资料/dict-形神俱妙' },
          ],
        },
        {
          text: '心法概念',
          items: [
            { text: '不二', link: '/50-概念资料/dict-不二' },
            { text: '平常心', link: '/50-概念资料/dict-平常心' },
            { text: '不住', link: '/50-概念资料/dict-不住' },
            { text: '无为', link: '/50-概念资料/dict-无为' },
            { text: '自然', link: '/50-概念资料/dict-自然' },
            { text: '中道', link: '/50-概念资料/dict-中道' },
          ],
        },
      ],
    },

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索', buttonAriaLabel: '搜索知识库' },
              modal: { noResultsText: '未找到相关内容', resetButtonTitle: '清除' },
            },
          },
        },
      },
    },

    footer: {
      message: '基于 了空居士 125 篇著述 · 200+ 模型原子 · 五层结构',
      copyright: '知识库持续更新中',
    },
  },
})
