#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器新闻采集器 - Browser-based News Collector

使用 OpenClaw 浏览器工具从新闻网站直接采集热点信息
支持多种热点榜单：微博热搜、知乎热榜、哔哩哔哩热门等

作者: OpenClaw Agent
创建时间: 2026-02-10
"""

import os
import sys
import json
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class BrowserNews:
    """浏览器采集的新闻"""
    title: str
    url: str
    source: str
    hot_level: Optional[str] = None  # 热度等级
    rank: Optional[int] = None  # 排名
    publish_time: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    raw_data: Dict = field(default_factory=dict)


class BaseNewsExtractor(ABC):
    """新闻提取器基类"""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.driver = None

    @abstractmethod
    def get_source_url(self) -> str:
        """获取源URL"""
        pass

    @abstractmethod
    def extract_news(self, page_content: Dict) -> List[BrowserNews]:
        """从页面内容提取新闻"""
        pass

    def get_hot_level(self, rank: int) -> str:
        """根据排名返回热度等级"""
        if rank <= 3:
            return "🔥🔥🔥"
        elif rank <= 10:
            return "🔥🔥"
        elif rank <= 20:
            return "🔥"
        else:
            return "📈"


class WeiboExtractor(BaseNewsExtractor):
    """微博热搜提取器"""

    def __init__(self):
        super().__init__("微博")

    def get_source_url(self) -> str:
        return "https://weibo.com/热搜"

    def extract_news(self, page_content: Dict) -> List[BrowserNews]:
        news_list = []

        # 从页面内容中提取
        if 'links' in page_content:
            for i, link in enumerate(page_content['links'][:20]):
                title = link.get('text', '')
                url = link.get('href', '')

                if title and url and '微博' not in title:
                    news = BrowserNews(
                        title=title[:50],
                        url=url,
                        source="微博热搜",
                        rank=i + 1,
                        hot_level=self.get_hot_level(i + 1),
                        category="综合"
                    )
                    news_list.append(news)

        return news_list


class ZhihuExtractor(BaseNewsExtractor):
    """知乎热榜提取器"""

    def __init__(self):
        super().__init__("知乎")

    def get_source_url(self) -> str:
        return "https://www.zhihu.com/hot"

    def extract_news(self, page_content: Dict) -> List[BrowserNews]:
        news_list = []

        # 从页面元素中提取
        if 'headings' in page_content:
            for i, heading in enumerate(page_content['headings'][:20]):
                title = heading.get('text', '')
                url = heading.get('href', '')

                if title and url:
                    news = BrowserNews(
                        title=title[:80],
                        url=url,
                        source="知乎热榜",
                        rank=i + 1,
                        hot_level=self.get_hot_level(i + 1),
                        category="综合"
                    )
                    news_list.append(news)

        return news_list


class BilibiliExtractor(BaseNewsExtractor):
    """哔哩哔哩热门提取器"""

    def __init__(self):
        super().__init__("哔哩哔哩")

    def get_source_url(self) -> str:
        return "https://www.bilibili.com/v/rank/all"

    def extract_news(self, page_content: Dict) -> List[BrowserNews]:
        news_list = []

        # 从视频列表提取
        if 'items' in page_content:
            for i, item in enumerate(page_content['items'][:20]):
                title = item.get('title', '')
                url = item.get('link', '')

                if title and url:
                    views = item.get('views', '')
                    news = BrowserNews(
                        title=f"[B站] {title[:50]}",
                        url=url,
                        source="哔哩哔哩",
                        rank=i + 1,
                        hot_level=f"👀 {views}" if views else "📺",
                        category="视频"
                    )
                    news_list.append(news)

        return news_list


class DoubanExtractor(BaseNewsExtractor):
    """豆瓣热门提取器"""

    def __init__(self):
        super().__init__("豆瓣")

    def get_source_url(self) -> str:
        return "https://movie.douban.com/"

    def extract_news(self, page_content: Dict) -> List[BrowserNews]:
        news_list = []

        if 'movies' in page_content:
            for i, movie in enumerate(page_content['movies'][:10]):
                title = movie.get('title', '')
                url = movie.get('url', '')
                rating = movie.get('rating', '')

                if title and url:
                    news = BrowserNews(
                        title=f"[电影] {title}",
                        url=url,
                        source="豆瓣",
                        rank=i + 1,
                        hot_level=f"⭐ {rating}" if rating else "🎬",
                        category="影视"
                    )
                    news_list.append(news)

        return news_list


class BrowserNewsCollector:
    """浏览器新闻采集器"""

    def __init__(self):
        self.extractors = {
            'weibo': WeiboExtractor(),
            'zhihu': ZhihuExtractor(),
            'bilibili': BilibiliExtractor(),
            'douban': DoubanExtractor(),
        }
        self.logger = logging.getLogger(__name__)

    def collect_from_source(self, source: str, browser_output: Dict) -> List[BrowserNews]:
        """从特定来源采集新闻"""
        if source not in self.extractors:
            self.logger.warning(f"未知的新闻源: {source}")
            return []

        extractor = self.extractors[source]
        try:
            news_list = extractor.extract_news(browser_output)
            self.logger.info(f"从 {source} 采集到 {len(news_list)} 条新闻")
            return news_list
        except Exception as e:
            self.logger.error(f"从 {source} 采集失败: {e}")
            return []

    def collect_all_sources(self, browser_outputs: Dict[str, Dict]) -> List[BrowserNews]:
        """从多个来源采集新闻"""
        all_news = []

        for source, output in browser_outputs.items():
            if output:
                news = self.collect_from_source(source, output)
                all_news.extend(news)

        self.logger.info(f"共采集到 {len(all_news)} 条新闻")
        return all_news

    def merge_with_rss(self, browser_news: List[BrowserNews], rss_news: List) -> List[Dict]:
        """合并浏览器采集和RSS采集的新闻"""
        merged = []

        # 添加浏览器新闻
        for news in browser_news:
            merged.append({
                'title': news.title,
                'url': news.url,
                'source': news.source,
                'hot_level': news.hot_level,
                'rank': news.rank,
                'category': news.category,
                'collection_method': 'browser'
            })

        # 添加RSS新闻
        for news in rss_news:
            merged.append({
                'title': getattr(news, 'title', str(news)),
                'url': getattr(news, 'url', ''),
                'source': getattr(news, 'source', 'RSS'),
                'hot_level': getattr(news, 'heat_score', 0),
                'rank': None,
                'category': getattr(news, 'category', '综合'),
                'collection_method': 'rss'
            })

        return merged


def demo():
    """演示"""
    print("=" * 70)
    print("浏览器新闻采集器演示")
    print("=" * 70)

    collector = BrowserNewsCollector()

    print("\n支持的新闻源:")
    for name in collector.extractors:
        print(f"  - {name}")

    print("\n注意: 实际使用时需要先通过 browser 工具访问网页")
    print("然后使用 snapshot 获取页面结构，再提取新闻")

    print("\n使用流程:")
    print("  1. browser action=start profile=openclaw")
    print("  2. browser action=open targetUrl=<新闻源URL>")
    print("  3. browser action=snapshot")
    print("  4. 使用 BrowserNewsCollector 解析结果")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo()
