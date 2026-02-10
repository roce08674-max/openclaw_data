# Team Tasks - Multi-Agent Pipeline Coordination

A Python CLI tool for coordinating multi-agent development workflows through shared JSON task files. Designed for use with OpenClaw and AI agent orchestration systems.

## Features

Three coordination modes for different workflows:

### Mode A: Linear Pipeline
Sequential pipeline with auto-advance for bug fixes, simple features, and step-by-step workflows.

**Flow:**
```
Agent A → Agent B → Agent C → Agent D
   ↓          ↓          ↓          ↓
  Done      Done       Done       Done
```

### Mode B: DAG (Dependency Graph)
Dependency graph with parallel dispatch for large features, spec-driven development, and complex dependencies.

**Flow:**
```
       [Task A]
          ↓
    ┌─────┴─────┐
    ↓           ↓
[Task B]    [Task C]
    ↓           ↓
    └─────┬─────┘
          ↓
    [Task D with deps B, C]
```

### Mode C: Debate (Multi-Agent Deliberation)
Multi-agent position + cross-review for code reviews, architecture decisions, and competing hypotheses.

**Flow:**
```
Question → [Agent A] → Position A ─┐
         → [Agent B] → Position B ─┤── Cross-Review ── Synthesis
         → [Agent C] → Position C ─┘
```

## Requirements

- Python 3.12+ (stdlib only, no external dependencies)
- Data stored as JSON in `TEAM_TASKS_DIR` (default: `/home/ubuntu/clawd/data/team-tasks/`)

## Installation

```bash
# Clone or copy to skills directory
cp -r team-tasks/ /path/to/skills/

# Run directly
python3 scripts/task_manager.py --help
```

## Usage

### Linear Mode

```bash
# Initialize
python3 scripts/task_manager.py init my-api \
  -g "Build REST API with tests and docs" \
  -p "code-agent,test-agent,docs-agent"

# Assign tasks
python3 scripts/task_manager.py assign my-api code-agent "Implement API"
python3 scripts/task_manager.py assign my-api test-agent "Write tests"

# Check and advance
python3 scripts/task_manager.py next my-api
python3 scripts/task_manager.py update my-api code-agent done

# View status
python3 scripts/task_manager.py status my-api
```

### DAG Mode

```bash
# Initialize
python3 scripts/task_manager.py init my-feature \
  -g "Build search feature" \
  -m dag

# Add tasks with dependencies
python3 scripts/task_manager.py add my-feature design -a docs-agent --desc "Write spec"
python3 scripts/task_manager.py add my-feature scaffold -a code-agent --desc "Create project"
python3 scripts/task_manager.py add my-feature implement -a code-agent -d "design,scaffold"

# View graph
python3 scripts/task_manager.py graph my-feature

# Get ready tasks
python3 scripts/task_manager.py ready my-feature
```

### Debate Mode

```bash
# Initialize
python3 scripts/task_manager.py init security-review \
  -g "Review auth module" \
  -m debate

# Add debaters
python3 scripts/task_manager.py add-debater security-review code-agent -r "security expert"
python3 scripts/task_manager.py add-debater security-review test-agent -r "QA engineer"

# Run debate
python3 scripts/task_manager.py round security-review start
python3 scripts/task_manager.py round security-review collect code-agent "SQL injection found"
python3 scripts/task_manager.py round security-review collect test-agent "Missing validation"
python3 scripts/task_manager.py round security-review cross-review
python3 scripts/task_manager.py round security-review synthesize
```

## Integration with OpenClaw

This tool is designed as an OpenClaw Skill. The orchestrating agent dispatches tasks to worker agents via `sessions_send` and tracks state through this CLI.

### Linear Dispatch Loop

```python
# 1. Get next stage
next_stage = exec("task_manager.py next <project> --json")

# 2. Update status
exec("task_manager.py update <project> <agent> in-progress")

# 3. Dispatch to agent
sessions_send(agent=next_stage['agent'], message=next_stage['description'])

# 4. Wait for result, then save
exec(f"task_manager.py result <project> <agent> \"{output}\"")

# 5. Mark done (auto-advances)
exec("task_manager.py update <project> <agent> done")
```

### DAG Dispatch Loop

```python
# 1. Get all ready tasks
ready_tasks = exec("task_manager.py ready <project> --json")

# 2. Dispatch each in parallel
for task in ready_tasks:
    exec("task_manager.py update <project> <task> in-progress")
    sessions_send(agent=task['agent'], message=task['description'])
    # Wait and save results
```

## Commands Reference

| Command | Mode | Description |
|---------|------|-------------|
| `init` | all | Create new project |
| `add` | dag | Add task with dependencies |
| `add-debater` | debate | Add debater |
| `assign` | linear/dag | Set task description |
| `update` | linear/dag | Update task status |
| `next` | linear | Get next stage |
| `ready` | dag | Get dispatchable tasks |
| `status` | all | Show project status |
| `graph` | dag | Show dependency tree |
| `round` | debate | Debate actions |
| `result` | linear/dag | Save stage output |
| `log` | linear/dag | Add log entry |
| `history` | linear/dag | Show log history |
| `list` | all | List all projects |
| `reset` | linear/dag | Reset project |

## Status Values

| Status | Icon | Meaning |
|--------|------|---------|
| pending | ⬜ | Waiting for dispatch |
| in-progress | 🔄 | Agent is working |
| done | ✅ | Completed |
| failed | ❌ | Failed |
| skipped | ⏭️ | Intentionally skipped |

## Project Structure

```
team-tasks/
├── _meta.json          # Skill metadata
├── SKILL.md            # This file
├── HOW_TO_USE.md       # Detailed usage guide
└── scripts/
    └── task_manager.py # Main CLI tool
```

## File Location

**Skills Directory**: `skills/team-tasks/`
**Data Directory**: `/home/ubuntu/clawd/data/team-tasks/`
**Config**: `TEAM_TASKS_DIR` environment variable
