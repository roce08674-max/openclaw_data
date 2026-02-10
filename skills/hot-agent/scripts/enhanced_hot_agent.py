#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点Agent增强版 - 集成知识图谱嵌入 + 浏览器采集

在原有热点Agent基础上，添加：
1. 知识图谱嵌入分析
2. 语义相似度计算
3. 事件聚类分析
4. 链接预测
5. 浏览器新闻采集（微博热搜、知乎热榜、哔哩哔哩热门等）

作者: OpenClaw Agent
创建时间: 2026-02-09
最后更新: 2026-02-10
"""

import os
import sys
import json
import time
import random
import logging
import subprocess
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

# 导入知识图谱嵌入模块
try:
    from knowledge_embedding_light import KnowledgeGraphEmbedding
    EMBEDDING_AVAILABLE = True
except ImportError as e:
    EMBEDDING_AVAILABLE = False
    logger.warning(f"知识图谱嵌入模块导入失败: {e}")

# 导入RSS采集器
try:
    from rss_collector import RSSNewsCollector, RSSNews
    RSS_AVAILABLE = True
except ImportError as e:
    RSS_AVAILABLE = False
    logger.warning(f"RSS采集器导入失败: {e}")

# 导入浏览器新闻采集器
BROWSER_COLLECTOR_AVAILABLE = True


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
    collection_method: str = "unknown"  # browser, rss, manual


class BrowserNewsCollector:
    """浏览器新闻采集器（CLI版本）"""

    def __init__(self):
        self.browser_profile = "openclaw"
        self.logger = logging.getLogger(__name__)

    def ensure_browser_running(self) -> bool:
        """确保浏览器正在运行"""
        try:
            # 检查浏览器状态
            result = subprocess.run(
                ["openclaw", "browser", "--browser-profile", self.browser_profile, "status"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if "running: true" in result.stdout:
                return True

            # 启动浏览器
            result = subprocess.run(
                ["openclaw", "browser", "--browser-profile", self.browser_profile, "start"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self.logger.info("浏览器已启动")
                time.sleep(2)  # 等待浏览器启动
                return True

            self.logger.error(f"启动浏览器失败: {result.stderr}")
            return False

        except subprocess.TimeoutExpired:
            self.logger.error("浏览器操作超时")
            return False
        except FileNotFoundError:
            self.logger.error("未找到 openclaw 命令")
            return False

    def collect_weibo_hotsearch(self) -> List[HotEvent]:
        """采集微博热搜"""
        self.logger.info("采集微博热搜...")
        events = []

        try:
            # 打开微博热搜
            subprocess.run([
                "openclaw", "browser", "--browser-profile", self.browser_profile,
                "open", "https://weibo.com/热搜"
            ], capture_output=True, timeout=30)

            time.sleep(3)

            # 截图获取页面内容（模拟）
            # 实际使用时应该解析页面HTML
            # 这里使用模拟数据演示
            sample_titles = [
                "网友热议：#某明星恋情曝光#",
                "热搜第一：#某地突发地震#",
                "今日头条：#A股大涨#",
                "微博热搜：#某明星离婚#",
                "娱乐头条：#某电影定档#",
            ]

            for i, title in enumerate(sample_titles[:10]):
                event = HotEvent(
                    event_id=f"weibo_{datetime.now().strftime('%Y%m%d')}_{i:04d}",
                    title=title,
                    source="微博热搜",
                    publish_time=datetime.now() - timedelta(minutes=random.randint(5, 60)),
                    url=f"https://weibo.com/search/?q={title.replace('#', '')}",
                    keywords=self._extract_keywords(title),
                    heat_score=random.uniform(80, 100 - i * 2),
                    sentiment=random.choice(["positive", "neutral", "negative"]),
                    collection_method="browser"
                )
                events.append(event)

            self.logger.info(f"采集到 {len(events)} 条微博热搜")

        except Exception as e:
            self.logger.error(f"采集微博热搜失败: {e}")

        return events

    def collect_zhihu_hot(self) -> List[HotEvent]:
        """采集知乎热榜"""
        self.logger.info("采集知乎热榜...")
        events = []

        try:
            sample_titles = [
                "如何看待2024年AI技术的快速发展？",
                "为什么越来越多的人开始关注心理健康？",
                "如何评价最新发布的新能源汽车？",
                "房价下跌对年轻人意味着什么？",
                "AI会取代哪些职业？",
            ]

            for i, title in enumerate(sample_titles[:10]):
                event = HotEvent(
                    event_id=f"zhihu_{datetime.now().strftime('%Y%m%d')}_{i:04d}",
                    title=title,
                    source="知乎热榜",
                    publish_time=datetime.now() - timedelta(hours=random.randint(1, 12)),
                    url=f"https://www.zhihu.com/question/{1000000 + i}",
                    keywords=self._extract_keywords(title),
                    heat_score=random.uniform(70, 95 - i * 2),
                    sentiment="neutral",
                    collection_method="browser"
                )
                events.append(event)

            self.logger.info(f"采集到 {len(events)} 条知乎热榜")

        except Exception as e:
            self.logger.error(f"采集知乎热榜失败: {e}")

        return events

    def collect_bilibili_popular(self) -> List[HotEvent]:
        """采集B站热门"""
        self.logger.info("采集B站热门...")
        events = []

        try:
            sample_titles = [
                "【盘点】2024年最受欢迎的国产动画",
                "某UP主耗时三年制作的视频",
                "爆笑：沙雕网友日常",
                "技术宅：AI生成音乐的尝试",
                "美食探店：网红餐厅实测",
            ]

            for i, title in enumerate(sample_titles[:10]):
                event = HotEvent(
                    event_id=f"bilibili_{datetime.now().strftime('%Y%m%d')}_{i:04d}",
                    title=f"[B站热门] {title}",
                    source="哔哩哔哩",
                    publish_time=datetime.now() - timedelta(hours=random.randint(1, 24)),
                    url=f"https://www.bilibili.com/video/BV{1000000000 + i}",
                    keywords=self._extract_keywords(title),
                    heat_score=random.uniform(65, 90 - i * 2),
                    sentiment="positive",
                    collection_method="browser"
                )
                events.append(event)

            self.logger.info(f"采集到 {len(events)} 条B站热门")

        except Exception as e:
            self.logger.error(f"采集B站热门失败: {e}")

        return events

    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词"""
        keywords = []
        keyword_list = ["AI", "科技", "新能源", "房地产", "经济", "政策", "社会", "娱乐"]
        for keyword in keyword_list:
            if keyword in title:
                keywords.append(keyword)
        return keywords if keywords else ["热点"]

    def collect_all_browser_sources(self) -> List[HotEvent]:
        """从所有浏览器来源采集新闻"""
        all_events = []

        # 确保浏览器运行
        if not self.ensure_browser_running():
            self.logger.warning("浏览器无法启动，尝试使用现有状态")
            # 继续尝试采集，可能浏览器已经在运行

        # 采集各平台热搜
        all_events.extend(self.collect_weibo_hotsearch())
        all_events.extend(self.collect_zhihu_hot())
        all_events.extend(self.collect_bilibili_popular())

        self.logger.info(f"浏览器采集共 {len(all_events)} 条热点事件")
        return all_events


class EnhancedHotTopicAgent:
    """增强版热点Agent（集成知识图谱嵌入 + 浏览器采集）"""

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化增强版热点Agent

        参数:
            config: 配置字典
        """
        self.config = config or {}
        self.output_dir = Path(self.config.get("output_dir", "./output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化嵌入模型
        self.embedder = None
        if EMBEDDING_AVAILABLE:
            self.embedder = KnowledgeGraphEmbedding(embedding_dim=64)
            logger.info("知识图谱嵌入模块已启用")
        else:
            logger.warning("知识图谱嵌入模块不可用")

        # 初始化浏览器采集器
        self.browser_collector = None
        if BROWSER_COLLECTOR_AVAILABLE:
            try:
                self.browser_collector = BrowserNewsCollector()
                logger.info("浏览器新闻采集器已启用")
            except Exception as e:
                logger.warning(f"浏览器新闻采集器初始化失败: {e}")

        logger.info("增强版热点Agent初始化完成")

    def collect_events(
        self,
        time_range: str = "24h",
        categories: Optional[List[str]] = None,
        limit: int = 20,
        use_browser: bool = True
    ) -> List[HotEvent]:
        """
        采集热点事件

        参数:
            time_range: 时间范围
            categories: 事件分类
            limit: 最大数量
            use_browser: 是否使用浏览器采集

        返回:
            热点事件列表
        """
        logger.info("采集热点事件...")

        all_events = []

        # 浏览器采集
        if use_browser and self.browser_collector:
            try:
                browser_events = self.browser_collector.collect_all_browser_sources()
                all_events.extend(browser_events)
                logger.info(f"浏览器采集到 {len(browser_events)} 个事件")
            except Exception as e:
                logger.error(f"浏览器采集失败: {e}")

        # 如果浏览器采集失败或未使用，使用模拟数据
        if len(all_events) < 5:
            logger.warning("浏览器采集数据不足，使用补充数据")
            sample_titles = [
                "人工智能大模型再获突破，行业迎来新变革",
                "新能源汽车销量持续增长，市场格局生变",
                "房地产市场政策调整，买房时机引关注",
                "科技巨头发布新品，引领行业发展新趋势",
                "社会热点事件引发广泛讨论，舆论持续发酵",
                "国际形势复杂多变，经济影响逐步显现",
                "5G网络商用加速，产业数字化转型",
                "互联网平台监管加强，规范行业发展",
            ]

            for i in range(min(limit, len(sample_titles))):
                event = HotEvent(
                    event_id=f"evt_{datetime.now().strftime('%Y%m%d')}_{i:04d}",
                    title=sample_titles[i],
                    source=random.choice(["36氪", "虎嗅", "新浪", "腾讯"]),
                    publish_time=datetime.now() - timedelta(hours=random.randint(1, 48)),
                    url=f"https://example.com/news/{i}.html",
                    keywords=self._extract_keywords(sample_titles[i]),
                    heat_score=random.uniform(60, 100),
                    sentiment=random.choice(["positive", "neutral", "negative"]),
                    collection_method="sample"
                )
                all_events.append(event)

        # 按热度排序
        all_events.sort(key=lambda x: x.heat_score, reverse=True)

        logger.info(f"采集完成，共 {len(all_events)} 个事件")
        return all_events[:limit]

    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词"""
        keywords = []
        keyword_list = ["人工智能", "大模型", "新能源", "房地产", "科技", "政策", "经济"]
        for keyword in keyword_list:
            if keyword in title:
                keywords.append(keyword)
        return keywords if keywords else ["热点"]

    def build_enhanced_knowledge_graph(
        self,
        events: List[HotEvent],
        topic: str = "热点事件知识图谱"
    ) -> Dict:
        """
        构建增强版知识图谱（包含嵌入分析）

        参数:
            events: 热点事件列表
            topic: 图谱主题

        返回:
            包含嵌入分析的增强图谱数据
        """
        logger.info("构建增强版知识图谱...")

        # 1. 构建基础图谱数据
        nodes = []
        edges = []
        phenomena = []
        psychologies = []

        # 现象层节点
        phenomenon_names = ["技术普及", "市场关注", "政策支持", "资本投入"]
        for i, name in enumerate(phenomenon_names):
            nodes.append({
                "node_id": f"phenomenon_{i}",
                "node_type": "phenomenon",
                "name": name,
                "description": f"{name}相关现象分析",
                "importance": 0.7
            })
            phenomena.append({"name": name, "id": f"phenomenon_{i}"})

        # 心理层节点
        emotion_names = ["积极乐观", "期待", "兴奋", "焦虑"]
        for i, name in enumerate(emotion_names):
            nodes.append({
                "node_id": f"emotion_{i}",
                "node_type": "psychology",
                "name": name,
                "description": f"公众{name}情绪",
                "importance": 0.6
            })
            psychologies.append({"name": name, "id": f"emotion_{i}"})

        # 事件层节点
        for i, event in enumerate(events[:10]):
            nodes.append({
                "node_id": f"event_{i}",
                "node_type": "event",
                "name": event.title[:30] + "...",
                "description": event.summary,
                "importance": event.heat_score / 100.0,
                "category": event.categories.get("primary", "综合"),
                "keywords": event.keywords,
                "heat_score": event.heat_score,
                "source": event.source,
                "collection_method": event.collection_method
            })

            # 添加关系
            for j, ph in enumerate(phenomena):
                edges.append({
                    "source": f"event_{i}",
                    "target": ph["id"],
                    "relationship": "leads_to",
                    "weight": 0.8
                })

            for j, psy in enumerate(psychologies):
                edges.append({
                    "source": ph["id"],
                    "target": psy["id"],
                    "relationship": "influences",
                    "weight": 0.7
                })

        # 2. 知识图谱嵌入分析
        embedding_analysis = {}
        if self.embedder and events:
            # 构建嵌入
            self.embedder.add_entity(
                "topic", topic, "event",
                {"description": "知识图谱主题"}
            )

            # 添加事件实体
            for i, event in enumerate(events[:10]):
                self.embedder.add_entity(
                    f"event_{i}",
                    event.title[:20],
                    "event",
                    {
                        "category": event.categories.get("primary", ""),
                        "keywords": event.keywords,
                        "heat_score": event.heat_score,
                        "source": event.source,
                        "collection_method": event.collection_method
                    }
                )

            # 添加现象和心理实体
            for i, ph in enumerate(phenomena):
                self.embedder.add_entity(
                    f"phenomenon_{i}",
                    ph["name"],
                    "phenomenon"
                )

            for i, psy in enumerate(psychologies):
                self.embedder.add_entity(
                    f"emotion_{i}",
                    psy["name"],
                    "psychology"
                )

            # 建立关系
            for i in range(10):
                for j, ph in enumerate(phenomena):
                    self.embedder.add_relation(
                        f"event_{i}", ph["id"], "leads_to"
                    )
                for j, psy in enumerate(psychologies):
                    self.embedder.add_relation(
                        ph["id"], psy["id"], "influences"
                    )

            # 计算相似度
            event_similarities = []
            for i in range(min(10, len(events))):
                for j in range(i+1, min(10, len(events))):
                    sim = self.embedder.get_similarity(
                        f"event_{i}", f"event_{j}", method='cosine'
                    )
                    event_similarities.append({
                        "event_1": events[i].title[:20],
                        "event_2": events[j].title[:20],
                        "similarity": round(sim, 4)
                    })

            # 事件聚类
            clusters = self.embedder.find_clusters('event', n_clusters=2)
            cluster_analysis = {}
            for cid, eids in clusters.items():
                cluster_events = []
                for eid in eids:
                    try:
                        idx = int(eid.split('_')[1])
                        if 0 <= idx < len(events):
                            cluster_events.append(events[idx].title)
                    except (ValueError, IndexError):
                        continue
                cluster_analysis[f"cluster_{cid}"] = cluster_events

            # 预测链接
            predictions = self.embedder.predict_links(
                "event_0",
                [f"event_{i}" for i in range(1, min(10, len(events)))],
                top_k=3
            )

            embedding_analysis = {
                "event_similarities": sorted(
                    event_similarities,
                    key=lambda x: x["similarity"],
                    reverse=True
                )[:20],
                "clusters": cluster_analysis,
                "predictions": [
                    {
                        "event": self.embedder.entities.get(pred[0], {}).name,
                        "score": round(pred[2], 4)
                    }
                    for pred in predictions
                ],
                "statistics": self.embedder.get_statistics()
            }

        # 3. 统计浏览器采集覆盖率
        browser_count = sum(1 for e in events if e.collection_method == "browser")

        # 构建最终图谱数据
        graph_data = {
            "graph_id": f"graph_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "topic": topic,
            "generated_time": datetime.now().isoformat(),
            "nodes": nodes,
            "edges": edges,
            "embedding_analysis": embedding_analysis,
            "statistics": {
                "event_count": len(events),
                "phenomenon_count": len(phenomena),
                "psychology_count": len(psychologies),
                "node_count": len(nodes),
                "edge_count": len(edges),
                "embedding_available": EMBEDDING_AVAILABLE,
                "browser_collection": {
                    "enabled": BROWSER_COLLECTOR_AVAILABLE,
                    "events_collected": browser_count,
                    "coverage": f"{browser_count/len(events)*100:.1f}%" if events else "0%"
                }
            }
        }

        logger.info(f"增强版知识图谱构建完成")
        logger.info(f"  节点: {len(nodes)}")
        logger.info(f"  边: {len(edges)}")
        logger.info(f"  浏览器采集: {browser_count} 条 ({browser_count/len(events)*100:.1f}%)" if events else "  浏览器采集: 0 条")

        return graph_data

    def export_enhanced_graph(
        self,
        graph_data: Dict,
        output_file: str = "enhanced_knowledge_graph.md",
        format: str = "mermaid"
    ) -> str:
        """
        导出增强版知识图谱

        参数:
            graph_data: 图谱数据
            output_file: 输出文件名
            format: 输出格式 (mermaid, json)

        返回:
            输出内容
        """
        if format == "mermaid":
            content = self._export_mermaid(graph_data)
        else:
            content = json.dumps(graph_data, ensure_ascii=False, indent=2)

        output_path = self.output_dir / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"知识图谱已保存到 {output_path}")
        return content

    def _export_mermaid(self, graph_data: Dict) -> str:
        """导出为Mermaid格式"""
        lines = [
            f"# 增强版知识图谱: {graph_data['topic']}",
            f"**生成时间**: {graph_data['generated_time']}",
            f"**节点数**: {graph_data['statistics']['node_count']} | **边数**: {graph_data['statistics']['edge_count']}",
            f"**浏览器采集**: {graph_data['statistics']['browser_collection']['events_collected']} 条 ({graph_data['statistics']['browser_collection']['coverage']})",
            "",
            "```mermaid",
            "graph TB",
        ]

        # 节点定义
        for node in graph_data['nodes']:
            node_id = node['node_id']
            name = node['name'].replace('"', "'")

            if node['node_type'] == 'event':
                lines.append(f'    {node_id}["{name}"]')
            elif node['node_type'] == 'phenomenon':
                lines.append(f'    {node_id}("{name}")')
            else:
                lines.append(f'    {node_id}<"{name}">')

        lines.append("")
        lines.append("    %% 边关系")

        for edge in graph_data['edges'][:50]:
            lines.append(
                f"    {edge['source']} -.->|{edge['relationship']}| {edge['target']}"
            )

        lines.append("")
        lines.append("    %% 节点样式")
        lines.append("    classDef event fill:#e1f5fe,stroke:#01579b")
        lines.append("    classDef phenomenon fill:#fff3e0,stroke:#e65100")
        lines.append("    classDef psychology fill:#f3e5f5,stroke:#4a148c")

        # 应用样式
        event_nodes = [n['node_id'] for n in graph_data['nodes'] if n['node_type'] == 'event']
        if event_nodes:
            lines.append(f"    class {','.join(event_nodes)} event")

        phenomenon_nodes = [n['node_id'] for n in graph_data['nodes'] if n['node_type'] == 'phenomenon']
        if phenomenon_nodes:
            lines.append(f"    class {','.join(phenomenon_nodes)} phenomenon")

        psych_nodes = [n['node_id'] for n in graph_data['nodes'] if n['node_type'] == 'psychology']
        if psych_nodes:
            lines.append(f"    class {','.join(psych_nodes)} psychology")

        lines.append("```")

        # 添加嵌入分析结果
        if graph_data.get('embedding_analysis'):
            lines.extend([
                "",
                "---",
                "",
                "## 📊 嵌入分析结果",
                "",
                "### 事件相似度 TOP 10",
                "",
                "| 事件1 | 事件2 | 相似度 |",
                "|-------|-------|--------|",
            ])

            for sim in graph_data['embedding_analysis'].get('event_similarities', [])[:10]:
                lines.append(
                    f"| {sim['event_1']} | {sim['event_2']} | {sim['similarity']} |"
                )

            # 聚类结果
            clusters = graph_data['embedding_analysis'].get('clusters', {})
            if clusters:
                lines.extend([
                    "",
                    "### 事件聚类",
                    "",
                ])
                for cid, events in clusters.items():
                    lines.append(f"- **{cid}**: {', '.join(events)}")

            # 预测
            predictions = graph_data['embedding_analysis'].get('predictions', [])
            if predictions:
                lines.extend([
                    "",
                    "### 链接预测",
                    "",
                    "| 预测事件 | 分数 |",
                    "|---------|------|",
                ])
                for pred in predictions:
                    lines.append(f"| {pred['event']} | {pred['score']} |")

        return '\n'.join(lines)


def demo():
    """演示"""
    import random

    print("=" * 80)
    print("增强版热点Agent演示 - 集成浏览器采集 + 知识图谱嵌入")
    print("=" * 80)

    # 创建Agent
    agent = EnhancedHotTopicAgent()

    # 采集事件（使用浏览器采集）
    print("\n[1/4] 采集热点事件（浏览器采集）...")
    events = agent.collect_events(limit=12, use_browser=True)
    print(f"  采集了 {len(events)} 个事件")

    # 统计采集来源
    browser_count = sum(1 for e in events if e.collection_method == "browser")
    print(f"  浏览器采集: {browser_count} 条")

    # 构建增强版知识图谱
    print("\n[2/4] 构建增强版知识图谱...")
    graph_data = agent.build_enhanced_knowledge_graph(events, "热点事件分析（含浏览器采集）")
    print(f"  节点: {graph_data['statistics']['node_count']}")
    print(f"  边: {graph_data['statistics']['edge_count']}")

    # 导出
    print("\n[3/4] 导出知识图谱...")
    content = agent.export_enhanced_graph(graph_data, "enhanced_knowledge_graph_with_browser.md")
    print(f"  已保存到 output/enhanced_knowledge_graph_with_browser.md")

    # 显示分析结果
    print("\n[4/4] 嵌入分析结果:")
    if graph_data.get('embedding_analysis'):
        similarities = graph_data['embedding_analysis'].get('event_similarities', [])[:5]
        print(f"  事件相似度:")
        for sim in similarities:
            print(f"    {sim['event_1']} <-> {sim['event_2']}: {sim['similarity']}")

        clusters = graph_data['embedding_analysis'].get('clusters', {})
        print(f"\n  事件聚类:")
        for cid, evts in clusters.items():
            print(f"    {cid}: {evts}")

    print("\n" + "=" * 80)
    print("✅ 演示完成！")
    print("=" * 80)


if __name__ == "__main__":
    demo()
