#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS新闻采集器 - 热点事件数据来源

基于feedparser的RSS/Atom订阅源解析
支持多分类新闻采集

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

import feedparser
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Generator
from dataclasses import dataclass, field
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RSSNews:
    """RSS新闻条目"""
    news_id: str
    title: str
    link: str
    source: str
    publish_time: datetime
    summary: str
    category: str
    author: str = ""
    keywords: List[str] = field(default_factory=list)
    heat_score: float = 0.0
    sentiment: str = "neutral"

    def __post_init__(self):
        # 从URL提取域名作为备用来源
        if not self.source or self.source == "":
            if "://" in self.link:
                domain = self.link.split("://")[1].split("/")[0]
                self.source = domain


@dataclass
class RSSFeedConfig:
    """RSS订阅源配置"""
    name: str
    url: str
    category: str
    priority: int = 1  # 优先级 (1-10)
    enabled: bool = True


class RSSNewsCollector:
    """RSS新闻采集器"""

    # 默认新闻订阅源配置
    DEFAULT_FEEDS = [
        # 科技新闻
        RSSFeedConfig(
            name="36氪",
            url="https://36kr.com/feed",
            category="科技",
            priority=10
        ),
        RSSFeedConfig(
            name="虎嗅",
            url="https://www.huxiu.com/rss",
            category="科技",
            priority=9
        ),
        RSSFeedConfig(
            name="雷锋网",
            url="https://www.leiphone.com/category/ai.rss",
            category="科技",
            priority=8
        ),
        RSSFeedConfig(
            name="InfoQ",
            url="https://www.infoq.com/feed/",
            category="科技",
            priority=7
        ),
        RSSFeedConfig(
            name="TechCrunch",
            url="https://techcrunch.com/feed/",
            category="科技",
            priority=6
        ),
        RSSFeedConfig(
            name="The Verge",
            url="https://www.theverge.com/rss/index.xml",
            category="科技",
            priority=5
        ),
        
        # 财经新闻
        RSSFeedConfig(
            name="华尔街见闻",
            url="https://wallstreetcn.com/rss",
            category="财经",
            priority=10
        ),
        RSSFeedConfig(
            name="财新",
            url="https://feeds.caixin.com/mobile/finance.xml",
            category="财经",
            priority=8
        ),
        RSSFeedConfig(
            name="第一财经",
            url="https://www.yicai.com/rss/",
            category="财经",
            priority=7
        ),
        RSSFeedConfig(
            name="雪球",
            url="https://xueqiu.com/company/pensionlist?column=chinadaily&type=stock",
            category="财经",
            priority=6
        ),
        
        # 综合/社会新闻
        RSSFeedConfig(
            name="新浪新闻",
            url="https://news.sina.com.cn/rss/",
            category="社会",
            priority=8
        ),
        RSSFeedConfig(
            name="网易新闻",
            url="https://www.163.com/rss/",
            category="社会",
            priority=7
        ),
        RSSFeedConfig(
            name="凤凰网",
            url="https://news.ifeng.com/rss/index.xml",
            category="社会",
            priority=6
        ),
        
        # 国际新闻
        RSSFeedConfig(
            name="BBC World",
            url="http://feeds.bbci.co.uk/news/world/rss.xml",
            category="国际",
            priority=8
        ),
        RSSFeedConfig(
            name="Reuters World",
            url="https://www.reutersagency.com/feed/",
            category="国际",
            priority=7
        ),
    ]

    def __init__(
        self,
        feeds: Optional[List[RSSFeedConfig]] = None,
        cache_dir: str = "./cache/rss",
        request_timeout: int = 30,
        max_workers: int = 5
    ):
        """
        初始化RSS新闻采集器

        参数:
            feeds: RSS订阅源配置列表
            cache_dir: 缓存目录
            request_timeout: 请求超时时间（秒）
            max_workers: 并行采集的最大工作线程数
        """
        self.feeds = feeds or self.DEFAULT_FEEDS
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.request_timeout = request_timeout
        self.max_workers = max_workers
        
        # 从缓存加载已处理的文章ID
        self._load_cache()

    def _load_cache(self):
        """加载缓存"""
        self.processed_ids = set()
        cache_file = self.cache_dir / "processed_ids.txt"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.processed_ids = set(line.strip() for line in f)
                logger.info(f"加载了 {len(self.processed_ids)} 个已处理的文章ID")
            except Exception as e:
                logger.warning(f"加载缓存失败: {e}")
                self.processed_ids = set()

    def _save_cache(self):
        """保存缓存"""
        cache_file = self.cache_dir / "processed_ids.txt"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                for news_id in self.processed_ids:
                    f.write(f"{news_id}\n")
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")

    def _generate_news_id(self, entry) -> str:
        """生成新闻ID"""
        # 优先使用GUID/ID
        if hasattr(entry, 'id') and entry.id:
            return entry.id
        if hasattr(entry, 'link') and entry.link:
            # 使用链接的哈希值作为ID
            return str(hash(entry.link))
        # 使用标题的哈希值
        return str(hash(entry.get('title', '')))

    def _parse_time(self, entry) -> datetime:
        """解析发布时间"""
        # 尝试多种时间格式
        time_formats = [
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%d',
        ]
        
        # 优先使用published_parsed
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        
        # 尝试解析published字段
        if hasattr(entry, 'published') and entry.published:
            for fmt in time_formats:
                try:
                    # 尝试解析
                    if 'GMT' in entry.published:
                        dt = datetime.strptime(entry.published.replace('GMT', '+0000'), '%a, %d %b %Y %H:%M:%S %z')
                        return dt
                    return datetime.strptime(entry.published[:19], fmt)
                except (ValueError, TypeError):
                    continue
        
        # 默认当前时间
        return datetime.now()

    def _extract_keywords(self, title: str, summary: str) -> List[str]:
        """提取关键词"""
        keywords = []
        keyword_patterns = [
            "人工智能", "AI", "大模型", "GPT", "机器学习",
            "新能源", "电动车", "特斯拉", "比亚迪",
            "房地产", "房价", "房贷",
            "股市", "A股", "美股", "加密货币",
            "互联网", "电商", "直播",
            "芯片", "半导体", "5G",
        ]
        
        text = title + " " + summary
        for pattern in keyword_patterns:
            if pattern.lower() in text.lower():
                keywords.append(pattern)
        
        return keywords if keywords else ["热点"]

    def _calculate_heat_score(self, entry) -> float:
        """计算热度分数"""
        score = 50.0  # 基础分数
        
        # 根据发布时间衰减（最近24小时内的新闻加分）
        pub_time = self._parse_time(entry)
        hours_ago = (datetime.now() - pub_time).total_seconds() / 3600
        if hours_ago < 24:
            score += (24 - hours_ago) * 2  # 每小时加分
        elif hours_ago < 72:
            score += (72 - hours_ago) * 0.5
        
        # 简单情感判断（基于标题词汇）
        title_lower = entry.get('title', '').lower()
        positive_words = ['突破', '创新', '增长', '成功', '利好', '大涨']
        negative_words = ['暴跌', '危机', '风险', '警告', '裁员', '下滑']
        
        for word in positive_words:
            if word in title_lower:
                score += 2
        for word in negative_words:
            if word in title_lower:
                score -= 2
        
        return min(100, max(0, score))

    def _parse_feed(self, config: RSSFeedConfig, time_range: str = "24h") -> List[RSSNews]:
        """
        解析单个RSS订阅源

        参数:
            config: RSS订阅源配置
            time_range: 时间范围 (24h, 7d, 30d, 90d)

        返回:
            新闻列表
        """
        logger.info(f"解析订阅源: {config.name} ({config.url})")
        
        try:
            # 解析RSS（feedparser不支持timeout参数，使用urllib单独控制）
            import urllib.request
            import ssl
            
            # 创建SSL上下文（忽略证书验证）
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # 带超时请求
            req = urllib.request.Request(
                config.url,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; HotTopicAgent/1.0)'}
            )
            
            with urllib.request.urlopen(req, context=ssl_context, timeout=self.request_timeout) as response:
                content = response.read().decode('utf-8', errors='ignore')
            
            # 解析内容
            feed = feedparser.parse(content)
            
            # 检查解析结果
            if feed.bozo:
                logger.warning(f"RSS格式异常: {config.name}")
                return []
            
            if not hasattr(feed, 'entries'):
                logger.warning(f"无新闻条目: {config.name}")
                return []
            
            # 计算时间范围
            time_range_map = {
                "24h": 1,
                "7d": 7,
                "30d": 30,
                "90d": 90
            }
            days = time_range_map.get(time_range, 1)
            min_time = datetime.now() - timedelta(days=days)
            
            news_list = []
            for entry in feed.entries[:50]:  # 每个源最多50条
                # 生成ID并检查是否已处理
                news_id = self._generate_news_id(entry)
                if news_id in self.processed_ids:
                    continue
                
                # 检查时间
                pub_time = self._parse_time(entry)
                if pub_time < min_time:
                    continue
                
                # 创建新闻对象
                news = RSSNews(
                    news_id=news_id,
                    title=entry.get('title', '无标题'),
                    link=entry.get('link', ''),
                    source=config.name,
                    publish_time=pub_time,
                    summary=entry.get('summary', '')[:500],  # 截取摘要
                    category=config.category,
                    author=entry.get('author', ''),
                    keywords=self._extract_keywords(
                        entry.get('title', ''),
                        entry.get('summary', '')
                    ),
                    heat_score=self._calculate_heat_score(entry),
                    sentiment="neutral"
                )
                
                news_list.append(news)
                self.processed_ids.add(news_id)
            
            logger.info(f"  从 {config.name} 获取 {len(news_list)} 条新新闻")
            return news_list
            
        except Exception as e:
            logger.error(f"解析失败 {config.name}: {e}")
            return []

    def collect(
        self,
        categories: Optional[List[str]] = None,
        time_range: str = "24h",
        limit: int = 100,
        parallel: bool = True
    ) -> List[RSSNews]:
        """
        采集RSS新闻

        参数:
            categories: 关注的分类列表（None表示所有分类）
            time_range: 时间范围 (24h, 7d, 30d, 90d)
            limit: 采集数量上限
            parallel: 是否并行采集

        返回:
            新闻列表（按时间排序）
        """
        logger.info(f"开始采集RSS新闻...")
        logger.info(f"  时间范围: {time_range}")
        logger.info(f"  分类过滤: {categories or '全部'}")
        logger.info(f"  数量上限: {limit}")
        
        # 过滤订阅源
        enabled_feeds = [
            f for f in self.feeds 
            if f.enabled and 
            (not categories or f.category in categories)
        ]
        
        # 按优先级排序
        enabled_feeds.sort(key=lambda x: x.priority, reverse=True)
        
        # 采集新闻
        all_news = []
        
        if parallel and len(enabled_feeds) > 1:
            # 并行采集
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._parse_feed, feed, time_range): feed 
                    for feed in enabled_feeds
                }
                
                for future in as_completed(futures):
                    try:
                        news_list = future.result()
                        all_news.extend(news_list)
                    except Exception as e:
                        logger.error(f"并行采集失败: {e}")
        else:
            # 顺序采集
            for feed in enabled_feeds:
                news_list = self._parse_feed(feed, time_range)
                all_news.extend(news_list)
        
        # 按时间排序（最新的在前）
        all_news.sort(key=lambda x: x.publish_time, reverse=True)
        
        # 限制数量
        all_news = all_news[:limit]
        
        # 保存缓存
        self._save_cache()
        
        logger.info(f"采集完成！共获取 {len(all_news)} 条新闻")
        
        # 统计
        category_stats = {}
        for news in all_news:
            if news.category not in category_stats:
                category_stats[news.category] = 0
            category_stats[news.category] += 1
        
        for cat, count in sorted(category_stats.items(), key=lambda x: -x[1]):
            logger.info(f"  {cat}: {count} 条")
        
        return all_news

    def get_feed_stats(self) -> Dict[str, Any]:
        """获取订阅源统计信息"""
        stats = {
            "total_feeds": len(self.feeds),
            "enabled_feeds": len([f for f in self.feeds if f.enabled]),
            "category_counts": {},
            "sources": []
        }
        
        for feed in self.feeds:
            if feed.category not in stats["category_counts"]:
                stats["category_counts"][feed.category] = 0
            stats["category_counts"][feed.category] += 1
            
            stats["sources"].append({
                "name": feed.name,
                "category": feed.category,
                "url": feed.url,
                "enabled": feed.enabled,
                "priority": feed.priority
            })
        
        return stats


def main():
    """主函数 - 测试采集"""
    print("=" * 60)
    print("RSS新闻采集器测试")
    print("=" * 60)
    
    # 创建采集器
    collector = RSSNewsCollector()
    
    # 获取订阅源统计
    stats = collector.get_feed_stats()
    print(f"\n订阅源统计:")
    print(f"  总数: {stats['total_feeds']}")
    print(f"  启用: {stats['enabled_feeds']}")
    print(f"\n分类分布:")
    for cat, count in stats["category_counts"].items():
        print(f"  {cat}: {count} 个订阅源")
    
    # 采集新闻
    print(f"\n开始采集新闻...")
    news_list = collector.collect(
        categories=["科技", "财经", "社会"],
        time_range="24h",
        limit=20
    )
    
    print(f"\n采集结果:")
    print(f"  总数: {len(news_list)} 条")
    
    # 显示前5条
    print(f"\n最新5条新闻:")
    for i, news in enumerate(news_list[:5], 1):
        print(f"\n{i}. [{news.category}] {news.title}")
        print(f"   来源: {news.source}")
        print(f"   时间: {news.publish_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   热度: {news.heat_score:.1f}")
        print(f"   链接: {news.link[:80]}...")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
