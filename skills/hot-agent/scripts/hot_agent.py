#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点Agent - 智能热点事件分析与知识图谱生成

基于多源数据采集、事件分类、现象追溯、心理分析和知识图谱生成的
智能热点事件分析工具

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EventCategory(Enum):
    """事件分类枚举"""
    TECH = "科技"
    FINANCE = "财经"
    SOCIETY = "社会"
    ENTERTAINMENT = "娱乐"
    SPORTS = "体育"
    EDUCATION = "教育"
    HEALTH = "健康"
    MILITARY = "军事"
    INTERNATIONAL = "国际"
    REAL_ESTATE = "房地产"
    AUTO = "汽车"
    GAME = "游戏"
    TRAVEL = "旅游"
    FOOD = "美食"


class PsychologicalDimension(Enum):
    """心理分析维度"""
    COGNITIVE = "认知影响"
    EMOTIONAL = "情感影响"
    BEHAVIORAL = "行为影响"
    SOCIAL = "社会影响"


class EmotionType(Enum):
    """情绪类型"""
    FEAR = "恐惧"
    ANGER = "愤怒"
    JOY = "喜悦"
    SADNESS = "悲伤"
    ANXIETY = "焦虑"
    SURPRISE = "惊讶"
    DISGUST = "厌恶"
    TRUST = "信任"


@dataclass
class HotEvent:
    """热点事件"""
    event_id: str
    title: str
    source: str
    publish_time: datetime
    url: str
    categories: Dict[str, Any] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)
    heat_score: float = 0.0
    sentiment: str = "neutral"
    summary: str = ""
    description: str = ""


@dataclass
class EventClassification:
    """事件分类结果"""
    primary_category: EventCategory
    secondary_category: Optional[str] = None
    confidence: float = 0.0
    keywords: List[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class Phenomenon:
    """社会现象"""
    name: str
    description: str
    category: str
    evidence: List[str] = field(default_factory=list)
    impact_level: str = "medium"
    trend: str = "unknown"


@dataclass
class PhenomenonTrace:
    """现象追溯结果"""
    event_id: str
    root_causes: List[str] = field(default_factory=list)
    key_factors: List[str] = field(default_factory=list)
    phenomena: List[Phenomenon] = field(default_factory=list)
    development_chain: List[str] = field(default_factory=list)
    future_trends: List[str] = field(default_factory=list)


@dataclass
class PsychologicalImpact:
    """心理影响"""
    dimension: PsychologicalDimension
    emotion_type: EmotionType
    emotion_intensity: float = 0.0
    affected_groups: List[str] = field(default_factory=list)
    impact_description: str = ""
    behavioral_indication: str = ""


@dataclass
class PsychologicalAnalysis:
    """心理状态分析结果"""
    event_id: str
    overall_mood: str = ""
    mood_score: float = 0.0
    primary_emotions: List[Dict[str, Any]] = field(default_factory=list)
    secondary_emotions: List[Dict[str, Any]] = field(default_factory=list)
    psychological_triggers: List[str] = field(default_factory=list)
    behavioral_suggestions: List[str] = field(default_factory=list)


@dataclass
class KnowledgeNode:
    """知识图谱节点"""
    node_id: str
    node_type: str
    name: str
    description: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.0


@dataclass
class KnowledgeEdge:
    """知识图谱边"""
    edge_id: str
    source_node: str
    target_node: str
    relationship: str
    weight: float = 1.0
    description: str = ""


@dataclass
class KnowledgeGraph:
    """知识图谱"""
    graph_id: str
    topic: str
    generated_time: datetime
    nodes: List[KnowledgeNode]
    edges: List[KnowledgeEdge]
    statistics: Dict[str, Any] = field(default_factory=dict)


class HotTopicAgent:
    """热点事件分析与知识图谱生成Agent"""

    # 默认配置
    DEFAULT_CONFIG = {
        "time_range": "24h",
        "categories": None,
        "keywords": None,
        "sources": None,
        "limit": 50,
        "deduplicate": True,
        "sort_by": "heat",
    }

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        api_keys: Optional[Dict[str, str]] = None
    ):
        """
        初始化热点Agent

        参数:
            config: 配置字典
            api_keys: API密钥字典
        """
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.api_keys = api_keys or self._load_api_keys()
        
        # 初始化日志
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 设置输出目录
        self.output_dir = Path(config.get("output_dir", "./output")) if config else Path("./output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化分类器
        self._init_classifier()
        
        # 初始化分析器
        self._init_analyzer()
        
        self.logger.info("热点Agent初始化完成")

    def _load_api_keys(self) -> Dict[str, str]:
        """加载API密钥"""
        keys = {}
        
        # 从环境变量加载
        env_keys = ["OPENAI_API_KEY", "BRAVE_API_KEY"]
        for key in env_keys:
            value = os.environ.get(key)
            if value:
                keys[key.lower()] = value
        
        # 从.env文件加载
        env_file = Path(".env")
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv(env_file)
            for key in env_keys:
                value = os.environ.get(key)
                if value:
                    keys[key.lower()] = value
        
        return keys

    def _init_classifier(self):
        """初始化分类器"""
        # 分类关键词映射
        self.category_keywords = {
            EventCategory.TECH: ["科技", "AI", "人工智能", "大模型", "互联网", "数码", "手机", "电脑", "软件", "硬件"],
            EventCategory.FINANCE: ["财经", "股票", "基金", "投资", "经济", "金融", "房价", "通胀", "GDP"],
            EventCategory.SOCIETY: ["社会", "民生", "政策", "法规", "热点", "新闻", "事件"],
            EventCategory.ENTERTAINMENT: ["娱乐", "明星", "影视", "综艺", "音乐", "八卦", "综艺"],
            EventCategory.SPORTS: ["体育", "足球", "篮球", "奥运", "比赛", "运动员", "金牌"],
            EventCategory.EDUCATION: ["教育", "学校", "高考", "留学", "培训", "学习", "学生"],
            EventCategory.HEALTH: ["健康", "医疗", "疾病", "养生", "健身", "药物", "医院"],
            EventCategory.INTERNATIONAL: ["国际", "外交", "美国", "欧洲", "亚洲", "全球", "世界"],
        }

    def _init_analyzer(self):
        """初始化分析器"""
        # 情感词映射
        self.emotion_words = {
            EmotionType.FEAR: ["恐惧", "担忧", "害怕", "焦虑", "不安"],
            EmotionType.ANGER: ["愤怒", "生气", "不满", "反感", "讨厌"],
            EmotionType.JOY: ["高兴", "开心", "兴奋", "喜悦", "激动"],
            EmotionType.SADNESS: ["悲伤", "难过", "伤心", "失落", "沮丧"],
            EmotionType.ANXIETY: ["焦虑", "紧张", "压力", "担忧", "着急"],
            EmotionType.SURPRISE: ["惊讶", "惊奇", "意外", "惊喜", "震惊"],
            EmotionType.TRUST: ["信任", "相信", "支持", "认可", "肯定"],
        }

    def collect(
        self,
        time_range: Optional[str] = None,
        categories: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> List[HotEvent]:
        """
        采集热点事件

        参数:
            time_range: 时间范围 (24h, 7d, 30d, 90d)
            categories: 分类列表
            keywords: 关键词列表
            sources: 数据源列表
            limit: 采集上限

        返回:
            热点事件列表
        """
        self.logger.info("开始采集热点事件...")
        
        # 合并参数
        params = {
            "time_range": time_range or self.config.get("time_range", "24h"),
            "categories": categories or self.config.get("categories"),
            "keywords": keywords or self.config.get("keywords"),
            "sources": sources or self.config.get("sources"),
            "limit": limit or self.config.get("limit", 50),
        }
        
        # TODO: 实现实际的采集逻辑
        # 这里提供模拟数据作为示例
        events = self._generate_sample_events(params["limit"])
        
        self.logger.info(f"采集完成，共获取 {len(events)} 个事件")
        return events

    def _generate_sample_events(self, limit: int) -> List[HotEvent]:
        """生成示例事件数据"""
        import random
        
        sample_titles = [
            "人工智能大模型再获突破，行业迎来新变革",
            "新能源汽车销量持续增长，市场格局生变",
            "房地产市场政策调整，买房时机引关注",
            "科技巨头发布新品，引领行业发展新趋势",
            "社会热点事件引发广泛讨论，舆论持续发酵",
            "国际形势复杂多变，经济影响逐步显现",
            "教育政策新规出台，家长学生如何应对",
            "健康养生话题热度不减，专家解读科学建议",
            "体育赛事精彩纷呈，运动员表现引关注",
            "娱乐明星动态成热点，粉丝经济持续升温",
        ]
        
        events = []
        for i in range(limit):
            title = random.choice(sample_titles)
            event = HotEvent(
                event_id=f"evt_{datetime.now().strftime('%Y%m%d')}_{i:04d}",
                title=title,
                source=random.choice(["新浪科技", "腾讯新闻", "网易新闻", "凤凰网", "知乎"]),
                publish_time=datetime.now() - timedelta(hours=random.randint(1, 48)),
                url=f"https://example.com/news/{i}.html",
                keywords=self._extract_keywords(title),
                heat_score=random.uniform(60, 100),
                sentiment=random.choice(["positive", "neutral", "negative"]),
                summary=f"这是关于{title}的摘要描述..."
            )
            events.append(event)
        
        return events

    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词"""
        # 简单关键词提取（实际应用中应使用NLP工具）
        keywords = []
        keyword_list = ["人工智能", "大模型", "新能源", "房地产", "科技", "政策", "经济"]
        for keyword in keyword_list:
            if keyword in title:
                keywords.append(keyword)
        return keywords if keywords else ["热点"]

    def classify(self, events: List[HotEvent]) -> Dict[str, List[HotEvent]]:
        """
        对事件进行分类

        参数:
            events: 事件列表

        返回:
            按分类分组的事件字典
        """
        self.logger.info("开始事件分类...")
        
        classified = defaultdict(list)
        
        for event in events:
            category = self._classify_event(event)
            event.categories = {
                "primary": category.primary_category.value,
                "secondary": category.secondary_category,
                "confidence": category.confidence,
                "keywords": category.keywords,
            }
            classified[category.primary_category.value].append(event)
        
        self.logger.info(f"分类完成，共 {len(classified)} 个类别")
        return dict(classified)

    def _classify_event(self, event: HotEvent) -> EventClassification:
        """对单个事件进行分类"""
        title = event.title
        keywords = event.keywords
        
        # 统计各分类匹配次数
        category_scores = defaultdict(float)
        
        for category, category_kw_list in self.category_keywords.items():
            score = 0
            for kw in category_kw_list:
                if kw in title:
                    score += 2
                if kw in keywords:
                    score += 1
            category_scores[category] = score
        
        # 选择得分最高的分类
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[best_category]
            
            if max_score > 0:
                confidence = min(max_score / 5.0, 1.0)
                return EventClassification(
                    primary_category=best_category,
                    confidence=confidence,
                    keywords=[kw for kw in keywords if kw in 
                             sum([list(kw_list) for kw_list in self.category_keywords.values()], [])],
                    reasoning=f"标题和关键词匹配度较高"
                )
        
        # 默认分类
        return EventClassification(
            primary_category=EventCategory.SOCIETY,
            confidence=0.5,
            keywords=keywords,
            reasoning="使用默认分类"
        )

    def trace_phenomenon(self, event: HotEvent) -> PhenomenonTrace:
        """
        追溯事件背后的现象

        参数:
            event: 热点事件

        返回:
            现象追溯结果
        """
        # TODO: 实现实际的现象追溯逻辑
        # 这里提供模拟结果作为示例
        
        phenomena = [
            Phenomenon(
                name="技术普及加速",
                description="新技术的快速普及改变了人们的生活方式",
                category="技术现象",
                evidence=["用户规模快速增长", "媒体报道增多"],
                impact_level="high",
                trend="上升"
            ),
            Phenomenon(
                name="市场关注度提升",
                description="越来越多的人开始关注这一领域",
                category="社会现象",
                evidence=["搜索指数上升", "社交媒体讨论增加"],
                impact_level="medium",
                trend="稳定"
            )
        ]
        
        return PhenomenonTrace(
            event_id=event.event_id,
            root_causes=["技术突破", "市场需求增长"],
            key_factors=["政策支持", "资本投入", "用户接受度提升"],
            phenomena=phenomena,
            development_chain=["技术突破 → 产品落地 → 市场推广 → 用户增长"],
            future_trends=["预计将继续保持增长态势"]
        )

    def analyze_psychology(self, events: List[HotEvent]) -> PsychologicalAnalysis:
        """
        分析热点事件对大众心理的影响

        参数:
            events: 事件列表

        返回:
            心理分析结果
        """
        self.logger.info("开始心理分析...")
        
        # TODO: 实现实际的心理分析逻辑
        # 这里提供模拟结果作为示例
        
        primary_emotions = [
            {
                "dimension": "认知影响",
                "emotion_type": "期待",
                "intensity": 0.75,
                "description": "对新技术的未来发展持积极态度"
            },
            {
                "dimension": "情感影响",
                "emotion_type": "兴奋",
                "intensity": 0.68,
                "description": "对创新突破感到兴奋和激动"
            }
        ]
        
        secondary_emotions = [
            {
                "dimension": "情感影响",
                "emotion_type": "焦虑",
                "intensity": 0.45,
                "description": "对职业发展前景存在一定担忧"
            }
        ]
        
        analysis = PsychologicalAnalysis(
            event_id="batch_analysis",
            overall_mood="积极乐观",
            mood_score=0.72,
            primary_emotions=primary_emotions,
            secondary_emotions=secondary_emotions,
            psychological_triggers=[
                "技术突破带来的变革感",
                "对未来发展的不确定性",
                "与自身利益的关联性"
            ],
            behavioral_suggestions=[
                "关注技术发展趋势",
                "提升相关技能储备",
                "理性看待市场波动"
            ]
        )
        
        self.logger.info(f"心理分析完成，整体情绪: {analysis.overall_mood}")
        return analysis

    def generate_knowledge_graph(
        self,
        topic: str,
        events: List[HotEvent],
        format: str = "mermaid"
    ) -> KnowledgeGraph:
        """
        生成知识图谱

        参数:
            topic: 图谱主题
            events: 事件列表
            format: 输出格式 (mermaid, json, graphviz)

        返回:
            知识图谱对象
        """
        self.logger.info("开始生成知识图谱...")
        
        # 构建节点
        nodes = []
        edges = []
        
        # 事件层节点
        for event in events[:10]:  # 限制节点数量
            node = KnowledgeNode(
                node_id=f"event_{event.event_id}",
                node_type="event",
                name=event.title[:20] + "...",
                description=event.summary,
                importance=event.heat_score / 100.0
            )
            nodes.append(node)
        
        # 现象层节点
        phenomena_names = ["技术普及", "市场关注", "政策支持", "资本投入"]
        for i, name in enumerate(phenomena_names):
            node = KnowledgeNode(
                node_id=f"phenomenon_{i}",
                node_type="phenomenon",
                name=name,
                description=f"{name}相关现象分析",
                importance=0.7
            )
            nodes.append(node)
        
        # 心理层节点
        emotions = ["积极乐观", "期待", "兴奋", "焦虑"]
        for i, emotion in enumerate(emotions):
            node = KnowledgeNode(
                node_id=f"emotion_{i}",
                node_type="psychology",
                name=emotion,
                description=f"公众{emotion}情绪",
                importance=0.6
            )
            nodes.append(node)
        
        # 构建边关系
        edge_id = 0
        for i, event_node in enumerate(nodes[:10]):
            # 事件 -> 现象
            for j in range(len(phenomena_names)):
                edge = KnowledgeEdge(
                    edge_id=f"edge_{edge_id}",
                    source_node=event_node.node_id,
                    target_node=f"phenomenon_{j}",
                    relationship="leads_to",
                    weight=0.8
                )
                edges.append(edge)
                edge_id += 1
        
        # 现象 -> 心理
        for j in range(len(phenomena_names)):
            for k in range(len(emotions)):
                edge = KnowledgeEdge(
                    edge_id=f"edge_{edge_id}",
                    source_node=f"phenomenon_{j}",
                    target_node=f"emotion_{k}",
                    relationship="influences",
                    weight=0.7
                )
                edges.append(edge)
                edge_id += 1
        
        # 创建图谱对象
        graph = KnowledgeGraph(
            graph_id=f"graph_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            topic=topic,
            generated_time=datetime.now(),
            nodes=nodes,
            edges=edges,
            statistics={
                "node_count": len(nodes),
                "edge_count": len(edges),
                "event_count": len([n for n in nodes if n.node_type == "event"]),
                "phenomenon_count": len([n for n in nodes if n.node_type == "phenomenon"]),
                "psychology_count": len([n for n in nodes if n.node_type == "psychology"]),
            }
        )
        
        self.logger.info(f"知识图谱生成完成，共 {len(nodes)} 个节点，{len(edges)} 条边")
        return graph

    def export_graph(self, graph: KnowledgeGraph, output_path: str, format: str = "mermaid"):
        """
        导出知识图谱

        参数:
            graph: 知识图谱对象
            output_path: 输出文件路径
            format: 输出格式
        """
        self.logger.info(f"导出知识图谱到 {output_path}...")
        
        output_file = self.output_dir / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "mermaid":
            content = self._export_mermaid(graph)
        elif format == "json":
            content = self._export_json(graph)
        else:
            content = self._export_mermaid(graph)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"知识图谱已保存到 {output_file}")

    def _export_mermaid(self, graph: KnowledgeGraph) -> str:
        """导出为Mermaid格式"""
        lines = [
            f"# 知识图谱: {graph.topic}",
            f"**生成时间**: {graph.generated_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**节点数**: {len(graph.nodes)} | **边数**: {len(graph.edges)}",
            "",
            "```mermaid",
            "graph TB",
            "    %% 节点定义",
            "    subgraph 事件层",
        ]
        
        # 事件层节点
        for node in graph.nodes:
            if node.node_type == "event":
                safe_name = node.name.replace("[", "(").replace("]", ")").replace('"', "'")
                lines.append(f'        {node.node_id}["{safe_name}"]')
        
        lines.append("    end")
        lines.append("")
        lines.append("    subgraph 现象层")
        
        # 现象层节点
        for node in graph.nodes:
            if node.node_type == "phenomenon":
                lines.append(f'        {node.node_id}("{node.name}")')
        
        lines.append("    end")
        lines.append("")
        lines.append("    subgraph 心理层")
        
        # 心理层节点
        for node in graph.nodes:
            if node.node_type == "psychology":
                lines.append(f'        {node.node_id}<"{node.name}">')
        
        lines.append("    end")
        lines.append("")
        lines.append("    %% 边关系")
        
        # 边
        for edge in graph.edges:
            lines.append(f"    {edge.source_node} -.->|{edge.relationship}| {edge.target_node}")
        
        lines.append("")
        lines.append("    %% 节点样式")
        lines.append("    classDef event fill:#e1f5fe,stroke:#01579b")
        lines.append("    classDef phenomenon fill:#fff3e0,stroke:#e65100")
        lines.append("    classDef psychology fill:#f3e5f5,stroke:#4a148c")
        lines.append("")
        
        # 应用样式
        event_nodes = [n.node_id for n in graph.nodes if n.node_type == "event"]
        if event_nodes:
            lines.append(f"    class {','.join(event_nodes)} event")
        
        phenomenon_nodes = [n.node_id for n in graph.nodes if n.node_type == "phenomenon"]
        if phenomenon_nodes:
            lines.append(f"    class {','.join(phenomenon_nodes)} phenomenon")
        
        psych_nodes = [n.node_id for n in graph.nodes if n.node_type == "psychology"]
        if psych_nodes:
            lines.append(f"    class {','.join(psych_nodes)} psychology")
        
        lines.append("```")
        lines.append("")
        
        return '\n'.join(lines)

    def _export_json(self, graph: KnowledgeGraph) -> str:
        """导出为JSON格式"""
        data = {
            "graph_id": graph.graph_id,
            "topic": graph.topic,
            "generated_time": graph.generated_time.isoformat(),
            "nodes": [
                {
                    "id": n.node_id,
                    "type": n.node_type,
                    "name": n.name,
                    "description": n.description,
                    "importance": n.importance
                }
                for n in graph.nodes
            ],
            "edges": [
                {
                    "source": e.source_node,
                    "target": e.target_node,
                    "relationship": e.relationship,
                    "weight": e.weight
                }
                for e in graph.edges
            ],
            "statistics": graph.statistics
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def batch_analyze(
        self,
        events: List[HotEvent],
        batch_size: int = 50,
        parallel: bool = False,
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        批量分析事件

        参数:
            events: 事件列表
            batch_size: 批处理大小
            parallel: 是否并行处理
            progress_callback: 进度回调函数

        返回:
            分析结果列表
        """
        self.logger.info(f"开始批量分析，共 {len(events)} 个事件...")
        
        results = []
        total_batches = (len(events) + batch_size - 1) // batch_size
        
        for i in range(0, len(events), batch_size):
            batch = events[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            if progress_callback:
                progress_callback(batch_num, total_batches)
            
            # 分类
            classified = self.classify(batch)
            
            # 心理分析
            psych = self.analyze_psychology(batch)
            
            for event in batch:
                result = {
                    "event": event,
                    "classification": event.categories,
                    "phenomenon": self.trace_phenomenon(event),
                    "psychology": psych if event.event_id == "batch_analysis" else None
                }
                results.append(result)
        
        self.logger.info(f"批量分析完成，共 {len(results)} 个结果")
        return results

    def generate_report(
        self,
        events: List[HotEvent],
        report_type: str = "daily",
        sections: Optional[List[str]] = None
    ) -> str:
        """
        生成分析报告

        参数:
            events: 事件列表
            report_type: 报告类型 (daily, weekly, monthly)
            sections: 包含的章节

        返回:
            报告内容
        """
        self.logger.info(f"生成{report_type}分析报告...")
        
        # 分类统计
        classified = self.classify(events)
        
        # 心理分析
        psych = self.analyze_psychology(events)
        
        # 生成报告
        lines = [
            f"# 热点事件{report_type}分析报告",
            "",
            f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**分析事件数**: {len(events)}",
            "",
            "---",
            "",
            "## 一、概述",
            "",
            f"本报告分析了{len(events)}个热点事件，涵盖{len(classified)}个主要领域。",
            "",
        ]
        
        # 分类统计
        if "classification" in (sections or []):
            lines.extend([
                "## 二、事件分类统计",
                "",
                "| 分类 | 事件数量 | 占比 |",
                "|------|---------|------|",
            ])
            
            for category, event_list in classified.items():
                percentage = len(event_list) / len(events) * 100
                lines.append(f"| {category} | {len(event_list)} | {percentage:.1f}% |")
            
            lines.append("")
        
        # 心理分析
        if "psychology" in (sections or []) or not sections:
            lines.extend([
                "## 三、心理影响分析",
                "",
                f"### 整体情绪倾向",
                f"- **情绪倾向**: {psych.overall_mood}",
                f"- **情绪评分**: {psych.mood_score}",
                "",
                f"### 主要情绪",
            ])
            
            for emotion in psych.primary_emotions:
                lines.append(f"- **{emotion['emotion_type']}** ({emotion['dimension']}): {emotion['description']}")
            
            lines.extend([
                "",
                f"### 行为建议",
            ])
            
            for suggestion in psych.behavioral_suggestions:
                lines.append(f"- {suggestion}")
            
            lines.append("")
        
        # 知识图谱
        if "graph" in (sections or []):
            lines.extend([
                "## 四、知识图谱",
                "",
                "```mermaid",
                "graph TB",
                "    E1[事件示例] --> P1[现象]",
                "    P1 --> M1[心理影响]",
                "```",
                "",
                "*（完整知识图谱请查看生成的图谱文件）*",
                "",
            ])
        
        lines.extend([
            "---",
            "",
            "## 五、结论与建议",
            "",
            "基于以上分析，建议关注以下方向：",
            "",
            "1. **持续跟踪**热点事件的演变趋势",
            "2. **关注**事件对公众心理的长期影响",
            "3. **结合**知识图谱理解事件之间的关联",
            "",
            "---",
            "",
            "*报告生成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "*",
        ])
        
        return '\n'.join(lines)

    def save_report(self, report: str, output_path: str):
        """保存报告"""
        output_file = self.output_dir / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"报告已保存到 {output_file}")


def main():
    """主函数 - 命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='热点Agent - 热点事件分析与知识图谱生成')
    
    parser.add_argument('--time-range', type=str, default='24h',
                        help='时间范围 (24h, 7d, 30d, 90d)')
    parser.add_argument('--categories', type=str, nargs='+',
                        default=['科技', '财经', '社会'],
                        help='事件分类')
    parser.add_argument('--keywords', type=str, nargs='+',
                        help='关键词过滤')
    parser.add_argument('--limit', type=int, default=50,
                        help='采集上限')
    parser.add_argument('--output', type=str, default='output/report.md',
                        help='输出文件路径')
    parser.add_argument('--format', type=str, default='mermaid',
                        choices=['mermaid', 'json', 'html'],
                        help='输出格式')
    parser.add_argument('--verbose', action='store_true',
                        help='详细输出')
    
    args = parser.parse_args()
    
    # 配置日志
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # 初始化Agent
    agent = HotTopicAgent()
    
    # 采集事件
    print(f"采集过去{args.time_range}的热点事件...")
    events = agent.collect(
        time_range=args.time_range,
        categories=args.categories,
        keywords=args.keywords,
        limit=args.limit
    )
    
    # 分类
    print("事件分类...")
    classified = agent.classify(events)
    for category, event_list in classified.items():
        print(f"  {category}: {len(event_list)} 个事件")
    
    # 心理分析
    print("心理分析...")
    psych = agent.analyze_psychology(events)
    print(f"  整体情绪: {psych.overall_mood}")
    
    # 生成图谱
    print("生成知识图谱...")
    graph = agent.generate_knowledge_graph(
        topic="热点事件知识图谱",
        events=events,
        format=args.format
    )
    
    # 导出图谱
    agent.export_graph(graph, args.output, format=args.format)
    print(f"知识图谱已保存")
    
    # 生成报告
    print("生成分析报告...")
    report = agent.generate_report(events, report_type="daily")
    agent.save_report(report, "output/daily_report.md")
    print("报告已保存")
    
    print("\n完成！")


if __name__ == "__main__":
    main()
