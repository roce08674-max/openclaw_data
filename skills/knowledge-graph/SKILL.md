---
name: knowledge-graph
description: 知识图谱构建、嵌入学习和分析工具。用于构建实体关系图、计算语义相似度、进行链接预测和知识推理。支持多种嵌入模型（TransE、RotatE、ComplEx等），适用于热点事件分析、舆情监测、知识管理等场景。
---

# 知识图谱技能

本技能提供完整的知识图谱构建、嵌入学习和分析功能。通过实体识别、关系抽取、嵌入表示和语义分析，实现知识的结构化表示和智能推理。

## 功能概览

### 核心能力
- **实体识别与嵌入**：将文本中的实体（人物、事件、概念等）识别并表示为向量
- **关系建模**：构建实体间的语义关系（因果、包含、关联等）
- **语义相似度计算**：基于嵌入向量计算实体间的语义相似度
- **链接预测**：预测实体间可能存在但未被明确标注的关系
- **知识推理**：基于知识图谱进行逻辑推理和知识补全

### 嵌入模型
| 模型 | 特点 | 适用场景 |
|------|------|---------|
| TransE | 翻译模型，简单高效 | 基础关系学习 |
| RotatE | 旋转建模，对称/反对称关系 | 复杂关系模式 |
| ComplEx | 复数嵌入，支持多重关系 | 复杂语义表示 |
| DistMult | 双线性模型，简单可解释 | 推荐系统 |

### 应用场景
- 热点事件分析：发现事件间的关联和传播路径
- 舆情监测：追踪情绪演变和观点传播
- 知识管理：组织和管理结构化知识
- 智能问答：基于知识图谱的问答系统

## 使用方法

### 基本用法

```python
from knowledge_graph import KnowledgeGraph, EmbeddingModel

# 创建知识图谱
kg = KnowledgeGraph()

# 添加实体
kg.add_entity("AI突破", entity_type="事件", attributes={"热度": 95})
kg.add_entity("ChatGPT发布", entity_type="事件")
kg.add_entity("大语言模型", entity_type="技术")

# 添加关系
kg.add_relation("AI突破", "导致", "大语言模型")
kg.add_relation("ChatGPT发布", "属于", "大语言模型")

# 训练嵌入模型
model = EmbeddingModel(model_name="TransE", embedding_dim=128)
model.train(kg)

# 计算相似度
similarity = model.similarity("AI突破", "ChatGPT发布")
```

### 热点事件分析

```python
# 从热点新闻构建知识图谱
events = [
    {"title": "AI大模型取得突破", "category": "科技", "heat": 95},
    {"title": "新能源车销量增长", "category": "财经", "heat": 90},
]

# 构建图谱
kg = KnowledgeGraph()
kg.build_from_events(events)

# 分析关联
analysis = kg.analyze_correlations()
print(analysis)
```

## 嵌入分析

### 语义相似度
计算两个实体在语义空间中的相似程度，取值范围为0到1，值越大表示越相似。

### 链接预测
给定头实体和关系，预测可能的尾实体；或给定尾实体和关系，预测可能的头实体。

### 实体聚类
基于嵌入向量对实体进行聚类，发现具有相似特征的实体群组。

## 最佳实践

1. **实体粒度控制**
   - 避免过细：不要为每个词创建实体
   - 避免过粗：确保实体有明确的语义边界
   - 推荐：主题级实体（事件、概念、组织）

2. **关系质量**
   - 使用标准关系类型（因果、包含、关联等）
   - 避免循环依赖
   - 保持关系的语义一致性

3. **嵌入维度选择**
   - 小规模图谱（<1000实体）：64-128维
   - 中等规模图谱（1000-10000实体）：128-256维
   - 大规模图谱（>10000实体）：256-512维

4. **训练数据准备**
   - 确保实体和关系的数量平衡
   - 避免数据泄露，正确划分训练/验证/测试集

## 示例

### 示例1：科技领域知识图谱

```python
# 创建科技领域知识图谱
kg = KnowledgeGraph()

# 添加科技实体
entities = [
    ("人工智能", "领域", {"描述": "模拟人类智能的技术"}),
    ("深度学习", "技术", {"描述": "基于神经网络的机器学习方法"}),
    ("Transformer", "架构", {"描述": "注意力机制为核心的神经网络架构"}),
    ("GPT", "模型", {"描述": "生成式预训练Transformer模型"}),
    ("ChatGPT", "产品", {"描述": "OpenAI开发的对话AI产品"}),
]

for name, etype, attrs in entities:
    kg.add_entity(name, entity_type=etype, attributes=attrs)

# 添加关系
relations = [
    ("深度学习", "属于", "人工智能"),
    ("Transformer", "实现", "深度学习"),
    ("GPT", "基于", "Transformer"),
    ("ChatGPT", "基于", "GPT"),
]

for src, rel, tgt in relations:
    kg.add_relation(src, rel, tgt)

# 训练嵌入
model = EmbeddingModel("TransE", embedding_dim=128)
model.train(kg)

# 预测链接
predictions = model.predict_links("ChatGPT", "属于")
```

### 示例2：热点事件关联分析

```python
# 从新闻构建知识图谱
news_data = [
    {"title": "AI大模型再获突破", "source": "36氪", "category": "科技", "keywords": ["AI", "大模型"]},
    {"title": "新能源汽车销量增长", "source": "虎嗅", "category": "财经", "keywords": ["新能源", "汽车"]},
    {"title": "房地产市场政策调整", "source": "36氪", "category": "财经", "keywords": ["房地产", "政策"]},
]

# 构建图谱
kg = KnowledgeGraph()
kg.build_from_news(news_data)

# 嵌入分析
model = EmbeddingModel("RotatE", embedding_dim=64)
model.train(kg)

# 找相似事件
similar = model.find_similar_entities("AI大模型再获突破", top_k=3)

# 聚类分析
clusters = model.cluster_entities("event", n_clusters=2)
```

## 与其他技能的配合

### 与热点Agent配合
1. 使用热点Agent采集热点事件
2. 使用本技能构建知识图谱
3. 使用嵌入分析发现事件关联
4. 生成关联分析报告

### 与浏览器采集配合
1. 使用浏览器采集微博热搜、知乎热榜
2. 使用本技能提取实体和关系
3. 构建实时更新的知识图谱
4. 进行舆情分析和趋势预测

## 限制与注意事项

1. **计算资源**
   - 大规模图谱需要GPU加速
   - 建议使用批处理避免内存溢出

2. **数据质量**
   - 实体和关系的准确性直接影响分析结果
   - 建议人工验证关键实体和关系

3. **模型选择**
   - 不同模型适合不同类型的知识图谱
   - 建议根据具体场景选择合适的模型

4. **冷启动问题**
   - 实体数量少时嵌入效果有限
   - 建议在实体数量>100时使用嵌入分析
