# Team Tasks 详细使用指南

本指南详细介绍如何在不同场景下使用 Team Tasks 多代理协调工具，包括线性管道模式、DAG 依赖图模式和辩论模式的具体操作方法。无论您是想要协调简单的顺序任务，还是需要管理复杂的并行工作流，抑或是要进行多代理评审讨论，本指南都将为您提供完整的操作步骤和实际示例。

## 一、快速入门

### 1.1 环境准备

Team Tasks 是一个纯 Python 实现的命令行工具，不需要安装任何第三方依赖库。确保您的系统满足以下要求即可开始使用：Python 版本需要 3.12 或更高版本；操作系统可以是 Linux、macOS 或 Windows（通过 WSL）；数据存储目录默认为 `/home/ubuntu/clawd/data/team-tasks/`，您可以通过设置 `TEAM_TASKS_DIR` 环境变量来更改数据存储位置。

在使用之前，建议您先创建一个专门用于存放任务数据的目录。如果使用默认目录，请确保该目录具有适当的读写权限。以下命令可以快速检查您的 Python 版本和环境配置是否满足要求：

```bash
# 检查 Python 版本
python3 --version

# 设置数据目录（可选）
export TEAM_TASKS_DIR="/path/to/your/data"

# 验证工具是否可用
python3 skills/team-tasks/scripts/task_manager.py --help
```

### 1.2 首次使用

第一次使用 Team Tasks 时，建议按照以下步骤进行初始化和基本配置。首先，将 Team Tasks 技能复制到您的 OpenClaw 技能目录中，然后运行帮助命令确认工具正常工作，接着创建一个测试项目来熟悉基本操作流程。这个初始配置过程大约需要 5 分钟，完成后您就可以开始正式使用工具进行多代理协调工作了。

下面是首次使用的完整流程演示，您可以直接复制这些命令到终端执行。假设您已经将 Team Tasks 放在正确的位置：

```bash
# 切换到技能目录
cd skills/team-tasks

# 查看帮助信息
python3 scripts/task_manager.py --help

# 创建一个测试项目来体验功能
python3 scripts/task_manager.py init test-project \
  -g "Test project for learning" \
  -p "agent-a,agent-b,agent-c"

# 查看项目状态
python3 scripts/task_manager.py status test-project

# 列出所有项目
python3 scripts/task_manager.py list

# 完成后清理测试项目
python3 scripts/task_manager.py reset test-project --all
```

## 二、线性管道模式详解

线性管道模式是 Team Tasks 中最简单也最常用的协调模式。在这种模式下，任务按照预定义的顺序依次执行，每个代理完成自己的任务后自动推进到下一个阶段。这种模式特别适合Bug修复、简单功能开发、文档编写等步骤明确、依赖关系简单的场景。线性模式的优势在于流程清晰、易于理解和调试，缺点是无法并行执行任务，对于大型项目可能效率较低。

### 2.1 创建线性管道项目

创建线性管道项目的核心是定义任务的执行顺序。通过 `-p` 参数指定管道中的代理序列，工具会自动创建对应的任务阶段并管理状态流转。以下是一个实际的开发场景示例，展示了如何创建一个包含编码、测试、文档和部署检查四个阶段的完整管道：

```bash
# 初始化一个 REST API 开发项目
python3 scripts/task_manager.py init rest-api-project \
  -g "Build REST API with user authentication and CRUD operations" \
  -p "backend-agent,qa-agent,docs-agent,security-audit"

# 为每个阶段分配具体任务描述
python3 scripts/task_manager.py assign rest-api-project backend-agent \
  "Implement Flask REST API: POST/GET/PUT/DELETE /users endpoints with JWT authentication"

python3 scripts/task_manager.py assign rest-api-project qa-agent \
  "Write pytest tests for all API endpoints, target 90%+ coverage, include edge cases"

python3 scripts/task_manager.py assign rest-api-project docs-agent \
  "Write API documentation with OpenAPI spec, include examples and error codes"

python3 scripts/task_manager.py assign rest-api-project security-audit \
  "Perform security audit: SQL injection, XSS, CSRF, rate limiting checks"
```

### 2.2 任务执行流程

线性管道的执行遵循严格顺序，每个阶段有四种可能的状态：待处理（pending）表示等待开始，进行中（in-progress）表示代理正在工作，已完成（done）表示任务已成功结束，失败（failed）表示任务执行出错。下面是完整的执行流程演示，包括状态检查、任务分发、结果保存和自动推进：

```bash
# 查看下一个需要执行的任务
python3 scripts/task_manager.py next rest-api-project

# 更新第一个任务状态为进行中
python3 scripts/task_manager.py update rest-api-project backend-agent in-progress

# 在此处，代理开始工作...
# 工作完成后保存结果
python3 scripts/task_manager.py result rest-api-project backend-agent \
  "Created user.py with 4 endpoints, implemented JWT auth in auth.py, total 500 lines"

# 标记第一个任务完成，系统自动推进到下一个任务
python3 scripts/task_manager.py update rest-api-project backend-agent done

# 再次查看当前状态，应该显示 qa-agent 是下一个任务
python3 scripts/task_manager.py next rest-api-project

# 查看完整项目状态
python3 scripts/task_manager.py status rest-api-project
```

执行完上述命令后，您会看到类似以下的项目状态输出：

```
📋 Project: rest-api-project
🎯 Goal: Build REST API with user authentication and CRUD operations
📊 Status: active | Mode: linear
▶️ Current: qa-agent

 ✅ backend-agent: done
 Task: Implement Flask REST API
 Output: Created user.py with 4 endpoints...
 🔄 qa-agent: in-progress
 Task: Write pytest tests for all API endpoints
 ⬜ docs-agent: pending
 ⬜ security-audit: pending

 Progress: [██░░] 2/4
```

### 2.3 日志记录与历史追踪

在任务执行过程中，记录关键信息和追踪历史变更非常重要。Team Tasks 提供了日志功能，可以为每个阶段添加时间戳标记的日志条目。这对于审计、问题排查和团队协作都非常有价值。以下是日志功能的使用方法：

```bash
# 为已完成的任务添加日志记录
python3 scripts/task_manager.py log rest-api-project backend-agent \
  "Started implementation using Flask-JWT-Extended"

python3 scripts/task_manager.py log rest-api-project backend-agent \
  "Completed /users POST endpoint with password hashing"

python3 scripts/task_manager.py log rest-api-project backend-agent \
  "Completed all 4 endpoints, total 523 lines of code"

# 查看阶段历史
python3 scripts/task_manager.py history rest-api-project backend-agent

# 输出示例：
# [2026-02-09T10:00:00.000000] Started implementation using Flask-JWT-Extended
# [2026-02-09T10:30:00.000000] Completed /users POST endpoint with password hashing
# [2026-02-09T11:00:00.000000] Completed all 4 endpoints, total 523 lines of code
```

## 三、DAG依赖图模式详解

DAG（有向无环图）模式是处理复杂任务依赖关系的理想选择。在这种模式下，任务可以并行执行，只要它们的所有依赖条件都已满足。这种模式特别适合大型功能开发、规范驱动开发、复杂依赖管理等场景。DAG模式的优势在于可以最大化并行度、提高执行效率，缺点是需要仔细设计依赖关系、理解成本较高。

### 3.1 创建DAG项目

创建DAG项目时，您需要为每个任务定义唯一标识符、指定负责的代理、编写任务描述，并声明该任务所依赖的其他任务。系统会自动检测循环依赖并拒绝会导致循环依赖的任务添加。下面是一个完整的工作流定义示例，展示了如何规划一个搜索功能模块的开发过程：

```bash
# 初始化 DAG 项目
python3 scripts/task_manager.py init search-feature \
  -g "Build Elasticsearch-based search feature with autocomplete" \
  -m dag

# 设计阶段：编写 API 规范
python3 scripts/task_manager.py add search-feature design \
  -a docs-agent \
  --desc "Write OpenAPI specification for search endpoints"

# 脚手架阶段：创建项目基础结构
python3 scripts/task_manager.py add search-feature scaffold \
  -a backend-agent \
  --desc "Create project structure, config files, and Elasticsearch connection"

# 实现阶段：依赖设计和脚手架
python3 scripts/task_manager.py add search-feature implement \
  -a backend-agent \
  -d "design,scaffold" \
  --desc "Implement search API and autocomplete logic"

# 编写测试：依赖设计规范
python3 scripts/task_manager.py add search-feature write-tests \
  -a qa-agent \
  -d "design" \
  --desc "Write test cases based on API spec"

# 运行测试：依赖实现代码和测试用例
python3 scripts/task_manager.py add search-feature run-tests \
  -a qa-agent \
  -d "implement,write-tests" \
  --desc "Execute all tests and generate coverage report"

# 编写文档：依赖实现代码
python3 scripts/task_manager.py add search-feature write-docs \
  -a docs-agent \
  -d "implement" \
  --desc "Write final documentation with examples"

# 评审阶段：依赖测试运行和文档完成
python3 scripts/task_manager.py add search-feature review \
  -a security-audit \
  -d "run-tests,write-docs" \
  --desc "Final review and deployment readiness check"
```

### 3.2 可视化依赖图

DAG模式的一个重要特性是可以直观地查看任务之间的依赖关系。通过 `graph` 命令，您可以生成当前任务依赖关系的树形可视化表示，这对于理解项目结构、识别关键路径和发现潜在的瓶颈都非常有帮助。以下命令和输出展示了如何查看依赖图：

```bash
# 生成并显示依赖图
python3 scripts/task_manager.py graph search-feature
```

输出结果如下：

```
📋 search-feature — DAG Graph

├─ ⬜ design [docs-agent]
│ ├─ ⬜ implement [backend-agent]
│ │ ├─ ⬜ run-tests [qa-agent]
│ │ │ └─ ⬜ review [security-audit]
│ │ └─ ⬜ write-docs [docs-agent]
│ └─ ⬜ write-tests [qa-agent]
└─ ⬜ scaffold [backend-agent]
 └─ ⬜ implement (↑ see above)

 Progress: [░░░░░░░] 0/7
```

从图中可以清晰看出：`design` 和 `scaffold` 是根任务，没有依赖可以并行执行；`implement` 依赖 `design` 和 `scaffold` 都完成后才能开始；`write-tests` 只依赖 `design`；`run-tests` 依赖 `implement` 和 `write-tests` 都完成；`write-docs` 依赖 `implement`；`review` 依赖 `run-tests` 和 `write-docs` 都完成。

### 3.3 并行任务分发

DAG模式的核心优势在于可以并行分发和执行独立的任务。通过 `ready` 命令，您可以获取所有当前可执行的任务（依赖条件都已满足），然后将这些任务分发给不同的代理并行执行。这种机制可以显著缩短大型项目的总体完成时间。以下是完整的并行执行流程：

```bash
# 查看当前可执行的任务
python3 scripts/task_manager.py ready search-feature
```

输出显示有两个任务可以并行执行：

```
🟢 Ready to dispatch (2 tasks):
📌 design → agent: docs-agent (deps: none)
📌 scaffold → agent: backend-agent (deps: none)
```

然后，您可以并行地执行这两个任务：

```bash
# 并行执行两个独立任务
# 终端1：执行 design 任务
python3 scripts/task_manager.py update search-feature design in-progress
# ... 代理工作 ...
python3 scripts/task_manager.py result search-feature design "API spec completed in openapi.yaml"
python3 scripts/task_manager.py update search-feature design done

# 终端2：执行 scaffold 任务
python3 scripts/task_manager.py update search-feature scaffold in-progress
# ... 代理工作 ...
python3 scripts/task_manager.py result search-feature scaffold "Project structure created"
python3 scripts/task_manager.py update search-feature scaffold done
```

当这两个任务都完成后，系统会自动检测到被阻塞的任务现在可以执行了：

```bash
# 再次检查可执行任务
python3 scripts/task_manager.py ready search-feature
```

输出显示现在有多个新任务可以执行：

```
🟢 Ready to dispatch (3 tasks):
📌 write-tests → agent: qa-agent (deps: design)
📌 implement → agent: backend-agent (deps: design, scaffold)
📌 write-docs → agent: docs-agent (deps: implement)
```

### 3.4 循环依赖检测

DAG模式会自动检测并拒绝会导致循环依赖的任务添加。这是一个重要的安全特性，可以防止配置错误导致的任务死锁。以下是一个尝试添加无效依赖的示例：

```bash
# 尝试添加一个会导致循环依赖的任务
# 假设 implement 已经依赖 design，如果尝试让 design 依赖 implement
python3 scripts/task_manager.py add search-feature invalid-task \
  -a backend-agent \
  -d "implement" \
  --desc "This would create a cycle"

# 系统会拒绝这个请求并给出错误提示
# Error: Circular dependency: design -> implement -> design
```

这个功能确保了任务依赖图始终保持有向无环的结构，从而保证了任务执行的可终止性。

## 四、辩论模式详解

辩论模式是 Team Tasks 中最独特的协调模式，适用于需要进行多方讨论、观点权衡和综合判断的场景。在这种模式下，多个代理（辩手）对同一个问题提出不同的观点和立场，然后进行交叉评审，最后由人工或协调代理进行综合判断。辩论模式特别适合代码评审、架构决策、安全评估等需要多角度分析的场合。

### 4.1 创建辩论项目

创建辩论项目需要定义评审目标和参与评审的代理。每个代理可以有不同的角色和视角，这有助于确保评审的全面性和深度。以下是一个安全审计场景的完整设置过程：

```bash
# 初始化辩论项目
python3 scripts/task_manager.py init security-review \
  -g "Comprehensive security review of authentication module" \
  -m debate

# 添加辩手（具有不同视角的代理）
python3 scripts/task_manager.py add-debater security-review security-expert \
  -r "Security expert focused on injection attacks, authentication bypasses, and cryptographic issues"

python3 scripts/task_manager.py add-debater security-review qa-engineer \
  -r "QA engineer focused on edge cases, error handling, and input validation"

python3 scripts/task_manager.py add-debater security-review devops-engineer \
  -r "Operations engineer focused on deployment security, secrets management, and rate limiting"
```

### 4.2 辩论流程执行

辩论模式包含四个阶段：初始陈述阶段（initial）让每个代理提出自己的发现和建议，交叉评审阶段（cross_review）让代理评论其他人的观点，综合阶段（synthesis）汇总所有观点形成最终报告。以下是完整的辩论执行流程：

```bash
# 阶段1：开始初始陈述阶段
python3 scripts/task_manager.py round security-review start

# 系统输出每个代理需要评审的提示
# 🗣️ Debate Round 1 (initial) started

# 阶段2：收集各代理的初始陈述
python3 scripts/task_manager.py round security-review collect security-expert \
  "Found SQL injection vulnerability in login() function on line 45. \
   User input directly concatenated into WHERE clause. \
   Recommend using parameterized queries immediately."

python3 scripts/task_manager.py round security-review collect qa-engineer \
  "Missing input validation on email field allows malformed addresses. \
   Error messages reveal whether email exists (user enumeration). \
   Need proper validation and generic error messages."

python3 scripts/task_manager.py round security-review collect devops-engineer \
  "No rate limiting on authentication endpoints. \
   Brute force attack is trivial. \
   Recommend implementing exponential backoff and CAPTCHA."

# 检查所有陈述是否已收集
python3 scripts/task_manager.py status security-review
```

当所有代理完成初始陈述后，系统会自动推进到交叉评审阶段：

```bash
# 阶段3：开始交叉评审
python3 scripts/task_manager.py round security-review cross-review
```

系统会生成交叉评审提示，让每个代理评论其他人的发现：

```bash
# 收集交叉评审意见
python3 scripts/task_manager.py round security-review collect security-expert \
  "I agree with the SQL injection findings (critical). \
   The rate limiting issue is also important but less urgent. \
   The email validation is a medium severity issue."

python3 scripts/task_manager.py round security-review collect qa-engineer \
  "SQL injection is definitely the most critical. \
   I'll add test cases for the edge cases I found. \
   Rate limiting tests should be included in the test suite."

python3 scripts/task_manager.py round security-review collect devops-engineer \
  "All findings are valid. \
   SQL injection is critical - fix immediately. \
   Recommend adding a WAF as an additional layer of defense. \
   Rate limiting should be implemented at multiple levels."
```

### 4.3 综合分析结果

辩论模式的最后阶段是综合所有观点形成最终报告。这个报告包含所有初始陈述、交叉评审意见以及综合分析结论，为决策提供全面的参考：

```bash
# 阶段4：综合所有观点
python3 scripts/task_manager.py round security-review synthesize
```

综合结果输出示例：

```json
{
  "initial_positions": {
    "security-expert": "Found SQL injection vulnerability in login() function...",
    "qa-engineer": "Missing input validation on email field...",
    "devops-engineer": "No rate limiting on authentication endpoints..."
  },
  "cross_reviews": {
    "security-expert": "I agree with the SQL injection findings (critical)...",
    "qa-engineer": "SQL injection is definitely the most critical...",
    "devops-engineer": "All findings are valid..."
  },
  "synthesized_at": "2026-02-09T23:51:00.000000"
}
```

## 五、OpenClaw集成指南

Team Tasks 设计之初就考虑了与 OpenClaw 多代理系统的深度集成。通过 `sessions_send` 工具，主代理可以协调多个工作代理协同完成复杂任务，同时通过 Team Tasks CLI 跟踪和管理整个工作流程。以下详细介绍如何将 Team Tasks 集成到 OpenClaw 工作流中。

### 5.1 线性模式集成

在线性模式下，主代理的调度循环包括以下步骤：查询下一个待执行任务、设置任务状态为进行中、向代理发送任务、等待代理返回结果、保存结果并更新任务状态为已完成。以下是一个完整的集成示例脚本，展示了如何实现这个调度循环：

```python
# linear_dispatch_loop.py - 线性模式调度示例

import subprocess
import json

def get_next_task(project_name):
    """获取下一个待执行的任务"""
    result = subprocess.run(
        ["python3", "scripts/task_manager.py", "next", project_name, "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def dispatch_task(agent_name, task_description):
    """向代理发送任务"""
    from sessions_send import sessions_send
    sessions_send(
        sessionKey=agent_name,
        message=task_description
    )

def update_status(project_name, task_name, status):
    """更新任务状态"""
    subprocess.run([
        "python3", "scripts/task_manager.py", "update",
        project_name, task_name, status
    ])

def save_result(project_name, task_name, result):
    """保存任务结果"""
    subprocess.run([
        "python3", "scripts/task_manager.py", "result",
        project_name, task_name, result
    ])

def run_linear_pipeline(project_name):
    """运行线性管道"""
    while True:
        # 获取下一个任务
        next_task = get_next_task(project_name)
        if not next_task:
            print("所有任务已完成！")
            break
        
        task_name = next_task["stage"]
        agent_name = next_task["agent"]
        description = next_task["description"]
        
        # 更新状态
        update_status(project_name, task_name, "in-progress")
        
        # 发送任务给代理
        dispatch_task(agent_name, description)
        
        # 等待结果（这里简化处理，实际需要等待代理回复）
        result = input(f"请输入 {agent_name} 的执行结果: ")
        
        # 保存结果
        save_result(project_name, task_name, result)
        
        # 标记完成（自动推进到下一个任务）
        update_status(project_name, task_name, "done")
        
        print(f"完成阶段: {task_name}")

# 使用示例
if __name__ == "__main__":
    run_linear_pipeline("my-rest-api")
```

### 5.2 DAG模式集成

DAG模式的集成稍微复杂一些，因为需要处理并行任务分发。主代理需要获取所有当前可执行的任务，然后并行地向不同代理发送任务。以下是DAG模式集成的实现示例：

```python
# dag_dispatch_loop.py - DAG模式调度示例

import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_ready_tasks(project_name):
    """获取所有可执行的任务"""
    result = subprocess.run(
        ["python3", "scripts/task_manager.py", "ready", project_name, "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def run_dag_pipeline(project_name):
    """运行DAG管道"""
    while True:
        # 获取所有可执行任务
        ready_tasks = get_ready_tasks(project_name)
        
        if not ready_tasks:
            # 检查是否所有任务都已完成
            result = subprocess.run(
                ["python3", "scripts/task_manager.py", "status", project_name, "--json"],
                capture_output=True,
                text=True
            )
            project_data = json.loads(result.stdout)
            all_done = all(
                stage.get("status") == "done"
                for stage in project_data.get("stages", {}).values()
            )
            if all_done:
                print("所有任务已完成！")
            else:
                print("等待依赖任务完成...")
            break
        
        # 并行执行所有可执行任务
        with ThreadPoolExecutor(max_workers=len(ready_tasks)) as executor:
            futures = []
            for task in ready_tasks:
                future = executor.submit(
                    execute_task,
                    project_name,
                    task["task"],
                    task["agent"],
                    task["description"]
                )
                futures.append(future)
            
            # 等待所有任务完成
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"任务执行错误: {e}")

def execute_task(project_name, task_id, agent_name, description):
    """执行单个任务"""
    # 更新状态
    subprocess.run([
        "python3", "scripts/task_manager.py", "update",
        project_name, task_id, "in-progress"
    ])
    
    # 这里应该调用 sessions_send，实际实现取决于具体需求
    print(f"向 {agent_name} 发送任务: {task_id}")
    result = input(f"请输入 {agent_name} 对 {task_id} 的执行结果: ")
    
    # 保存结果
    subprocess.run([
        "python3", "scripts/task_manager.py", "result",
        project_name, task_id, result
    ])
    
    # 标记完成
    subprocess.run([
        "python3", "scripts/task_manager.py", "update",
        project_name, task_id, "done"
    ])
    
    print(f"任务 {task_id} 完成")

# 使用示例
if __name__ == "__main__":
    run_dag_pipeline("search-feature")
```

### 5.3 辩论模式集成

辩论模式的集成主要用于多代理评审场景。主代理协调各代理依次提交观点、进行交叉评审，最后生成综合报告。以下是集成的关键步骤：

```python
# debate_integration.py - 辩论模式集成

import subprocess
import json
from sessions_send import sessions_send

def start_debate(project_name):
    """启动辩论"""
    result = subprocess.run(
        ["python3", "scripts/task_manager.py", "round", project_name, "start"],
        capture_output=True,
        text=True
    )
    return result.stdout

def collect_position(project_name, agent_id, position):
    """收集代理观点"""
    subprocess.run([
        "python3", "scripts/task_manager.py", "round", project_name,
        "collect", agent_id, position
    ])

def start_cross_review(project_name):
    """启动交叉评审"""
    result = subprocess.run(
        ["python3", "scripts/task_manager.py", "round", project_name, "cross-review"],
        capture_output=True,
        text=True
    )
    # 返回其他代理的观点供当前代理参考
    return json.loads(result.stdout)

def synthesize_debate(project_name):
    """综合辩论结果"""
    result = subprocess.run(
        ["python3", "scripts/task_manager.py", "round", project_name, "synthesize"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def run_debate_review(project_name, topic, debaters):
    """
    运行多代理辩论评审
    
    参数:
        project_name: 项目名称
        topic: 评审主题
        debaters: 辩手列表 [{"agent": "agent-id", "role": "role description"}]
    """
    # 初始化辩论
    print(f"启动辩论: {topic}")
    start_debate(project_name)
    
    # 收集初始观点
    for debater in debaters:
        print(f"收集 {debater['agent']} 的观点...")
        # 发送评审请求
        sessions_send(
            sessionKey=debater["agent"],
            message=f"请对以下主题进行评审: {topic}\n你的角色: {debater['role']}"
        )
        # 简化处理：实际需要等待代理回复
        position = input(f"请输入 {debater['agent']} 的观点: ")
        collect_position(project_name, debater["agent"], position)
    
    # 开始交叉评审
    print("启动交叉评审...")
    cross_review_data = start_cross_review(project_name)
    
    for debater in debaters:
        other_positions = {
            k: v for k, v in cross_review_data["outputs"].items()
            if k != debater["agent"]
        }
        print(f"收集 {debater['agent']} 的交叉评审...")
        sessions_send(
            sessionKey=debater["agent"],
            message=f"请对以下其他代理的观点进行评论: {json.dumps(other_positions, ensure_ascii=False)}"
        )
        cross_review = input(f"请输入 {debater['agent']} 的交叉评审: ")
        collect_position(project_name, debater["agent"], cross_review)
    
    # 综合结果
    print("生成综合报告...")
    synthesis = synthesize_debate(project_name)
    
    return synthesis

# 使用示例
if __name__ == "__main__":
    result = run_debate_review(
        "security-review",
        "认证模块安全评审",
        [
            {"agent": "security-expert", "role": "安全专家，专注注入攻击"},
            {"agent": "qa-engineer", "role": "QA工程师，专注边界条件"},
            {"agent": "devops", "role": "运维工程师，专注部署安全"}
        ]
    )
    print("综合结果:", result)
```

## 六、常见问题与解决方案

在使用 Team Tasks 的过程中，您可能会遇到一些常见问题。本节整理了这些问题及其解决方案，帮助您快速排除故障并顺利使用工具。

### 6.1 项目管理问题

**问题：尝试创建已存在的项目时收到错误**

这是预期行为，用于防止意外覆盖现有项目。如果您确实想要覆盖，可以添加 `--force` 参数，或者使用 `reset` 命令重置现有项目。解决方案如下：

```bash
# 强制覆盖现有项目
python3 scripts/task_manager.py init my-project -g "New goal" --force

# 或者先重置再重新初始化
python3 scripts/task_manager.py reset my-project --all
python3 scripts/task_manager.py init my-project -g "New goal"
```

**问题：任务状态更新后没有自动推进**

请确保您使用的是线性模式，只有线性模式支持自动推进功能。在DAG模式下，任务完成后需要手动检查 `ready` 命令来获取新解锁的任务。另外，请确认您使用的是 `done` 状态而不是其他状态：

```bash
# 正确的状态更新
python3 scripts/task_manager.py update my-project task-a done

# 错误的示例（不会触发自动推进）
python3 scripts/task_manager.py update my-project task-a completed
```

### 6.2 依赖关系问题

**问题：添加任务时报告循环依赖**

这表明您尝试添加的任务与现有任务形成了循环依赖关系，这是DAG模式不允许的。请重新规划任务依赖结构，确保依赖关系是有向无环的。以下是解决步骤：

```bash
# 首先查看现有依赖关系
python3 scripts/task_manager.py graph my-project

# 重新设计依赖，避免循环
# 正确的做法：确保依赖方向始终向前
python3 scripts/task_manager.py add my-project new-task \
  -a some-agent \
  -d "earlier-task-1,earlier-task-2"
```

**问题：任务显示为待处理但依赖已完成**

这可能是因为依赖关系配置不正确，或者依赖的任务没有正确标记为 `done`。请检查以下几点：

```bash
# 1. 查看任务详情
python3 scripts/task_manager.py status my-project

# 2. 验证依赖配置
# 检查 project.json 中的 dependencies 字段

# 3. 确认依赖任务状态
# 确保所有依赖任务状态都是 "done"
```

### 6.3 辩论模式问题

**问题：辩论阶段不推进**

辩论模式的阶段推进依赖于所有参与者的完成状态。请确保所有辩手都已提交观点才能进入下一阶段：

```bash
# 检查辩论状态
python3 scripts/task_manager.py status debate-project

# 查看各辩手状态
# 确保所有辩手状态都是 "done"

# 如果某个辩手遗漏了观点，需要补交
python3 scripts/task_manager.py round debate-project collect missing-agent "他们的观点"
```

**问题：交叉评审无法启动**

交叉评审阶段需要在初始陈述阶段所有辩手都提交完成后才能启动。如果还有辩手未提交，请先完成收集：

```bash
# 检查是否所有观点都已收集
python3 scripts/task_manager.py status debate-project

# 查看缺失的辩手
# 如果有缺失，先收集所有观点
```

## 七、高级技巧与最佳实践

本节分享一些高级使用技巧和最佳实践，帮助您更高效地使用 Team Tasks 协调多代理工作流程。

### 7.1 项目命名规范

采用清晰一致的命名规范可以提高项目的可维护性。建议使用项目类型前缀、简明的主题描述和版本或序号组合的方式。例如，`feature-user-auth` 表示用户认证功能开发，`bugfix-login-crash` 表示登录崩溃Bug修复，`refactor-payment-module` 表示支付模块重构。这种命名方式让您一眼就能看出项目的性质和范围。

### 7.2 任务粒度控制

任务粒度的选择直接影响协调效率和执行效果。任务过细会导致协调开销增加、状态管理复杂；任务过粗会降低并行度、延长等待时间。建议每个任务保持在一到两小时的工作量，这样既能充分利用并行优势，又不会因为任务过大而难以追踪进度。以下是一个良好的任务划分示例：

```bash
# 良好粒度示例
python3 scripts/task_manager.py add feature-user-auth implement-login \
  -a backend-agent \
  -d "design" \
  --desc "Implement user login with JWT (1-2小时)"

# 避免粒度过细
python3 scripts/task_manager.py add feature-user-auth write-import \
  -a backend-agent \
  -d "scaffold" \
  --desc "Add import statement for JWT library (5分钟) <- 粒度过细"

# 避免粒度过粗
python3 scripts/task_manager.py add feature-user-auth implement-everything \
  -a backend-agent \
  -d "design" \
  --desc "Implement entire user authentication module (2天) <- 粒度过粗"
```

### 7.3 依赖规划策略

良好的依赖规划是DAG模式成功的关键。建议采用以下策略：设计阶段应该先于所有实现阶段，这样可以为实现提供明确的规范；脚手架阶段应该与设计阶段并行，两者没有依赖关系；测试编写应该与实现并行，依赖设计规范但不依赖实现代码；最终评审应该等待所有开发任务完成。这些原则帮助最大化并行度同时保证质量。

### 7.4 结果保存规范

保存任务结果时，建议包含关键信息和执行摘要。以下是推荐的结果保存格式：

```bash
# 推荐的结果格式
python3 scripts/task_manager.py result my-project implement \
  "Created user.py with 3 models, auth.py with JWT handling, \
   total 423 lines. Tests in test_user.py with 28 test cases. \
   Coverage: 91.2%. Issues: none. Next: integration testing."

# 结果应该包含：
# 1. 完成的主要工作
# 2. 代码行数
# 3. 测试覆盖情况
# 4. 发现的问题
# 5. 对下游任务的建议
```

### 7.5 版本控制集成

Team Tasks 的项目数据文件（JSON格式）非常适合纳入版本控制系统。通过Git等工具，您可以追踪项目规划的历史变更、协调多人协作、并保留完整的审计记录。建议将项目文件放在版本控制中，并定期提交变更：

```bash
# 版本控制建议的提交信息格式
git add data/team-tasks/my-project.json
git commit -m "feat(team-tasks): Add user authentication feature project
- Initial design and scaffold tasks completed
- Backend implementation in progress
- Add qa-agent for testing phase"
```

## 八、配置文件参考

Team Tasks 使用环境变量进行配置，主要配置项如下表所示：

| 环境变量 | 说明 | 默认值 | 示例 |
|---------|------|--------|------|
| `TEAM_TASKS_DIR` | 数据存储目录 | `/home/ubuntu/clawd/data/team-tasks` | `/home/user/projects/team-tasks` |
| `TEAM_TASKS_WORKSPACE` | 默认工作区 | 项目目录内的workspace | `/shared/workspace` |

可以通过在shell配置文件中设置这些环境变量来定制工具行为：

```bash
# ~/.bashrc 或 ~/.zshrc 添加
export TEAM_TASKS_DIR="/home/user/projects/team-tasks-data"
export TEAM_TASKS_WORKSPACE="/shared/agent-workspace"
```

## 九、总结与进阶学习

Team Tasks 提供了三种强大的多代理协调模式，可以满足从简单顺序任务到复杂并行工作流的各种需求。线性模式适合流程明确、依赖简单的场景；DAG模式适合需要并行执行、依赖关系明确的复杂项目；辩论模式适合需要多角度分析、多代理评审的场景。

建议您按照以下路径逐步深入学习：首先使用线性模式完成几个简单项目，熟悉基本操作；然后尝试DAG模式管理较复杂的项目，练习依赖规划和并行分发；最后在需要进行评审或决策时使用辩论模式，发挥多代理讨论的优势。随着使用经验的积累，您将能够灵活运用这三种模式来协调各种复杂的多代理工作流程。
