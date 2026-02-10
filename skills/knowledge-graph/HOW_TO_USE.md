# 知识图谱技能使用指南

本指南详细介绍知识图谱技能的安装、配置、使用方法和最佳实践。通过本指南，您将学会如何构建知识图谱、训练嵌入模型、进行语义分析和知识推理。无论您是初学者还是有经验的开发者，都能找到适合自己的学习路径和实践方案。

## 一、安装与配置

### 1.1 环境要求

本技能支持Python 3.8及以上版本，无需安装任何外部依赖即可使用基础功能。对于需要使用高级嵌入模型（如TransE、RotatE）的场景，建议安装以下依赖：

```
Python >= 3.8
numpy >= 1.20.0  （可选，用于数值计算）
scipy >= 1.7.0   （可选，用于高级数学运算）
```

安装命令如下：

```bash
# 基础安装（仅核心功能）
pip install -e ./skills/knowledge-graph/

# 完整安装（包含所有依赖）
pip install -e ./skills/knowledge-graph/[full]
```

### 1.2 技能目录结构

安装后，技能文件将位于以下目录：

```
skills/knowledge-graph/
├── SKILL.md              # 技能说明文档
├── HOW_TO_USE.md         # 本使用指南
├── _meta.json            # 元数据配置
├── README.md             # 快速入门
└── scripts/
    ├── knowledge_graph.py    # 核心模块（32KB）
    ├── embedding_models.py   # 嵌入模型实现
    └── __init__.py           # 包初始化
```

### 1.3 导入和使用

在Python代码中导入知识图谱技能的方法如下：

```python
# 导入核心类
from knowledge_graph import KnowledgeGraph, create_embedding_model

# 导入特定模型
from knowledge_graph import TransEModel, RotatEModel, SimpleEmbeddingModel

# 创建知识图谱
kg = KnowledgeGraph("我的知识图谱")
```

## 二、快速入门

### 2.1 创建第一个知识图谱

让我们从创建一个简单的知识图谱开始，了解基本操作流程：

```python
from knowledge_graph import KnowledgeGraph, create_embedding_model

# 1. 创建知识图谱实例
kg = KnowledgeGraph("科技领域知识图谱")

# 2. 添加实体
kg.add_entity(
    name="人工智能",
    entity_type="领域",
    attributes={"描述": "模拟人类智能的技术领域"}
)

kg.add_entity(
    name="机器学习",
    entity_type="技术",
    attributes={"描述": "让计算机从数据中学习的技术"}
)

# 3. 添加关系
kg.add_relation(
    source_entity="机器学习",
    relation_type="属于",
    target_entity="人工智能"
)

# 4. 查看图谱摘要
print(kg.summary())
```

运行结果将显示：

```
知识图谱: 科技领域知识图谱
实体数量: 2
关系数量: 1
实体类型: {'领域': 1, '技术': 1}
关系类型: ['属于']
```

### 2.2 训练嵌入模型

知识图谱嵌入是将实体和关系表示为低维向量的过程，这些向量可以捕捉语义信息并支持各种分析任务：

```python
# 创建嵌入模型（支持TransE、RotatE、Simple）
model = create_embedding_model(
    model_name="TransE",    # 模型名称
    embedding_dim=128       # 嵌入维度
)

# 训练模型
model.train(
    knowledge_graph=kg,
    epochs=100,            # 训练轮数
    lr=0.01,              # 学习率
    batch_size=32         # 批大小
)

print("模型训练完成！")
```

### 2.3 语义相似度计算

训练完成后，我们可以计算任意两个实体之间的语义相似度：

```python
# 计算两个实体的相似度
similarity = model.similarity("人工智能", "机器学习")
print(f"人工智能与机器学习的相似度: {similarity:.4f}")

# 查找与指定实体最相似的实体
similar_entities = kg.find_similar_entities(
    entity_id="人工智能",
    model=model,
    top_k=5                # 返回前5个最相似的实体
)

print("\n与'人工智能'最相似的实体:")
for entity, score in similar_entities:
    print(f"  - {entity.name}: {score:.4f}")
```

### 2.4 链接预测

链接预测是知识图谱嵌入的核心应用之一，可以预测实体间可能存在但未被明确标注的关系：

```python
# 预测链接：给定头实体和关系类型，预测可能的尾实体
predictions = kg.predict_links(
    entity_id="机器学习",
    relation_type="属于",
    model=model,
    top_k=5
)

print("链接预测结果（机器学习，属于）:")
for entity, score in predictions:
    print(f"  - {entity.name}: {score:.4f}")
```

## 三、进阶功能

### 3.1 批量添加实体和关系

在构建大规模知识图谱时，批量添加实体和关系可以显著提高效率：

```python
# 批量添加实体
entities_data = [
    {"name": "深度学习", "type": "技术", "attrs": {"层级": "机器学习"}},
    {"name": "神经网络", "type": "架构", "attrs": {"结构": "多层"}},
    {"name": "卷积神经网络", "type": "模型", "attrs": {"应用": "图像处理"}},
    {"name": "循环神经网络", "type": "模型", "attrs": {"应用": "序列处理"}},
    {"name": "Transformer", "type": "架构", "attrs": {"特点": "注意力机制"}},
]

for data in entities_data:
    kg.add_entity(
        name=data["name"],
        entity_type=data["type"],
        attributes=data["attrs"]
    )

# 批量添加关系
relations_data = [
    ("深度学习", "基于", "神经网络"),
    ("卷积神经网络", "属于", "深度学习"),
    ("循环神经网络", "属于", "深度学习"),
    ("Transformer", "实现", "注意力机制"),
]

for src, rel, tgt in relations_data:
    kg.add_relation(src, rel, tgt)
```

### 3.2 从事件数据构建知识图谱

本技能支持从事件列表自动构建知识图谱，特别适用于热点事件分析场景：

```python
# 准备事件数据
events = [
    {
        "title": "AI大模型再获突破",
        "category": "科技",
        "heat_score": 95,
        "keywords": ["AI", "大模型", "突破"],
        "source": "36氪",
        "publish_time": "2024-01-15"
    },
    {
        "title": "新能源汽车销量增长",
        "category": "财经",
        "heat_score": 90,
        "keywords": ["新能源", "汽车", "销量"],
        "source": "虎嗅",
        "publish_time": "2024-01-14"
    },
    {
        "title": "房地产市场政策调整",
        "category": "财经",
        "heat_score": 88,
        "keywords": ["房地产", "政策", "调控"],
        "source": "新浪",
        "publish_time": "2024-01-13"
    }
]

# 从事件构建知识图谱
event_count = kg.build_from_events(events, extract_entities=True)
print(f"从{len(events)}个事件中构建了{event_count}个实体")

# 自动提取的实体包括：
# - 事件实体（AI大模型再获突破、新能源汽车销量增长等）
# - 关键词概念实体（AI、大模型、新能源等）
# - 以及它们之间的关系
```

### 3.3 实体聚类分析

基于嵌入向量，我们可以对实体进行聚类，发现具有相似特征的实体群组：

```python
# 对所有事件实体进行聚类
clusters = kg.cluster_entities(
    entity_type="event",   # 只聚类事件类型的实体
    model=model,
    n_clusters=2           # 分成2个聚类
)

print("实体聚类结果:")
for cluster_id, entities in clusters.items():
    print(f"\n聚类 {cluster_id}:")
    for entity in entities:
        print(f"  - {entity.name} ({entity.entity_type})")
        if entity.attributes.get("keywords"):
            print(f"    关键词: {entity.attributes['keywords']}")
```

### 3.4 导出和保存

知识图谱支持多种导出格式，便于保存和分享：

```python
# 导出为JSON格式
json_output = kg.export(format="json")
with open("knowledge_graph.json", "w", encoding="utf-8") as f:
    f.write(json_output)

# 导出为RDF格式（简化版）
rdf_output = kg.export(format="rdf")
with open("knowledge_graph.rdf", "w", encoding="utf-8") as f:
    f.write(rdf_output)

# 加载已保存的知识图谱
with open("knowledge_graph.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

## 四、嵌入模型详解

### 4.1 TransE模型

TransE（Translating Embeddings）是最经典的的知识图谱嵌入模型之一。它的核心思想是将关系建模为实体嵌入空间中的翻译向量。对于正确的关系三元组（h, r, t），应满足h + r ≈ t。

TransE模型适用于以下场景：关系类型相对简单、实体数量较大、对训练效率有要求、需要良好的可解释性。以下是使用示例：

```python
from knowledge_graph import TransEModel

# 创建TransE模型
model = TransEModel(
    embedding_dim=128,   # 嵌入维度
    margin=1.0          # 边际损失参数
)

# 训练模型
model.train(
    knowledge_graph=kg,
    epochs=100,
    lr=0.01
)

# 使用模型
similarity = model.similarity("实体A", "实体B")
```

### 4.2 RotatE模型

RotatE模型将关系建模为复平面上的旋转操作。对于关系r和实体h、t，满足h ∘ r = t（复数乘法）。RotatE能够自然地建模对称关系、反对称关系和逆转关系。

RotatE模型适用于以下场景：关系模式复杂、需要建模对称性和反对称性、对预测精度有较高要求、计算资源充足。以下是使用示例：

```python
from knowledge_graph import RotatEModel

# 创建RotatE模型
model = RotatEModel(
    embedding_dim=128  # 注意：RotatE实际使用 embedding_dim/2 维实部 + embedding_dim/2 维虚部
)

# 训练模型
model.train(kg, epochs=150, lr=0.005)

# RotatE在处理对称关系时表现更好
symmetry_score = model.symmetry_score("实体A", "实体B")
```

### 4.3 SimpleEmbeddingModel

SimpleEmbeddingModel是一个轻量级模型，不需要任何外部依赖。它基于实体名称和类型生成简单的向量表示，适用于资源受限环境或快速原型验证。

SimpleEmbeddingModel适用于以下场景：没有numpy等依赖、需要进行快速原型验证、资源极其受限、不需要高精度的嵌入表示。以下是使用示例：

```python
from knowledge_graph import SimpleEmbeddingModel

# 创建简单模型（无需任何依赖）
model = SimpleEmbeddingModel(embedding_dim=64)

# 训练（实际上是初始化）
model.train(kg, epochs=0)

# 使用
similarity = model.similarity("实体A", "实体B")
```

### 4.4 模型选择指南

选择合适的嵌入模型需要考虑多个因素。以下是详细对比：

| 模型 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| TransE | 简单高效、可解释性好、训练快 | 难以建模复杂关系 | 大规模图谱、简单关系 |
| RotatE | 建模复杂关系模式、对称性支持 | 参数多、训练慢 | 复杂关系、需要高精度 |
| Simple | 无依赖、轻量级 | 精度有限 | 原型验证、资源受限 |

对于大多数热点事件分析场景，建议从TransE模型开始，它在效率和效果之间取得了良好的平衡。如果发现模型效果不佳，可以尝试RotatE模型。

## 五、与热点Agent集成

### 5.1 集成架构

知识图谱技能可以与热点Agent无缝集成，形成完整的热点事件分析系统。集成架构如下：

```
数据采集层 -> 知识图谱构建 -> 嵌入分析 -> 可视化输出
   ↑              ↓              ↓          ↓
热点Agent    知识图谱技能    嵌入模型    报告生成
浏览器采集    (本技能)      (TransE等)  (Mermaid)
```

### 5.2 集成代码示例

以下是完整的集成示例：

```python
from knowledge_graph import KnowledgeGraph, create_embedding_model
from enhanced_hot_agent import EnhancedHotTopicAgent

# 1. 创建热点Agent并采集事件
hot_agent = EnhancedHotTopicAgent()
events = hot_agent.collect_events(limit=20, use_browser=True)

# 2. 创建知识图谱并从事件构建
kg = KnowledgeGraph("热点事件知识图谱")
kg.build_from_events(events)

# 3. 训练嵌入模型
model = create_embedding_model("TransE", embedding_dim=64)
model.train(kg, epochs=50)

# 4. 进行嵌入分析
print("\n=== 语义相似度分析 ===")
for i in range(min(5, len(events))):
    for j in range(i+1, min(6, len(events))):
        entity_id_i = f"event_{i}"
        entity_id_j = f"event_{j}"
        sim = model.similarity(entity_id_i, entity_id_j)
        if sim > 0.9:
            title_i = events[i].title[:30]
            title_j = events[j].title[:30]
            print(f"  {title_i} <-> {title_j}: {sim:.4f}")

# 5. 聚类分析
print("\n=== 事件聚类 ===")
clusters = kg.cluster_entities("event", model, n_clusters=3)
for cid, entities in clusters.items():
    print(f"\n聚类 {cid} ({len(entities)}个事件):")
    for entity in entities[:3]:  # 每个聚类只显示前3个
        print(f"  - {entity.name[:40]}")
    if len(entities) > 3:
        print(f"  ... 等共{len(entities)}个")

# 6. 导出知识图谱
kg.export("json")
print(f"\n✅ 知识图谱构建完成！")
print(f"   实体数: {kg.statistics['entity_count']}")
print(f"   关系数: {kg.statistics['relation_count']}")
```

### 5.3 分析结果解读

知识图谱嵌入分析可以提供以下洞察：

第一是事件关联发现。通过计算事件间的语义相似度，可以发现表面上不相关但实际上有内在联系的事件。例如，AI技术突破和新能源政策调整可能在某些维度上高度相似。

第二是趋势识别。聚类分析可以识别出热点事件的主题分布，帮助理解当前舆论焦点。例如，科技类事件可能聚成一类，财经类事件聚成另一类。

第三是舆情预测。通过链接预测，可以推断哪些事件可能会引发后续连锁反应，为舆情预警提供参考。

## 六、热点事件分析实战

### 6.1 完整分析流程

以下是一个完整的热点事件知识图谱分析实战案例：

```python
from knowledge_graph import KnowledgeGraph, create_embedding_model
import random
from datetime import datetime, timedelta

# 创建知识图谱
kg = KnowledgeGraph("2024年热点事件分析")

# 模拟热点事件数据
events_data = [
    {"title": "AI大模型再获突破，行业迎来新变革", "category": "科技", "heat": 95},
    {"title": "新能源汽车销量持续增长，市场格局生变", "category": "财经", "heat": 92},
    {"title": "房地产市场政策调整，买房时机引关注", "category": "财经", "heat": 91},
    {"title": "科技巨头发布新品，引领行业发展新趋势", "category": "科技", "heat": 90},
    {"title": "社会热点事件引发广泛讨论，舆论持续发酵", "category": "社会", "heat": 89},
    {"title": "国际形势复杂多变，经济影响逐步显现", "category": "国际", "heat": 88},
    {"title": "5G网络商用加速，产业数字化转型", "category": "科技", "heat": 87},
    {"title": "互联网平台监管加强，规范行业发展", "category": "科技", "heat": 86},
    {"title": "芯片技术自主可控成为焦点", "category": "科技", "heat": 85},
    {"title": "数字经济蓬勃发展，新业态不断涌现", "category": "经济", "heat": 84},
]

# 添加事件实体
event_entities = []
for i, event in enumerate(events_data):
    entity = kg.add_entity(
        name=event["title"],
        entity_type="event",
        attributes={
            "category": event["category"],
            "heat_score": event["heat"],
            "keywords": ["科技", "创新", "发展"]
        }
    )
    event_entities.append(entity)

# 添加现象层实体
phenomena = [
    ("技术普及", "phenomenon"),
    ("市场关注", "phenomenon"),
    ("政策支持", "phenomenon"),
    ("资本投入", "phenomenon"),
]

for name, ptype in phenomena:
    kg.add_entity(name, entity_type=ptype)

# 建立事件与现象的关系
for i, event in enumerate(events_data):
    for j, (phenom, _) in enumerate(phenomena):
        kg.add_relation(
            event["title"],
            "导致",
            phenom,
            weight=random.uniform(0.6, 0.9)
        )

# 添加心理层实体
emotions = [
    ("积极乐观", "psychology"),
    ("期待", "psychology"),
    ("兴奋", "psychology"),
    ("焦虑", "psychology"),
]

for name, etype in emotions:
    kg.add_entity(name, entity_type=etype)

# 建立现象与心理的关系
for j, (phenom, _) in enumerate(phenomena):
    for k, (emotion, _) in enumerate(emotions):
        kg.add_relation(
            phenom,
            "影响",
            emotion,
            weight=random.uniform(0.5, 0.8)
        )

print("=" * 80)
print("热点事件知识图谱分析")
print("=" * 80)

# 统计信息
print(f"\n📊 统计信息:")
print(f"   实体数: {kg.statistics['entity_count']}")
print(f"   关系数: {kg.statistics['relation_count']}")
print(f"   实体类型: {kg.statistics['entity_types']}")

# 训练嵌入模型
print(f"\n🔧 训练嵌入模型...")
model = create_embedding_model("TransE", embedding_dim=64)
model.train(kg, epochs=100)

# 事件相似度分析
print(f"\n📈 事件相似度分析:")
for i in range(min(5, len(events_data))):
    for j in range(i+1, min(6, len(events_data))):
        sim = model.similarity(event_entities[i].entity_id, event_entities[j].entity_id)
        if sim > 0.85:
            print(f"   {events_data[i]['title'][:25]}... <-> {events_data[j]['title'][:25]}...")
            print(f"   相似度: {sim:.4f}")

# 聚类分析
print(f"\n🎯 事件聚类:")
clusters = kg.cluster_entities("event", model, n_clusters=2)
for cid, entities in clusters.items():
    categories = {}
    for entity in entities:
        cat = entity.attributes.get("category", "未知")
        categories[cat] = categories.get(cat, 0) + 1
    print(f"   聚类{cid+1}: {len(entities)}个事件")
    for cat, count in categories.items():
        print(f"      - {cat}: {count}个")

# 链接预测
print(f"\n🔗 链接预测示例:")
predictions = kg.predict_links(
    event_entities[0].entity_id,
    "导致",
    model,
    top_k=3
)
print(f"   预测'{events_data[0]['title'][:20]}...'可能导致的现象:")
for entity, score in predictions:
    print(f"      - {entity.name}: {score:.4f}")

print("\n" + "=" * 80)
print("✅ 分析完成！")
print("=" * 80)
```

### 6.2 结果解读

运行上述代码后，你将获得以下分析结果：

第一层是统计概览。知识图谱包含事件实体、现象实体、心理实体等多种类型的节点，以及它们之间的关系。通过统计信息可以了解图谱的规模和复杂度。

第二层是相似度分析。通过计算事件间的语义相似度，可以发现表面上不相关但实际上有内在联系的事件对。高相似度的事件可能在主题、受众或影响范围上相近。

第三层是聚类分析。通过K-Means聚类，可以将事件按照语义特征分成若干组。每个聚类代表一类主题相近的事件，有助于理解热点分布格局。

第四层是链接预测。通过链接预测，可以推断给定事件可能导致的后续现象。这对于舆情监测和趋势预测非常有价值。

## 七、性能优化

### 7.1 大规模图谱优化

当知识图谱规模较大时（实体数超过10000），需要注意以下优化：

第一是嵌入维度选择。对于大规模图谱，建议使用128-256维的嵌入。维度太低可能无法捕捉足够的语义信息，维度太高则会增加计算成本。

```python
# 大规模图谱推荐配置
model = create_embedding_model(
    model_name="TransE",
    embedding_dim=128  # 或256
)
```

第二是批处理训练。大规模图谱应该使用批处理方式进行训练，避免一次性加载所有数据。

```python
from knowledge_graph import TransEModel

class LargeScaleTransE(TransEModel):
    def train(self, kg, epochs=100, lr=0.01, batch_size=1024, **kwargs):
        """大规模图谱训练（分批处理）"""
        entities = list(kg.entities.values())
        relations = list(kg.relations)

        # 分批处理
        for epoch in range(epochs):
            # 随机采样一批三元组
            batch_size = min(batch_size, len(relations))
            sampled_relations = random.sample(relations, batch_size)

            # 计算损失并更新
            for rel in sampled_relations:
                # ... 训练逻辑
                pass

            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs}")
```

### 7.2 内存优化

对于内存受限环境，可以考虑以下优化策略：

第一是稀疏表示。对于高维稀疏向量，使用稀疏矩阵存储可以显著减少内存占用。

第二是增量计算。不需要一次性计算所有实体的嵌入，可以按需计算。

```python
# 延迟加载嵌入
class LazyKnowledgeGraph(KnowledgeGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._embeddings_loaded = False

    def get_entity_embedding(self, entity_id, model):
        """按需加载嵌入"""
        entity = self.entities.get(entity_id)
        if entity and entity.embedding is None:
            # 只有在需要时才训练
            if not model.is_trained:
                model.train(self, epochs=0)
        return entity.embedding if entity else None
```

### 7.3 并行计算

对于需要处理大量查询的场景，可以使用多线程或异步计算：

```python
import concurrent.futures

def batch_similarity(entity_ids, model):
    """批量计算相似度"""
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for i, eid1 in enumerate(entity_ids):
            for eid2 in entity_ids[i+1:]:
                future = executor.submit(model.similarity, eid1, eid2)
                futures[future] = (eid1, eid2)

        for future in concurrent.futures.as_completed(futures):
            eid1, eid2 = futures[future]
            results[(eid1, eid2)] = future.result()

    return results
```

## 八、常见问题

### 8.1 模型训练问题

问题一：训练时间过长怎么办？

解决方案：首先检查实体数量是否过多。如果是，可以使用批处理训练或简化模型（如使用SimpleEmbeddingModel）。也可以减少epochs数量或增大学习率。

问题二：模型收敛效果不好怎么办？

解决方案：尝试调整学习率（通常0.001-0.1）、增加训练轮数、或更换其他嵌入模型。也可以检查数据质量，确保实体和关系的准确性。

问题三：相似度计算结果异常（全部为0或1）？

解决方案：检查实体是否存在，嵌入是否已训练。如果使用SimpleEmbeddingModel，确保实体名称不为空。

### 8.2 内存问题

问题一：内存不足怎么办？

解决方案：减少嵌入维度、使用稀疏表示、分批处理数据、或者使用SimpleEmbeddingModel（无外部依赖，内存占用小）。

问题二：大规模图谱导出失败怎么办？

解决方案：使用流式导出，避免一次性加载所有数据到内存。也可以只导出子图。

### 8.3 功能问题

问题一：找不到实体怎么办？

解决方案：检查实体ID和名称是否正确。使用`kg._find_entity_id()`方法可以根据名称查找实体ID。

问题二：关系添加失败怎么办？

解决方案：检查源实体和目标实体是否存在。如果实体不存在，方法会发出警告但仍会创建关系，只是关系头尾可能指向不存在的实体。

问题三：嵌入分析没有结果怎么办？

解决方案：确保模型已训练（`model.is_trained == True`），确保图谱中有足够的实体（建议至少10个以上）。

## 九、最佳实践

### 9.1 数据质量

第一是实体命名规范。使用有意义的名称，便于理解和检索。建议使用"主题+类型"的命名方式，如"AI大模型（事件）"。

第二是关系类型标准化。定义一套标准的关系类型，如"属于""导致""影响""相关"等，保持语义一致性。

第三是属性完整性。为实体添加必要的属性，如来源、时间、热度等，便于后续分析。

### 9.2 模型选择

对于初学者，建议从SimpleEmbeddingModel开始，它无需任何依赖，可以快速验证思路。

对于正式项目，建议使用TransEModel，它在效率和效果之间取得了良好的平衡。

对于高精度要求的场景，可以使用RotatEModel，它能够建模更复杂的关系模式。

### 9.3 性能调优

第一是维度选择。小规模图谱（<1000实体）建议64-128维，中等规模（1000-10000实体）建议128-256维，大规模（>10000实体）建议256-512维。

第二是迭代次数。通常50-200次迭代即可达到收敛，具体取决于图谱规模和复杂度。

第三是批量大小。对于大规模图谱，建议使用较大的批大小（如256-1024）以提高训练效率。

### 9.4 可视化

知识图谱可以导出为多种格式进行可视化：

```python
# 导出为JSON用于D3.js可视化
json_data = kg.export("json")
import json
data = json.loads(json_data)
# 结构: {"entities": {...}, "relations": [...]}

# 导出为Mermaid用于文档展示
mermaid_code = kg.export("mermaid")  # 如果支持
```

## 十、总结

本指南涵盖了知识图谱技能的各个方面，从基础概念到高级应用，从安装配置到性能优化。通过学习和实践，您应该能够：

熟练掌握知识图谱的创建、实体和关系的管理。理解并能够使用不同的嵌入模型（TransE、RotatE、Simple）。进行语义相似度计算、链接预测和实体聚类分析。将知识图谱技能与热点Agent等工具集成使用。针对不同场景选择合适的模型和参数配置。

知识图谱是一项强大的技术，可以帮助我们更好地理解、组织和分析结构化知识。希望本指南能够帮助您在实际项目中充分发挥知识图谱技能的潜力。如有任何问题或建议，欢迎提出反馈。

## 附录

### A. 支持的实体类型

| 类型 | 说明 | 示例 |
|------|------|------|
| event | 事件 | 会议发布、事故发生 |
| concept | 概念 | 人工智能、区块链 |
| person | 人物 | 企业家、科学家 |
| organization | 组织 | 公司、机构 |
| location | 地点 | 国家、城市 |
| technology | 技术 | 深度学习、云计算 |
| product | 产品 | 软件、硬件 |

### B. 支持的关系类型

| 关系类型 | 说明 | 示例 |
|----------|------|------|
| 属于 | 分类关系 | 深度学习属于人工智能 |
| 导致 | 因果关系 | 政策调整导致市场变化 |
| 影响 | 影响关系 | 技术创新影响行业发展 |
| 相关 | 关联关系 | A与B相关 |
| 包含 | 包含关系 | 中国包含北京 |
| 实现 | 实现关系 | Transformer实现注意力机制 |

### C. 配置文件示例

```json
{
  "model": "TransE",
  "embedding_dim": 128,
  "epochs": 100,
  "learning_rate": 0.01,
  "batch_size": 32,
  "margin": 1.0
}
```

### D. 参考资源

相关技能和工具包括：热点Agent技能（hot-agent）用于热点事件采集，浏览器工具用于数据采集，Mermaid用于可视化。

如需更多帮助，请参考SKILL.md文件或联系技术支持。
