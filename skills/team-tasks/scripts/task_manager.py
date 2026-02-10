#!/usr/bin/env python3
"""
Team Tasks - Multi-Agent Pipeline Coordination

A Python CLI tool for coordinating multi-agent development workflows
through shared JSON task files.

Modes:
- Linear: Sequential pipeline with auto-advance
- DAG: Dependency graph with parallel dispatch
- Debate: Multi-agent position + cross-review

Author: OpenClaw Agent
Created: 2026-02-09
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
from uuid import uuid4

# Configuration
TEAM_TASKS_DIR = os.environ.get('TEAM_TASKS_DIR', '/home/ubuntu/clawd/data/team-tasks')
DATA_DIR = Path(TEAM_TASKS_DIR)
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Mode(Enum):
    """Pipeline modes"""
    LINEAR = "linear"
    DAG = "dag"
    DEBATE = "debate"


class Status(Enum):
    """Task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


# Status icons
STATUS_ICONS = {
    Status.PENDING: "⬜",
    Status.IN_PROGRESS: "🔄",
    Status.DONE: "✅",
    Status.FAILED: "❌",
    Status.SKIPPED: "⏭️"
}


class TaskManager:
    """Main task manager class"""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or DATA_DIR

    def get_project_file(self, project: str) -> Path:
        """Get project JSON file path"""
        return self.data_dir / f"{project}.json"

    def load_project(self, project: str) -> Dict:
        """Load project data"""
        project_file = self.get_project_file(project)
        if not project_file.exists():
            raise FileNotFoundError(f"Project not found: {project}")
        with open(project_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_project(self, project: str, data: Dict):
        """Save project data"""
        project_file = self.get_project_file(project)
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def init_project(
        self,
        project: str,
        goal: str,
        mode: str = "linear",
        pipeline: List[str] = None,
        workspace: str = None,
        force: bool = False
    ) -> Dict:
        """Initialize a new project"""
        project_file = self.get_project_file(project)

        if project_file.exists() and not force:
            raise ValueError(f"Project already exists: {project}")

        # Validate mode
        try:
            mode_enum = Mode(mode)
        except ValueError:
            raise ValueError(f"Invalid mode: {mode}. Must be: linear, dag, debate")

        # Create project structure
        project_data = {
            "id": project,
            "goal": goal,
            "mode": mode.value,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "workspace": workspace or str(self.data_dir / project),
            "stages": {},
            "history": []
        }

        # Initialize based on mode
        if mode_enum == Mode.LINEAR:
            project_data["stages"] = {
                stage: {
                    "status": Status.PENDING.value,
                    "description": "",
                    "agent": agent,
                    "result": "",
                    "log": [],
                    "created_at": datetime.now().isoformat()
                }
                for i, stage in enumerate(pipeline or [])
            }

        elif mode_enum == Mode.DAG:
            project_data["stages"] = {}
            project_data["dependencies"] = {}

        elif mode_enum == Mode.DEBATE:
            project_data["stages"] = {
                "initial": {
                    "status": Status.PENDING.value,
                    "outputs": {},
                    "created_at": datetime.now().isoformat()
                },
                "cross_review": {
                    "status": Status.PENDING.value,
                    "outputs": {},
                    "created_at": datetime.now().isoformat()
                },
                "synthesis": {
                    "status": Status.PENDING.value,
                    "output": "",
                    "created_at": datetime.now().isoformat()
                }
            }
            project_data["debaters"] = {}

        # Create workspace
        if project_data["workspace"]:
            Path(project_data["workspace"]).mkdir(parents=True, exist_ok=True)

        # Save project
        self.save_project(project, project_data)

        return project_data

    def add_task(
        self,
        project: str,
        task_id: str,
        agent: str,
        description: str = "",
        dependencies: List[str] = None
    ) -> Dict:
        """Add a task to a DAG project"""
        project_data = self.load_project(project)

        if project_data["mode"] != Mode.DAG.value:
            raise ValueError("add is only available for DAG mode")

        # Check for circular dependencies
        deps = dependencies or []
        self._check_circular_deps(project_data, task_id, deps)

        # Add task
        project_data["stages"][task_id] = {
            "status": Status.PENDING.value,
            "description": description,
            "agent": agent,
            "result": "",
            "log": [],
            "created_at": datetime.now().isoformat()
        }
        project_data["dependencies"][task_id] = deps
        project_data["updated_at"] = datetime.now().isoformat()

        self.save_project(project, project_data)
        return project_data["stages"][task_id]

    def _check_circular_deps(self, project_data: Dict, new_task: str, new_deps: List[str]):
        """Check for circular dependencies"""
        existing_deps = project_data.get("dependencies", {})

        def has_path_to(target: str, visited: set = None) -> bool:
            if visited is None:
                visited = set()
            if target in visited:
                return False
            visited.add(target)

            for task, deps in existing_deps.items():
                if new_task in deps:
                    if has_path_to(task, visited):
                        return True
            return False

        for dep in new_deps:
            if dep == new_task:
                raise ValueError(f"Circular dependency: {new_task} depends on itself")
            if has_path_to(dep):
                raise ValueError(f"Circular dependency: {new_task} -> {dep}")

    def add_debater(self, project: str, agent_id: str, role: str = "") -> Dict:
        """Add a debater to a debate project"""
        project_data = self.load_project(project)

        if project_data["mode"] != Mode.DEBATE.value:
            raise ValueError("add-debater is only available for debate mode")

        project_data["debaters"][agent_id] = {
            "role": role,
            "position": "",
            "cross_review": "",
            "status": Status.PENDING.value,
            "created_at": datetime.now().isoformat()
        }
        project_data["updated_at"] = datetime.now().isoformat()

        self.save_project(project, project_data)
        return project_data["debaters"][agent_id]

    def assign(self, project: str, stage: str, description: str) -> Dict:
        """Set task description (linear/dag mode)"""
        project_data = self.load_project(project)
        project_data["stages"][stage]["description"] = description
        project_data["updated_at"] = datetime.now().isoformat()
        self.save_project(project, project_data)
        return project_data["stages"][stage]

    def update(self, project: str, stage: str, status: str) -> Dict:
        """Update task status"""
        project_data = self.load_project(project)

        try:
            status_enum = Status(status)
        except ValueError:
            raise ValueError(f"Invalid status: {status}")

        project_data["stages"][stage]["status"] = status_enum.value
        project_data["stages"][stage]["updated_at"] = datetime.now().isoformat()
        project_data["updated_at"] = datetime.now().isoformat()

        self.save_project(project, project_data)

        # Auto-advance for linear mode
        if project_data["mode"] == Mode.LINEAR.value and status_enum == Status.DONE:
            self._auto_advance(project)

        return project_data["stages"][stage]

    def _auto_advance(self, project_data: Dict):
        """Auto-advance to next stage in linear mode"""
        stages = project_data["stages"]
        for stage_name, stage_data in stages.items():
            if stage_data["status"] == Status.IN_PROGRESS.value:
                stage_data["status"] = Status.PENDING.value
                break

    def next(self, project: str) -> Optional[Dict]:
        """Get next stage info (linear mode)"""
        project_data = self.load_project(project)

        if project_data["mode"] != Mode.LINEAR.value:
            raise ValueError("next is only available for linear mode")

        stages = project_data["stages"]
        for stage_name, stage_data in stages.items():
            if stage_data["status"] == Status.PENDING.value:
                return {
                    "stage": stage_name,
                    "agent": stage_data.get("agent", ""),
                    "description": stage_data.get("description", "")
                }

        return None

    def ready(self, project: str) -> List[Dict]:
        """Get ready-to-dispatch tasks (DAG mode)"""
        project_data = self.load_project(project)

        if project_data["mode"] != Mode.DAG.value:
            raise ValueError("ready is only available for DAG mode")

        ready_tasks = []
        stages = project_data["stages"]
        dependencies = project_data.get("dependencies", {})

        for task_id, task_data in stages.items():
            if task_data["status"] == Status.PENDING.value:
                deps = dependencies.get(task_id, [])
                if all(
                    stages.get(dep, {}).get("status") == Status.DONE.value
                    for dep in deps
                ):
                    ready_tasks.append({
                        "task": task_id,
                        "agent": task_data.get("agent", ""),
                        "description": task_data.get("description", ""),
                        "dependencies": deps
                    })

        return ready_tasks

    def result(self, project: str, stage: str, output: str) -> Dict:
        """Save stage output"""
        project_data = self.load_project(project)
        project_data["stages"][stage]["result"] = output
        project_data["updated_at"] = datetime.now().isoformat()
        self.save_project(project, project_data)
        return project_data["stages"][stage]

    def log(self, project: str, stage: str, message: str) -> Dict:
        """Add log entry"""
        project_data = self.load_project(project)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        project_data["stages"][stage]["log"].append(entry)
        self.save_project(project, project_data)
        return entry

    def history(self, project: str, stage: str) -> List[Dict]:
        """Get stage log history"""
        project_data = self.load_project(project)
        return project_data["stages"][stage].get("log", [])

    def status(self, project: str) -> Dict:
        """Get project status"""
        return self.load_project(project)

    def list_projects(self) -> List[str]:
        """List all projects"""
        projects = []
        for f in self.data_dir.glob("*.json"):
            projects.append(f.stem)
        return sorted(projects)

    def graph(self, project: str) -> str:
        """Generate DAG graph representation"""
        project_data = self.load_project(project)

        if project_data["mode"] != Mode.DAG.value:
            raise ValueError("graph is only available for DAG mode")

        stages = project_data["stages"]
        dependencies = project_data.get("dependencies", {})

        # Build tree structure
        def build_tree(task_id: str, visited: set = None) -> Dict:
            if visited is None:
                visited = set()
            if task_id in visited:
                return {"task": task_id, "error": "circular"}
            visited.add(task_id)

            task_data = stages.get(task_id, {})
            deps = dependencies.get(task_id, [])

            children = []
            for dep in deps:
                if dep in stages:
                    children.append(build_tree(dep, visited.copy()))

            return {
                "task": task_id,
                "agent": task_data.get("agent", ""),
                "status": task_data.get("status", ""),
                "children": children
            }

        # Find root tasks (no dependencies)
        all_tasks = set(stages.keys())
        dependent_tasks = set()
        for deps in dependencies.values():
            dependent_tasks.update(deps)

        roots = all_tasks - dependent_tasks

        def format_tree(node: Dict, indent: int = 0) -> List[str]:
            lines = []
            prefix = "│ " * indent
            status = node.get("status", "")
            icon = STATUS_ICONS.get(Status(status), "⬜")
            agent = node.get("agent", "")
            lines.append(f"{prefix}├─ {icon} {node['task']} [{agent}]")

            children = node.get("children", [])
            for child in children:
                lines.extend(format_tree(child, indent + 1))

            return lines

        lines = [f"📋 {project} — DAG Graph", ""]
        for root in roots:
            lines.extend(format_tree(build_tree(root)))

        lines.append("")
        total = len(stages)
        done = sum(1 for s in stages.values() if s["status"] == Status.DONE.value)
        progress = f"[{'█' * done}{'░' * (total - done)}] {done}/{total}"

        return '\n'.join(lines)

    def round(
        self,
        project: str,
        action: str,
        agent_id: str = None,
        output: str = None
    ) -> Dict:
        """Handle debate round actions"""
        project_data = self.load_project(project)

        if project_data["mode"] != Mode.DEBATE.value:
            raise ValueError("round is only available for debate mode")

        if action == "start":
            project_data["stages"]["initial"]["status"] = Status.IN_PROGRESS.value
            self.save_project(project, project_data)
            return {"message": f"Debate Round 1 (initial) started"}

        elif action == "collect":
            if not agent_id or not output:
                raise ValueError("collect requires agent_id and output")
            project_data["stages"]["initial"]["outputs"][agent_id] = output
            project_data["debaters"][agent_id]["position"] = output
            project_data["debaters"][agent_id]["status"] = Status.DONE.value

            # Check if all debaters have submitted
            all_done = all(
                d.get("status") == Status.DONE.value
                for d in project_data["debaters"].values()
            )
            if all_done:
                project_data["stages"]["initial"]["status"] = Status.DONE.value
                project_data["stages"]["cross_review"]["status"] = Status.IN_PROGRESS.value

            self.save_project(project, project_data)
            return {"message": f"Collected from {agent_id}"}

        elif action == "cross_review":
            outputs = project_data["stages"]["initial"]["outputs"]
            project_data["stages"]["cross_review"]["outputs"] = outputs
            project_data["stages"]["cross_review"]["status"] = Status.IN_PROGRESS.value
            project_data["stages"]["initial"]["status"] = Status.DONE.value
            self.save_project(project, project_data)
            return {
                "message": "Cross-review started",
                "outputs": outputs
            }

        elif action == "synthesize":
            initial = project_data["stages"]["initial"]["outputs"]
            cross = project_data["stages"]["cross_review"]["outputs"]

            synthesis = {
                "initial_positions": initial,
                "cross_reviews": cross,
                "synthesized_at": datetime.now().isoformat()
            }
            project_data["stages"]["synthesis"]["output"] = json.dumps(
                synthesis, ensure_ascii=False
            )
            project_data["stages"]["synthesis"]["status"] = Status.DONE.value
            project_data["status"] = "completed"
            self.save_project(project, project_data)

            return synthesis

        raise ValueError(f"Unknown action: {action}")

    def reset(self, project: str, stage: str = None, all: bool = False):
        """Reset project or stage"""
        project_data = self.load_project(project)

        if all:
            for stage_data in project_data["stages"].values():
                stage_data["status"] = Status.PENDING.value
                stage_data["result"] = ""
        elif stage:
            project_data["stages"][stage]["status"] = Status.PENDING.value
        else:
            raise ValueError("reset requires stage or --all")

        project_data["updated_at"] = datetime.now().isoformat()
        self.save_project(project, project_data)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Team Tasks - Multi-Agent Pipeline Coordination",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("project", help="Project name")
    init_parser.add_argument("-g", "--goal", required=True, help="Project goal")
    init_parser.add_argument("-m", "--mode", default="linear",
                            choices=["linear", "dag", "debate"], help="Pipeline mode")
    init_parser.add_argument("-p", "--pipeline", help="Comma-separated pipeline stages")
    init_parser.add_argument("-w", "--workspace", help="Workspace directory")
    init_parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing")

    # add command (DAG)
    add_parser = subparsers.add_parser("add", help="Add task to DAG project")
    add_parser.add_argument("project", help="Project name")
    add_parser.add_argument("task_id", help="Task identifier")
    add_parser.add_argument("-a", "--agent", required=True, help="Agent to execute")
    add_parser.add_argument("-d", "--deps", help="Comma-separated dependencies")
    add_parser.add_argument("--desc", default="", help="Task description")

    # add-debater command (Debate)
    debater_parser = subparsers.add_parser("add-debater", help="Add debater to debate project")
    debater_parser.add_argument("project", help="Project name")
    debater_parser.add_argument("agent_id", help="Debater agent ID")
    debater_parser.add_argument("-r", "--role", default="", help="Debater role/perspective")

    # assign command
    assign_parser = subparsers.add_parser("assign", help="Set task description")
    assign_parser.add_argument("project", help="Project name")
    assign_parser.add_argument("stage", help="Stage name")
    assign_parser.add_argument("description", help="Task description", nargs="+")

    # update command
    update_parser = subparsers.add_parser("update", help="Update task status")
    update_parser.add_argument("project", help="Project name")
    update_parser.add_argument("stage", help="Stage/task name")
    update_parser.add_argument("status", help="New status",
                              choices=["pending", "in-progress", "done", "failed", "skipped"])

    # result command
    result_parser = subparsers.add_parser("result", help="Save stage output")
    result_parser.add_argument("project", help="Project name")
    result_parser.add_argument("stage", help="Stage name")
    result_parser.add_argument("output", help="Stage output", nargs="+")

    # log command
    log_parser = subparsers.add_parser("log", help="Add log entry")
    log_parser.add_argument("project", help="Project name")
    log_parser.add_argument("stage", help="Stage name")
    log_parser.add_argument("message", help="Log message", nargs="+")

    # next command
    subparsers.add_parser("next", help="Get next stage (linear mode)").add_argument("project")

    # ready command
    ready_parser = subparsers.add_parser("ready", help="Get ready tasks (DAG mode)")
    ready_parser.add_argument("project", help="Project name")

    # status command
    status_parser = subparsers.add_parser("status", help="Show project status")
    status_parser.add_argument("project", help="Project name")

    # graph command
    subparsers.add_parser("graph", help="Show DAG graph").add_argument("project")

    # round command (Debate)
    round_parser = subparsers.add_parser("round", help="Debate round actions")
    round_parser.add_argument("project", help="Project name")
    round_parser.add_argument("action", choices=["start", "collect", "cross-review", "synthesize"])
    round_parser.add_argument("agent_id", nargs="?", help="Agent ID (for collect)")
    round_parser.add_argument("output", nargs="?", help="Output (for collect)")

    # list command
    subparsers.add_parser("list", help="List all projects")

    # reset command
    reset_parser = subparsers.add_parser("reset", help="Reset project")
    reset_parser.add_argument("project", help="Project name")
    reset_parser.add_argument("stage", nargs="?", help="Stage to reset")
    reset_parser.add_argument("--all", action="store_true", help="Reset all stages")

    # history command
    history_parser = subparsers.add_parser("history", help="Show stage history")
    history_parser.add_argument("project", help="Project name")
    history_parser.add_argument("stage", help="Stage name")

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    tm = TaskManager()

    try:
        if args.command == "init":
            pipeline = args.pipeline.split(",") if args.pipeline else None
            result = tm.init_project(
                args.project, args.goal, args.mode, pipeline, args.workspace, args.force
            )
            print(f"✅ Project '{args.project}' initialized")
            print(f"   Mode: {args.mode}")
            print(f"   Goal: {args.goal}")

        elif args.command == "add":
            deps = args.deps.split(",") if args.deps else None
            tm.add_task(args.project, args.task_id, args.agent, args.desc, deps)
            print(f"✅ Task '{args.task_id}' added to '{args.project}'")

        elif args.command == "add-debater":
            tm.add_debater(args.project, args.agent_id, args.role)
            print(f"✅ Debater '{args.agent_id}' added to '{args.project}'")

        elif args.command == "assign":
            description = " ".join(args.description)
            tm.assign(args.project, args.stage, description)
            print(f"✅ Stage '{args.stage}' description updated")

        elif args.command == "update":
            tm.update(args.project, args.stage, args.status)
            print(f"✅ Stage '{args.stage}' status: {args.status}")

        elif args.command == "result":
            output = " ".join(args.output)
            tm.result(args.project, args.stage, output)
            print(f"✅ Result saved for '{args.stage}'")

        elif args.command == "log":
            message = " ".join(args.message)
            entry = tm.log(args.project, args.stage, message)
            print(f"✅ Log entry added at {entry['timestamp']}")

        elif args.command == "next":
            next_stage = tm.next(args.project)
            if next_stage:
                print(f"▶️ Next stage: {next_stage['stage']}")
                print(f"   Agent: {next_stage['agent']}")
                print(f"   Description: {next_stage['description']}")
            else:
                print("✅ All stages completed!")

        elif args.command == "ready":
            ready_tasks = tm.ready(args.project)
            if ready_tasks:
                print(f"🟢 Ready to dispatch ({len(ready_tasks)} tasks):")
                for task in ready_tasks:
                    deps = ", ".join(task["dependencies"]) if task["dependencies"] else "none"
                    print(f"   📌 {task['task']} → agent: {task['agent']} (deps: {deps})")
            else:
                print("🟡 No tasks ready")

        elif args.command == "status":
            data = tm.status(args.project)
            print(f"📋 Project: {data['id']}")
            print(f"🎯 Goal: {data['goal']}")
            print(f"📊 Status: {data['status']} | Mode: {data['mode']}")

            print("\nStages:")
            for stage, info in data.get("stages", {}).items():
                icon = STATUS_ICONS.get(Status(info["status"]), "⬜")
                print(f"   {icon} {stage}: {info.get('status', 'pending')}")

        elif args.command == "graph":
            print(tm.graph(args.project))

        elif args.command == "round":
            result = tm.round(args.project, args.action, args.agent_id, args.output)
            if "message" in result:
                print(f"🗣️ {result['message']}")

        elif args.command == "list":
            projects = tm.list_projects()
            if projects:
                print("📁 Projects:")
                for p in projects:
                    print(f"   - {p}")
            else:
                print("📁 No projects found")

        elif args.command == "reset":
            tm.reset(args.project, args.stage, args.all)
            print(f"✅ Project '{args.project}' reset")

        elif args.command == "history":
            entries = tm.history(args.project, args.stage)
            if entries:
                for entry in entries:
                    print(f"[{entry['timestamp']}] {entry['message']}")
            else:
                print("📭 No history")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
