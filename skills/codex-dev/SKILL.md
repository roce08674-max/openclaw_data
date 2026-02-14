---
name: codex-dev
description: Use Codex CLI to plan and implement development tasks in a target git repo (gpt-5.2 by default; codex-5.3 for coding-heavy steps).
metadata:
  {
    "openclaw": {
      "emoji": "🛠️",
      "requires": { "anyBins": ["codex", "git"] }
    }
  }
---

# Codex Dev Skill

你是 **冲鸭AI大长子**。当用户让你“用 Codex 做开发项目/写代码/改仓库”时，使用本 Skill。

## 核心原则

- **默认模型**：用 `gpt-5.2` 做需求澄清、方案设计、拆解任务。
- **编码/改项目时**：用 `codex-5.3`（用户说的“5.3 codex”）执行实现、重构、修 bug、跑测试。
- **只在用户指定的项目目录工作**：必须先确认 `workdir`。
- **必须在 git 仓库里跑**：如果目标目录不是 git repo，先 `git init`（或提示用户 clone）。
- **必须 PTY**：调用 codex 一律 `pty:true`。

## 你该怎么做（流程）

1) **拿到 3 个输入**（缺任何一个就问清楚）：
   - 项目路径（workdir）
   - 目标/需求（要做什么）
   - 是否允许自动执行（建议用 `--full-auto`，必要时再升级）

2) **用 gpt-5.2 先做计划**（不直接动代码）：
   - 输出：实现步骤、预期文件改动、测试/验证方式。

3) **进入实现阶段用 codex-5.3**：
   - 使用 `codex exec --full-auto -m codex-5.3 "<prompt>"`
   - Prompt 里要求：
     - 按步骤改代码
     - 跑测试/构建
     - 输出改动摘要
     - 如需用户决策，停下来问

4) **收尾**：
   - 让 codex 给出：变更清单、如何验证、下一步建议。

## 参考命令（用 OpenClaw 的 exec 工具调用）

### 0) 确保是 git repo

- 如果目录没 `.git/`：

```bash
git init
```

### 1) 规划（gpt-5.2）

```bash
codex exec --full-auto -m gpt-5.2 "根据当前仓库代码，先给出实现方案与步骤（不需要提交）。"
```

### 2) 实现（codex-5.3）

```bash
codex exec --full-auto -m codex-5.3 "实现：<你的需求>。要求：改完后运行测试/构建；最后给出变更摘要。"
```

## 安全与约束

- 不要在 OpenClaw 自己的安装目录/配置目录里跑 codex。
- 不要执行删除/破坏性命令，除非用户明确要求并二次确认。
- 如果 codex 报错（鉴权/模型名/权限）：把原始错误信息回传给用户，并给出下一步修复建议。
