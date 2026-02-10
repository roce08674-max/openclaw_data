# 热点Agent 使用指南

**创建时间**: 2026-02-09 19:39 GMT+8
**版本**: v1.0
**前置条件**: 请先阅读 `SKILL.md` 了解完整功能

---

## 一、安装配置

### 1.1 环境要求

- Python 3.8+
- 操作系统: Windows / macOS / Linux
- 网络: 能够访问互联网（用于数据采集）

### 1.2 安装依赖

```bash
# 进入技能目录
cd skills/hot-agent

# 创建虚拟环境（推荐）
python -m venv hot_agent_env
source hot_agent_env/bin/activate  # Linux/macOS
# 或
hot_agent_env\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 1.3 API配置

热点Agent需要以下API密钥：

| 服务 | 必需性 | 获取方式 |
|------|--------|---------|
| **Brave Search API** | 必需 | https://api.brave.com/ |
| **OpenAI API** | 必需 | https://platform.openai.com/ |
| **社交媒体API** | 可选 | 各平台开发者后台 |

#### 环境变量配置

```bash
# 创建 .env 文件
cat > .env << 'EOF'
# API配置
BRAVE_API_KEY=your_brave_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# 可选配置
LOG_LEVEL=INFO
CACHE_DIR=./cache
OUTPUT_DIR=./output
MAX_CONCURRENT=3
EOF
```

### 1.4 项目结构

```
hot-agent/
├── SKILL.md              # 技能描述
├── HOW_TO_USE.md         # 使用指南（本文档）
├── requirements.txt      # 依赖列表
├── scripts/
│   ├── __init__.py
│   ├── hot_agent.py      # 核心Agent代码
│   ├── collector.py      # 数据采集模块
│   ├── classifier.py     # 事件分类模块
│   ├── tracer.py         # 现象追溯模块
│   ├── analyzer.py       # 心理分析模块
│   ├── graph_builder.py  # 知识图谱模块
│   └── utils.py          # 工具函数
├── references/           # 参考文档
├── cache/                # 缓存目录
└── output/               # 输出目录
```

---

## 二、快速开始

### 2.1 基本使用流程

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点Agent快速示例
"""

import sys
import os

# 添加scripts目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hot_agent import HotTopicAgent

def main():
    """主函数"""
    print("=" * 60)
    print("热点Agent - 热点事件分析与知识图谱生成")
    print("=" * 60)
    
    # 1. 初始化Agent
    print("\n[1/5] 初始化Agent...")
    agent = HotTopicAgent()
    print("✅ Agent初始化完成")
    
    # 2. 采集热点事件
    print("\n[2/5] 采集热点事件...")
    events = agent.collect(
        time_range="24h",           # 过去24小时
        categories=["科技", "财经", "社会"],  # 关注的分类
        keywords=None,              # 不设置关键词，获取综合热点
        limit=50                    # 采集上限
    )
    print(f"✅ 采集完成，共获取 {len(events)} 个事件")
    
    # 3. 查看事件分类
    print("\n[3/5] 事件分类统计...")
    classification = agent.classify(events)
    for category, event_list in classification.items():
        print(f"  {category}: {len(event_list)} 个事件")
    
    # 4. 心理分析
    print("\n[4/5] 心理状态分析...")
    psych_analysis = agent.analyze_psychology(events)
    print(f"  整体情绪: {psych_analysis['overall_mood']}")
    print(f"  情绪评分: {psych_analysis['mood_score']}")
    print(f"  主要情绪: {', '.join(psych_analysis['primary_emotions'])}")
    
    # 5. 生成知识图谱
    print("\n[5/5] 生成知识图谱...")
    graph = agent.generate_knowledge_graph(
        topic="热点事件知识图谱",
        events=events,
        format="mermaid"
    )
    
    # 保存图谱
    output_file = "output/hot_topic_graph.md"
    agent.export_graph(graph, output_file)
    print(f"✅ 知识图谱已保存到 {output_file}")
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

### 2.2 运行示例

```bash
# 进入技能目录
cd skills/hot-agent

# 运行示例
python scripts/example.py

# 或直接运行主脚本
python scripts/hot_agent.py --time-range 24h --categories 科技 财经 社会
```

---

## 三、详细配置

### 3.1 采集配置

```python
from hot_agent import HotTopicAgent

# 自定义采集配置
config = {
    "time_range": "7d",  # 时间范围: 24h, 7d, 30d, 90d
    "categories": ["科技", "财经", "社会", "娱乐"],
    "keywords": ["人工智能", "大模型", "新能源汽车"],
    "sources": ["weibo", "zhihu", "douyin", "news"],
    "limit": 100,  # 采集上限
    "deduplicate": True,  # 去重
    "sort_by": "heat",  # 排序方式: heat, time, relevance
}

agent = HotTopicAgent(config=config)

# 执行采集
events = agent.collect()
```

### 3.2 分类配置

```python
# 自定义分类体系
custom_categories = {
    "人工智能": ["大模型", "GPT", "AI", "机器学习", "深度学习"],
    "新能源汽车": ["电动车", "特斯拉", "比亚迪", "宁德时代", "电池"],
    "元宇宙": ["VR", "AR", "虚拟现实", "数字孪生", "Web3"],
    "消费升级": ["新消费", "品牌升级", "高端化", "品质生活"]
}

agent = HotTopicAgent(categories=custom_categories)
```

### 3.3 心理分析配置

```python
# 心理分析配置
psych_config = {
    "dimensions": ["cognitive", "emotional", "behavioral", "social"],
    "emotion_types": ["fear", "anger", "joy", "sadness", "anxiety", "trust"],
    "sensitivity": "high",  # 分析敏感度: low, medium, high
    "output_format": "detailed"  # 输出格式: brief, detailed, full
}

agent = HotTopicAgent(psych_config=psych_config)
```

### 3.4 知识图谱配置

```python
# 知识图谱配置
graph_config = {
    "node_types": ["event", "phenomenon", "person", "organization", "location"],
    "edge_types": ["causes", "influences", "belongs_to", "happens_before", "related_to"],
    "importance_threshold": 0.3,  # 节点重要性阈值
    "max_nodes": 100,  # 最大节点数
    "visual_format": "mermaid",  # 可视化格式: mermaid, graphviz, json, html
    "show_labels": True,  # 显示标签
    "show_weights": True,  # 显示权重
    "color_scheme": "default"  # 配色方案
}

agent = HotTopicAgent(graph_config=graph_config)
```

### 3.5 RSS新闻采集（无需API密钥）✅

热点Agent集成了RSS新闻采集功能，**无需API密钥**即可立即使用！

#### 支持的RSS订阅源

| 分类 | 订阅源 | 优先级 |
|------|--------|--------|
| **科技** | 36氪、虎嗅、雷锋网、InfoQ、TechCrunch、The Verge | 10 |
| **财经** | 华尔街见闻、财新、第一财经、雪球 | 10 |
| **社会** | 新浪新闻、网易新闻、凤凰网 | 8 |
| **国际** | BBC World、Reuters | 8 |

#### 使用方法

```python
from hot_agent import HotTopicAgent

# 创建Agent（无需API密钥）
agent = HotTopicAgent()

# 使用RSS采集（推荐）
events = agent.collect(
    time_range="24h",           # 时间范围: 24h, 7d, 30d, 90d
    categories=["科技", "财经", "社会"],  # 关注的分类
    limit=100,                   # 采集数量上限
    use_rss=True,                # 启用RSS采集
    use_sample=False,            # 不使用模拟数据
)

print(f"采集到 {len(events)} 条新闻")

# 显示前5条
for i, event in enumerate(events[:5], 1):
    print(f"{i}. [{event.categories.get('primary', 'N/A')}] {event.title}")
    print(f"   来源: {event.source} | 热度: {event.heat_score:.1f}")
```

#### 命令行使用

```bash
# RSS采集模式（推荐）
python scripts/hot_agent.py --time-range 24h --categories 科技 财经 社会 --limit 50

# 混合模式（RSS + 模拟数据）
python scripts/hot_agent.py --time-range 7d --limit 20

# 纯模拟模式（测试用）
python scripts/hot_agent.py --time-range 24h --limit 10 --use-sample
```

#### RSS采集特点

| 特点 | 说明 |
|------|------|
| **无需API密钥** | 直接从RSS源采集数据 |
| **多源聚合** | 同时采集多个RSS订阅源（默认15+源） |
| **自动去重** | 自动过滤已处理的内容 |
| **热度计算** | 根据发布时间和关键词计算热度分数 |
| **缓存支持** | 本地缓存已处理内容 |
| **并行采集** | 多线程并行采集，提高速度 |

---

## 四、高级功能

### 4.1 批量分析模式

```python
# 批量分析大量事件
batch_results = agent.batch_analyze(
    events=all_events,
    batch_size=50,
    parallel=True,  # 启用并行处理
    progress_callback=lambda x: print(f"进度: {x}/{len(all_events)}")
)

# 获取批量分析结果
for result in batch_results:
    print(f"事件: {result.event_id}")
    print(f"  分类: {result.category}")
    print(f"  现象: {[p.name for p in result.phenomena]}")
    print(f"  情绪: {result.psychology.overall_mood}")
```

### 4.2 持续追踪模式

```python
# 持续追踪特定事件
tracker = agent.create_tracker(
    keywords=["AI大模型", "ChatGPT", "人工智能"],
    track_interval=3600,  # 追踪间隔（秒）
    notify_callback=print
)

# 启动追踪
tracker.start()

# 停止追踪
tracker.stop()

# 获取追踪报告
report = tracker.get_report()
print(report)
```

### 4.3 定制报告生成

```python
# 生成定制报告
report = agent.generate_report(
    events=events,
    report_type="daily",  # 报告类型: daily, weekly, monthly, custom
    sections=["overview", "classification", "phenomena", "psychology", "graph"],
    template="formal",  # 报告模板: formal, casual, technical
    output_format="markdown"
)

# 保存报告
agent.save_report(report, "output/daily_report.md")
```

### 4.4 API服务模式

```python
# 启动API服务（可选）
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.post("/analyze")
    async def analyze_hot_topics(request: AnalyzeRequest):
        return agent.analyze(request)
    
    @app.get("/graph")
    async def get_knowledge_graph(topic: str):
        return agent.generate_graph(topic)
    
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 五、输出说明

### 5.1 命令行参数

```bash
python scripts/hot_agent.py [OPTIONS]

可选参数:
  --time-range    时间范围 (default: 24h)
  --categories    事件分类，多个用空格分隔
  --keywords      关键词过滤，多个用空格分隔
  --sources       数据源，多个用空格分隔
  --limit         采集上限 (default: 50)
  --output        输出文件路径
  --format        输出格式 (mermaid/json/html)
  --config        配置文件路径
  --verbose       详细输出
  --help          显示帮助信息
```

### 5.2 使用示例

```bash
# 基本使用 - 采集过去24小时的科技热点
python scripts/hot_agent.py --time-range 24h --categories 科技

# 高级使用 - 多分类、多关键词、指定输出
python scripts/hot_agent.py \
    --time-range 7d \
    --categories 科技 财经 社会 \
    --keywords 人工智能 大模型 \
    --limit 100 \
    --output output/report.md \
    --format mermaid

# 批量模式 - 使用配置文件
python scripts/hot_agent.py --config config.json --verbose
```

### 5.3 配置文件示例 (config.json)

```json
{
  "采集": {
    "time_range": "24h",
    "categories": ["科技", "财经", "社会"],
    "keywords": ["人工智能", "大模型"],
    "sources": ["weibo", "zhihu", "news"],
    "limit": 50,
    "deduplicate": true
  },
  "分类": {
    "custom_categories": {
      "AI": ["大模型", "GPT", "机器学习"]
    }
  },
  "心理分析": {
    "dimensions": ["cognitive", "emotional", "behavioral"],
    "sensitivity": "high"
  },
  "知识图谱": {
    "importance_threshold": 0.3,
    "max_nodes": 100,
    "visual_format": "mermaid"
  },
  "输出": {
    "output_dir": "./output",
    "format": "mermaid"
  }
}
```

---

## 六、常见问题

### 6.1 安装问题

**问题**: pip安装失败

**解决方案**:
```bash
# 升级pip
pip install --upgrade pip

# 使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**问题**: 缺少依赖库

**解决方案**:
```bash
# 逐一安装依赖
pip install openai requests beautifulsoup4 pandas numpy
```

### 6.2 运行问题

**问题**: API密钥错误

**解决方案**:
```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $BRAVE_API_KEY

# 或检查.env文件
cat .env
```

**问题**: 采集不到数据

**解决方案**:
- 检查网络连接
- 确认API密钥有效
- 调整时间范围和分类参数
- 尝试其他数据源

**问题**: 内存不足

**解决方案**:
```python
# 减少采集数量
agent.collect(limit=20)

# 分批处理
for batch in split_batches(all_events, 50):
    process(batch)
```

### 6.3 使用问题

**问题**: 分类不准确

**解决方案**:
- 自定义分类关键词
- 调整分类置信度阈值
- 提供更多事件描述信息

**问题**: 知识图谱太复杂

**解决方案**:
```python
# 提高节点重要性阈值
agent.generate_knowledge_graph(
    importance_threshold=0.7,  # 只保留重要节点
    max_nodes=50  # 限制节点数量
)
```

**问题**: 心理分析结果偏差

**解决方案**:
- 提供更详细的事件文本
- 调整分析维度
- 交叉验证多个事件

---

## 七、最佳实践

### 7.1 日常使用建议

- 每天固定时间执行热点采集，形成数据积累
- 结合多个数据源，提高数据可靠性
- 定期导出分析报告，便于回顾和对比

### 7.2 性能优化建议

- 合理设置采集上限，避免过多数据
- 使用缓存功能，避免重复采集
- 启用并行处理，提高分析速度

### 7.3 数据安全建议

- API密钥使用环境变量管理
- 敏感数据不写入日志
- 定期更换API密钥

### 7.4 结果应用建议

- 结合具体场景使用分析结果
- 交叉验证重要结论
- 持续跟踪热点发展趋势

---

## 八、参考资源

### 8.1 官方文档

- 热点Agent使用指南: `openclaw_data/docs/热点agent使用指南.md`
- 其他Agent指南: `openclaw_data/docs/`

### 8.2 技术文档

- Mermaid语法: https://mermaid.js.org/
- NetworkX文档: https://networkx.org/
- OpenAI API: https://platform.openai.com/docs/

### 8.3 学习资源

- 社会心理学: 《社会心理学》（戴维·迈尔斯著）
- 数据分析: 《数据分析方法》（复旦大学教材）
- 知识图谱: 《知识图谱导论》

---

## 九、联系与支持

### 9.1 问题反馈

遇到问题请先查看：
1. 常见问题章节（本文档第六部分）
2. 官方文档
3. GitHub Issues

### 9.2 功能建议

如有功能建议，请：
1. 描述使用场景
2. 说明期望功能
3. 提供参考案例

---

**文档更新时间**: 2026-02-09 19:39 GMT+8
**版本**: v1.0
**状态**: ✅ 已创建
