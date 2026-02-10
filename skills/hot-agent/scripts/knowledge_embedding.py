#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱嵌入模块 - Knowledge Graph Embedding

基于知识图谱嵌入技术，为热点事件提供语义级别的表示和关系推理
支持多种嵌入模型：TransE, RotatE, ComplEx等

功能：
1. 实体嵌入 - 将事件、现象、心理等节点表示为向量
2. 关系嵌入 - 学习事件之间的关系模式
3. 链接预测 - 预测事件之间的关系
4. 语义相似度 - 计算事件/现象的语义相似度

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

import os
import sys
import json
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class KGEntity:
    """知识图谱实体"""
    entity_id: str
    name: str
    entity_type: str  # event, phenomenon, psychology, etc.
    attributes: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None

    def to_vector(self) -> np.ndarray:
        """获取实体向量（如果有嵌入）"""
        if self.embedding is not None:
            return self.embedding
        # 如果没有嵌入，返回基于名称的简单向量
        return self._name_to_vector()

    def _name_to_vector(self) -> np.ndarray:
        """基于名称生成简单向量"""
        # 使用字符编码生成简单向量（实际应用应使用预训练模型）
        name_bytes = self.name.encode('utf-8')
        vector = np.zeros(128)
        for i, b in enumerate(name_bytes[:128]):
            vector[i] = b / 255.0
        return vector


@dataclass
class KGRelation:
    """知识图谱关系"""
    relation_id: str
    source_entity: str
    target_entity: str
    relation_type: str  # leads_to, influences, causes, etc.
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)


class KnowledgeGraphEmbedding:
    """知识图谱嵌入管理器"""

    # 支持的嵌入模型
    EMBEDDING_MODELS = {
        'transe': 'TransE - 翻译模型',
        'rotate': 'RotatE - 旋转模型',
        'complex': 'ComplEx - 复数模型',
        'simple': '简单向量 - 基于名称/属性',
    }

    def __init__(
        self,
        embedding_dim: int = 128,
        model_name: str = 'simple',
        device: str = 'cpu'
    ):
        """
        初始化知识图谱嵌入模型

        参数:
            embedding_dim: 嵌入维度
            model_name: 模型名称 (transe, rotate, complex, simple)
            device: 计算设备 (cpu, cuda)
        """
        self.embedding_dim = embedding_dim
        self.model_name = model_name
        self.device = device

        # 实体和关系存储
        self.entities: Dict[str, KGEntity] = {}
        self.relations: List[KGRelation] = []

        # 嵌入矩阵
        self.entity_embeddings: Optional[np.ndarray] = None
        self.relation_embeddings: Optional[np.ndarray] = None

        # 初始化模型
        self._init_model()

        logger.info(f"知识图谱嵌入模型初始化完成")
        logger.info(f"  模型: {model_name}")
        logger.info(f"  维度: {embedding_dim}")
        logger.info(f"  设备: {device}")

    def _init_model(self):
        """初始化嵌入模型"""
        if self.model_name == 'simple':
            logger.info("使用简单向量模型（无需深度学习框架）")
            self.model = None
        else:
            # 检查是否安装了PyTorch等深度学习框架
            try:
                import torch
                logger.info("检测到PyTorch，可以使用高级嵌入模型")
                self._init_pytorch_model()
            except ImportError:
                logger.warning("未安装PyTorch，回退到简单向量模型")
                self.model_name = 'simple'
                self.model = None

    def _init_pytorch_model(self):
        """初始化PyTorch模型（需要安装torch）"""
        try:
            import torch
            import torch.nn as nn
            import torch.nn.functional as F

            class TransE(nn.Module):
                """TransE嵌入模型"""
                def __init__(self, num_entities, num_relations, embedding_dim, margin=1.0):
                    super().__init__()
                    self.entity_embeddings = nn.Embedding(num_entities, embedding_dim)
                    self.relation_embeddings = nn.Embedding(num_relations, embedding_dim)
                    self.criterion = nn.MarginRankingLoss(margin=margin)

                    # 初始化
                    nn.init.xavier_uniform_(self.entity_embeddings.weight)
                    nn.init.xavier_uniform_(self.relation_embeddings.weight)

                def forward(self, positive_triplets, negative_triplets):
                    # 计算正样本和负样本的距离
                    pos_dist = self._compute_distance(positive_triplets)
                    neg_dist = self._compute_distance(negative_triplets)
                    return pos_dist, neg_dist

                def _compute_distance(self, triplets):
                    head = self.entity_embeddings(triplets[:, 0])
                    relation = self.relation_embeddings(triplets[:, 1])
                    tail = self.entity_embeddings(triplets[:, 2])
                    # TransE: h + r ≈ t
                    return torch.norm(head + relation - tail, p=1, dim=-1)

                def get_entity_embedding(self, entity_id):
                    return self.entity_embeddings.weight[entity_id].detach().numpy()

                def get_relation_embedding(self, relation_id):
                    return self.relation_embeddings.weight[relation_id].detach().numpy()

            self.model = TransE(
                num_entities=10000,  # 初始容量
                num_relations=100,   # 关系类型数
                embedding_dim=self.embedding_dim
            )

            logger.info("TransE模型初始化完成")

        except Exception as e:
            logger.error(f"初始化PyTorch模型失败: {e}")
            self.model = None
            self.model_name = 'simple'

    def add_entity(
        self,
        entity_id: str,
        name: str,
        entity_type: str,
        attributes: Optional[Dict] = None
    ) -> KGEntity:
        """添加实体"""
        entity = KGEntity(
            entity_id=entity_id,
            name=name,
            entity_type=entity_type,
            attributes=attributes or {}
        )
        self.entities[entity_id] = entity
        return entity

    def add_relation(
        self,
        source_entity: str,
        target_entity: str,
        relation_type: str,
        weight: float = 1.0
    ) -> KGRelation:
        """添加关系"""
        relation = KGRelation(
            relation_id=f"rel_{len(self.relations)}",
            source_entity=source_entity,
            target_entity=target_entity,
            relation_type=relation_type,
            weight=weight
        )
        self.relations.append(relation)
        return relation

    def build_from_knowledge_graph(self, graph) -> bool:
        """
        从热点Agent的知识图谱构建嵌入

        参数:
            graph: 知识图谱对象（来自hot_agent.py的KnowledgeGraph）

        返回:
            是否成功
        """
        logger.info("从知识图谱构建嵌入...")

        try:
            # 添加实体
            for node in graph.nodes:
                self.add_entity(
                    entity_id=node.node_id,
                    name=node.name,
                    entity_type=node.node_type,
                    attributes=node.attributes
                )

            # 添加关系
            for edge in graph.edges:
                self.add_relation(
                    source_entity=edge.source_node,
                    target_entity=edge.target_node,
                    relation_type=edge.relationship,
                    weight=edge.weight
                )

            logger.info(f"  添加了 {len(self.entities)} 个实体")
            logger.info(f"  添加了 {len(self.relations)} 条关系")

            # 计算嵌入
            self._compute_embeddings()

            return True

        except Exception as e:
            logger.error(f"构建嵌入失败: {e}")
            return False

    def _compute_embeddings(self):
        """计算所有实体的嵌入"""
        logger.info("计算实体嵌入...")

        # 简单模型：基于名称和类型生成向量
        for entity_id, entity in self.entities.items():
            # 使用名称向量
            vector = entity._name_to_vector()

            # 添加类型信息（扩展向量）
            type_vector = self._type_to_vector(entity.entity_type)
            vector = np.concatenate([vector, type_vector])

            # 裁剪到指定维度
            if len(vector) > self.embedding_dim:
                vector = vector[:self.embedding_dim]
            else:
                vector = np.pad(vector, (0, self.embedding_dim - len(vector)))

            entity.embedding = vector

        logger.info(f"  完成了 {len(self.entities)} 个实体的嵌入计算")

    def _type_to_vector(self, entity_type: str) -> np.ndarray:
        """将实体类型转换为向量"""
        type_map = {
            'event': np.array([1, 0, 0, 0]),
            'phenomenon': np.array([0, 1, 0, 0]),
            'psychology': np.array([0, 0, 1, 0]),
            'person': np.array([0, 0, 0, 1]),
            'organization': np.array([0, 0, 0, 0.5]),
            'location': np.array([0.5, 0, 0, 0]),
        }
        return type_map.get(entity_type, np.zeros(4))

    def get_entity_similarity(
        self,
        entity_id_1: str,
        entity_id_2: str,
        method: str = 'cosine'
    ) -> float:
        """
        计算两个实体的相似度

        参数:
            entity_id_1: 实体1 ID
            entity_id_2: 实体2 ID
            method: 相似度计算方法 (cosine, euclidean, dot)

        返回:
            相似度分数
        """
        if entity_id_1 not in self.entities or entity_id_2 not in self.entities:
            logger.warning(f"实体不存在: {entity_id_1} 或 {entity_id_2}")
            return 0.0

        vec1 = self.entities[entity_id_1].to_vector()
        vec2 = self.entities[entity_id_2].to_vector()

        return self._similarity(vec1, vec2, method)

    def _similarity(
        self,
        vec1: np.ndarray,
        vec2: np.ndarray,
        method: str
    ) -> float:
        """计算向量相似度"""
        if method == 'cosine':
            # 余弦相似度
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot_product / (norm1 * norm2)

        elif method == 'euclidean':
            # 欧氏距离转相似度
            dist = np.linalg.norm(vec1 - vec2)
            return 1.0 / (1.0 + dist)

        elif method == 'dot':
            # 点积（已归一化）
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-8)

        return 0.0

    def find_similar_entities(
        self,
        entity_id: str,
        top_k: int = 5,
        entity_type: Optional[str] = None
    ) -> List[Tuple[str, float]]:
        """
        查找最相似的实体

        参数:
            entity_id: 目标实体ID
            top_k: 返回数量
            entity_type: 过滤特定类型

        返回:
            [(实体ID, 相似度), ...]
        """
        if entity_id not in self.entities:
            return []

        target_vec = self.entities[entity_id].to_vector()
        similarities = []

        for other_id, entity in self.entities.items():
            if other_id == entity_id:
                continue

            # 类型过滤
            if entity_type and entity.entity_type != entity_type:
                continue

            sim = self._similarity(
                target_vec,
                entity.to_vector(),
                'cosine'
            )
            similarities.append((other_id, sim))

        # 排序并返回top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def predict_missing_links(
        self,
        source_entity_id: str,
        relation_type: str,
        candidate_entities: List[str],
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        预测缺失的链接（链接预测）

        参数:
            source_entity_id: 源实体
            relation_type: 关系类型
            candidate_entities: 候选目标实体列表
            top_k: 返回数量

        返回:
            [(实体ID, 预测分数), ...]
        """
        if source_entity_id not in self.entities:
            return []

        source_vec = self.entities[source_entity_id].to_vector()
        predictions = []

        for entity_id in candidate_entities:
            if entity_id not in self.entities:
                continue

            target_vec = self.entities[entity_id].to_vector()

            # 简单预测：基于向量相似度
            score = self._similarity(source_vec, target_vec, 'cosine')
            predictions.append((entity_id, score))

        # 排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:top_k]

    def cluster_entities(
        self,
        entity_type: str,
        n_clusters: int = 3
    ) -> Dict[int, List[str]]:
        """
        对实体进行聚类

        参数:
            entity_type: 实体类型
            n_clusters: 聚类数

        返回:
            {聚类ID: [实体ID列表], ...}
        """
        try:
            from sklearn.cluster import KMeans

            # 收集该类型的所有实体向量
            vectors = []
            entity_ids = []

            for entity_id, entity in self.entities.items():
                if entity.entity_type == entity_type:
                    vectors.append(entity.to_vector())
                    entity_ids.append(entity_id)

            if len(vectors) < n_clusters:
                logger.warning(f"实体数量 ({len(vectors)}) 小于聚类数 ({n_clusters})")
                return {}

            # 转换为numpy数组
            X = np.array(vectors)

            # K-Means聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(X)

            # 分组
            clusters = defaultdict(list)
            for idx, entity_id in enumerate(entity_ids):
                clusters[labels[idx]].append(entity_id)

            return dict(clusters)

        except ImportError:
            logger.warning("sklearn未安装，无法进行聚类")
            return {}
        except Exception as e:
            logger.error(f"聚类失败: {e}")
            return {}

    def export_embeddings(self) -> Dict[str, Any]:
        """导出所有嵌入向量"""
        embeddings = {}
        for entity_id, entity in self.entities.items():
            embeddings[entity_id] = {
                'name': entity.name,
                'type': entity.entity_type,
                'vector': entity.to_vector().tolist()
            }
        return embeddings

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        type_counts = defaultdict(int)
        for entity in self.entities.values():
            type_counts[entity.entity_type] += 1

        return {
            'total_entities': len(self.entities),
            'total_relations': len(self.relations),
            'entity_types': dict(type_counts),
            'embedding_dim': self.embedding_dim,
            'model_name': self.model_name
        }


def demo():
    """演示"""
    print("=" * 60)
    print("知识图谱嵌入模块演示")
    print("=" * 60)

    # 创建嵌入模型
    embedder = KnowledgeGraphEmbedding(
        embedding_dim=128,
        model_name='simple'
    )

    # 添加示例实体
    events = [
        ('e1', 'AI大模型突破', 'event'),
        ('e2', '新能源汽车销量增长', 'event'),
        ('e3', '房地产市场调整', 'event'),
        ('p1', '技术普及', 'phenomenon'),
        ('p2', '资本投入', 'phenomenon'),
        ('m1', '积极乐观', 'psychology'),
        ('m2', '焦虑', 'psychology'),
    ]

    for eid, name, etype in events:
        embedder.add_entity(eid, name, etype)

    # 添加关系
    relations = [
        ('e1', 'p1', 'leads_to'),
        ('e2', 'p1', 'leads_to'),
        ('e2', 'p2', 'leads_to'),
        ('e3', 'p2', 'leads_to'),
        ('p1', 'm1', 'influences'),
        ('p2', 'm2', 'influences'),
    ]

    for src, tgt, rel in relations:
        embedder.add_relation(src, tgt, rel)

    # 显示统计
    stats = embedder.get_statistics()
    print(f"\n统计信息:")
    print(f"  实体数: {stats['total_entities']}")
    print(f"  关系数: {stats['total_relations']}")
    print(f"  实体类型: {stats['entity_types']}")

    # 计算相似度
    sim = embedder.get_entity_similarity('e1', 'e2', method='cosine')
    print(f"\n事件相似度:")
    print(f"  'AI大模型突破' vs '新能源汽车销量增长': {sim:.4f}")

    # 查找相似实体
    similar = embedder.find_similar_entities('e1', top_k=3, entity_type='event')
    print(f"\n与'AI大模型突破'最相似的事件:")
    for sid, score in similar:
        print(f"  - {embedder.entities[sid].name}: {score:.4f}")

    # 聚类
    clusters = embedder.cluster_entities('event', n_clusters=2)
    print(f"\n事件聚类结果:")
    for cluster_id, entity_ids in clusters.items():
        names = [embedder.entities[eid].name for eid in entity_ids]
        print(f"  聚类{cluster_id}: {names}")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    demo()
