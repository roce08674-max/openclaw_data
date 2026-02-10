# 知识图谱资源索引

**创建时间**: 2026-02-09
**最后更新**: 2026-02-09 22:33 GMT+8

---

## 文档索引

| 文档 | 说明 | 创建时间 |
|------|------|---------|
| `knowledge-graph-github-resources.md` | GitHub搜索结果汇总 | 2026-02-09 22:27 |
| `openke-integration.md` | OpenKE集成指南 | 2026-02-09 22:33 |
| `this file` | 资源索引 | 2026-02-09 22:33 |

---

## 代码索引

| 文件 | 说明 | 大小 |
|------|------|------|
| `scripts/knowledge_embedding.py` | 知识图谱嵌入模块 | 18KB |
| `scripts/knowledge_embedding_example.py` | 集成示例 | - |

---

## 使用流程

### 1. 快速开始

```python
from knowledge_embedding import KnowledgeEmbeddingManager

# 创建管理器
manager = KnowledgeEmbeddingManager(embedding_dim=128)

# 注册实体
manager.register_entity("event_1", "event")
manager.register_entity("event_2", "event")

# 注册关系
manager.register_relation("leads_to")

# 训练
manager.train([("event_1", "leads_to", "event_2")], epochs=100)

# 计算相似度
similarity = manager.compute_similarity("event_1", "event_2")
```

### 2. 与热点Agent集成

参考: `openke-integration.md`

### 3. 可视化

参考: `openke-integration.md` - 可视化部分

---

## 依赖要求

### 必需
```txt
torch>=2.0
numpy>=1.24.0
```

### 可选
```txt
torch-geometric  # 图神经网络
scikit-learn    # t-SNE降维
matplotlib     # 可视化
```

---

## 下一步

1. 测试嵌入模块
2. 调整参数优化性能
3. 集成到热点Agent中
4. 添加可视化功能

---

**维护建议**:
- 每月检查OpenKE更新
- 定期测试嵌入效果
- 根据实际数据调整参数
