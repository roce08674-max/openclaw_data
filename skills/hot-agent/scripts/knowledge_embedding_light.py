#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱嵌入模块 - 轻量版 (无需numpy)

基于知识图谱嵌入技术，为热点事件提供语义级别的表示和关系推理

功能：
1. 实体表示 - 将事件、现象、心理等节点表示为向量
2. 关系建模 - 学习事件之间的关系模式  
3. 语义相似度 - 计算事件/现象的语义相似度
4. 链接预测 - 预测事件之间可能的关系
5. 实体聚类 - 自动发现相似事件群组

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

import os
import json
import math
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
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
    vector: List[float] = field(default_factory=list)

    def to_vector(self) -> List[float]:
        """获取实体向量"""
        if self.vector:
            return self.vector
        return self._name_to_vector()

    def _name_to_vector(self) -> List[float]:
        """基于名称生成简单向量"""
        name_bytes = self.name.encode('utf-8')
        vector = [0.0] * 64
        for i, b in enumerate(name_bytes[:64]):
            vector[i] = b / 255.0
        return vector


class SimpleVector:
    """简单向量运算（替代numpy）"""

    @staticmethod
    def dot(v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def norm(v: List[float]) -> float:
        return math.sqrt(sum(x * x for x in v))

    @staticmethod
    def cosine(v1: List[float], v2: List[float]) -> float:
        """余弦相似度"""
        dot = SimpleVector.dot(v1, v2)
        norm1 = SimpleVector.norm(v1)
        norm2 = SimpleVector.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    @staticmethod
    def euclidean(v1: List[float], v2: List[float]) -> float:
        """欧氏距离"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    @staticmethod
    def add(v1: List[float], v2: List[float]) -> List[float]:
        return [a + b for a, b in zip(v1, v2)]

    @staticmethod
    def sub(v1: List[float], v2: List[float]) -> List[float]:
        return [a - b for a, b in zip(v1, v2)]


class KnowledgeGraphEmbedding:
    """知识图谱嵌入管理器（轻量版）"""

    def __init__(self, embedding_dim: int = 64):
        """
        初始化知识图谱嵌入模型

        参数:
            embedding_dim: 嵌入维度
        """
        self.embedding_dim = embedding_dim
        self.entities: Dict[str, KGEntity] = {}
        self.relations: List[Dict] = []
        self.relation_types: set = set()

        logger.info(f"知识图谱嵌入模型初始化完成 (维度: {embedding_dim})")

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
        # 生成向量
        entity.vector = self._generate_vector(name, entity_type)
        self.entities[entity_id] = entity
        return entity

    def _generate_vector(self, name: str, entity_type: str) -> List[float]:
        """生成实体向量"""
        # 名称向量
        name_bytes = name.encode('utf-8')
        name_vec = [0.0] * 48
        for i, b in enumerate(name_bytes[:48]):
            name_vec[i] = b / 255.0

        # 类型向量（4维）
        type_vec = self._type_to_vector(entity_type)

        # 合并
        return name_vec + type_vec

    def _type_to_vector(self, entity_type: str) -> List[float]:
        """实体类型转向量"""
        type_map = {
            'event': [1.0, 0.0, 0.0, 0.0],
            'phenomenon': [0.0, 1.0, 0.0, 0.0],
            'psychology': [0.0, 0.0, 1.0, 0.0],
            'person': [0.0, 0.0, 0.0, 1.0],
            'organization': [0.5, 0.5, 0.0, 0.0],
            'location': [0.0, 0.0, 0.5, 0.5],
        }
        return type_map.get(entity_type, [0.0] * 4)

    def add_relation(
        self,
        source_entity: str,
        target_entity: str,
        relation_type: str,
        weight: float = 1.0
    ) -> Dict:
        """添加关系"""
        relation = {
            'id': f"rel_{len(self.relations)}",
            'source': source_entity,
            'target': target_entity,
            'type': relation_type,
            'weight': weight
        }
        self.relations.append(relation)
        self.relation_types.add(relation_type)
        return relation

    def build_from_events(
        self,
        events: List[Dict],
        phenomena: List[Dict],
        psychologies: List[Dict]
    ) -> bool:
        """从热点事件数据构建知识图谱嵌入"""
        logger.info("从热点事件构建知识图谱嵌入...")

        try:
            # 添加事件实体
            for i, event in enumerate(events):
                self.add_entity(
                    entity_id=f"event_{i}",
                    name=event.get('title', f'Event_{i}'),
                    entity_type='event',
                    attributes=event
                )

            # 添加现象实体
            for i, ph in enumerate(phenomena):
                self.add_entity(
                    entity_id=f"phenomenon_{i}",
                    name=ph.get('name', f'Phenomenon_{i}'),
                    entity_type='phenomenon',
                    attributes=ph
                )

            # 添加心理实体
            for i, psy in enumerate(psychologies):
                self.add_entity(
                    entity_id=f"psych_{i}",
                    name=psy.get('name', f'Psychology_{i}'),
                    entity_type='psychology',
                    attributes=psy
                )

            # 建立关系
            for i in range(len(events)):
                for j in range(len(phenomena)):
                    self.add_relation(
                        f"event_{i}",
                        f"phenomenon_{j}",
                        'leads_to'
                    )

            for j in range(len(phenomena)):
                for k in range(len(psychologies)):
                    self.add_relation(
                        f"phenomenon_{j}",
                        f"psych_{k}",
                        'influences'
                    )

            logger.info(f"  实体: {len(self.entities)}")
            logger.info(f"  关系: {len(self.relations)}")
            logger.info(f"  类型: {self.relation_types}")

            return True

        except Exception as e:
            logger.error(f"构建失败: {e}")
            return False

    def get_similarity(
        self,
        entity_id_1: str,
        entity_id_2: str,
        method: str = 'cosine'
    ) -> float:
        """计算两个实体的相似度"""
        if entity_id_1 not in self.entities or entity_id_2 not in self.entities:
            return 0.0

        vec1 = self.entities[entity_id_1].to_vector()
        vec2 = self.entities[entity_id_2].to_vector()

        if method == 'cosine':
            return SimpleVector.cosine(vec1, vec2)
        elif method == 'euclidean':
            dist = SimpleVector.euclidean(vec1, vec2)
            return 1.0 / (1.0 + dist)
        else:
            return SimpleVector.cosine(vec1, vec2)

    def find_similar_entities(
        self,
        entity_id: str,
        top_k: int = 5,
        entity_type: Optional[str] = None
    ) -> List[Tuple[str, str, float]]:
        """查找最相似的实体"""
        if entity_id not in self.entities:
            return []

        target_vec = self.entities[entity_id].to_vector()
        similarities = []

        for other_id, entity in self.entities.items():
            if other_id == entity_id:
                continue

            if entity_type and entity.entity_type != entity_type:
                continue

            sim = SimpleVector.cosine(target_vec, entity.to_vector())
            similarities.append((other_id, entity.name, sim))

        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:top_k]

    def predict_links(
        self,
        source_entity_id: str,
        candidate_ids: List[str],
        top_k: int = 3
    ) -> List[Tuple[str, str, float]]:
        """预测可能的关系目标"""
        if source_entity_id not in self.entities:
            return []

        source_vec = self.entities[source_entity_id].to_vector()
        predictions = []

        for entity_id in candidate_ids:
            if entity_id not in self.entities:
                continue

            sim = SimpleVector.cosine(source_vec, self.entities[entity_id].to_vector())
            predictions.append((entity_id, self.entities[entity_id].name, sim))

        predictions.sort(key=lambda x: x[2], reverse=True)
        return predictions[:top_k]

    def find_clusters(
        self,
        entity_type: str,
        n_clusters: int = 3
    ) -> Dict[int, List[str]]:
        """对实体进行聚类（简化版K-Means）"""
        # 收集实体
        entity_list = [
            (eid, ent) for eid, ent in self.entities.items()
            if ent.entity_type == entity_type
        ]

        if len(entity_list) < n_clusters:
            return {}

        # 初始化聚类中心
        centers = {}
        for i in range(n_clusters):
            _, entity = entity_list[i % len(entity_list)]
            centers[i] = entity.to_vector().copy()

        # 迭代聚类（简化版）
        max_iter = 10
        for _ in range(max_iter):
            clusters = defaultdict(list)

            for eid, entity in entity_list:
                vec = entity.to_vector()
                best_cluster = 0
                best_sim = -1

                for cid, center in centers.items():
                    sim = SimpleVector.cosine(vec, center)
                    if sim > best_sim:
                        best_sim = sim
                        best_cluster = cid

                clusters[best_cluster].append(eid)

            # 更新聚类中心
            for cid in centers:
                if cid in clusters and clusters[cid]:
                    cluster_entities = [self.entities[eid] for eid in clusters[cid]]
                    # 计算所有向量的平均值
                    all_vectors = [ent.to_vector() for ent in cluster_entities]
                    avg_vector = []
                    for i in range(self.embedding_dim):
                        avg_value = sum(v[i] if i < len(v) else 0 for v in all_vectors) / len(all_vectors)
                        avg_vector.append(avg_value)
                    centers[cid] = avg_vector

        return dict(clusters)

    def export_data(self) -> Dict:
        """导出所有数据"""
        return {
            'entities': {
                eid: {
                    'name': ent.name,
                    'type': ent.entity_type,
                    'vector': ent.vector,
                    'attributes': ent.attributes
                }
                for eid, ent in self.entities.items()
            },
            'relations': self.relations,
            'statistics': self.get_statistics()
        }

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        type_counts = defaultdict(int)
        for ent in self.entities.values():
            type_counts[ent.entity_type] += 1

        return {
            'total_entities': len(self.entities),
            'total_relations': len(self.relations),
            'entity_types': dict(type_counts),
            'relation_types': list(self.relation_types),
            'embedding_dim': self.embedding_dim
        }


def demo():
    """演示"""
    print("=" * 70)
    print("知识图谱嵌入模块演示")
    print("=" * 70)

    # 创建嵌入模型
    embedder = KnowledgeGraphEmbedding(embedding_dim=64)

    # 添加示例实体
    events = [
        ('e1', 'AI大模型突破', 'event'),
        ('e2', '新能源汽车销量增长', 'event'),
        ('e3', '房地产市场调整', 'event'),
        ('e4', '互联网平台监管加强', 'event'),
        ('e5', '5G网络商用加速', 'event'),
        ('p1', '技术普及', 'phenomenon'),
        ('p2', '资本投入', 'phenomenon'),
        ('p3', '政策规范', 'phenomenon'),
        ('m1', '积极乐观', 'psychology'),
        ('m2', '焦虑担忧', 'psychology'),
        ('m3', '期待兴奋', 'psychology'),
    ]

    for eid, name, etype in events:
        embedder.add_entity(eid, name, etype)

    # 建立关系
    relations = [
        ('e1', 'p1', 'leads_to'),
        ('e2', 'p1', 'leads_to'),
        ('e2', 'p2', 'leads_to'),
        ('e3', 'p2', 'leads_to'),
        ('e4', 'p3', 'leads_to'),
        ('e5', 'p1', 'leads_to'),
        ('p1', 'm1', 'influences'),
        ('p1', 'm3', 'influences'),
        ('p2', 'm2', 'influences'),
        ('p3', 'm2', 'influences'),
    ]

    for src, tgt, rel in relations:
        embedder.add_relation(src, tgt, rel)

    # 显示统计
    stats = embedder.get_statistics()
    print(f"\n📊 统计信息:")
    print(f"   实体数: {stats['total_entities']}")
    print(f"   关系数: {stats['total_relations']}")
    print(f"   实体类型: {stats['entity_types']}")
    print(f"   关系类型: {stats['relation_types']}")

    # 计算相似度
    print(f"\n🔍 事件相似度:")
    pairs = [('e1', 'e2'), ('e1', 'e5'), ('e2', 'e3')]
    for e1, e2 in pairs:
        sim = embedder.get_similarity(e1, e2)
        print(f"   {embedder.entities[e1].name} vs {embedder.entities[e2].name}: {sim:.4f}")

    # 查找相似实体
    print(f"\n🎯 与'AI大模型突破'最相似的事件:")
    similar = embedder.find_similar_entities('e1', top_k=3, entity_type='event')
    for sid, name, score in similar:
        print(f"   - {name}: {score:.4f}")

    # 链接预测
    print(f"\n🔗 预测与'房地产市场调整'可能相关的事件:")
    candidates = [eid for eid in embedder.entities if eid.startswith('e') and eid != 'e3']
    predictions = embedder.predict_links('e3', candidates, top_k=3)
    for pid, name, score in predictions:
        print(f"   - {name}: {score:.4f}")

    # 聚类
    print(f"\n📂 事件聚类结果 (2类):")
    clusters = embedder.find_clusters('event', n_clusters=2)
    for cid, eids in clusters.items():
        names = [embedder.entities[eid].name for eid in eids]
        print(f"   聚类{cid}: {names}")

    # 现象关联
    print(f"\n🔗 现象之间的关系:")
    phenomenon_ids = [eid for eid in embedder.entities if eid.startswith('p')]
    for i, pid1 in enumerate(phenomenon_ids):
        for pid2 in phenomenon_ids[i+1:]:
            sim = embedder.get_similarity(pid1, pid2)
            print(f"   {embedder.entities[pid1].name} <-> {embedder.entities[pid2].name}: {sim:.4f}")

    print("\n" + "=" * 70)
    print("✅ 演示完成！")
    print("=" * 70)


if __name__ == "__main__":
    demo()
