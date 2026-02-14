#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   run_codex_exec.sh <workdir> <model> <prompt>
# Example:
#   run_codex_exec.sh ~/proj gpt-5.2 "Plan changes..."

WORKDIR=${1:?workdir required}
MODEL=${2:?model required}
PROMPT=${3:?prompt required}

cd "$WORKDIR"

if [ ! -d .git ]; then
  echo "[codex-dev] No .git found; initializing git repo in $WORKDIR" >&2
  git init -q
fi

# --full-auto keeps commands sandboxed (workspace-write) and reduces friction.
exec codex exec --full-auto -m "$MODEL" "$PROMPT"
