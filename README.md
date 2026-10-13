# 三个训练型 AutoResearch 题目交接

本仓库交接三个选题的制作要求，以及完整的 `autoresearch-manager` Skill。接手后按题目要求完成真实训练、成对对照、双模型研究轨迹和独立质检。

| 顺序 | 题目 | 首轮范围 | 要求 |
|---|---|---|---|
| 1 | [GAD-NR 图异常检测](requirements/gad-nr.md) | Cora、Books、Weibo；先用 inj_cora 验证运行 | 有训练、可复现、正式难度为困难 |
| 2 | [SoftCLT 低标注时间序列分类](requirements/softclt.md) | Epilepsy，1%／5%标注，多阶段半监督版本 | 有训练、可复现、正式难度为困难 |
| 3 | [RecDCL 双重对比推荐](requirements/recdcl.md) | 公开 Beauty 数据，全物品排序 | 有训练、可复现、正式难度为困难 |

三个候选在 2026-10-13 的在线查重均通过，当前特定范围的 Skill 预评为困难。正式评级、目标 GPU 耗时、完整复现和 Reference 提升仍需实跑确认。实证无法满足困难或改善条件的候选应更换，不降低验收要求。

用户希望尽量一天完成，可放宽到两天；这是每题的排期目标。三题都涉及训练，不能使用非训练任务的 7 小时轨迹例外。此前的选题检查没有启动这些题目的正式实验。

## 接手顺序

1. 阅读 [共同制作与验收要求](requirements/common.md) 和要制作的题目文件。
2. 阅读 [manager Skill](skills/autoresearch-manager/SKILL.md) 和 [运行合同](skills/autoresearch-manager/references/runtime-contract.md)。
3. 按 [安装及使用说明](INSTALL.md) 安装完整 Skill，重新核对当期平台规则。
4. 先完成真实小规模复现、健康 Baseline 和合法方法候选的成对实验，确认成本与难度，再冻结正式合同。
5. 根据真实命令建立任务专用 drivers，预检通过后用 manager 持续推进；同一最终 ZIP 获得两个独立 PASS 且无分歧才算完成。

`requirements/` 是作者侧要求，`skills/` 是主控与审查工具。正式候选 Actor 仅接收干净的公开任务快照；作者要求、管理状态、Reference、私有测试和 QA 材料保留在其可访问范围之外。

## 已包含的材料

- 三个题目的来源、官方代码版本、研究范围、训练与评测要求、具体复现风险。
- 完整 manager 源码、运行合同、Agent 配置、测试，以及随附 QA v0.3.4 和 Baseline 合理性 Skill。
- 文件哈希清单与交接包验证脚本。

生产源码、SKILL、运行合同及 QA v0.3.4 文件保持原样；交接副本仅将管理器测试中的一个局部变量改名以避免隐私扫描误报，测试语义不变。差异记录在 `manifests/provenance.json`。

论文、第三方源码、数据和模型通过各题列出的官方来源取得，按相应许可使用。运行凭据在可信主控侧单独配置。
