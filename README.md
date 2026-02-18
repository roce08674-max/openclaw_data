# openclaw_data

This repo stores OpenClaw-related assets for this machine.

## Custom Skills

- `skills/codex-dev/` — a skill that instructs OpenClaw to use the **Codex CLI** for software development.

### Install

Copy or symlink into your OpenClaw workspace:

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/codex-dev ~/.openclaw/workspace/skills/
# or: ln -s "$PWD/skills/codex-dev" ~/.openclaw/workspace/skills/codex-dev
```

Then restart OpenClaw Gateway (or wait for skills watch to reload)
