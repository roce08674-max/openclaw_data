# OpenClaw 数据仓库

⚠️ **注意**: 此仓库不包含任何敏感数据（如 API 密钥、密码、个人信息等）。

## 仓库内容

- **AGENTS.md** - Agent 系统配置和规则
- **AGENTS_LIST.md** - 完整 Agent 列表和说明
- **BOOTSTRAP.md** - 启动配置
- **HEARTBEAT.md** - 心跳检查配置
- **IDENTITY.md** - Agent 身份定义
- **SOUL.md** - Agent 核心价值观
- **TOOLS.md** - 可用工具列表
- **USER.md** - 用户信息模板
- **skills/** - Agent 技能模块
- **memory/** - 记忆文件
- **scripts/** - 辅助脚本

## 安全说明

所有敏感信息（API 密钥、密码、Token 等）均通过以下方式管理：
- 环境变量
- `.env` 文件（不包含在此仓库中）
- GitHub CLI (`gh auth login`)

## 使用方法

请参考各模块的 `SKILL.md` 和 `HOW_TO_USE.md` 文件。

## 更新日志

### 2026-02-10
- 添加热点 Agent (Hot Topic Agent)
- 增强知识图谱嵌入分析功能
- 整理文档结构

## 注意事项

⚠️ **重要**: 请勿将任何敏感信息提交到此仓库。
