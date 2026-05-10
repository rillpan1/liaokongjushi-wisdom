// @ts-check
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '了空居士智慧',
  description: '了空居士智慧知识库 —— 系统性结构化智慧体系',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  ignoreDeadLinks: true,
  base: '/',

  head: [
    ['link', { rel: 'icon', href: '/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#1A2332' }],
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '核心模型', link: '/10-核心模型/10-核心模型_INDEX' },
      { text: '专题研究', link: '/20-专题研究/20-专题研究_INDEX' },
      { text: '学习路径', link: '/30-学习路径/30-学习路径_INDEX' },
      { text: '金句', link: '/40-原话金句/40-原话金句_INDEX' },
      { text: '概念', link: '/50-概念资料/50-概念资料_INDEX' },
      { text: 'AI 助手', link: '/ai-assistant' },
      { text: '关于', link: '/00-创始人/biography-了空居士' },
    ],

    sidebar: {
      '/': [
        {
          text: '核心模型',
          collapsible: true, collapsed: true,
          items: [
            { text: '🌐 整体观（元方法）', link: '/10-核心模型/meta-整体观' },
            { text: '🌍 天人合一', link: '/10-核心模型/model-天人合一' },
            { text: '🧘 对境不住', link: '/10-核心模型/model-对境不住' },
            { text: '👐 对法不执', link: '/10-核心模型/model-对法不执' },
            { text: '⚡ 自然务实', link: '/10-核心模型/model-自然务实' },
            { text: '🌊 圆融中和', link: '/10-核心模型/model-圆融中和' },
            { text: '🔥 历境炼心', link: '/10-核心模型/model-历境炼心' },
            { text: '💪 性命双修', link: '/10-核心模型/model-性命双修' },
          ],
        },
        {
          text: '专题研究',
          collapsible: true, collapsed: true,
          items: [
            { text: '如何面对焦虑', link: '/20-专题研究/topic-焦虑' },
            { text: '如何处理情绪', link: '/20-专题研究/topic-情绪' },
            { text: '如何处理人际关系', link: '/20-专题研究/topic-人际关系' },
            { text: '如何做出选择', link: '/20-专题研究/topic-选择' },
            { text: '如何面对拖延与行动', link: '/20-专题研究/topic-拖延与行动' },
            { text: '如何面对失败', link: '/20-专题研究/topic-面对失败' },
            { text: '如何做到包容与接纳', link: '/20-专题研究/topic-包容与接纳' },
            { text: '如何面对婚姻关系', link: '/20-专题研究/topic-婚姻关系' },
            { text: '如何面对疾病与健康', link: '/20-专题研究/topic-疾病与健康' },
            { text: '如何看待财富与布施', link: '/20-专题研究/topic-财富与布施' },
            { text: '如何面对忍辱与原谅', link: '/20-专题研究/topic-忍辱与原谅' },
            { text: '如何面对生死', link: '/20-专题研究/topic-生死观' },
            { text: '如何面对孤独', link: '/20-专题研究/topic-孤独' },
            { text: '如何修感恩之心', link: '/20-专题研究/topic-感恩' },
            { text: '如何教育子女', link: '/20-专题研究/topic-亲子教育' },
            { text: '如何开始实修', link: '/20-专题研究/topic-入门实修' },
            { text: '在工作中修行', link: '/20-专题研究/topic-工作修行' },
            { text: '如何做到自律与坚持', link: '/20-专题研究/topic-自律与坚持' },
            { text: '如何在日常生活中保持正念', link: '/20-专题研究/topic-日常正念' },
            { text: '修行进阶', link: '/20-专题研究/topic-修行进阶' },
            { text: '🏠 家庭教育体系', link: '/20-专题研究/topic-家庭教育体系' },
          ],
        },
        {
          text: '学习路径',
          collapsible: true, collapsed: true,
          items: [
            { text: '认知路径', link: '/30-学习路径/path-认知路径' },
            { text: '问题路径', link: '/30-学习路径/path-问题路径' },
            { text: '新手入门', link: '/30-学习路径/path-新手入门' },
          ],
        },
        {
          text: '原话金句',
          collapsible: true, collapsed: true,
          items: [
            { text: '金刚经', link: '/40-原话金句/quote-金刚经' },
            { text: '道德经', link: '/40-原话金句/quote-道德经' },
            { text: '心经', link: '/40-原话金句/quote-心经' },
            { text: '中论丹道', link: '/40-原话金句/quote-中论丹道' },
            { text: '答疑精选', link: '/40-原话金句/quote-答疑精选' },
            { text: '7大模型金句索引', link: '/40-原话金句/quote-按模型索引' },
          ],
        },
        {
          text: '概念资料',
          collapsible: true, collapsed: true,
          items: [
            { text: '佛家', link: '/50-概念资料/dict-清净心' },
            { text: '道家', link: '/50-概念资料/dict-自然' },
            { text: '儒家', link: '/50-概念资料/dict-仁' },
            { text: '丹道', link: '/50-概念资料/dict-丹田' },
          ],
        },
        {
          text: '关于',
          collapsible: true, collapsed: true,
          items: [
            { text: '了空居士简介', link: '/00-创始人/biography-了空居士' },
            { text: '独特贡献', link: '/00-创始人/contribution-独特贡献' },
            { text: 'AI 助手', link: '/ai-assistant' },
          ],
        },
      ],

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
            { text: '如何面对拖延与行动', link: '/20-专题研究/topic-拖延与行动' },
            { text: '如何面对失败', link: '/20-专题研究/topic-面对失败' },
            { text: '如何做到包容与接纳', link: '/20-专题研究/topic-包容与接纳' },
            { text: '如何面对婚姻关系', link: '/20-专题研究/topic-婚姻关系' },
            { text: '如何面对疾病与健康', link: '/20-专题研究/topic-疾病与健康' },
            { text: '如何看待财富与布施', link: '/20-专题研究/topic-财富与布施' },
            { text: '如何面对忍辱与原谅', link: '/20-专题研究/topic-忍辱与原谅' },
            { text: '如何面对生死', link: '/20-专题研究/topic-生死观' },
            { text: '如何面对孤独', link: '/20-专题研究/topic-孤独' },
            { text: '如何修感恩之心', link: '/20-专题研究/topic-感恩' },
            { text: '如何教育子女', link: '/20-专题研究/topic-亲子教育' },
          ],
        },
        {
          text: '实践指导',
          items: [
            { text: '如何开始实修', link: '/20-专题研究/topic-入门实修' },
            { text: '在工作中修行', link: '/20-专题研究/topic-工作修行' },
            { text: '如何做到自律与坚持', link: '/20-专题研究/topic-自律与坚持' },
            { text: '如何在日常生活中保持正念', link: '/20-专题研究/topic-日常正念' },
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
          text: '佛家（13）',
          items: [
            { text: '清净心', link: '/50-概念资料/dict-清净心' },
            { text: '烦恼', link: '/50-概念资料/dict-烦恼' },
            { text: '观照', link: '/50-概念资料/dict-观照' },
            { text: '菩提', link: '/50-概念资料/dict-菩提' },
            { text: '我执', link: '/50-概念资料/dict-我执' },
            { text: '法执', link: '/50-概念资料/dict-法执' },
            { text: '无明', link: '/50-概念资料/dict-无明' },
            { text: '止观', link: '/50-概念资料/dict-止观' },
            { text: '顽空', link: '/50-概念资料/dict-顽空' },
            { text: '般若', link: '/50-概念资料/dict-般若' },
            { text: '自性', link: '/50-概念资料/dict-自性' },
            { text: '涅槃', link: '/50-概念资料/dict-涅槃' },
            { text: '不二', link: '/50-概念资料/dict-不二' },
          ],
        },
        {
          text: '道家（6）',
          items: [
            { text: '自然', link: '/50-概念资料/dict-自然' },
            { text: '无为', link: '/50-概念资料/dict-无为' },
            { text: '柔弱', link: '/50-概念资料/dict-柔弱' },
            { text: '守中', link: '/50-概念资料/dict-守中' },
            { text: '和光同尘', link: '/50-概念资料/dict-和光同尘' },
            { text: '道', link: '/50-概念资料/dict-道' },
          ],
        },
        {
          text: '儒家（10）',
          items: [
            { text: '孝', link: '/50-概念资料/dict-孝' },
            { text: '敬', link: '/50-概念资料/dict-敬' },
            { text: '恕', link: '/50-概念资料/dict-恕' },
            { text: '处世', link: '/50-概念资料/dict-处世' },
            { text: '家庭道场', link: '/50-概念资料/dict-家庭道场' },
            { text: '礼', link: '/50-概念资料/dict-礼' },
            { text: '正', link: '/50-概念资料/dict-正' },
            { text: '义', link: '/50-概念资料/dict-义' },
            { text: '仁', link: '/50-概念资料/dict-仁' },
            { text: '平常心', link: '/50-概念资料/dict-平常心' },
          ],
        },
        {
          text: '丹道（9）',
          items: [
            { text: '丹田', link: '/50-概念资料/dict-丹田' },
            { text: '任脉', link: '/50-概念资料/dict-任脉' },
            { text: '督脉', link: '/50-概念资料/dict-督脉' },
            { text: '小周天', link: '/50-概念资料/dict-小周天' },
            { text: '大周天', link: '/50-概念资料/dict-大周天' },
            { text: '炼精化气', link: '/50-概念资料/dict-炼精化气' },
            { text: '炼气化神', link: '/50-概念资料/dict-炼气化神' },
            { text: '炼神还虚', link: '/50-概念资料/dict-炼神还虚' },
            { text: '形神俱妙', link: '/50-概念资料/dict-形神俱妙' },
          ],
        },
        {
          text: '其他（2）',
          items: [
            { text: '不住', link: '/50-概念资料/dict-不住' },
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

    outlineTitle: '在这页',
    sidebarMenuLabel: '菜单',

    footer: {
      message: '基于了空居士 125 篇著述 · 由AI系统性结构化智慧体系 · 未经了空居士本人审核',
      copyright: '了空居士智慧宝库，明树制作',
    },
  },
})
