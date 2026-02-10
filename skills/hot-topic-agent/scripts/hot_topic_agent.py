#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hot Topic Agent Skill - Demo

热点头条Agent技能演示

功能：
- 多源热点数据采集（微博、知乎、抖音、B站等）
- 趋势分析
- 情感分析
- 知识图谱生成

作者: OpenClaw Agent
创建时间: 2026-02-10
"""

import os
import sys
import json
import random
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class HotTopic:
    """热点话题"""
    topic_id: str
    title: str
    platform: str
    heat_score: float  # 0-100
    velocity: str  # rising, stable, falling
    sentiment: str  # positive, neutral, negative
    keywords: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)
    publish_time: str = field(default_factory=lambda: datetime.now().isoformat())


class HotTopicAgent:
    """热点头条Agent"""

    # 支持的平台
    PLATFORMS = {
        "weibo": {"name": "微博", "update_freq": "实时", "quality": "高"},
        "zhihu": {"name": "知乎", "update_freq": "小时级", "quality": "高"},
        "douyin": {"name": "抖音", "update_freq": "实时", "quality": "高"},
        "bilibili": {"name": "哔哩哔哩", "update_freq": "实时", "quality": "高"},
        "xiaohongshu": {"name": "小红书", "update_freq": "小时级", "quality": "中"},
        "twitter": {"name": "Twitter/X", "update_freq": "实时", "quality": "高"},
        "hackernews": {"name": "Hacker News", "update_freq": "10分钟", "quality": "高"},
        "reddit": {"name": "Reddit", "update_freq": "实时", "quality": "中"},
    }

    def __init__(self):
        """初始化Agent"""
        logger.info("Hot Topic Agent 初始化完成")
        self.topics: List[HotTopic] = []
        self._generate_sample_data()

    def _generate_sample_data(self):
        """生成示例数据用于演示"""
        sample_topics = [
            ("AI大模型再获突破，行业迎来新变革", "weibo", "科技", 95, ["AI", "大模型", "突破"]),
            ("新能源汽车销量持续增长，市场格局生变", "weibo", "财经", 92, ["新能源", "汽车"]),
            ("房地产市场政策调整，买房时机引关注", "zhihu", "财经", 91, ["房地产", "政策"]),
            ("科技巨头发布新品，引领行业发展新趋势", "douyin", "科技", 90, ["科技", "新品"]),
            ("社会热点事件引发广泛讨论，舆论持续发酵", "twitter", "社会", 89, ["热点", "讨论"]),
            ("国际形势复杂多变，经济影响逐步显现", "reddit", "国际", 88, ["国际", "经济"]),
            ("5G网络商用加速，产业数字化转型", "hackernews", "科技", 87, ["5G", "数字化"]),
            ("互联网平台监管加强，规范行业发展", "bilibili", "科技", 86, ["监管", "互联网"]),
            ("芯片技术自主可控成为焦点", "xiaohongshu", "科技", 85, ["芯片", "自主"]),
            ("数字经济蓬勃发展，新业态不断涌现", "weibo", "经济", 84, ["数字经济", "新业态"]),
            ("直播带货规范化，行业发展进入新阶段", "douyin", "电商", 83, ["直播带货", "规范"]),
            ("元宇宙概念持续升温，应用场景不断拓展", "zhihu", "科技", 82, ["元宇宙", "VR"]),
            ("碳中和目标推动新能源产业快速发展", "hackernews", "环保", 81, ["碳中和", "新能源"]),
            ("AI绘画工具大火，创作者生态面临变革", "twitter", "科技", 80, ["AI绘画", "创作者"]),
            ("互联网大厂年终奖引发热议", "weibo", "职场", 79, ["年终奖", "大厂"]),
        ]

        sentiments = ["positive", "neutral", "negative"]
        velocities = ["rising", "stable", "falling"]

        for i, (title, platform, category, heat, keywords) in enumerate(sample_topics):
            topic = HotTopic(
                topic_id=f"topic_{i:03d}",
                title=title,
                platform=platform,
                heat_score=heat - random.uniform(0, 5),  # 轻微随机波动
                velocity=random.choice(velocities),
                sentiment=random.choice(sentiments),
                keywords=keywords,
                related_topics=[sample_topics[(i + 1) % len(sample_topics)][0][:20]]
            )
            self.topics.append(topic)

    def collect_all(self, limit: int = 50) -> List[HotTopic]:
        """
        从所有平台采集热点话题

        参数:
            limit: 返回数量限制

        返回:
            热点话题列表
        """
        logger.info(f"正在采集所有平台的热点话题...")
        # 模拟采集过程
        time.sleep(0.5)
        logger.info(f"采集完成，共 {len(self.topics)} 个话题")
        return self.topics[:limit]

    def collect_from_platform(self, platform: str, limit: int = 20) -> List[HotTopic]:
        """
        从特定平台采集热点话题

        参数:
            platform: 平台名称
            limit: 返回数量限制

        返回:
            该平台的热点话题列表
        """
        logger.info(f"正在采集 {self.PLATFORMS.get(platform, {}).get('name', platform)} 的热点...")
        time.sleep(0.3)
        platform_topics = [t for t in self.topics if t.platform == platform]
        logger.info(f"采集完成，共 {len(platform_topics)} 个话题")
        return platform_topics[:limit]

    def get_trending(self, top_k: int = 10) -> List[HotTopic]:
        """
        获取热门榜单

        参数:
            top_k: 返回数量

        返回:
            热度最高的话题列表
        """
        sorted_topics = sorted(self.topics, key=lambda x: x.heat_score, reverse=True)
        return sorted_topics[:top_k]

    def analyze_sentiment(self, topic_id: str) -> Dict[str, Any]:
        """
        分析话题情感

        参数:
            topic_id: 话题ID

        返回:
            情感分析结果
        """
        topic = next((t for t in self.topics if t.topic_id == topic_id), None)
        if not topic:
            return {"error": "话题不存在"}

        # 模拟情感分析
        sentiment_scores = {
            "positive": random.uniform(0.6, 0.9),
            "neutral": random.uniform(0.4, 0.6),
            "negative": random.uniform(0.1, 0.4)
        }

        return {
            "topic_id": topic_id,
            "title": topic.title,
            "overall_sentiment": topic.sentiment,
            "scores": {
                "positive": sentiment_scores["positive"],
                "neutral": sentiment_scores["neutral"],
                "negative": sentiment_scores["negative"]
            },
            "emotions": {
                "joy": random.uniform(0.1, 0.5),
                "anger": random.uniform(0.0, 0.3),
                "anxiety": random.uniform(0.1, 0.4),
                "hope": random.uniform(0.3, 0.7)
            }
        }

    def predict_trends(self, hours_ahead: int = 24) -> List[Dict[str, Any]]:
        """
        预测趋势走向

        参数:
            hours_ahead: 预测时长（小时）

        返回:
            趋势预测列表
        """
        logger.info(f"正在预测未来 {hours_ahead} 小时的趋势...")

        # 按关键词分组
        keyword_counts = defaultdict(float)
        for topic in self.topics:
            for keyword in topic.keywords:
                keyword_counts[keyword] += topic.heat_score

        # 排序并生成预测
        predictions = []
        for keyword, score in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            trend_prob = min(0.95, score / 100 + random.uniform(-0.1, 0.2))
            predictions.append({
                "keyword": keyword,
                "current_score": score,
                "prediction": "rising" if trend_prob > 0.6 else ("stable" if trend_prob > 0.4 else "falling"),
                "probability": round(trend_prob, 2),
                "hours_ahead": hours_ahead
            })

        return predictions

    def build_knowledge_graph(self, topics: List[HotTopic]) -> Dict[str, Any]:
        """
        从热点话题构建知识图谱

        参数:
            topics: 话题列表

        返回:
            知识图谱数据
        """
        logger.info(f"正在从 {len(topics)} 个话题构建知识图谱...")

        nodes = []
        edges = []
        keyword_entities = defaultdict(list)

        # 创建话题节点
        for topic in topics:
            nodes.append({
                "id": topic.topic_id,
                "type": "topic",
                "name": topic.title[:30],
                "attributes": {
                    "platform": topic.platform,
                    "heat_score": topic.heat_score,
                    "sentiment": topic.sentiment
                }
            })

            # 记录关键词
            for keyword in topic.keywords:
                keyword_entities[keyword].append(topic.topic_id)

        # 创建关键词节点和边
        keyword_id = 0
        for keyword, topic_ids in keyword_entities.items():
            keyword_node_id = f"keyword_{keyword_id:03d}"
            keyword_id += 1

            nodes.append({
                "id": keyword_node_id,
                "type": "keyword",
                "name": keyword,
                "attributes": {
                    "topic_count": len(topic_ids)
                }
            })

            # 创建边
            for topic_id in topic_ids:
                edges.append({
                    "source": topic_id,
                    "target": keyword_node_id,
                    "relationship": "has_keyword",
                    "weight": 1.0
                })

        # 按平台分组创建边
        platform_groups = defaultdict(list)
        for topic in topics:
            platform_groups[topic.platform].append(topic.topic_id)

        for platform, topic_ids in platform_groups.items():
            if len(topic_ids) > 1:
                for i in range(len(topic_ids) - 1):
                    edges.append({
                        "source": topic_ids[i],
                        "target": topic_ids[i + 1],
                        "relationship": "same_platform",
                        "weight": 0.5
                    })

        graph = {
            "graph_id": f"hot_topic_kg_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "nodes": nodes,
            "edges": edges,
            "statistics": {
                "topic_count": len(topics),
                "keyword_count": len(keyword_entities),
                "edge_count": len(edges),
                "platforms": list(set(t.platform for t in topics))
            }
        }

        logger.info(f"知识图谱构建完成: {len(nodes)} 节点, {len(edges)} 边")
        return graph

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        返回:
            统计信息字典
        """
        platform_stats = defaultdict(lambda: {"count": 0, "avg_heat": 0})
        sentiment_stats = defaultdict(int)

        for topic in self.topics:
            platform_stats[topic.platform]["count"] += 1
            platform_stats[topic.platform]["avg_heat"] += topic.heat_score
            sentiment_stats[topic.sentiment] += 1

        # 计算平均值
        for platform in platform_stats:
            if platform_stats[platform]["count"] > 0:
                platform_stats[platform]["avg_heat"] /= platform_stats[platform]["count"]

        return {
            "total_topics": len(self.topics),
            "platforms": dict(platform_stats),
            "sentiments": dict(sentiment_stats),
            "velocity_distribution": {
                "rising": sum(1 for t in self.topics if t.velocity == "rising"),
                "stable": sum(1 for t in self.topics if t.velocity == "stable"),
                "falling": sum(1 for t in self.topics if t.velocity == "falling")
            }
        }


def demo():
    """演示"""
    print("=" * 80)
    print("Hot Topic Agent Skill 演示")
    print("=" * 80)

    # 创建Agent
    agent = HotTopicAgent()

    # 1. 采集所有热点
    print("\n[1/5] 采集热点话题...")
    topics = agent.collect_all(limit=15)
    print(f"  采集到 {len(topics)} 个热点话题")

    # 2. 获取热门榜单
    print("\n[2/5] 热门榜单 TOP 10")
    trending = agent.get_trending(top_k=10)
    platform_names = {
        "weibo": "微博", "zhihu": "知乎", "douyin": "抖音",
        "bilibili": "B站", "twitter": "Twitter", "hackernews": "HN",
        "reddit": "Reddit", "xiaohongshu": "小红书"
    }

    print(f"  {'排名':<4} {'平台':<8} {'热度':<8} {'趋势':<10} {'标题'}")
    print("  " + "-" * 70)
    for i, topic in enumerate(trending, 1):
        platform = platform_names.get(topic.platform, topic.platform)
        emoji = "📈" if topic.velocity == "rising" else ("📊" if topic.velocity == "stable" else "📉")
        print(f"  {i:<4} {platform:<8} {topic.heat_score:<8.1f} {emoji} {topic.velocity:<8} {topic.title[:25]}...")

    # 3. 情感分析示例
    print("\n[3/5] 情感分析示例")
    if topics:
        sample_topic = topics[0]
        sentiment = agent.analyze_sentiment(sample_topic.topic_id)
        print(f"  话题: {sample_topic.title[:40]}...")
        print(f"  总体情感: {sentiment['overall_sentiment']}")
        print(f"  情感分布:")
        print(f"    积极: {sentiment['scores']['positive']:.2%}")
        print(f"    中性: {sentiment['scores']['neutral']:.2%}")
        print(f"    消极: {sentiment['scores']['negative']:.2%}")

    # 4. 趋势预测
    print("\n[4/5] 趋势预测")
    predictions = agent.predict_trends(hours_ahead=24)
    print(f"  {'关键词':<15} {'当前热度':<12} {'预测趋势':<12} {'概率':<8}")
    print("  " + "-" * 50)
    for pred in predictions[:5]:
        emoji = "📈" if pred["prediction"] == "rising" else ("📊" if pred["prediction"] == "stable" else "📉")
        print(f"  {pred['keyword']:<15} {pred['current_score']:<12.1f} {emoji} {pred['prediction']:<10} {pred['probability']:.0%}")

    # 5. 知识图谱
    print("\n[5/5] 知识图谱构建")
    graph = agent.build_knowledge_graph(topics)
    print(f"  节点数: {len(graph['nodes'])}")
    print(f"  边数: {len(graph['edges'])}")
    print(f"  平台: {', '.join(graph['statistics']['platforms'])}")

    # 统计信息
    print("\n" + "=" * 80)
    stats = agent.get_statistics()
    print("\n📊 统计概览")
    print(f"  总话题数: {stats['total_topics']}")
    print(f"\n  平台分布:")
    for platform, data in stats['platforms'].items():
        name = platform_names.get(platform, platform)
        print(f"    {name}: {data['count']} 个 (平均热度 {data['avg_heat']:.1f})")
    print(f"\n  情感分布:")
    for sentiment, count in stats['sentiments'].items():
        print(f"    {sentiment}: {count} 个")

    print("\n" + "=" * 80)
    print("✅ 演示完成！")
    print("=" * 80)


if __name__ == "__main__":
    demo()
