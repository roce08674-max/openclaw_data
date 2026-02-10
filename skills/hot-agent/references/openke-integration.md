# OpenKE知识图谱嵌入集成

**项目名称**: OpenKE (Open-Source Knowledge Embedding)
**GitHub**: https://github.com/thunlp/OpenKE
**创建时间**: 2026-02-09 22:33 GMT+8
**维护者**: OpenClaw Agent

---

## 📖 项目概述

OpenKE是清华大学NLP实验室开源的知识嵌入工具包，基于PyTorch实现。

### 核心论文

```
@InProceedings{han2018openke,
  title={OpenKE: An Open Toolkit for Knowledge Embedding},
  author={Han, Xu and Cao, Shulin and Lv, Xin and Lin, Yankai and Liu, Zhiyuan and Sun, Maosong and Li, Juanzi},
  booktitle={Proceedings of EMNLP},
  year={2018}
}
```

### 主要贡献者

Xu Han, Yankai Lin, Ruobing Xie, Zhiyuan Liu, Xin Lv, Shulin Cao, Weize Chen, Jingqin Yang

---

## 🏗️ 技术架构

### 模型支持

#### 基于PyTorch的实现

| 模型 | 年份 | 特点 | 复杂度 |
|------|------|------|--------|
| **TransE** | 2013 | 翻译模型，基础版 | ⭐ |
| **TransH** | 2014 | 关系特定超平面 | ⭐⭐ |
| **TransR** | 2015 | 关系特定空间 | ⭐⭐⭐ |
| **TransD** | 2015 | 动态映射 | ⭐⭐⭐ |
| **DistMult** | 2014 | 双线性模型 | ⭐⭐ |
| **ComplEx** | 2016 | 复数嵌入 | ⭐⭐⭐ |
| **RotatE** | 2019 | 旋转空间建模 | ⭐⭐⭐⭐ |
| **ConvE** | 2017 | 卷积神经网络 | ⭐⭐⭐⭐ |

### 性能对比

在FB15K-237和WN18RR数据集上的Hits@10性能：

| 模型 | WN18RR | FB15K237 |
|------|--------|----------|
| TransE | 0.512 | 0.476 |
| TransR | 0.519 | 0.511 |
| DistMult | 0.479 | 0.419 |
| RotatE | 0.565 | 0.522 |
| RotatE+adv | 0.571 | 0.533 |

---

## 📦 安装与配置

### 方式1：完整安装OpenKE

```bash
# 克隆OpenKE-PyTorch分支
git clone -b OpenKE-PyTorch https://github.com/thunlp/OpenKE --depth 1
cd OpenKE
cd openke

# 编译C++文件
bash make.sh
```

### 方式2：轻量级集成（推荐）

本项目提供了一个简化的TransE实现，可以直接使用：

```python
from knowledge_embedding import TransEModel, KnowledgeEmbeddingManager
```

### 数据格式

#### 训练数据 (train2id.txt)

```
# 第一行：三元组数量
1000
# 后续行：(头实体ID, 尾实体ID, 关系ID)
0 1 0
2 3 1
4 5 2
...
```

#### 实体列表 (entity2id.txt)

```
# 第一行：实体数量
10000
# 后续行：(实体名称, ID)
实体1 0
实体2 1
...
```

#### 关系列表 (relation2id.txt)

```
# 第一行：关系数量
10
# 后续行：(关系名称, ID)
关系1 0
关系2 1
...
```

---

## 🎯 集成到热点Agent

### 当前热点Agent的知识图谱结构

```
事件层 (Events)
  ↓ leads_to
现象层 (Phenomena)
  ↓ influences
心理层 (Psychology)
```

### 增强后的结构

```
原始事件 (Event)
  ↓ [实体嵌入]
事件向量 (Event Vector) ⭐ 新增
  ↓ [关系预测]
事件关联 (Event Relations) ⭐ 新增
  ↓ [相似度计算]
事件聚类 (Event Clusters) ⭐ 新增
```

### 使用示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱嵌入集成示例

将知识图谱嵌入集成到热点Agent中

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

import sys
import json
from pathlib import Path
from knowledge_embedding import KnowledgeEmbeddingManager

def integrate_with_hot_agent():
    """
    与热点Agent集成
    
    在热点Agent生成知识图谱后，
    使用嵌入模型增强分析能力
    """
    
    # 1. 从知识图谱提取三元组
    triples = [
        ("event_ai_news", "leads_to", "phenomenon_tech_popularization"),
        ("event_ev_policy", "leads_to", "phenomenon_market_growth"),
        ("event_stock_market", "influences", "phenomenon_public_anxiety"),
        # ... 更多三元组
    ]
    
    # 2. 初始化嵌入管理器
    embedding_manager = KnowledgeEmbeddingManager(
        embedding_dim=128,
        margin=1.0
    )
    
    # 3. 注册所有实体
    print("注册实体...")
    for head, relation, tail in triples:
        embedding_manager.register_entity(head, "event")
        embedding_manager.register_entity(tail, "phenomenon")
        embedding_manager.register_relation(relation)
    
    # 4. 训练嵌入模型
    print("训练嵌入模型...")
    embedding_manager.train(triples, epochs=100, batch_size=16)
    
    # 5. 计算事件相似度
    print("\n计算事件相似度...")
    events = [
        "event_ai_news",
        "event_ev_policy",
        "event_stock_market"
    ]
    
    similarity_matrix = {}
    for event1 in events:
        for event2 in events:
            if event1 != event2:
                sim = embedding_manager.compute_similarity(event1, event2)
                similarity_matrix[(event1, event2)] = sim
                print(f"  {event1} <-> {event2}: {sim:.4f}")
    
    # 6. 查找相似事件
    print("\n查找与'AI新闻'最相似的事件...")
    similar = embedding_manager.find_similar_events(
        "event_ai_news",
        top_k=3,
        exclude=["event_ai_news"]
    )
    
    for event_id, sim in similar:
        print(f"  {event_id}: {sim:.4f}")
    
    # 7. 预测事件关系
    print("\n预测'AI新闻'和'EV政策'的关系...")
    predicted_relations = embedding_manager.predict_relation(
        "event_ai_news",
        "event_ev_policy",
        candidates=["leads_to", "influences", "related_to"]
    )
    
    for rel, score in sorted(predicted_relations.items(), key=lambda x: -x[1]):
        print(f"  {rel}: {score:.4f}")
    
    # 8. 保存嵌入结果
    print("\n保存嵌入结果...")
    embedding_manager.save_embeddings()
    
    return embedding_manager, similarity_matrix


def analyze_event_clusters(embedding_manager, events):
    """
    事件聚类分析
    
    基于嵌入向量的相似度对事件进行聚类
    """
    from collections import defaultdict
    
    # 计算相似度矩阵
    similarities = defaultdict(dict)
    for event1 in events:
        for event2 in events:
            if event1 != event2:
                sim = embedding_manager.compute_similarity(event1, event2)
                similarities[event1][event2] = sim
    
    # 简单聚类（基于阈值）
    clusters = []
    visited = set()
    
    for event in events:
        if event in visited:
            continue
        
        cluster = [event]
        visited.add(event)
        
        for other_event, sim in similarities[event].items():
            if sim > 0.7:  # 相似度阈值
                if other_event not in visited:
                    cluster.append(other_event)
                    visited.add(other_event)
        
        clusters.append(cluster)
    
    return clusters


def main():
    """主函数"""
    print("=" * 60)
    print("知识图谱嵌入集成测试")
    print("=" * 60)
    
    # 运行集成测试
    embedding_manager, similarities = integrate_with_hot_agent()
    
    # 示例事件列表
    sample_events = [
        "event_ai_news",
        "event_ev_policy",
        "event_stock_market",
        "event_tech_new_product",
        "event_social_discussion"
    ]
    
    # 事件聚类分析
    print("\n事件聚类分析...")
    clusters = analyze_event_clusters(embedding_manager, sample_events)
    
    for i, cluster in enumerate(clusters, 1):
        print(f"\n聚类 {i}:")
        for event in cluster:
            print(f"  - {event}")
    
    print("\n" + "=" * 60)
    print("集成测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

## 📊 性能优化

### 1. 训练优化

```python
# 使用GPU加速
device = "cuda" if torch.cuda.is_available() else "cpu"

# 批量大小
batch_size = 64

# 学习率调度
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', patience=10, factor=0.5
)
```

### 2. 内存优化

```python
# 使用混合精度训练
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

with autocast():
    loss = model.forward(...)
    
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 3. 数据优化

```python
# 使用DataLoader
from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(heads, relations, tails)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

---

## 🎨 可视化

### 使用t-SNE降维可视化

```python
import matplotlib.pyplot as plt
from sklearn.manifold import tsne

def visualize_embeddings(embedding_manager, event_types=None):
    """可视化嵌入向量"""
    # 收集所有嵌入
    embeddings = []
    labels = []
    
    for entity_id, emb_obj in embedding_manager.embedding_cache.items():
        if event_types is None or emb_obj.entity_type in event_types:
            embeddings.append(emb_obj.embedding)
            labels.append(emb_obj.entity_type)
    
    # 降维
    embeddings = np.array(embeddings)
    tsne_result = tsne.fit_transform(embeddings)
    
    # 绘制
    plt.figure(figsize=(10, 8))
    
    for entity_type in set(labels):
        mask = [l == entity_type for l in labels]
        plt.scatter(
            tsne_result[mask, 0],
            tsne_result[mask, 1],
            label=entity_type,
            alpha=0.7
        )
    
    plt.legend()
    plt.title('知识图谱嵌入可视化 (t-SNE)')
    plt.xlabel('t-SNE维度1')
    plt.ylabel('t-SNE维度2')
    plt.savefig('embedding_visualization.png', dpi=150)
    plt.show()
```

---

## 📈 效果评估

### 评估指标

| 指标 | 说明 | 计算方式 |
|------|------|---------|
| **MR (Mean Rank)** | 平均排名 | 正确实体排名的平均值 |
| **MRR (Mean Reciprocal Rank)** | 平均倒数排名 | 1/排名的平均值 |
| **Hits@10** | 前10命中率 | 排名≤10的比例 |
| **Hits@3** | 前3命中率 | 排名≤3的比例 |
| **Hits@1** | 第1命中率 | 排名第1的比例 |

### 评估代码

```python
def evaluate_model(model, test_triples, all_entities):
    """
    评估模型性能
    
    参数:
        model: 训练好的模型
        test_triples: 测试三元组 [(h, r, t), ...]
        all_entities: 所有实体ID列表
    """
    from collections import defaultdict
    
    # 统计
    ranks = []
    reciprocal_ranks = []
    hits_at_10 = 0
    hits_at_3 = 0
    hits_at_1 = 0
    
    for head, relation, tail in test_triples:
        # 预测尾实体
        scores = []
        for entity in all_entities:
            if entity != head:
                score = model.predict(head, relation, entity)
                scores.append((entity, score))
        
        scores.sort(key=lambda x: x[1])
        
        # 找真实尾实体的排名
        for rank, (entity, _) in enumerate(scores, 1):
            if entity == tail:
                ranks.append(rank)
                reciprocal_ranks.append(1.0 / rank)
                
                if rank <= 10:
                    hits_at_10 += 1
                if rank <= 3:
                    hits_at_3 += 1
                if rank == 1:
                    hits_at_1 += 1
                break
    
    # 计算指标
    mr = sum(ranks) / len(ranks)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    hits_10 = hits_at_10 / len(test_triples)
    hits_3 = hits_at_3 / len(test_triples)
    hits_1 = hits_at_1 / len(test_triples)
    
    return {
        "MR": mr,
        "MRR": mrr,
        "Hits@10": hits_10,
        "Hits@3": hits_3,
        "Hits@1": hits_1
    }
```

---

## 🔧 故障排除

### 问题1: CUDA内存不足

**解决方案**:
- 减小batch_size
- 使用梯度累积
- 使用混合精度训练

### 问题2: 收敛慢

**解决方案**:
- 调整学习率
- 添加学习率调度
- 检查数据格式

### 问题3: 嵌入质量差

**解决方案**:
- 增加嵌入维度
- 增加训练轮数
- 使用更复杂的模型（如RotatE）

---

## 📚 参考资源

### 论文
- [TransE: Translating Embeddings for Modeling Multi-relational Data (2013)](https://proceedings.mlr.press/v28/bordes13.html)
- [TransR: Learning Entity and Relation Embeddings (2015)](https://ojs.aaai.org/index.php/AAAI/article/view/9491)
- [RotatE: Relation Modeling with Rotation (2019)](https://arxiv.org/abs/1906.01195)

### 代码
- [OpenKE官方GitHub](https://github.com/thunlp/OpenKE)
- [PyKEEN: Python Knowledge Embedding Networks](https://github.com/pykeen/pykeen)
- [AmpliGraph: Knowledge Graph Embeddings](https://github.com/Accenture/AmpliGraph)

### 数据集
- FB15K-237: 知识图谱链接预测标准数据集
- WN18RR: WordNet知识图谱数据集
- Wikidata: 开放知识图谱

---

**文档更新时间**: 2026-02-09 22:33 GMT+8
**状态**: ✅ 已创建OpenKE集成模块
**下一步**: 测试和优化嵌入效果
