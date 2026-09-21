# 方法来源与融合方式

Research Loop 将文献证据、候选假设、实验记录、研究记忆、成稿和评议连接为可继续执行的科研流程。项目的编排、文档、模板和辅助程序采用独立实现；以下项目提供方法启发，也可作为单独安装的可选技能接入。本仓库不附带这些上游的技能全文、脚本、模型或素材。

以下审阅记录固定到 2026-09-21 检查的提交，避免把后续上游更新误认为本版本的来源。项目原始内容采用 [Apache-2.0](../LICENSE)；上游独立保有各自许可，详见 [第三方声明](../THIRD_PARTY_NOTICES.md)。来源记录不表示上游作者参与、认可或背书本项目。

## 审阅版本

| 项目 | 审阅提交 | 上游许可 | 在本项目中的作用 |
| --- | --- | --- | --- |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | [`341f914024d270dc5c8fa51337d1ad38829273aa`](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/tree/341f914024d270dc5c8fa51337d1ad38829273aa) | [MIT](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/LICENSE) | 实验规划、恢复执行、创新核查、结果到主张、研究记忆 |
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | [`9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5`](https://github.com/Yuan1z0825/nature-skills/tree/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5) | [Apache-2.0](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/LICENSE) | 来源可追溯的精读、证据与主张对应、独立评议、论文组织 |
| [Adkid-Zephyr / anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | [`102c8b21acf5eda3a0aef3d9779a65db646c8980`](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill/tree/102c8b21acf5eda3a0aef3d9779a65db646c8980) | [MIT](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill/blob/102c8b21acf5eda3a0aef3d9779a65db646c8980/LICENSE) | 围绕真实贡献组织论文，减少实验流水账和无信息的自我削弱 |
| [Kiterlin / anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing) | [`0f6491de75f95cb47ad8f0a4f24deff55f06a583`](https://github.com/Kiterlin/anti-defensive-writing/tree/0f6491de75f95cb47ad8f0a4f24deff55f06a583) | [MIT](https://github.com/Kiterlin/anti-defensive-writing/blob/0f6491de75f95cb47ad8f0a4f24deff55f06a583/LICENSE) | 直接表达、积极界定范围，同时保留必要的方法限制和真实不确定性 |

两个 anti-defensive-writing 项目是不同作品，不能互换归属或把它们描述成同一项目的版本。

## 具体吸收的做法

| 能力 | 查阅的上游材料 | Research Loop 的融合方式 |
| --- | --- | --- |
| 实验前明确问题与决策 | ARIS [experiment-plan](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/skills/experiment-plan/SKILL.md) | 候选假设对应最小实验、对照、资源预算和继续或停止条件；先做成本较低的筛选，再扩大验证。 |
| 任务中断后可继续 | ARIS [resumable-runs](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/skills/shared-references/resumable-runs.md) | 将研究状态、已生成产物与下一步记录在持久化工作区，恢复时核对运行实际状态，避免重复提交任务。 |
| 创新判断可核查 | ARIS [novelty-check](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/skills/novelty-check/SKILL.md) | 对候选点子检索最近邻工作，比较问题、假设、机制和证据；记录检索范围，把未找到同类工作与已证明新颖区分开。 |
| 从实验结果形成主张 | ARIS [result-to-claim](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/skills/result-to-claim/SKILL.md) | 区分测得现象、合理解释和待验证机制；每个论文主张关联结果、适用条件和反例。 |
| 将经验沉淀为研究记忆 | ARIS [wiki-enrich](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/skills/wiki-enrich/SKILL.md) | 记录有出处的事实和有适用条件的经验；失败结果参与后续检索，未经重复验证的经验保留候选状态。 |
| 精读可回到原文 | nature-skills [reader workflow](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-reader/static/core/workflow.md)、[grounding rules](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-reader/references/grounding-rules.md) | 阅读记录保留稳定的论文编号和页、节、图、表或公式位置。只有摘要时标记证据范围，不冒充完成全文精读。 |
| 拆解论文而非只压缩摘要 | nature-skills [paper-card principles](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-paper-card/static/core/principles.md) | 区分作者报告、外部核实、分析和假设；解释模块目的、支持实验、成立条件及证据不足的位置。 |
| 先构建论证再写文字 | nature-skills [writing stance](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-writing/static/core/stance.md)、[workflow](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-writing/static/core/workflow.md) | 先确定核心主张、决定性证据和范围，再分配章节任务；统一术语，按证据强弱选择动词。 |
| 保留完整证据，压缩重复论述 | nature-skills [main-text discipline](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-shared/core/main-text-discipline.md) | 区分主结果、必要支持、限定条件和实现细节。决定性反例与改变结论的结果保持可见，压缩过程保留产物去向。 |
| 评议保持独立 | ARIS [reviewer independence](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/341f914024d270dc5c8fa51337d1ad38829273aa/skills/shared-references/reviewer-independence.md)、nature-skills [reviewer](https://github.com/Yuan1z0825/nature-skills/blob/9cecfef6ac683fa59d7d15d2e22f98fa71dacaf5/skills/nature-reviewer/SKILL.md) | 每名评议者只接收共同的固定材料和自己的检查重点；各自完成后再综合，不通过共享意见制造共识。无隔离能力时说明评议并非独立。 |
| 以贡献为中心组织论文 | Adkid-Zephyr [academic writing skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill/blob/102c8b21acf5eda3a0aef3d9779a65db646c8980/skills/anti-defensive-writing/SKILL.md) | 围绕最有证据支持的贡献展开，给每个实验明确的论证职责，避免用探索过程充当最终论证。 |
| 清晰而准确地表达 | Kiterlin [writing skill](https://github.com/Kiterlin/anti-defensive-writing/blob/0f6491de75f95cb47ad8f0a4f24deff55f06a583/SKILL.md) | 删除重复道歉、空泛修饰和无信息的保留句；保留影响解释的方法限制、适用范围和真实不确定性。 |

## 有意保留的边界与差异

- 探索可以先组合方法、观察现象，再提出解释。事后提出的解释记为假设，不能写成事前预测；需要新实验或独立证据支持。
- 写作可以突出优势，但不能删除改变结论的不利证据、只报告最有利的指标，或将改过的任务口径冒充原始实验方案。调整评价维度时保留原因与时间，并明确探索性质。
- 直接表达不等于增强因果、机制或新颖性主张。语言修改保持事实、数量、比较口径、置信程度和结论范围一致。
- 阅读几百篇论文不会自动证明创新。文献记忆保存来源，研究策略保存触发条件与验证历史，两者分别维护。
- 技能提供研究流程。后台调度、计算资源、检索服务和外部写入能力取决于使用它的宿主及用户授权，不能把安装技能描述为已经启动持续运行。
- 社区的 Nature 风格写作建议不代表 Nature 或任何期刊的官方政策，也不保证接收。投稿要求按目标期刊当前公开规则核对。

## 可选技能接入

本项目另外独立实现“围绕固定基线逐篇判断模块迁移、保留有效改动、再组织论文叙事”的工作模式。其基线结构图、迁移卡、版本关系、可配置的 2～3 模块目标和初始化工具属于本项目的流程设计，并非从上述任一项目原样移植。具体见 [模块迁移流程](../skills/research-loop/references/model-grafting.md)。

专业技能可单独安装，由 Research Loop 按任务调用；没有安装时仍可按本项目的核心流程完成对应产物，并说明缺失的能力。接入时读取实际安装版本，保留其许可与依赖，不假定上游文件名、工具或行为永久不变。技能之间出现冲突时，以用户要求、科学证据和本项目的证据完整性约束确定执行方式。

本项目未复制上游完整技能，不将来源记录等同于兼容性测试。变更接入方式或引入实际上游代码时，应更新审阅版本、适用范围、许可和测试记录。

English note: Research Loop is an original implementation inspired by the pinned sources above. Upstream skills are optional, separately installed integrations. No upstream endorsement or journal affiliation is implied.
