# Research Loop

**让每轮科研留下可核查的证据、可复用的经验和明确的下一步。**

Research Loop 是一个通用科研智能体 skill，把文献精读、跨论文综合、创新假设、实验与分析、独立评议、研究记忆和论文写作连接起来。研究领域、模型、机器、数据和预算由项目配置决定。

[English](README_EN.md) · [核心技能](skills/research-loop/SKILL.md) · [来源与融合](docs/PROVENANCE.md) · [记录格式](skills/research-loop/references/memory.md)

## 工作方式

```mermaid
flowchart LR
  A[文献与原始证据] --> B[跨论文综合]
  B --> C[问题或探索性组合]
  C --> D[有预算的区分实验]
  D --> E[独立检查与结论]
  E --> F[论文与研究产物]
  E --> G[有条件的成功与失败经验]
  G --> B
```

- **读懂来源**：明确区分元数据、摘要、部分阅读和全文阅读；方法与结果回到原文位置。
- **提出可验证的创新**：支持从问题出发，也支持先组合方法寻找现象；记录最近工作、替代解释和便宜的验证办法。
- **持续实验与分析**：按证据逐步投入，区分进程完成、结果核查和科学主张成立。
- **积累研究记忆**：保存论文、主张、实验和经验之间的关联；新证据可以修正、缩小或淘汰旧经验。
- **写成有力的论文**：围绕最强的有证据贡献组织叙事，减少套话和无效防御，同时保留影响结论的不确定性和反例。

## 融合了什么

| 来源 | 融合到本项目的做法 |
|---|---|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 有预算的迭代、独立评议、可恢复状态、结果到主张的检查 |
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | 来源定位、方法与证据链、互盲审稿、证据驱动的写作和科研产物 |
| [学术反防御性写作](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | 找到最值得发表的贡献，按论证组织实验与正文 |
| [Anti-Defensive Writing](https://github.com/Kiterlin/anti-defensive-writing) | 直接、具体的表达，保留必要的方法条件与真实不确定性 |

本项目独立编写通用流程与辅助脚本，提供可选技能接入；没有打包上述项目的完整技能。已核对的版本、融合位置和调整见 [PROVENANCE](docs/PROVENANCE.md)，许可与署名见 [第三方声明](THIRD_PARTY_NOTICES.md)。

## 安装

辅助脚本使用 Python 3.10+，无第三方 Python 依赖。将 `skills/research-loop` 作为一个完整文件夹安装到宿主支持的技能目录。

```bash
git clone https://github.com/Online404/research-loop.git
cd research-loop
python scripts/install.py --dest /your/agent/skills
```

`--dest` 是技能目录的父目录，最终生成 `/your/agent/skills/research-loop`。安装器拒绝覆盖已有同名技能，不下载其他依赖。也可以手动复制该目录。

对于支持 `SKILL.md` 的宿主，按其当前文档选择安装位置。Codex 可在技能被发现后使用 `$research-loop`；其他宿主可直接加载 `SKILL.md`。本仓库不要求某个模型供应商。

## 开始一个项目

```bash
python skills/research-loop/scripts/init_project.py --path ../my-study --domain "你的研究领域" --objective "希望回答的研究问题或获得的能力"
python skills/research-loop/scripts/validate_project.py --path ../my-study
```

初始化只创建项目内的 `.research` 记录，不启动实验、不读取账户凭据。已有 `.research` 时拒绝覆盖。把项目放在代码仓库外，或保留 `.research/` 的忽略规则，避免把研究材料误当成技能源码发布。

随后给智能体这样的任务：

> 使用 research-loop，读取我的研究项目。先整理已有文献与结果，围绕当前条件提出三个可检验的候选，给出最近工作、最小区分实验与预算，并更新研究记忆。

也可以只执行一个阶段：

> 这次先精读和综合，不运行实验。明确哪些结论来自原文，哪些是你的假设。

> 根据已有运行记录继续科研循环，独立检查关键结果，把有证据的经验写入记忆，再决定下一轮实验。

## 记忆结构

```text
my-study/.research/
  project.json       # 领域、目标、阶段和资源条件
  STATE.md           # 当前决策、证据和下一步
  memory/
    papers.jsonl     # 论文与阅读深度
    claims.jsonl     # 有来源的主张
    lessons.jsonl    # 带适用条件的经验
  experiments/       # 执行状态与证据核查状态
```

阅读卡、原始结果和图表可以按需放入工作区，并由记录引用。验证器检查结构、ID、引用和工件存在性；文献理解、实验有效性、新颖性及论证质量仍需实际审查。

## 能力与边界

核心 skill 提供研究方法、状态和工具协作约定。全文阅读依赖宿主可用的原文访问与解析能力；实验依赖已配置的环境和实际预算；独立评议需要对应代理或人工参与。可选接入说明见 [integrations.md](skills/research-loop/references/integrations.md)。

后台持续运行需要宿主的调度功能。安装 skill 本身不会启动守护进程，也不意味着训练或投稿已经发生。它不承诺论文录用、固定发文速度或 AI 检测器结果。

## 开发与贡献

```bash
python -m unittest discover -s tests -v
```

欢迎贡献可复现的流程改进、不同领域的案例和行为测试。请使用合成或可公开材料，保留来源和适用范围。贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

原始内容使用 [Apache-2.0](LICENSE)；可选上游项目保留各自许可证。
