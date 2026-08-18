---
name: polishing-chinese-prose
description: >
  The canonical Chinese-prose authority — checkable rules for Chinese output, in two bands. 翻译腔 band (R14–R20: active voice, no vague modifiers, sentence-splitting, unambiguous pronouns, consistent terminology, 的/地/得, consistent persona) + 文牍腔 band (R33–R39: verbs over noun-stacks, no self-coined abbreviations, ≤1 arrow-chain per paragraph, ≤1 parenthetical per sentence, the read-aloud test, term-preservation with human prose, no self-coined concept-terms / metaphor-as-jargon) + an EN→zh term table. Use when authoring/reviewing Chinese deliverables, reviewing the README_zh mirror's fluency, or when an agent replies to the user in Chinese. Other skills cite this by name as the prose authority; it does not restate their rules.
allowed-tools: Read, Grep, Glob
---

# Polishing Chinese Prose (the canonical Chinese-prose authority)

The single home for **checkable Chinese-prose rules**. Other skills (`publishing-deliverables`,
`readme-style`, `structuring-solution-docs`) **cite this skill by name** as the prose authority — they do not
restate the rules, and this skill does not restate theirs. **Generic content**, zero project/identity values
(skill_spec §9).

> **This skill is the authority/spec — not the runtime enforcement surface.** Skills are invoked on demand; the
> always-on reach over agent dialogue (the 文牍腔 band below) is carried by the consuming project's memory
> (`speak-plain-chinese`), which this skill **codifies**. Read this file as the canonical standard the memory points at.

## Two activation classes

- **R14–R20 (翻译腔 / translation-ese): instance-activated.** Turns on via the business-repo instance language
  switch — only when the project's language policy assigns Chinese to outward deliverables
  (`technical-report-style.md` R13). Applies to outward-deliverable Chinese body, **and** to the `README_zh.md`
  mirror's fluency review (the R32 advisory rubric, see `readme-style.md`).
- **R33–R39 (文牍腔 / bureaucratese): agent-layer always-on.** NOT gated by the deliverable-language switch. They
  apply **whenever an agent replies to the user in Chinese** — agent dialogue is not a deliverable, so the
  deliverable switch would miss exactly the case the user complained about (the complaint target is *conversation*,
  not an artifact). 适用范围**点名 agent 的中文会话语体**；中文交付物是其超集，也适用。

写完逐条自检。

## 翻译腔段（R14–R20）—— 治"翻译腔/不通顺"

- R14. **主动语态优先**，少用"被字句"。注意中文"被"≠英文被动式，机翻常滥用。
  反例「假如此软件尚未*被*安装」→ 正例「假如*尚未安装*这个软件」。
- R15. **不用模糊程度词**，用具体数据/阈值代替（与"用具体数据代替模糊量"的报告体规则同源）。反例「准确率提升了*数倍*/*很大*」→
  正例「准确率从 87% 提升到 95%」。
- R16. **长难句断句**：一句话只表达一个完整意思；从句堆叠/超过约 40 字就拆成短句。
- R17. **代词指代必须无歧义**：当"它/其/该"可能指向多个对象时，直接写出具体名词。
- R18. **术语全文统一**：同一概念全文用同一译名/写法，不混用（如"关键点"不与"特征点/landmark"混写；
  首次出现可中英并注，之后固定一种）。配套术语表见文末。
- R19. **的/地/得 用法正确**；删冗余虚词（"进行/予以/的话/方面"等可省即省）。
- R20. **人称与口吻统一**：技术报告用客观陈述，不夹"我觉得/大概"；全文人称一致。

## 文牍腔段（R33–R39）—— agent 层 always-on，治"不是人话"

> 治**文牍腔**（不是翻译腔，R14–R20 管翻译腔）：名词堆串、自造缩略语、箭头流水账、括号补注成灾，读起来像电报不像人说话。
> **agent 用中文回复用户时一律适用**，不受交付物语言开关门控（见上文）。规则来自团队用户反馈；R33 理论框架引自余光中《中文的常态与变态》。

- R33. **动词优先于名词串。** 把动作写成动词谓语，别压成名词堆。抽象名词不做主语——用人或事做主语。
  反例「已**入账派工**」「完成**盘验收账**」→ 正例「我把账记了，活派给 X 了」「我自己查过、收到了」。
  （余光中《中文的常态与变态》：名词化是恶性西化，中文的活力在动词与短句。）
- R34. **自造缩略语禁用，给替换表。** 不自己生造双字缩略词。**保留 vs 替换**——必要专名保留，自造缩略语替换：

  | 自造缩略语（禁用） | 说人话 |
  |---|---|
  | 盘验 | 我自己查过了 / 核对过了 |
  | 坐实 | 确认了 |
  | 折入 | 写进去了 / 并进去了 |
  | 入账 | 记下了 / 收到并记下 |
  | 派工 | 把活派给了 X |
  | 收账 | 收到了 |

  表是**种子**，按真实出现的造词继续加；判据见 R37。专名（Gate-2、compliance、pin、tag、版本门）不在此列，保留。
- R35. **箭头链每段最多一处。** `A→B→C` 这种流水账一段只许一处；再多就拆成句子，把先后写清楚。
- R36. **括号补注每句最多一个。** 满屏 `（…）` 补注是文牍腔标志；一句话最多留一个括号，能去就去，重要的补注提升为正文句子。
- R37. **「念出来测试」终检（总闸）。** 写完每句问：这句话当面跟人说，会不会这么说？不会就重写。R33–R36 是症状，R37 是判据。
  正例语体参考——一句把激活模型讲清的人话：「文牍腔段只要 agent 用中文回复用户就适用，不看项目交付物是什么语言。」（自然、无名词堆、无箭头）。
- R38. **术语保留与人话连接并存。** 必要专名（Gate-2、compliance、pin、版本门、tag）不强翻、不强拆；但**连接这些专名的话必须是人话**。表格仍可用于多任务状态盘点，但表格外的叙述句要自然。
- R39. **自造概念词 / 比喻命名禁直接进对人输出。** R34 治自造缩略语；R39 治更上一层的自造概念词和比喻命名。三条：
  1. **先用大白话把现象讲清，再谈命名。** 新概念第一次出现必须先描述它指的是什么现象，不能甩一个生造的名字让人猜。
  2. **要命名，名字后面必须紧跟一句定义。** 比如先讲清现象再命名：「这次改动让一部分本该报错的样本被压住、当前测试集又恰好测不到，于是这笔代价看不见——可以叫它『隐性代价』，也就是改动引入了但现有测试覆盖不到的损失」，而不是张口先甩一个生造名词让人猜。
  3. **比喻不当术语用。** 借物理 / 数学 / 医学等术语来比喻可以帮理解，但不能把比喻词当成正式术语反复使用、还不解释。第一次借喻要点明「这是打个比方」，之后回到大白话。
  - **适用范围**：一切给人看的输出——对用户的消息、报告、群发。**agent 之间的内部通信豁免**（内部黑话提速，对外才治理）。
  - **项目术语对照表是实例资产，不在本仓。** 本 skill 只立规则，不收录任何项目词条（A3 解耦——项目特定取值住业务仓实例）。去项目化的示例写法（仅示范、非词条）：生造「X 病」（借动力学 / 医学术语 + 自造病名 + 不解释）、「X-3」（不展开的内部编号当概念用）这类直接进对人输出都不合格，按上面三条改写。

## EN→zh 术语表（generic — R18 配套，跨仓统一）

> 配合 R18（术语全文统一）。供任何中文产物 / README 中文镜像复用——尤其治理生态高频英文术语，避免每仓各译一版。
> 通用内容，零实例取值。`readme-style` R32 的语义评审以本 skill 为准（cross-cite，不复制）。

| EN | 翻译腔（避免） | 推荐中文 |
|---|---|---|
| pin（钉住子模块版本） | 提升其固定 | 锚定 / 钉到（tag）；或保留 `pin` |
| home（skill home） | 家园 | （skill）库 / 主仓 |
| materialize / regen into | 物化进 | 生成到 / 落地到 |
| template-owned | 模板所有的 | 模板托管的 / 由模板统管 |
| bump（升版本） | 提升 | 升版 / 提版 |
| gate（版本门 / 准出门） | 门 | 版本门 / 准出门（保留语义，不简化为「门」） |
| build artifact | — | 构建产物（已通顺，沿用） |
| canonical | 规范的 | 权威源 / 正本（视语境） |

> 首次出现可中英并注（如「锚定（pin）」），之后固定一种；专有名词 / 工具名 / 代码标识（mermaid、mmdc、`git`、SKILL.md）保留英文。

> **Provenance.** R14–R20 borrowed from yikeke/zh-style-guide, MIT — checkable, Vale-style
> (<https://github.com/yikeke/zh-style-guide>). R33–R39 的具体规则来自团队用户反馈；R33 的理论框架
> （名词化=恶性西化）引自余光中《中文的常态与变态》。Contributor attribution recorded in `contributors.yaml`; third-party
> sources in `THIRD-PARTY-NOTICES.md`.
