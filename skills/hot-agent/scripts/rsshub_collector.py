#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSSHub热点新闻采集器

使用RSSHub采集社交媒体热点新闻
然后传递给热点Agent进行深度分析

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

import sys
import os
import json
import time
import logging
import urllib.request
import urllib.parse
import ssl
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from html import unescape

# 添加scripts目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsshub_feeds import RSSHubFeedManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RSSNews:
    """RSS新闻"""
    news_id: str
    title: str
    link: str
    source: str
    platform: str
    publish_time: datetime
    summary: str
    category: str
    keywords: List[str] = field(default_factory=list)
    heat_score: float = 0.0


class RSSHubCollector:
    """RSSHub采集器"""

    def __init__(self, base_url: str = "https://rsshub.app"):
        self.base_url = base_url
        self.feed_manager = RSSHubFeedManager(base_url)
        self.cache_dir = "./cache/rsshub"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _fetch_feed(self, url: str, timeout: int = 30) -> Optional[str]:
        """获取RSS内容"""
        try:
            # 构建请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; HotTopicAgent/1.0)'
            }
            req = urllib.request.Request(url, headers=headers)

            # SSL上下文
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # 发送请求
            with urllib.request.urlopen(req, context=ssl_context, timeout=timeout) as response:
                content = response.read().decode('utf-8', errors='ignore')
                return content

        except Exception as e:
            logger.warning(f"获取失败: {url} - {e}")
            return None

    def _parse_rss_item(self, item: Dict, source: str, platform: str) -> Optional[RSSNews]:
        """解析RSS条目"""
        try:
            # 提取标题
            title = ""
            if 'title' in item:
                title = unescape(str(item['title']))

            # 提取链接
            link = ""
            if 'link' in item:
                link = str(item['link'])
            elif 'id' in item:
                link = str(item['id'])

            # 提取发布时间
            pub_time = datetime.now()
            if 'pubDate' in item:
                try:
                    pub_str = str(item['pubDate'])
                    # 简单解析
                    if ' GMT' in pub_str:
                        pub_time = datetime.strptime(pub_str, "%a, %d %b %Y %H:%M:%S GMT")
                except:
                    pass

            # 提取摘要
            summary = ""
            if 'summary' in item:
                summary = unescape(str(item['summary']))
            elif 'description' in item:
                summary = unescape(str(item['description']))
            elif 'content' in item:
                content = item['content']
                if isinstance(content, list) and len(content) > 0:
                    summary = unescape(str(content[0].get('value', '')))

            # 提取关键词
            keywords = []
            if 'categories' in item:
                for cat in item['categories']:
                    keywords.append(str(cat))

            # 计算热度分数
            heat_score = self._calculate_heat_score(title, pub_time)

            # 生成ID
            news_id = str(hash(link or title))[:16]

            return RSSNews(
                news_id=news_id,
                title=title[:200],  # 截断过长标题
                link=link,
                source=source,
                platform=platform,
                publish_time=pub_time,
                summary=summary[:500],
                category=self._categorize(title, summary),
                keywords=keywords[:5],
                heat_score=heat_score
            )

        except Exception as e:
            logger.warning(f"解析RSS条目失败: {e}")
            return None

    def _calculate_heat_score(self, title: str, pub_time: datetime) -> float:
        """计算热度分数"""
        score = 50.0  # 基础分数

        # 时间衰减（最近24小时加分）
        hours_ago = (datetime.now() - pub_time).total_seconds() / 3600
        if hours_ago < 24:
            score += (24 - hours_ago) * 2

        # 标题热度词
        hot_words = ['热搜', '爆', '第一', '最新', '重磅', '官宣', '突破', '震惊']
        for word in hot_words:
            if word in title:
                score += 3

        return min(100, max(0, score))

    def _categorize(self, title: str, summary: str) -> str:
        """分类"""
        text = (title + " " + summary).lower()

        categories = {
            '科技': ['AI', '人工智能', 'GPT', '科技', '互联网', '数码', '手机', '电脑'],
            '财经': ['股市', '基金', '经济', '金融', '投资', '房价', '商业'],
            '娱乐': ['明星', '综艺', '电影', '音乐', '娱乐圈', '八卦', '偶像'],
            '体育': ['体育', '足球', '篮球', '奥运', '比赛', '运动员', '金牌'],
            '社会': ['社会', '新闻', '热点', '事件', '政策', '民生'],
        }

        for category, keywords in categories.items():
            for kw in keywords:
                if kw.lower() in text:
                    return category

        return '综合'

    def collect(
        self,
        platforms: Optional[List[str]] = None,
        limit_per_feed: int = 5,
        max_feeds: int = 10
    ) -> List[RSSNews]:
        """采集热点新闻"""
        logger.info("开始从RSSHub采集热点新闻...")

        # 获取RSS源
        if platforms:
            feeds = []
            for platform in platforms:
                feeds.extend(self.feed_manager.get_feeds_by_platform(platform))
        else:
            feeds = self.feed_manager.get_priority_feeds(max_feeds)

        logger.info(f"将采集 {len(feeds)} 个RSS源...")

        all_news = []
        processed_urls = set()

        for feed in feeds[:max_feeds]:
            try:
                # 生成URL
                url = self.feed_manager.generate_feed_url(feed)

                # 获取内容
                content = self._fetch_feed(url)
                if not content:
                    continue

                # 简单解析（寻找item标签）
                items = self._parse_rss_content(content)
                if not items:
                    continue

                logger.info(f"  从 {feed.platform} - {feed.name} 获取 {len(items)} 条")

                # 解析每条
                count = 0
                for item in items:
                    if count >= limit_per_feed:
                        break

                    news = self._parse_rss_item(item, feed.name, feed.platform)
                    if news and news.link not in processed_urls:
                        all_news.append(news)
                        processed_urls.add(news.link)
                        count += 1

                # 延迟一下，避免请求过快
                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"  采集 {feed.name} 失败: {e}")
                continue

        # 按热度排序
        all_news.sort(key=lambda x: x.heat_score, reverse=True)

        logger.info(f"采集完成！共获取 {len(all_news)} 条热点新闻")

        # 统计
        platform_stats = {}
        for news in all_news:
            if news.platform not in platform_stats:
                platform_stats[news.platform] = 0
            platform_stats[news.platform] += 1

        for platform, count in sorted(platform_stats.items(), key=lambda x: -x[1]):
            logger.info(f"    {platform}: {count} 条")

        return all_news

    def _parse_rss_content(self, content: str) -> List[Dict]:
        """简单RSS内容解析"""
        items = []

        try:
            # 查找item标签
            import re
            pattern = r'<item[^>]*>(.*?)</item>'
            item_matches = re.findall(pattern, content, re.DOTALL)

            for item_xml in item_matches:
                item = {}

                # 提取标题
                title_match = re.search(r'<title[^>]*>(.*?)</title>', item_xml, re.DOTALL)
                if title_match:
                    item['title'] = title_match.group(1).strip()

                # 提取链接
                link_match = re.search(r'<link[^>]*>(.*?)</link>', item_xml, re.DOTALL)
                if link_match:
                    item['link'] = link_match.group(1).strip()

                # 提取发布时间
                pub_match = re.search(r'<pubDate[^>]*>(.*?)</pubDate>', item_xml, re.DOTALL)
                if pub_match:
                    item['pubDate'] = pub_match.group(1).strip()

                # 提取摘要
                desc_match = re.search(r'<description[^>]*>(.*?)</description>', item_xml, re.DOTALL)
                if desc_match:
                    item['summary'] = desc_match.group(1).strip()

                # 提取分类
                cat_matches = re.findall(r'<category[^>]*>(.*?)</category>', item_xml)
                if cat_matches:
                    item['categories'] = [c.strip() for c in cat_matches]

                if item.get('title'):
                    items.append(item)

        except Exception as e:
            logger.warning(f"解析RSS内容失败: {e}")

        return items


def main():
    """主函数"""
    print("=" * 70)
    print("RSSHub热点新闻采集器")
    print("=" * 70)

    # 创建采集器
    collector = RSSHubCollector()

    # 采集热点新闻（选择国内平台）
    platforms = ['Weibo', 'Bilibili', 'Zhihu', 'Douban']
    news_list = collector.collect(
        platforms=platforms,
        limit_per_feed=3,
        max_feeds=10
    )

    # 保存结果
    output_file = "./output/rsshub_news.json"
    os.makedirs("./output", exist_ok=True)

    news_data = []
    for news in news_list:
        news_data.append({
            'news_id': news.news_id,
            'title': news.title,
            'link': news.link,
            'source': news.source,
            'platform': news.platform,
            'publish_time': news.publish_time.isoformat(),
            'summary': news.summary,
            'category': news.category,
            'keywords': news.keywords,
            'heat_score': news.heat_score
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到: {output_file}")
    print(f"共采集 {len(news_list)} 条热点新闻")

    # 显示前10条
    print(f"\n热点新闻 TOP 10:")
    for i, news in enumerate(news_list[:10], 1):
        print(f"{i}. [{news.category}] {news.title[:50]}")
        print(f"   来源: {news.platform} | 热度: {news.heat_score:.1f}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
