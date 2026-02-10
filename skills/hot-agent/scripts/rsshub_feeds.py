#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSSHub社交媒体RSS源配置

从 https://rsshub.netlify.app/routes/social-media 采集的RSS订阅源
包含：Bilibili、Twitter、微博、知乎、YouTube、Telegram等热门平台

作者: OpenClaw Agent
创建时间: 2026-02-09
"""

from typing import List
from dataclasses import dataclass
from enum import Enum


class PlatformCategory(Enum):
    """平台分类"""
    VIDEO = "视频平台"
    SOCIAL = "社交媒体"
    NEWS = "新闻媒体"
    BLOG = "博客论坛"
    INTERNATIONAL = "国际平台"
    TECH = "科技数码"


@dataclass
class RSSHubFeed:
    """RSSHub订阅源配置"""
    name: str                    # 名称
    platform: str               # 平台
    category: PlatformCategory  # 分类
    route: str                  # RSSHub路由
    description: str            # 描述
    priority: int               # 优先级 (1-10)
    example_url: str            # 示例URL
    requires_cookie: bool = False  # 是否需要Cookie
    requires_config: bool = False  # 是否需要额外配置


# RSSHub社交媒体RSS订阅源列表
RSSHUB_SOCIAL_FEEDS = [
    # ========== Bilibili (B站) ==========
    RSSHubFeed(
        name="B站每周必看",
        platform="Bilibili",
        category=PlatformCategory.VIDEO,
        route="/bilibili/weekly",
        description="B站每周必看视频",
        priority=9,
        example_url="https://rsshub.app/bilibili/weekly"
    ),
    RSSHubFeed(
        name="UP主专栏",
        platform="Bilibili",
        category=PlatformCategory.VIDEO,
        route="/bilibili/user/article/:uid",
        description="UP主发布的专栏文章",
        priority=8,
        example_url="https://rsshub.app/bilibili/user/article/2267573",
        requires_cookie=False
    ),
    RSSHubFeed(
        name="UP主动态",
        platform="Bilibili",
        category=PlatformCategory.VIDEO,
        route="/bilibili/user/dynamic/:uid",
        description="UP主的最新动态",
        priority=9,
        example_url="https://rsshub.app/bilibili/user/dynamic/2267573",
        requires_cookie=True  # 需要登录Cookie
    ),
    RSSHubFeed(
        name="分区视频排行榜",
        platform="Bilibili",
        category=PlatformCategory.VIDEO,
        route="/bilibili/ranking/:rid/:day?",
        description="B站各分区视频排行榜",
        priority=8,
        example_url="https://rsshub.app/bilibili/ranking/1/7"
    ),
    RSSHubFeed(
        name="视频弹幕",
        platform="Bilibili",
        category=PlatformCategory.VIDEO,
        route="/bilibili/video/danmaku/:bvid",
        description="视频弹幕",
        priority=6,
        example_url="https://rsshub.app/bilibili/video/danmaku/BV1i7411M7N9"
    ),
    RSSHubFeed(
        name="B站热搜",
        platform="Bilibili",
        category=PlatformCategory.SOCIAL,
        route="/bilibili/hot-search",
        description="B站热搜榜",
        priority=9,
        example_url="https://rsshub.app/bilibili/hot-search"
    ),

    # ========== 微博 ==========
    RSSHubFeed(
        name="微博热搜榜",
        platform="Weibo",
        category=PlatformCategory.SOCIAL,
        route="/weibo/search/hot",
        description="微博热搜榜",
        priority=10,
        example_url="https://rsshub.app/weibo/search/hot"
    ),
    RSSHubFeed(
        name="微博博主",
        platform="Weibo",
        category=PlatformCategory.SOCIAL,
        route="/weibo/user/:uid",
        description="微博用户个人时间线",
        priority=9,
        example_url="https://rsshub.app/weibo/user/1642909335",
        requires_cookie=True  # 部分需要Cookie
    ),
    RSSHubFeed(
        name="微博超话",
        platform="Weibo",
        category=PlatformCategory.SOCIAL,
        route="/weibo/super topics/:id",
        description="微博超话帖子",
        priority=7,
        example_url="https://rsshub.app/weibo/super topics/100808"
    ),

    # ========== 知乎 ==========
    RSSHubFeed(
        name="知乎热榜",
        platform="Zhihu",
        category=PlatformCategory.BLOG,
        route="/zhihu/hot",
        description="知乎热榜",
        priority=10,
        example_url="https://rsshub.app/zhihu/hot"
    ),
    RSSHubFeed(
        name="知乎分类热榜",
        platform="Zhihu",
        category=PlatformCategory.BLOG,
        route="/zhihu/api/v4/ranking/:category/:day",
        description="知乎分类热榜",
        priority=9,
        example_url="https://rsshub.app/zhihu/api/v4/ranking/total/7"
    ),
    RSSHubFeed(
        name="知乎用户回答",
        platform="Zhihu",
        category=PlatformCategory.BLOG,
        route="/zhihu/people/answers/:id",
        description="知乎用户的回答",
        priority=7,
        example_url="https://rsshub.app/zhihu/people/answers/frederchen"
    ),
    RSSHubFeed(
        name="知乎用户文章",
        platform="Zhihu",
        category=PlatformCategory.BLOG,
        route="/zhihu/people/posts/:id",
        description="知乎用户的文章",
        priority=7,
        example_url="https://rsshub.app/zhihu/posts/people/frederchen"
    ),

    # ========== Twitter/X ==========
    RSSHubFeed(
        name="Twitter用户时间线",
        platform="Twitter",
        category=PlatformCategory.SOCIAL,
        route="/twitter/user/:id",
        description="Twitter用户推文时间线",
        priority=10,
        example_url="https://rsshub.app/twitter/user/DIYgod",
        requires_config=True  # 需要配置账号密码
    ),
    RSSHubFeed(
        name="Twitter关键词搜索",
        platform="Twitter",
        category=PlatformCategory.SOCIAL,
        route="/twitter/keyword/:keyword",
        description="Twitter关键词搜索结果",
        priority=9,
        example_url="https://rsshub.app/twitter/keyword/RSSHub",
        requires_config=True
    ),
    RSSHubFeed(
        name="Twitter趋势",
        platform="Twitter",
        category=PlatformCategory.SOCIAL,
        route="/twitter/trends/:woeid",
        description="Twitter热门趋势",
        priority=8,
        example_url="https://rsshub.app/twitter/trends/1"
    ),

    # ========== YouTube ==========
    RSSHubFeed(
        name="YouTube音乐榜",
        platform="YouTube",
        category=PlatformCategory.VIDEO,
        route="/youtube/charts/:category?/:country?",
        description="YouTube音乐排行榜",
        priority=9,
        example_url="https://rsshub.app/youtube/charts"
    ),
    RSSHubFeed(
        name="YouTube频道",
        platform="YouTube",
        category=PlatformCategory.VIDEO,
        route="/youtube/channel/:id",
        description="YouTube频道视频",
        priority=8,
        example_url="https://rsshub.app/youtube/channel/UC2wK-mnWwoIvpKNgJsn7Gxg"
    ),
    RSSHubFeed(
        name="YouTube用户",
        platform="YouTube",
        category=PlatformCategory.VIDEO,
        route="/youtube/user/:id",
        description="YouTube用户视频",
        priority=8,
        example_url="https://rsshub.app/youtube/user/GoogleDevelopers"
    ),
    RSSHubFeed(
        name="YouTube播放列表",
        platform="YouTube",
        category=PlatformCategory.VIDEO,
        route="/youtube/playlist/:id",
        description="YouTube播放列表",
        priority=7,
        example_url="https://rsshub.app/youtube/playlist/PLMCXHnjX7XmK1YMJKXmH3Xk4XEJ2qj4zL"
    ),

    # ========== Telegram ==========
    RSSHubFeed(
        name="Telegram频道",
        platform="Telegram",
        category=PlatformCategory.SOCIAL,
        route="/telegram/channel/:username",
        description="Telegram频道消息",
        priority=9,
        example_url="https://rsshub.app/telegram/channel/NewlearnerChannel"
    ),
    RSSHubFeed(
        name="Telegram贴纸包",
        platform="Telegram",
        category=PlatformCategory.SOCIAL,
        route="/telegram/stickerpack/:name",
        description="Telegram贴纸包",
        priority=6,
        example_url="https://rsshub.app/telegram/stickerpack/dogedoge"
    ),

    # ========== Instagram ==========
    RSSHubFeed(
        name="Instagram用户",
        platform="Instagram",
        category=PlatformCategory.SOCIAL,
        route="/instagram/user/:id",
        description="Instagram用户帖子",
        priority=8,
        example_url="https://rsshub.app/instagram/user/Instagram"
    ),
    RSSHubFeed(
        name="Instagram话题",
        platform="Instagram",
        category=PlatformCategory.SOCIAL,
        route="/instagram/tag/:tag",
        description="Instagram话题标签",
        priority=7,
        example_url="https://rsshub.app/instagram/tag/cat"
    ),

    # ========== 小红书 ==========
    RSSHubFeed(
        name="小红书专辑",
        platform="Xiaohongshu",
        category=PlatformCategory.SOCIAL,
        route="/xiaohongshu/album/:id",
        description="小红书专辑笔记",
        priority=8,
        example_url="https://rsshub.app/xiaohongshu/album/64f826ecd6846f0001dc0d5c"
    ),

    # ========== 抖音 ==========
    RSSHubFeed(
        name="抖音短视频",
        platform="Douyin",
        category=PlatformCategory.VIDEO,
        route="/douyin/user/:uid",
        description="抖音用户视频",
        priority=8,
        example_url="https://rsshub.app/douyin/user/94980952363",
        requires_config=True  # 需要配置
    ),

    # ========== 豆瓣 ==========
    RSSHubFeed(
        name="豆瓣实时热门电影",
        platform="Douban",
        category=PlatformCategory.NEWS,
        route="/douban/movie/real_time_hotest",
        description="豆瓣实时热门电影",
        priority=9,
        example_url="https://rsshub.app/douban/movie/real_time_hotest"
    ),
    RSSHubFeed(
        name="豆瓣一周口碑榜",
        platform="Douban",
        category=PlatformCategory.NEWS,
        route="/douban/list/:type",
        description="豆瓣一周口碑电影榜",
        priority=8,
        example_url="https://rsshub.app/douban/list/movie_weekly_best"
    ),
    RSSHubFeed(
        name="豆瓣小组",
        platform="Douban",
        category=PlatformCategory.BLOG,
        route="/douban/group/:groupid",
        description="豆瓣小组帖子",
        priority=7,
        example_url="https://rsshub.app/douban/group/63257"
    ),

    # ========== 即刻 ==========
    RSSHubFeed(
        name="即刻圈子",
        platform="Jike",
        category=PlatformCategory.SOCIAL,
        route="/jike/topic/text/:id",
        description="即刻圈子纯文字内容",
        priority=7,
        example_url="https://rsshub.app/jike/topic/text/553870e8e4b0cafb0a1bef68"
    ),
    RSSHubFeed(
        name="即刻用户动态",
        platform="Jike",
        category=PlatformCategory.SOCIAL,
        route="/jike/user/:id",
        description="即刻用户动态",
        priority=7,
        example_url="https://rsshub.app/jike/user/553870e8e4b0cafb0a1bef68"
    ),

    # ========== 简书 ==========
    RSSHubFeed(
        name="简书首页",
        platform="Jianshu",
        category=PlatformCategory.BLOG,
        route="/jianshu/home",
        description="简书首页文章",
        priority=7,
        example_url="https://rsshub.app/jianshu/home"
    ),
    RSSHubFeed(
        name="简书作者",
        platform="Jianshu",
        category=PlatformCategory.BLOG,
        route="/jianshu/user/:uid",
        description="简书作者文章",
        priority=7,
        example_url="https://rsshub.app/jianshu/user/xxxx"
    ),

    # ========== 腾讯新闻 ==========
    RSSHubFeed(
        name="腾讯新闻较真",
        platform="Tencent",
        category=PlatformCategory.NEWS,
        route="/tencentnews/jiaozhen",
        description="腾讯新闻较真查证",
        priority=7,
        example_url="https://rsshub.app/tencentnews/jiaozhen"
    ),

    # ========== 酷安 ==========
    RSSHubFeed(
        name="酷安热榜",
        platform="Coolapk",
        category=PlatformCategory.TECH,
        route="/coolapk/hot",
        description="酷安每日热门",
        priority=7,
        example_url="https://rsshub.app/coolapk/hot"
    ),
    RSSHubFeed(
        name="酷安话题",
        platform="Coolapk",
        category=PlatformCategory.TECH,
        route="/coolapk/topic/:type",
        description="酷安话题",
        priority=6,
        example_url="https://rsshub.app/coolapk/topic/jrrm"
    ),
]


class RSSHubFeedManager:
    """RSSHub订阅源管理器"""

    def __init__(self, rsshub_base_url: str = "https://rsshub.app"):
        self.base_url = rsshub_base_url
        self.feeds = RSSHUB_SOCIAL_FEEDS

    def get_feeds_by_category(self, category: PlatformCategory) -> List[RSSHubFeed]:
        """按分类获取订阅源"""
        return [f for f in self.feeds if f.category == category]

    def get_feeds_by_platform(self, platform: str) -> List[RSSHubFeed]:
        """按平台获取订阅源"""
        return [f for f in self.feeds if f.platform.lower() == platform.lower()]

    def get_feed_by_name(self, name: str) -> RSSHubFeed:
        """按名称获取订阅源"""
        for feed in self.feeds:
            if feed.name == name:
                return feed
        return None

    def get_priority_feeds(self, top_n: int = 10) -> List[RSSHubFeed]:
        """获取优先级最高的订阅源"""
        sorted_feeds = sorted(self.feeds, key=lambda x: x.priority, reverse=True)
        return sorted_feeds[:top_n]

    def get_all_platforms(self) -> List[str]:
        """获取所有平台列表"""
        return list(set(f.platform for f in self.feeds))

    def get_all_categories(self) -> List[PlatformCategory]:
        """获取所有分类列表"""
        return list(set(f.category for f in self.feeds))

    def generate_feed_url(self, feed: RSSHubFeed, **params) -> str:
        """生成完整的RSS源URL"""
        route = feed.route
        for key, value in params.items():
            route = route.replace(f":{key}", str(value))
        return f"{self.base_url}{route}"

    def export_feeds_config(self, format: str = "python") -> str:
        """导出订阅源配置"""
        if format == "python":
            lines = [
                "# RSSHub订阅源配置",
                f"# 生成时间: 2026-02-09",
                f"# 共有 {len(self.feeds)} 个订阅源",
                "",
                "SOCIAL_FEEDS = {"
            ]
            for feed in self.feeds:
                lines.append(f'    "{feed.name}": {{')
                lines.append(f'        "url": "{feed.example_url}",')
                lines.append(f'        "platform": "{feed.platform}",')
                lines.append(f'        "category": "{feed.category.value}",')
                lines.append(f'        "priority": {feed.priority},')
                lines.append(f'    }},')
            lines.append("}")
            return "\n".join(lines)

        return ""

    def print_feeds_summary(self):
        """打印订阅源汇总"""
        print("=" * 70)
        print("RSSHub社交媒体RSS订阅源汇总")
        print("=" * 70)
        print(f"总数: {len(self.feeds)} 个订阅源\n")

        # 按平台统计
        platforms = {}
        for feed in self.feeds:
            if feed.platform not in platforms:
                platforms[feed.platform] = []
            platforms[feed.platform].append(feed)

        print("按平台分类:")
        for platform, feeds in sorted(platforms.items(), key=lambda x: -len(x[1])):
            print(f"  {platform}: {len(feeds)} 个订阅源")

        print("\n优先级TOP 10订阅源:")
        top_feeds = self.get_priority_feeds(10)
        for i, feed in enumerate(top_feeds, 1):
            print(f"  {i}. [{feed.platform}] {feed.name} (优先级:{feed.priority})")

        print("\n" + "=" * 70)


def main():
    """主函数 - 演示使用"""
    manager = RSSHubFeedManager()

    # 打印汇总
    manager.print_feeds_summary()

    # 示例：获取微博相关的订阅源
    print("\n微博相关订阅源:")
    weibo_feeds = manager.get_feeds_by_platform("Weibo")
    for feed in weibo_feeds:
        print(f"  - {feed.name}: {feed.description}")
        print(f"    URL: {feed.example_url}")


if __name__ == "__main__":
    main()
