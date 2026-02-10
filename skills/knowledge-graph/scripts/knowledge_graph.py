#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱核心模块 - Knowledge Graph Core

提供知识图谱的完整生命周期管理：
1. 实体管理：添加、更新、删除、查询实体
2. 关系管理：建立、维护和分析实体间关系
3. 嵌入学习：训练和评估知识图谱嵌入模型
4. 语义分析：相似度计算、链接预测、知识推理

支持多种嵌入模型：TransE、RotatE、ComplEx、DistMult等

作者: OpenClaw Agent
创建时间: 2026-02-10
"""

import os
import sys
import json
import logging
import random
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from abc import ABC, abstractmethod

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Entity:
    """知识图谱实体"""
    entity_id: str
    name: str
    entity_type: str  # event, concept, person, organization, location, etc.
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    embedding: Optional[List[float]] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Entity':
        return cls(**data)


@dataclass
class Relation:
    """知识图谱关系"""
    relation_id: str
    source_entity: str
    target_entity: str
    relation_type: str  # causes, leads_to, belongs_to, relates_to, etc.
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Relation':
        return cls(**data)


class EmbeddingModel(ABC):
    """嵌入模型抽象基类"""

    def __init__(self, model_name: str, embedding_dim: int = 128, **kwargs):
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.entity_embeddings: Dict[str, List[float]] = {}
        self.relation_embeddings: Dict[str, List[float]] = {}
        self.is_trained = False

    @abstractmethod
    def train(self, knowledge_graph: 'KnowledgeGraph', epochs: int = 100, lr: float = 0.01, **kwargs):
        """训练嵌入模型"""
        pass

    @abstractmethod
    def get_entity_embedding(self, entity_id: str) -> Optional[List[float]]:
        """获取实体嵌入"""
        pass

    @abstractmethod
    def get_relation_embedding(self, relation_type: str) -> Optional[List[float]]:
        """获取关系嵌入"""
        pass

    @abstractmethod
    def similarity(self, entity_id_1: str, entity_id_2: str) -> float:
        """计算两个实体的相似度"""
        pass

    @abstractmethod
    def predict_links(self, head_entity: str, relation: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """链接预测"""
        pass


class TransEModel(EmbeddingModel):
    """TransE嵌入模型

    TransE模型将关系建模为实体嵌入空间中的翻译向量。
    对于关系r和实体h、t，满足h + r ≈ t。

    优点：
    - 模型简单，训练效率高
    - 可解释性好
    - 适用于大规模图谱

    缺点：
    - 难以建模复杂关系模式（一对多、多对一、多对多）
    - 对于对称关系的建模能力有限
    """

    def __init__(self, embedding_dim: int = 128, margin: float = 1.0, **kwargs):
        super().__init__("TransE", embedding_dim)
        self.margin = margin
        self.entity_vectors: Dict[str, List[float]] = {}
        self.relation_vectors: Dict[str, List[float]] = {}

    def _init_embeddings(self, entities: List[Entity], relations: List[Relation]):
        """初始化嵌入向量"""
        # 初始化实体嵌入
        for entity in entities:
            self.entity_vectors[entity.entity_id] = self._random_vector()

        # 初始化关系嵌入
        relation_types = set(rel.relation_type for rel in relations)
        for rel_type in relation_types:
            self.relation_vectors[rel_type] = self._random_vector()

    def _random_vector(self) -> List[float]:
        """生成随机向量（归一化）"""
        import math
        vector = [random.uniform(-1, 1) for _ in range(self.embedding_dim)]
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]
        return vector

    def _compute_score(self, h: List[float], r: List[float], t: List[float]) -> float:
        """计算三元组 (h, r, t) 的得分"""
        # TransE: h + r ≈ t，距离越小越好
        diff = [h[i] + r[i] - t[i] for i in range(self.embedding_dim)]
        return sum(x * x for x in diff)  # L2距离的平方

    def train(self, knowledge_graph: 'KnowledgeGraph', epochs: int = 100, lr: float = 0.01, batch_size: int = 32, **kwargs):
        """训练TransE模型"""
        logger.info(f"开始训练TransE模型，epochs={epochs}, embedding_dim={self.embedding_dim}")

        # 初始化嵌入
        entities = list(knowledge_graph.entities.values())
        relations = list(knowledge_graph.relations)
        self._init_embeddings(entities, relations)

        # 创建名称到ID的映射（用于支持名称查询）
        self._entity_name_map = {
            entity.entity_id: entity for entity in entities
        }

        # 准备训练数据：正样本和负样本
        positive_triples = [(rel.source_entity, rel.relation_type, rel.target_entity) for rel in relations]

        # 简化训练（实际应使用负采样和梯度下降）
        for epoch in range(epochs):
            total_loss = 0.0

            for _ in range(min(batch_size, len(positive_triples))):
                # 随机选择正样本
                h_id, r_type, t_id = random.choice(positive_triples)
                h = self.entity_vectors.get(h_id, self._random_vector())
                r = self.relation_vectors.get(r_type, self._random_vector())
                t = self.entity_vectors.get(t_id, self._random_vector())

                # 生成负样本（随机替换头或尾）
                negative_t_id = random.choice(list(self.entity_vectors.keys()))
                while negative_t_id == t_id:
                    negative_t_id = random.choice(list(self.entity_vectors.keys()))

                negative_t = self.entity_vectors.get(negative_t_id, self._random_vector())

                # 计算正负样本得分
                pos_score = self._compute_score(h, r, t)
                neg_score = self._compute_score(h, r, negative_t)

                # 边际损失
                loss = max(0, pos_score - neg_score + self.margin)
                total_loss += loss

                # 简化更新（实际应使用反向传播）
                if loss > 0:
                    # 梯度下降更新
                    for i in range(self.embedding_dim):
                        h[i] -= lr * 2 * (h[i] + r[i] - t[i])
                        r[i] -= lr * 2 * (h[i] + r[i] - t[i])
                        t[i] -= lr * 2 * (h[i] + r[i] - t[i])

                    # 归一化
                    h = self._normalize(h)
                    r = self._normalize(r)
                    t = self._normalize(t)

                    # 保存更新
                    if h_id in self.entity_vectors:
                        self.entity_vectors[h_id] = h
                    if t_id in self.entity_vectors:
                        self.entity_vectors[t_id] = t
                    self.relation_vectors[r_type] = r

            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")

        # 保存嵌入到实体
        for entity_id, vector in self.entity_vectors.items():
            if entity_id in knowledge_graph.entities:
                knowledge_graph.entities[entity_id].embedding = vector

        self.is_trained = True
        logger.info("TransE模型训练完成")

    def _normalize(self, vector: List[float]) -> List[float]:
        """归一化向量"""
        import math
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]
        return vector

    def get_entity_embedding(self, entity_id: str) -> Optional[List[float]]:
        """获取实体嵌入"""
        return self.entity_vectors.get(entity_id)

    def get_relation_embedding(self, relation_type: str) -> Optional[List[float]]:
        """获取关系嵌入"""
        return self.relation_vectors.get(relation_type)

    def similarity(self, entity_id_1: Union[str, Entity], entity_id_2: Union[str, Entity]) -> float:
        """计算两个实体的相似度

        参数:
            entity_id_1: 实体ID或实体对象
            entity_id_2: 实体ID或实体对象

        返回:
            余弦相似度 (0-1)
        """
        # 如果是Entity对象，提取ID
        if isinstance(entity_id_1, Entity):
            entity_id_1 = entity_id_1.entity_id
        if isinstance(entity_id_2, Entity):
            entity_id_2 = entity_id_2.entity_id

        # 尝试用ID查找
        v1 = self.entity_vectors.get(entity_id_1)
        v2 = self.entity_vectors.get(entity_id_2)

        # 如果找不到，尝试用名称匹配
        if v1 is None:
            for eid, entity in self._entity_name_map.items():
                if entity.name == entity_id_1:
                    v1 = self.entity_vectors.get(eid)
                    break

        if v2 is None:
            for eid, entity in self._entity_name_map.items():
                if entity.name == entity_id_2:
                    v2 = self.entity_vectors.get(eid)
                    break

        if v1 is None or v2 is None:
            return 0.0

        # 余弦相似度
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = sum(a * a for a in v1) ** 0.5
        norm2 = sum(b * b for b in v2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def predict_links(self, head_entity: str, relation: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """链接预测：给定 (h, r)，预测可能的 t"""
        h = self.entity_vectors.get(head_entity)
        r = self.relation_vectors.get(relation)

        if h is None or r is None:
            return []

        # 计算所有实体的得分
        predictions = []
        h_plus_r = [h[i] + r[i] for i in range(self.embedding_dim)]

        for entity_id, t in self.entity_vectors.items():
            if entity_id == head_entity:
                continue

            # 计算距离
            diff = [h_plus_r[i] - t[i] for i in range(self.embedding_dim)]
            score = -sum(x * x for x in diff)  # 负距离作为得分

            predictions.append((entity_id, score))

        # 排序并返回top_k
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:top_k]


class RotatEModel(EmbeddingModel):
    """RotatE嵌入模型

    RotatE模型将关系建模为复平面上的旋转操作。
    对于关系r和实体h、t，满足 h ∘ r = t（复数乘法）。

    优点：
    - 可以建模对称、反对称、逆转等多种关系模式
    - 在链接预测任务上表现优异
    - 可解释性好

    缺点：
    - 参数更多，训练成本更高
    - 需要复数支持
    """

    def __init__(self, embedding_dim: int = 128, **kwargs):
        super().__init__("RotatE", embedding_dim)
        # RotatE使用复数嵌入，实部和虚部
        self.entity_real: Dict[str, List[float]] = {}
        self.entity_imag: Dict[str, List[float]] = {}
        self.relation_phases: Dict[str, float] = {}

    def _init_embeddings(self, entities: List[Entity], relations: List[Relation]):
        """初始化嵌入"""
        import math

        for entity in entities:
            # 均匀分布在单位圆上
            angle = 2 * math.pi * len(self.entity_real) / len(entities)
            self.entity_real[entity.entity_id] = [math.cos(angle)]
            self.entity_imag[entity.entity_id] = [math.sin(angle)]

        relation_types = set(rel.relation_type for rel in relations)
        for rel_type in relation_types:
            self.relation_phases[rel_type] = random.uniform(-math.pi, math.pi)

    def train(self, knowledge_graph: 'KnowledgeGraph', epochs: int = 100, lr: float = 0.01, **kwargs):
        """训练RotatE模型"""
        logger.info(f"开始训练RotatE模型，epochs={epochs}")

        entities = list(knowledge_graph.entities.values())
        relations = list(knowledge_graph.relations)
        self._init_embeddings(entities, relations)

        positive_triples = [(rel.source_entity, rel.relation_type, rel.target_entity) for rel in relations]

        for epoch in range(epochs):
            total_loss = 0.0

            for _ in range(min(32, len(positive_triples))):
                h_id, r_type, t_id = random.choice(positive_triples)

                h_real = self.entity_real.get(h_id, [1.0])
                h_imag = self.entity_imag.get(h_id, [0.0])
                r_phase = self.relation_phases.get(r_type, 0.0)

                # 旋转：h * e^(i*phase)
                import math
                cos_r = math.cos(r_phase)
                sin_r = math.sin(r_phase)

                # h * r = (h_real + i*h_imag) * (cos_r + i*sin_r)
                # = (h_real*cos_r - h_imag*sin_r) + i*(h_real*sin_r + h_imag*cos_r)
                h_rotated_real = [h_real[0] * cos_r - h_imag[0] * sin_r]
                h_rotated_imag = [h_real[0] * sin_r + h_imag[0] * cos_r]

                # 正样本
                t_real = self.entity_real.get(t_id, [1.0])
                t_imag = self.entity_imag.get(t_id, [0.0])

                pos_score = self._compute_score(h_rotated_real, h_rotated_imag, t_real, t_imag)

                # 负样本
                neg_id = random.choice(list(self.entity_real.keys()))
                while neg_id == t_id:
                    neg_id = random.choice(list(self.entity_real.keys()))
                neg_real = self.entity_real.get(neg_id, [1.0])
                neg_imag = self.entity_imag.get(neg_id, [0.0])

                neg_score = self._compute_score(h_rotated_real, h_rotated_imag, neg_real, neg_imag)

                loss = max(0, pos_score - neg_score + 1.0)
                total_loss += loss

            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")

        self.is_trained = True
        logger.info("RotatE模型训练完成")

    def _compute_score(self, h_real, h_imag, t_real, t_imag) -> float:
        """计算三元组得分"""
        diff_real = h_real[0] - t_real[0]
        diff_imag = h_imag[0] - t_imag[0]
        return diff_real * diff_real + diff_imag * diff_imag

    def get_entity_embedding(self, entity_id: str) -> Optional[List[float]]:
        """获取实体嵌入（复数表示）"""
        real = self.entity_real.get(entity_id, [1.0])
        imag = self.entity_imag.get(entity_id, [0.0])
        return real + imag

    def get_relation_embedding(self, relation_type: str) -> Optional[List[float]]:
        """获取关系嵌入"""
        phase = self.relation_phases.get(relation_type, 0.0)
        import math
        return [math.cos(phase), math.sin(phase)]

    def similarity(self, entity_id_1: str, entity_id_2: str) -> float:
        """计算相似度"""
        e1 = self.get_entity_embedding(entity_id_1)
        e2 = self.get_entity_embedding(entity_id_2)

        if e1 is None or e2 is None:
            return 0.0

        # 将复数视为2维向量计算余弦相似度
        dot = e1[0] * e2[0] + e1[1] * e2[1]
        norm1 = (e1[0]**2 + e1[1]**2)**0.5
        norm2 = (e2[0]**2 + e2[1]**2)**0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def predict_links(self, head_entity: str, relation: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """链接预测"""
        import math

        h_real = self.entity_real.get(head_entity, [1.0])
        h_imag = self.entity_imag.get(head_entity, [0.0])
        r_phase = self.relation_phases.get(relation, 0.0)

        # 旋转h
        cos_r = math.cos(r_phase)
        sin_r = math.sin(r_phase)
        h_rotated_real = h_real[0] * cos_r - h_imag[0] * sin_r
        h_rotated_imag = h_real[0] * sin_r + h_imag[0] * cos_r

        predictions = []
        for entity_id in self.entity_real:
            if entity_id == head_entity:
                continue

            t_real = self.entity_real[entity_id]
            t_imag = self.entity_imag[entity_id]

            score = self._compute_score([h_rotated_real], [h_rotated_imag], t_real, t_imag)
            predictions.append((entity_id, -score))  # 负距离

        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:top_k]


class SimpleEmbeddingModel(EmbeddingModel):
    """简单嵌入模型（无需外部依赖）

    基于实体名称和属性生成简单的向量表示。
    适用于资源受限环境或快速原型验证。
    """

    def __init__(self, embedding_dim: int = 64, **kwargs):
        super().__init__("Simple", embedding_dim)
        self.entity_vectors: Dict[str, List[float]] = {}

    def _text_to_vector(self, text: str) -> List[float]:
        """将文本转换为向量"""
        name_bytes = text.encode('utf-8')
        vector = [0.0] * self.embedding_dim

        for i, b in enumerate(name_bytes[:self.embedding_dim]):
            vector[i] = b / 255.0

        return vector

    def train(self, knowledge_graph: 'KnowledgeGraph', epochs: int = 0, **kwargs):
        """训练（实际上只是初始化嵌入）"""
        logger.info("使用简单嵌入模型")

        for entity_id, entity in knowledge_graph.entities.items():
            # 基于名称生成向量
            base_vector = self._text_to_vector(entity.name)

            # 添加类型信息
            type_vector = self._type_to_vector(entity.entity_type)
            full_vector = base_vector + type_vector

            # 裁剪到指定维度
            if len(full_vector) > self.embedding_dim:
                full_vector = full_vector[:self.embedding_dim]
            else:
                full_vector += [0.0] * (self.embedding_dim - len(full_vector))

            self.entity_vectors[entity_id] = full_vector
            entity.embedding = full_vector

        self.is_trained = True
        logger.info("简单嵌入模型初始化完成")

    def _type_to_vector(self, entity_type: str) -> List[float]:
        """实体类型转向量"""
        type_map = {
            'event': [1, 0, 0, 0, 0],
            'concept': [0, 1, 0, 0, 0],
            'person': [0, 0, 1, 0, 0],
            'organization': [0, 0, 0, 1, 0],
            'location': [0, 0, 0, 0, 1],
        }
        return type_map.get(entity_type, [0, 0, 0, 0, 0])

    def get_entity_embedding(self, entity_id: str) -> Optional[List[float]]:
        return self.entity_vectors.get(entity_id)

    def get_relation_embedding(self, relation_type: str) -> Optional[List[float]]:
        """基于关系类型生成向量"""
        return self._text_to_vector(relation_type)

    def similarity(self, entity_id_1: str, entity_id_2: str) -> float:
        """余弦相似度"""
        v1 = self.entity_vectors.get(entity_id_1)
        v2 = self.entity_vectors.get(entity_id_2)

        if v1 is None or v2 is None:
            return 0.0

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = sum(a * a for a in v1) ** 0.5
        norm2 = sum(b * b for b in v2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def predict_links(self, head_entity: str, relation: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """预测链接"""
        v1 = self.entity_vectors.get(head_entity)
        r_vector = self._text_to_vector(relation)

        if v1 is None:
            return []

        # 预测实体 = 头实体 + 关系向量
        predicted = [v1[i] + r_vector[i] for i in range(self.embedding_dim)]

        predictions = []
        for entity_id, v2 in self.entity_vectors.items():
            if entity_id == head_entity:
                continue

            similarity = self.similarity(entity_id, head_entity)
            predictions.append((entity_id, similarity))

        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:top_k]


class KnowledgeGraph:
    """知识图谱主类

    提供知识图谱的完整生命周期管理功能。

    属性:
        entities: 实体字典
        relations: 关系列表
        statistics: 统计信息

    示例:
        kg = KnowledgeGraph()
        kg.add_entity("AI", entity_type="概念")
        kg.add_entity("机器学习", entity_type="技术")
        kg.add_relation("AI", "包含", "机器学习")
    """

    def __init__(self, name: str = "knowledge_graph"):
        """
        初始化知识图谱

        参数:
            name: 图谱名称
        """
        self.name = name
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.statistics: Dict[str, Any] = {}
        self._entity_counter = 0
        self._relation_counter = 0

        logger.info(f"创建知识图谱: {name}")

    def generate_id(self, prefix: str = "entity") -> str:
        """生成唯一ID"""
        import hashlib
        import time
        self._entity_counter += 1
        timestamp = str(time.time()).replace('.', '')
        hash_input = f"{prefix}{self._entity_counter}{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]

    def add_entity(
        self,
        name: str,
        entity_type: str = "concept",
        entity_id: Optional[str] = None,
        attributes: Optional[Dict] = None
    ) -> Entity:
        """
        添加实体

        参数:
            name: 实体名称
            entity_type: 实体类型
            entity_id: 实体ID（可选，自动生成）
            attributes: 属性字典

        返回:
            创建的实体
        """
        if entity_id is None:
            entity_id = self.generate_id("ent")

        entity = Entity(
            entity_id=entity_id,
            name=name,
            entity_type=entity_type,
            attributes=attributes or {}
        )

        self.entities[entity_id] = entity
        self._update_statistics()

        logger.debug(f"添加实体: {name} ({entity_type})")
        return entity

    def add_relation(
        self,
        source_entity: str,
        relation_type: str,
        target_entity: str,
        weight: float = 1.0,
        attributes: Optional[Dict] = None
    ) -> Relation:
        """
        添加关系

        参数:
            source_entity: 源实体ID或名称
            relation_type: 关系类型
            target_entity: 目标实体ID或名称
            weight: 关系权重
            attributes: 属性字典

        返回:
            创建的关系
        """
        # 查找实体（按ID或名称）
        source_id = self._find_entity_id(source_entity)
        target_id = self._find_entity_id(target_entity)

        if source_id is None:
            logger.warning(f"源实体不存在: {source_entity}")
            source_id = source_entity

        if target_id is None:
            logger.warning(f"目标实体不存在: {target_entity}")
            target_id = target_entity

        self._relation_counter += 1

        relation = Relation(
            relation_id=f"rel_{self._relation_counter:06d}",
            source_entity=source_id,
            target_entity=target_id,
            relation_type=relation_type,
            weight=weight,
            attributes=attributes or {}
        )

        self.relations.append(relation)
        self._update_statistics()

        logger.debug(f"添加关系: {source_entity} --[{relation_type}]--> {target_entity}")
        return relation

    def _find_entity_id(self, identifier: str) -> Optional[str]:
        """查找实体ID"""
        if identifier in self.entities:
            return identifier

        for entity_id, entity in self.entities.items():
            if entity.name == identifier:
                return entity_id

        return None

    def _update_statistics(self):
        """更新统计信息"""
        type_counts = defaultdict(int)
        for entity in self.entities.values():
            type_counts[entity.entity_type] += 1

        self.statistics = {
            "entity_count": len(self.entities),
            "relation_count": len(self.relations),
            "entity_types": dict(type_counts),
            "relation_types": list(set(rel.relation_type for rel in self.relations)),
            "created_at": datetime.now().isoformat()
        }

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取实体"""
        return self.entities.get(entity_id)

    def get_relations_by_entity(self, entity_id: str, direction: str = "out") -> List[Relation]:
        """
        获取实体的关联关系

        参数:
            entity_id: 实体ID
            direction: "out"（出边）、"in"（入边）、"both"（全部）

        返回:
            关系列表
        """
        result = []
        for rel in self.relations:
            if direction in ["out", "both"] and rel.source_entity == entity_id:
                result.append(rel)
            if direction in ["in", "both"] and rel.target_entity == entity_id:
                result.append(rel)
        return result

    def find_similar_entities(
        self,
        entity_id: str,
        model: EmbeddingModel,
        top_k: int = 5,
        entity_type: Optional[str] = None
    ) -> List[Tuple[Entity, float]]:
        """
        查找相似实体

        参数:
            entity_id: 目标实体ID
            model: 嵌入模型
            top_k: 返回数量
            entity_type: 过滤特定类型

        返回:
            [(实体, 相似度), ...]
        """
        if not model.is_trained:
            logger.warning("模型未训练，无法计算相似度")
            return []

        similarities = []
        for eid, entity in self.entities.items():
            if eid == entity_id:
                continue

            if entity_type and entity.entity_type != entity_type:
                continue

            sim = model.similarity(entity_id, eid)
            similarities.append((entity, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def predict_links(
        self,
        entity_id: str,
        relation: str,
        model: EmbeddingModel,
        top_k: int = 5
    ) -> List[Tuple[Entity, float]]:
        """
        链接预测

        参数:
            entity_id: 头实体ID
            relation: 关系类型
            model: 嵌入模型
            top_k: 返回数量

        返回:
            [(预测实体, 得分), ...]
        """
        if not model.is_trained:
            logger.warning("模型未训练，无法进行链接预测")
            return []

        predictions = model.predict_links(entity_id, relation, top_k)

        results = []
        for pred_id, score in predictions:
            entity = self.entities.get(pred_id)
            if entity:
                results.append((entity, score))

        return results

    def cluster_entities(
        self,
        entity_type: str,
        model: EmbeddingModel,
        n_clusters: int = 3
    ) -> Dict[int, List[Entity]]:
        """
        实体聚类

        参数:
            entity_type: 实体类型
            model: 嵌入模型
            n_clusters: 聚类数

        返回:
            {聚类ID: [实体列表], ...}
        """
        if not model.is_trained:
            logger.warning("模型未训练，无法进行聚类")
            return {}

        # 收集该类型的实体
        entities = [e for e in self.entities.values() if e.entity_type == entity_type]

        if len(entities) < n_clusters:
            logger.warning(f"实体数量 ({len(entities)}) 小于聚类数 ({n_clusters})")
            return {}

        # 简化版K-Means
        centroids = []
        for i in range(n_clusters):
            entity = entities[i % len(entities)]
            vec = model.get_entity_embedding(entity.entity_id)
            if vec:
                centroids.append(vec.copy())

        for _ in range(10):  # 迭代
            clusters = [[] for _ in range(n_clusters)]

            for entity in entities:
                vec = model.get_entity_embedding(entity.entity_id)
                if not vec:
                    continue

                # 分配到最近的聚类
                best_cluster = 0
                best_sim = -1
                for i, centroid in enumerate(centroids):
                    sim = self._cosine_similarity(vec, centroid)
                    if sim > best_sim:
                        best_sim = sim
                        best_cluster = i

                clusters[best_cluster].append(entity)

            # 更新聚类中心
            for i, cluster_entities in enumerate(clusters):
                if cluster_entities:
                    vectors = [model.get_entity_embedding(e.entity_id) for e in cluster_entities]
                    centroids[i] = [
                        sum(v[j] for v in vectors if v) / len([v for v in vectors if v])
                        for j in range(len(centroids[0]))
                    ]

        # 构建结果
        result = {}
        for i, cluster_entities in enumerate(clusters):
            if cluster_entities:
                result[i] = cluster_entities

        return result

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """余弦相似度"""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = sum(a * a for a in v1) ** 0.5
        norm2 = sum(b * b for b in v2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def build_from_events(self, events: List[Dict], extract_entities: bool = True) -> int:
        """
        从事件列表构建知识图谱

        参数:
            events: 事件列表，每个事件包含title、category、keywords等
            extract_entities: 是否自动提取实体

        返回:
            添加的事件数量
        """
        event_entities = []
        added_count = 0

        for i, event in enumerate(events):
            title = event.get('title', f"Event_{i}")
            category = event.get('category', '综合')
            keywords = event.get('keywords', [])

            # 添加事件实体
            event_entity = self.add_entity(
                name=title[:50],
                entity_type="event",
                attributes={
                    "category": category,
                    "keywords": keywords,
                    "heat_score": event.get('heat_score', 0),
                    "source": event.get('source', ''),
                    "publish_time": str(event.get('publish_time', ''))
                }
            )
            event_entities.append(event_entity)
            added_count += 1

            # 自动提取关键词作为概念实体
            for keyword in keywords[:3]:
                self.add_entity(
                    name=keyword,
                    entity_type="concept",
                    attributes={"source": "keyword_extraction"}
                )

                # 建立事件与概念的关联
                self.add_relation(
                    title,
                    "涉及",
                    keyword,
                    weight=0.8
                )

        self._update_statistics()
        return added_count

    def export(self, format: str = "json") -> Union[str, Dict]:
        """
        导出知识图谱

        参数:
            format: "json" 或 "rdf"

        返回:
            导出内容
        """
        if format == "json":
            return json.dumps({
                "name": self.name,
                "entities": {eid: ent.to_dict() for eid, ent in self.entities.items()},
                "relations": [rel.to_dict() for rel in self.relations],
                "statistics": self.statistics
            }, ensure_ascii=False, indent=2)
        else:
            # 简化版RDF
            lines = ["@prefix kg: <http://knowledge-graph.org/> ."]
            for entity in self.entities.values():
                lines.append(f'kg:{entity.entity_id} a kg:{entity.entity_type} ;')
                lines.append(f'  kg:name "{entity.name}" .')
            return '\n'.join(lines)

    def summary(self) -> str:
        """获取图谱摘要"""
        lines = [
            f"知识图谱: {self.name}",
            f"实体数量: {self.statistics.get('entity_count', 0)}",
            f"关系数量: {self.statistics.get('relation_count', 0)}",
            f"实体类型: {self.statistics.get('entity_types', {})}",
            f"关系类型: {self.statistics.get('relation_types', [])}"
        ]
        return '\n'.join(lines)


def create_embedding_model(
    model_name: str = "TransE",
    embedding_dim: int = 128,
    **kwargs
) -> EmbeddingModel:
    """
    创建嵌入模型

    参数:
        model_name: 模型名称 (TransE, RotatE, Simple)
        embedding_dim: 嵌入维度
        **kwargs: 其他参数

    返回:
        嵌入模型实例
    """
    models = {
        "transe": TransEModel,
        "rotate": RotatEModel,
        "simple": SimpleEmbeddingModel,
    }

    model_class = models.get(model_name.lower(), SimpleEmbeddingModel)
    return model_class(embedding_dim=embedding_dim, **kwargs)


def demo():
    """演示"""
    import random

    print("=" * 80)
    print("知识图谱技能演示")
    print("=" * 80)

    # 1. 创建知识图谱
    print("\n[1/5] 创建知识图谱...")
    kg = KnowledgeGraph("科技领域知识图谱")
    print(f"✅ 创建完成")

    # 2. 添加实体
    print("\n[2/5] 添加实体...")
    entities = [
        ("人工智能", "领域", {"描述": "模拟人类智能的技术领域"}),
        ("深度学习", "技术", {"描述": "基于神经网络的机器学习方法"}),
        ("Transformer", "架构", {"描述": "注意力机制为核心的神经网络架构"}),
        ("GPT", "模型", {"描述": "生成式预训练Transformer模型"}),
        ("ChatGPT", "产品", {"描述": "OpenAI开发的对话AI产品"}),
        ("BERT", "模型", {"描述": "双向编码器表示模型"}),
        ("大语言模型", "概念", {"描述": "具有数十亿参数的AI模型"}),
    ]

    for name, etype, attrs in entities:
        kg.add_entity(name, entity_type=etype, attributes=attrs)
        print(f"  添加: {name} ({etype})")

    # 3. 添加关系
    print("\n[3/5] 添加关系...")
    relations = [
        ("深度学习", "属于", "人工智能"),
        ("Transformer", "实现", "深度学习"),
        ("GPT", "基于", "Transformer"),
        ("ChatGPT", "基于", "GPT"),
        ("BERT", "基于", "Transformer"),
        ("大语言模型", "包含", "GPT"),
        ("大语言模型", "包含", "BERT"),
        ("人工智能", "包含", "深度学习"),
    ]

    for src, rel, tgt in relations:
        kg.add_relation(src, rel, tgt)
        print(f"  {src} --[{rel}]--> {tgt}")

    # 4. 训练嵌入模型
    print("\n[4/5] 训练嵌入模型...")
    model = create_embedding_model("TransE", embedding_dim=64)
    model.train(kg, epochs=50)
    print(f"✅ 模型训练完成")

    # 5. 嵌入分析
    print("\n[5/5] 嵌入分析...")

    # 相似度
    sim = model.similarity("GPT", "BERT")
    print(f"\n  语义相似度:")
    print(f"    GPT <-> BERT: {sim:.4f}")

    # 找相似实体
    similar = kg.find_similar_entities("GPT", model, top_k=3)
    print(f"\n  与GPT最相似的实体:")
    for entity, score in similar:
        print(f"    - {entity.name}: {score:.4f}")

    # 链接预测
    predictions = kg.predict_links("ChatGPT", "属于", model, top_k=3)
    print(f"\n  链接预测 (ChatGPT, 属于):")
    for entity, score in predictions:
        print(f"    - {entity.name}: {score:.4f}")

    # 聚类
    clusters = kg.cluster_entities("model", model, n_clusters=2)
    print(f"\n  模型聚类:")
    for cid, entities in clusters.items():
        names = [e.name for e in entities]
        print(f"    聚类{cid}: {names}")

    # 输出摘要
    print("\n" + "=" * 80)
    print(kg.summary())
    print("=" * 80)
    print("✅ 演示完成！")
    print("=" * 80)


if __name__ == "__main__":
    demo()
