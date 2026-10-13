# 安装和启动

需要 Python 3.10+，正式运行环境另需 Linux Docker、所选 Harbor 版本、Linux Codex CLI、真实 GPU 训练环境，以及可信的模型网关。manager 本身使用 Python 标准库。

从仓库根复制整个 Skill 文件夹：

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/autoresearch-manager "${CODEX_HOME:-$HOME/.codex}/skills/"
```

若已有同名安装，先对比和备份已有版本，避免覆盖其他任务正在使用的 Skill。也可以直接在仓库中的 Skill 路径运行脚本。

## 先验证交接包

```sh
python3 tools/verify_handoff.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/autoresearch-manager/scripts -p 'test_manager.py'
```

框架测试使用模拟 Actor 和压缩的测试时钟，仅检查管理器行为。正式题目的 B/R、10h 双轨、NOP、12h 稳定性和双 AI PASS 需要真实运行。

随附 QA 源文件哈希固定在 `skills/autoresearch-manager/assets/qa-release.json`。不得修改 QA 源码或报告字段来取得 PASS。

## 建立任务专用运行

先阅读 `requirements/common.md`、具体题目要求及 `references/runtime-contract.md`。配置放在仓库之外的可信主控目录，采用机器自身的实际路径。每个 driver 必须是已经实测的真实命令，接收 `--request` 并生成规定的回执和运行证据。

正式训练任务至少配置以下合同值：

```json
{
  "qa_version": "0.3.4",
  "effective_seconds_per_track": 36000,
  "stability_seconds": 43200
}
```

完整 plan 还需要 `schema_version`、`task_root`、`goal`、两个不同 reviewer 和全部 drivers。按实际 Harbor、网关、隔离边界和题目命令填写，不能把这个片段当作完整可执行计划。

```sh
python3 skills/autoresearch-manager/scripts/manager.py init \
  --plan "$AUTORESEARCH_PLAN_FILE" --run-dir "$AUTORESEARCH_RUN_DIR"
python3 skills/autoresearch-manager/scripts/manager.py doctor \
  --run-dir "$AUTORESEARCH_RUN_DIR"
python3 skills/autoresearch-manager/scripts/manager.py start \
  --run-dir "$AUTORESEARCH_RUN_DIR"
python3 skills/autoresearch-manager/scripts/manager.py status \
  --run-dir "$AUTORESEARCH_RUN_DIR"
```

`AUTORESEARCH_PLAN_FILE` 和 `AUTORESEARCH_RUN_DIR` 由可信主控设置，run-dir 保留在题包之外。`start` 会启动后台管理进程，只有正式前置条件满足后才启动。

模型与凭据配置参考共同要求。长期 API 凭据保留在可信主控侧，通过隔离网关供 Actor 使用；不得存进本仓库、plan、request、题包或 Actor 环境。
