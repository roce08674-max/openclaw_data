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

Then restart OpenClaw Gateway (or wait for skills watch to reload).
<img width="225" height="251" alt="image" src="https://github.com/user-attachments/assets/f3291374-6f5a-4966-9cba-bdd8ac84ede6" />
