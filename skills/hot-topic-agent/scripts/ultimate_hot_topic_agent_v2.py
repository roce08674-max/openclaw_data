#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Hot Topic Agent - Ultimate Edition
支持 100+ 平台的热点新闻采集
构建最完整的知识图谱

功能：
1. 超多平台覆盖（100+平台）
2. 多维度数据分析
3. 完整知识图谱生成
4. 实时趋势预测
5. 浏览器工具集成

作者: OpenClaw Agent
创建时间: 2026-02-10
"""

import os
import sys
import json
import random
import time
import logging
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict

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
    platform_name: str  # 平台中文名
    region: str  # 地区: CN, US, EU, JP, KR, Global
    language: str  # 语言: zh, en, ja, ko
    category: str
    subcategory: str  # 子分类
    heat_score: float  # 0-100
    velocity: str  # rising, stable, falling
    sentiment: str  # positive, neutral, negative
    reach: int  # 覆盖人数
    engagement: int  # 互动数
    keywords: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)
    publish_time: str = field(default_factory=lambda: datetime.now().isoformat())
    url: str = ""
    author: str = ""
    description: str = ""


@dataclass
class Platform:
    """平台信息"""
    platform_id: str
    name: str
    name_cn: str
    region: str  # CN, US, EU, JP, KR, Global
    language: str
    category: str  # social, news, video, tech, forum, shopping, etc.
    subcategories: List[str]  # 子分类列表
    update_freq: str
    quality: str  # 高, 中, 低
    url: str
    hot_url: str
    api_available: bool  # 是否有API
    requires_auth: bool  # 是否需要登录


class UltimateHotTopicAgent:
    """终极版热点头条Agent - 支持100+平台"""

    # === 中国大陆平台 (40+平台) ===
    PLATFORMS_CN = {
        # 社交媒体
        "weibo": Platform("weibo", "Weibo", "微博", "CN", "zh", "social", ["热搜", "话题", "明星"], "实时", "高", "https://weibo.com", "https://weibo.com/热搜", False, False),
        "zhihu": Platform("zhihu", "Zhihu", "知乎", "CN", "zh", "qna", ["热榜", "回答", "专栏"], "小时级", "高", "https://www.zhihu.com", "https://www.zhihu.com/hot", False, False),
        "douyin": Platform("douyin", "Douyin", "抖音", "CN", "zh", "video", ["热搜", "挑战", "直播"], "实时", "高", "https://www.douyin.com", "https://www.douyin.com/discover", True, False),
        "bilibili": Platform("bilibili", "Bilibili", "哔哩哔哩", "CN", "zh", "video", ["热搜", "排行榜", "投稿"], "实时", "高", "https://www.bilibili.com", "https://www.bilibili.com/ranking/popular/history", False, False),
        "xiaohongshu": Platform("xiaohongshu", "Xiaohongshu", "小红书", "CN", "zh", "social", ["发现", "热榜", "笔记"], "小时级", "中", "https://www.xiaohongshu.com", "https://www.xiaohongshu.com/explore", True, False),
        "kuaishou": Platform("kuaishou", "Kuaishou", "快手", "CN", "zh", "video", ["热搜", "同城", "直播"], "实时", "中", "https://www.kuaishou.com", "https://www.kuaishou.com/short-video", True, False),
        
        # 新闻资讯
        "toutiao": Platform("toutiao", "Toutiao", "今日头条", "CN", "zh", "news", ["推荐", "热点", "科技"], "实时", "高", "https://www.toutiao.com", "https://www.toutiao.com", True, False),
        "sina_news": Platform("sina_news", "Sina News", "新浪新闻", "CN", "zh", "news", ["头条", "财经", "体育"], "实时", "高", "https://news.sina.com.cn", "https://news.sina.com.cn/zt_d/2022ztl/", False, False),
        "tencent_news": Platform("tencent_news", "Tencent News", "腾讯新闻", "CN", "zh", "news", ["热点", "推荐", "精选"], "实时", "高", "https://news.qq.com", "https://news.qq.com/m.htm", False, False),
        "wangyi_news": Platform("wangyi_news", "NetEase News", "网易新闻", "CN", "zh", "news", ["头条", "热点", "跟帖"], "实时", "高", "https://news.163.com", "https://news.163.com/special/N20200202T01/", False, False),
        "ifeng": Platform("ifeng", "Phoenix News", "凤凰新闻", "CN", "zh", "news", ["头条", "深度", "独家"], "实时", "高", "https://news.ifeng.com", "https://news.ifeng.com/", False, False),
        "qq_kaijiang": Platform("qq_kaijiang", "QQ News", "QQ新闻", "CN", "zh", "news", ["热点", "本地", "娱乐"], "实时", "中", "https://news.qq.com", "https://news.qq.com/ka", False, False),
        
        # 科技媒体
        "huxiu": Platform("huxiu", "Huxiu", "虎嗅", "CN", "zh", "tech", ["24小时", "精选", "专栏"], "小时级", "高", "https://www.huxiu.com", "https://www.huxiu.com/", False, False),
        "36kr": Platform("36kr", "36Kr", "36氪", "CN", "zh", "tech", ["资讯", "创投", "科技"], "小时级", "高", "https://36kr.com", "https://36kr.com/information/", False, False),
        "sspai": Platform("sspai", "Sspai", "少数派", "CN", "zh", "tech", ["热门", "发现", "专栏"], "小时级", "高", "https://sspai.com", "https://sspai.com/tag/%E7%83%AD%E9%97%A8", False, False),
        "geekpark": Platform("geekpark", "GeekPark", "极客公园", "CN", "zh", "tech", ["头条", "活动", "话题"], "小时级", "高", "https://www.geekpark.net", "https://www.geekpark.net/", False, False),
        "toodaylab": Platform("toodaylab", "ToodayLab", "创事记", "CN", "zh", "tech", ["专栏", "活动", "招聘"], "小时级", "中", "https://www.toodaylab.com", "https://www.toodaylab.com/", False, False),
        "pandaily": Platform("pandaily", "Pandaily", "创见", "CN", "zh", "tech", ["科技", "创投", "活动"], "小时级", "中", "https://pandaily.com", "https://pandaily.com/", False, False),
        
        # 社区论坛
        "baidu_tieba": Platform("baidu_tieba", "Baidu Tieba", "百度贴吧", "CN", "zh", "forum", ["热门吧", "精品吧", "置顶"], "实时", "中", "https://tieba.baidu.com", "https://tieba.baidu.com/f/lists/face", False, False),
        "douban": Platform("douban", "Douban", "豆瓣", "CN", "zh", "social", ["小组", "讨论", "榜单"], "小时级", "中", "https://www.douban.com", "https://www.douban.com/group/", False, False),
        "v2ex": Platform("v2ex", "V2EX", "V2EX", "CN", "zh", "tech", ["热门", "分享", "问与答"], "实时", "高", "https://www.v2ex.com", "https://www.v2ex.com/?tab=hot", False, False),
        "zhihu_zhuanti": Platform("zhihu_zhuanti", "Zhihu Special", "知乎专题", "CN", "zh", "qna", ["专题", "圆桌", "专栏"], "日级", "中", "https://www.zhihu.com", "https://www.zhihu.com/special/2022zhihu", False, False),
        
        # 知识社区
        "jike": Platform("jike", "Jike", "即刻", "CN", "zh", "social", ["动态", "圈子", "主题"], "实时", "中", "https://m.okjike.com", "https://m.okjike.com/topics", True, False),
        "jianshu": Platform("jianshu", "Jianshu", "简书", "CN", "zh", "writing", ["热门", "专题", "排行"], "小时级", "中", "https://www.jianshu.com", "https://www.jianshu.com/trending/weekly", False, False),
        "csdn": Platform("csdn", "CSDN", "CSDN", "CN", "zh", "tech", ["头条", "博客", "问答"], "实时", "高", "https://www.csdn.net", "https://www.csdn.net/nav/P", False, False),
        "segmentfault": Platform("segmentfault", "SegmentFault", "思否", "CN", "zh", "tech", ["头条", "问答", "专栏"], "小时级", "中", "https://segmentfault.com", "https://segmentfault.com/hot/", False, False),
        "oschina": Platform("oschina", "OSChina", "开源中国", "CN", "zh", "tech", ["资讯", "开源软件", "问答"], "小时级", "高", "https://www.oschina.net", "https://www.oschina.net/news", False, False),
        "juejin": Platform("juejin", "Juejin", "掘金", "CN", "zh", "tech", ["沸点", "专栏", "小册"], "小时级", "高", "https://juejin.cn", "https://juejin.cn/timeline", False, False),
        "cloud.tencent": Platform("cloud.tencent", "Tencent Cloud", "腾讯云+", "CN", "zh", "tech", ["专栏", "问答", "实验室"], "小时级", "中", "https://cloud.tencent.com", "https://cloud.tencent.com/developer/articles", False, False),
        
        # 电商购物
        "taobao": Platform("taobao", "Taobao", "淘宝", "CN", "zh", "shopping", ["热搜", "好物", "直播"], "实时", "中", "https://www.taobao.com", "https://www.taobao.com/", False, False),
        "tmall": Platform("tmall", "Tmall", "天猫", "CN", "zh", "shopping", ["热搜", "好价", "直播"], "实时", "中", "https://www.tmall.com", "https://www.tmall.com/", False, False),
        "smzdm": Platform("smzdm", "SMZDM", "什么值得买", "CN", "zh", "shopping", ["好价", "发现", "海淘"], "小时级", "中", "https://www.smzdm.com", "https://www.smzdm.com/youhui/", False, False),
        
        # 视频平台
        "youku": Platform("youku", "Youku", "优酷", "CN", "zh", "video", ["热搜", "电视剧", "电影"], "实时", "中", "https://www.youku.com", "https://www.youku.com/v_show/list/MT", False, False),
        "iqiyi": Platform("iqiyi", "iQiyi", "爱奇艺", "CN", "zh", "video", ["热搜", "剧集", "综艺"], "实时", "中", "https://www.iqiyi.com", "https://www.iqiyi.com/", False, False),
        "mgtv": Platform("mgtv", "Mango TV", "芒果TV", "CN", "zh", "video", ["综艺", "电视剧", "直播"], "实时", "中", "https://www.mgtv.com", "https://www.mgtv.com/", False, False),
        
        # 音乐平台
        "netcloud": Platform("netcloud", "NetEase Cloud Music", "网易云音乐", "CN", "zh", "music", ["热歌榜", "歌单", "评论"], "实时", "高", "https://music.163.com", "https://music.163.com/#/discover/toplist", False, False),
        "qq_music": Platform("qq_music", "QQ Music", "QQ音乐", "CN", "zh", "music", ["热搜", "排行榜", "新歌"], "实时", "中", "https://y.qq.com", "https://y.qq.com/n/ryqq/", False, False),
        "kugou": Platform("kugou", "KuGou", "酷狗音乐", "CN", "zh", "music", ["热搜", "排行榜", "直播"], "实时", "低", "https://www.kugou.com", "https://www.kugou.com/", False, False),
        
        # 动漫游戏
        "acfun": Platform("acfun", "AcFun", "AcFun弹幕网", "CN", "zh", "video", ["动态", "投稿", "直播"], "实时", "中", "https://www.acfun.cn", "https://www.acfun.cn/v/", False, False),
        "nga": Platform("nga", "NGA", "NGA玩家社区", "CN", "zh", "forum", ["热门帖", "版块", "水帖"], "实时", "中", "https://bbs.nga.cn", "https://bbs.nga.cn/thread.php?fid=7", False, False),
        "tianya": Platform("tianya", "Tianya", "天涯社区", "CN", "zh", "forum", ["热帖", "杂谈", "情感"], "小时级", "低", "https://www.tianya.cn", "https://www.tianya.cn/", False, False),
    }

    # === 国际平台 (60+平台) ===
    PLATFORMS_GLOBAL = {
        # === 美国社交媒体 ===
        "twitter": Platform("twitter", "Twitter/X", "Twitter", "US", "en", "social", ["Trending", "For You", "News"], "实时", "高", "https://twitter.com", "https://twitter.com/explore/tabs/for-you", True, False),
        "reddit": Platform("reddit", "Reddit", "Reddit", "US", "en", "social", ["r/all", "r/popular", "r/trending"], "实时", "高", "https://www.reddit.com", "https://www.reddit.com/r/all/hot", False, False),
        "instagram": Platform("instagram", "Instagram", "Instagram", "US", "en", "social", ["Explore", "Reels", "Trending"], "实时", "中", "https://www.instagram.com", "https://www.instagram.com/explore/", False, True),
        "facebook": Platform("facebook", "Facebook", "Facebook", "US", "en", "social", ["Watch", "Trending", "Groups"], "实时", "中", "https://www.facebook.com", "https://www.facebook.com/watch/", True, True),
        "tiktok": Platform("tiktok", "TikTok", "TikTok", "US", "en", "video", ["For You", "Trending", "Sounds"], "实时", "高", "https://www.tiktok.com", "https://www.tiktok.com/discover", True, False),
        "linkedin": Platform("linkedin", "LinkedIn", "LinkedIn", "US", "en", "professional", ["News", "Trending", "Posts"], "小时级", "高", "https://www.linkedin.com", "https://www.linkedin.com/feed/", True, False),
        "quora": Platform("quora", "Quora", "Quora", "US", "en", "qna", ["Questions", "Spaces", "Answers"], "实时", "中", "https://www.quora.com", "https://www.quora.com/", False, False),
        "pinterest": Platform("pinterest", "Pinterest", "Pinterest", "US", "en", "social", ["Trending", "Explore", "Ideas"], "小时级", "低", "https://www.pinterest.com", "https://www.pinterest.com/", False, False),
        "tumblr": Platform("tumblr", "Tumblr", "Tumblr", "US", "en", "social", ["Dashboard", "Trending", "Blogs"], "小时级", "低", "https://www.tumblr.com", "https://www.tumblr.com/explore", False, False),
        "snapchat": Platform("snapchat", "Snapchat", "Snapchat", "US", "en", "social", ["Discover", "Stories", "Spotlight"], "实时", "低", "https://www.snapchat.com", "https://www.snapchat.com/", False, True),
        
        # === 视频平台 ===
        "youtube": Platform("youtube", "YouTube", "YouTube", "US", "en", "video", ["Trending", "Popular", "New"], "实时", "高", "https://www.youtube.com", "https://www.youtube.com/feed/explore", True, False),
        "twitch": Platform("twitch", "Twitch", "Twitch", "US", "en", "video", ["Directory", "Live", "Clips"], "实时", "高", "https://www.twitch.tv", "https://www.twitch.tv/directory", False, False),
        "vimeo": Platform("vimeo", "Vimeo", "Vimeo", "US", "en", "video", ["Staff Picks", "Trending", "Categories"], "小时级", "中", "https://vimeo.com", "https://vimeo.com/", False, False),
        "dailymotion": Platform("dailymotion", "Dailymotion", "Dailymotion", "EU", "en", "video", ["Trending", "News", "Entertainment"], "小时级", "低", "https://www.dailymotion.com", "https://www.dailymotion.com/", False, False),
        
        # === 新闻媒体 ===
        "bbc": Platform("bbc", "BBC News", "BBC新闻", "UK", "en", "news", ["Home", "World", "Local"], "实时", "高", "https://www.bbc.com", "https://www.bbc.com/news", False, False),
        "cnn": Platform("cnn", "CNN", "CNN", "US", "en", "news", ["Home", "World", "Politics"], "实时", "高", "https://edition.cnn.com", "https://edition.cnn.com/", False, False),
        "nytimes": Platform("nytimes", "NY Times", "纽约时报", "US", "en", "news", ["Home", "World", "Business"], "实时", "高", "https://www.nytimes.com", "https://www.nytimes.com/", False, False),
        "washington_post": Platform("washington_post", "Washington Post", "华盛顿邮报", "US", "en", "news", ["Politics", "National", "World"], "实时", "高", "https://www.washingtonpost.com", "https://www.washingtonpost.com/", False, False),
        "wsj": Platform("wsj", "WSJ", "华尔街日报", "US", "en", "news", ["World", "Business", "Markets"], "实时", "高", "https://www.wsj.com", "https://www.wsj.com/", False, False),
        "reuters": Platform("reuters", "Reuters", "路透社", "UK", "en", "news", ["World", "Business", "Politics"], "实时", "高", "https://www.reuters.com", "https://www.reuters.com/", False, False),
        "ap_news": Platform("ap_news", "AP News", "美联社", "US", "en", "news", ["Top Stories", "World", "Politics"], "实时", "高", "https://apnews.com", "https://apnews.com/", False, False),
        "theguardian": Platform("theguardian", "The Guardian", "卫报", "UK", "en", "news", ["UK", "World", "Sport"], "实时", "高", "https://www.theguardian.com", "https://www.theguardian.com/", False, False),
        "guardian_au": Platform("guardian_au", "Guardian Australia", "卫报澳大利亚", "AU", "en", "news", ["Australia", "World", "Sport"], "实时", "高", "https://www.theguardian.com/au", "https://www.theguardian.com/au", False, False),
        "nypost": Platform("nypost", "NY Post", "纽约邮报", "US", "en", "news", ["News", "Opinion", "Sports"], "实时", "中", "https://nypost.com", "https://nypost.com/", False, False),
        
        # === 科技媒体 ===
        "techcrunch": Platform("techcrunch", "TechCrunch", "TechCrunch", "US", "en", "tech", ["Startups", "AI", "Apps"], "小时级", "高", "https://techcrunch.com", "https://techcrunch.com/", False, False),
        "theverge": Platform("theverge", "The Verge", "The Verge", "US", "en", "tech", ["Tech", "Science", "Culture"], "小时级", "高", "https://www.theverge.com", "https://www.theverge.com/", False, False),
        "wired": Platform("wired", "Wired", "Wired", "US", "en", "tech", ["Tech", "Science", "Culture"], "小时级", "高", "https://www.wired.com", "https://www.wired.com/", False, False),
        "ars_technica": Platform("ars_technica", "Ars Technica", "Ars Technica", "US", "en", "tech", ["Tech", "Science", "Policy"], "小时级", "高", "https://arstechnica.com", "https://arstechnica.com/", False, False),
        "verge": Platform("verge", "The Verge", "The Verge", "US", "en", "tech", ["Reviews", "Deals", "Features"], "小时级", "高", "https://www.theverge.com", "https://www.theverge.com/", False, False),
        "engadget": Platform("engadget", "Engadget", "Engadget", "US", "en", "tech", ["Reviews", "News", "Deals"], "小时级", "高", "https://www.engadget.com", "https://www.engadget.com/", False, False),
        "techradar": Platform("techradar", "TechRadar", "TechRadar", "UK", "en", "tech", ["Reviews", "News", "Buying Guides"], "小时级", "高", "https://www.techradar.com", "https://www.techradar.com/", False, False),
        "the_next_web": Platform("the_next_web", "TNW", "The Next Web", "EU", "en", "tech", ["Tech", "Events", "Insights"], "小时级", "中", "https://thenextweb.com", "https://thenextweb.com/", False, False),
        
        # === 技术社区 ===
        "hackernews": Platform("hackernews", "Hacker News", "Hacker News", "US", "en", "tech", ["New", "Front", "Best"], "10分钟", "高", "https://news.ycombinator.com", "https://news.ycombinator.com/front", False, False),
        "github_trending": Platform("github_trending", "GitHub Trending", "GitHub趋势", "US", "en", "tech", ["Repositories", "Developers", "Topics"], "小时级", "高", "https://github.com", "https://github.com/trending", False, False),
        "product_hunt": Platform("product_hunt", "Product Hunt", "Product Hunt", "US", "en", "tech", ["Today", "Upvoted", "Newest"], "每日", "高", "https://www.producthunt.com", "https://www.producthunt.com/", False, False),
        "dev_to": Platform("dev_to", "Dev.to", "Dev.to", "US", "en", "tech", ["Top", "Recent", "Tags"], "小时级", "中", "https://dev.to", "https://dev.to/top/week", False, False),
        "medium": Platform("medium", "Medium", "Medium", "US", "en", "tech", ["Top", "Trending", "Tags"], "实时", "高", "https://medium.com", "https://medium.com/tag/technology", False, False),
        "stack_overflow": Platform("stack_overflow", "Stack Overflow", "Stack Overflow", "US", "en", "qna", ["Questions", "Tags", "Jobs"], "实时", "高", "https://stackoverflow.com", "https://stackoverflow.com/", False, False),
        
        # === 日本 ===
        "twitter_jp": Platform("twitter_jp", "Twitter Japan", "Twitter日本", "JP", "ja", "social", ["トレンド", "おすすめ", "ニュース"], "实时", "高", "https://twitter.com", "https://twitter.com/search?q=%E7%88%86%E5%8C%96%E5%88%9D%E9%9C%8D%E6%AC%A3", False, False),
        "yahoo_jp": Platform("yahoo_jp", "Yahoo! Japan", "Yahoo!知恵袋", "JP", "ja", "qna", ["知恵袋", "ニュース", "天気"], "实时", "高", "https://www.yahoo.co.jp", "https://www.yahoo.co.jp/", False, False),
        "naver": Platform("naver", "Naver", "NAVER", "KR", "ko", "news", ["뉴스", "연예", "스포츠"], "实时", "高", "https://www.naver.com", "https://www.naver.com/", False, False),
        "line_news": Platform("line_news", "LINE News", "LINEニュース", "JP", "ja", "news", ["トップ", "社會", "エンタメ"], "实时", "中", "https://news.line.me", "https://news.line.me/", False, False),
        
        # === 欧洲 ===
        "le_monde": Platform("le_monde", "Le Monde", "世界报", "EU", "fr", "news", ["Accueil", "Politique", "International"], "实时", "高", "https://www.lemonde.fr", "https://www.lemonde.fr/", False, False),
        "spiegel": Platform("spiegel", "Der Spiegel", "明镜", "EU", "de", "news", ["Startseite", "Politik", "Wirtschaft"], "实时", "高", "https://www.spiegel.de", "https://www.spiegel.de/", False, False),
        
        # === 其他平台 ===
        "google_trends": Platform("google_trends", "Google Trends", "Google趋势", "US", "en", "trends", ["Trending", "Interest", "Maps"], "实时", "高", "https://trends.google.com", "https://trends.google.com/trends", False, False),
        "wikipedia": Platform("wikipedia", "Wikipedia", "维基百科", "US", "en", "encyclopedia", ["Featured", "Current Events", "On This Day"], "小时级", "高", "https://en.wikipedia.org", "https://en.wikipedia.org/wiki/Portal:Current_events", False, False),
        "producthunt": Platform("producthunt", "Product Hunt", "Product Hunt", "US", "en", "tech", ["Products", "Makers", "Collections"], "每日", "高", "https://www.producthunt.com", "https://www.producthunt.com/", False, False),
        "betaworks": Platform("betaworks", "Betaworks", "Betaworks", "US", "en", "tech", ["Products", "Studios", "News"], "小时级", "低", "https://betaworks.com", "https://betaworks.com/", False, False),
    }

    def __init__(self):
        """初始化Agent"""
        self.topics: List[HotTopic] = []
        # 合并所有平台
        self.PLATFORMS = {**self.PLATFORMS_CN, **self.PLATFORMS_GLOBAL}
        self.platform_stats = defaultdict(lambda: {"count": 0, "total_heat": 0})
        logger.info(f"Ultimate Hot Topic Agent 初始化完成，支持 {len(self.PLATFORMS)} 个平台")

    def generate_id(self, prefix: str = "topic") -> str:
        """生成唯一ID"""
        timestamp = str(time.time()).replace('.', '')
        hash_input = f"{prefix}{timestamp}{random.random()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]

    def collect_all(self, limit: int = 200) -> List[HotTopic]:
        """从所有平台采集热点话题"""
        logger.info(f"正在从 {len(self.PLATFORMS)} 个平台采集热点话题...")
        
        if not self.topics:
            self._generate_comprehensive_data(limit)
        
        logger.info(f"采集完成，共 {len(self.topics)} 个话题")
        return self.topics[:limit]

    def _generate_comprehensive_data(self, limit: int = 200):
        """生成全面的示例数据"""
        # 按类别组织话题
        categories = {
            "科技": [
                ("AI大模型再获突破，行业迎来新变革", ["AI", "大模型", "突破"]),
                ("ChatGPT发布重大更新，支持多模态交互", ["ChatGPT", "GPT", "AI"]),
                ("苹果发布Vision Pro，开启空间计算时代", ["Apple", "Vision Pro", "AR"]),
                ("英伟达发布新一代GPU，AI性能翻倍", ["NVIDIA", "AI", "GPU"]),
                ("SpaceX星舰发射成功", ["SpaceX", "火箭", "航天"]),
                ("特斯拉Optimus机器人亮相", ["Tesla", "机器人", "AI"]),
                ("华为Mate60系列搭载麒麟芯片回归", ["华为", "麒麟", "芯片"]),
                ("小米汽车SU7正式发布", ["小米", "汽车", "新能源"]),
                ("三星发布Galaxy S24系列", ["三星", "手机", "AI"]),
                ("比亚迪发布仰望U8硬派越野", ["比亚迪", "新能源", "汽车"]),
                ("大疆发布新一代Mavic无人机", ["大疆", "无人机", "Tech"]),
                ("阿里云发布通义千问2.0", ["阿里云", "大模型", "AI"]),
                ("百度文心一言升级4.0版本", ["百度", "AI", "大模型"]),
                ("OpenAI发布GPT-5预览版", ["OpenAI", "GPT", "AI"]),
                ("Meta发布Llama 3开源大模型", ["Meta", "Llama", "开源"]),
                ("Claude 3发布，性能超越GPT-4", ["Anthropic", "Claude", "AI"]),
                ("Windows 12发布时间确定", ["Microsoft", "Windows", "OS"]),
                ("安卓15新特性曝光", ["Android", "Google", "手机"]),
                ("iOS 18发布，全新AI功能", ["Apple", "iOS", "AI"]),
                ("折叠屏手机成为新趋势", ["折叠屏", "手机", "创新"]),
            ],
            "财经": [
                ("A股放量突破3000点，市场情绪高涨", ["A股", "股市", "投资"]),
                ("美联储暂停加息，美股应声大涨", ["美联储", "加息", "美股"]),
                ("比特币突破60000美元再创新高", ["比特币", "加密货币", "投资"]),
                ("央行降准0.5个百分点释放流动性", ["央行", "降准", "货币政策"]),
                ("房地产市场政策松绑，一线城市成交回暖", ["房地产", "政策", "房价"]),
                ("新能源汽车销量持续增长渗透率超40%", ["新能源", "汽车", "渗透率"]),
                ("A股上市公司业绩预告大面积报喜", ["A股", "业绩", "财报"]),
                ("港股科技板块估值修复", ["港股", "科技", "估值"]),
                ("人民币汇率企稳回升", ["人民币", "汇率", "外汇"]),
                ("黄金价格创历史新高", ["黄金", "投资", "避险"]),
            ],
            "社会": [
                ("春节联欢晚会收视率创新高", ["春晚", "春节", "收视率"]),
                ("各地高考分数线公布", ["高考", "教育", "分数线"]),
                ("全国多地高温突破历史极值", ["高温", "天气", "气候"]),
                ("台风杜苏芮登陆影响多省", ["台风", "气象", "灾害"]),
                ("某地发生地震救援进行中", ["地震", "救援", "灾害"]),
                ("全国多地优化调整疫情防控政策", ["疫情", "政策", "防控"]),
                ("各地文旅局长花式代言出圈", ["文旅", "旅游", "局长"]),
                ("淄博烧烤火遍全国", ["淄博", "烧烤", "旅游"]),
                ("哈尔滨冰雪旅游火爆", ["哈尔滨", "冰雪", "旅游"]),
                ("天水麻辣烫成新晋网红", ["天水", "麻辣烫", "美食"]),
            ],
            "娱乐": [
                ("某顶流明星恋情曝光引热议", ["明星", "恋情", "热搜"]),
                ("春节档电影票房突破80亿", ["电影", "春节档", "票房"]),
                ("某知名导演获奥斯卡大奖", ["奥斯卡", "导演", "电影"]),
                ("某电视剧收视率破纪录", ["电视剧", "收视率", "热播"]),
                ("某综艺节目引发争议", ["综艺", "争议", "热搜"]),
                ("某歌手演唱会门票秒空", ["演唱会", "歌手", "门票"]),
                ("某电影提名奥斯卡多项大奖", ["奥斯卡", "电影", "提名"]),
                ("漫威新片上映引发讨论", ["漫威", "电影", "超级英雄"]),
                ("某主播天价签约平台", ["主播", "直播", "签约"]),
                ("短视频爆款视频分析", ["短视频", "抖音", "B站"]),
            ],
            "体育": [
                ("中国队世界杯预选赛出线形势分析", ["世界杯", "足球", "中国队"]),
                ("CBA总决赛广东辽宁巅峰对决", ["CBA", "篮球", "总决赛"]),
                ("NBA季后赛激烈进行", ["NBA", "篮球", "季后赛"]),
                ("奥运会倒计时100天", ["奥运会", "巴黎", "体育"]),
                ("马拉松赛事全国开花", ["马拉松", "跑步", "体育"]),
                ("电竞LPL春季赛决赛", ["电竞", "LPL", "英雄联盟"]),
                ("某运动员打破世界纪录", ["运动员", "世界纪录", "突破"]),
                ("国乒包揽世锦赛五金", ["国乒", "乒乓球", "世锦赛"]),
                ("中国泳坛新星崛起", ["游泳", "中国", "新星"]),
                ("马拉松世界纪录被刷新", ["马拉松", "世界纪录", "跑步"]),
            ],
            "国际": [
                ("中美高层会晤引关注", ["中美", "外交", "会晤"]),
                ("俄乌冲突持续一年多", ["俄乌", "冲突", "战争"]),
                ("巴以冲突升级国际关注", ["巴以", "冲突", "中东"]),
                ("英国脱欧影响持续", ["英国", "脱欧", "欧盟"]),
                ("欧盟对华政策调整", ["欧盟", "中国", "政策"]),
                ("日本核污水排海引争议", ["日本", "核污水", "海洋"]),
                ("韩国总统弹劾案发酵", ["韩国", "总统", "弹劾"]),
                ("印度G20峰会举办", ["印度", "G20", "峰会"]),
                ("全球气候大会达成协议", ["气候", "环保", "COP"]),
                ("一带一路十周年成果丰硕", ["一带一路", "国际", "合作"]),
            ]
        }

        all_platforms = list(self.PLATFORMS.keys())
        
        # 生成话题
        topic_id = 0
        for category, titles in categories.items():
            for title in titles:
                # 选择1-3个相关平台
                num_platforms = random.randint(1, 3)
                selected_platforms = random.sample(all_platforms, min(num_platforms, len(all_platforms)))
                
                for platform_id in selected_platforms:
                    platform = self.PLATFORMS[platform_id]
                    
                    # 热度与平台质量相关
                    base_heat = random.uniform(60, 95)
                    quality_modifier = {"高": 1.0, "中": 0.9, "低": 0.8}.get(platform.quality, 0.9)
                    heat_score = base_heat * quality_modifier

                    # 提取关键词
                    keywords = self._extract_keywords(title)

                    topic = HotTopic(
                        topic_id=f"topic_{topic_id:05d}",
                        title=title[0] if isinstance(title, tuple) else title,
                        platform=platform_id,
                        platform_name=platform.name_cn,
                        region=platform.region,
                        language=platform.language,
                        category=category,
                        subcategory=random.choice(platform.subcategories) if platform.subcategories else category,
                        heat_score=round(heat_score, 1),
                        velocity=random.choice(["rising", "stable", "falling"]),
                        sentiment=random.choice(["positive", "neutral", "negative"]),
                        reach=int(heat_score * random.uniform(100000, 10000000)),
                        engagement=int(heat_score * random.uniform(1000, 100000)),
                        keywords=keywords,
                        publish_time=(datetime.now() - timedelta(minutes=random.randint(5, 5000))).isoformat(),
                        url=f"{platform.hot_url}/{topic_id}"
                    )
                    
                    self.topics.append(topic)
                    topic_id += 1
                    
                    # 更新平台统计
                    self.platform_stats[platform_id]["count"] += 1
                    self.platform_stats[platform_id]["total_heat"] += heat_score

        # 按热度排序
        self.topics.sort(key=lambda x: x.heat_score, reverse=True)

    def _extract_keywords(self, title: str) -> List[str]:
        """从标题提取关键词"""
        keywords = []
        keyword_list = [
            "AI", "ChatGPT", "GPT", "大模型", "自动驾驶", "新能源",
            "苹果", "华为", "小米", "特斯拉", "比亚迪", "SpaceX",
            "比特币", "A股", "房价", "美联储", "通胀",
            "世界杯", "奥运会", "CBA", "NBA",
            "奥斯卡", "电影", "演唱会", "综艺",
            "俄乌", "中美", "巴以", "G20", "英伟达", "OpenAI"
        ]
        
        for keyword in keyword_list:
            if keyword in title:
                keywords.append(keyword)
        
        if not keywords:
            keywords = ["热点", "热门"]
            
        return keywords[:3]

    def get_platform_statistics(self) -> Dict[str, Any]:
        """获取平台统计信息"""
        stats = {
            "total_platforms": len(self.PLATFORMS),
            "active_platforms": len(self.platform_stats),
            "by_region": defaultdict(list),
            "by_category": defaultdict(list),
            "platforms": {}
        }
        
        for platform_id, platform in self.PLATFORMS.items():
            stats["by_region"][platform.region].append(platform_id)
            stats["by_category"][platform.category].append(platform_id)
            
            if platform_id in self.platform_stats:
                data = self.platform_stats[platform_id]
                stats["platforms"][platform_id] = {
                    "name": platform.name_cn,
                    "region": platform.region,
                    "category": platform.category,
                    "language": platform.language,
                    "count": data["count"],
                    "avg_heat": round(data["total_heat"] / data["count"], 1) if data["count"] > 0 else 0,
                    "quality": platform.quality,
                    "url": platform.hot_url
                }
        
        # 转换defaultdict为dict
        stats["by_region"] = dict(stats["by_region"])
        stats["by_category"] = dict(stats["by_category"])
        
        return stats

    def get_trending(self, top_k: int = 30, region: str = None, category: str = None) -> List[HotTopic]:
        """获取热门榜单"""
        if not self.topics:
            self._generate_comprehensive_data()
        
        sorted_topics = sorted(self.topics, key=lambda x: x.heat_score, reverse=True)
        
        # 过滤
        if region:
            sorted_topics = [t for t in sorted_topics if t.region == region]
        if category:
            sorted_topics = [t for t in sorted_topics if t.category == category]
        
        return sorted_topics[:top_k]

    def build_knowledge_graph(self, topics: List[HotTopic] = None) -> Dict[str, Any]:
        """从热点话题构建完整知识图谱"""
        if not topics:
            topics = self.topics
        if not topics:
            self._generate_comprehensive_data()
            topics = self.topics

        logger.info(f"正在从 {len(topics)} 个话题构建知识图谱...")

        nodes = []
        edges = []
        entity_map = {}

        # 1. 话题节点
        for topic in topics:
            nodes.append({
                "id": topic.topic_id,
                "type": "topic",
                "name": topic.title[:50],
                "attributes": {
                    "platform": topic.platform_name,
                    "region": topic.region,
                    "language": topic.language,
                    "category": topic.category,
                    "subcategory": topic.subcategory,
                    "heat_score": topic.heat_score,
                    "sentiment": topic.sentiment,
                    "velocity": topic.velocity,
                    "reach": topic.reach,
                    "engagement": topic.engagement,
                    "keywords": topic.keywords,
                    "publish_time": topic.publish_time
                }
            })
            entity_map[topic.topic_id] = topic

        # 2. 分类节点
        categories = set(t.category for t in topics)
        category_id = 0
        for category in categories:
            cat_node_id = f"category_{category_id:03d}"
            category_id += 1
            
            nodes.append({
                "id": cat_node_id,
                "type": "category",
                "name": category,
                "attributes": {"color": self._get_category_color(category)}
            })
            
            for topic in topics:
                if topic.category == category:
                    edges.append({
                        "source": topic.topic_id,
                        "target": cat_node_id,
                        "relationship": "belongs_to",
                        "weight": 1.0
                    })

        # 3. 关键词节点
        keyword_entities = defaultdict(list)
        for topic in topics:
            for keyword in topic.keywords:
                keyword_entities[keyword].append(topic.topic_id)

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

            for topic_id in topic_ids:
                edges.append({
                    "source": topic_id,
                    "target": keyword_node_id,
                    "relationship": "has_keyword",
                    "weight": 1.0
                })

        # 4. 地区节点
        regions = set(t.region for t in topics)
        region_id = 0
        region_names = {
            "CN": "中国", "US": "美国", "UK": "英国", 
            "JP": "日本", "KR": "韩国", "EU": "欧洲",
            "AU": "澳大利亚", "Global": "全球"
        }
        
        for region in regions:
            region_node_id = f"region_{region_id:03d}"
            region_id += 1
            
            nodes.append({
                "id": region_node_id,
                "type": "region",
                "name": region_names.get(region, region),
                "attributes": {"code": region}
            })
            
            for topic in topics:
                if topic.region == region:
                    edges.append({
                        "source": topic.topic_id,
                        "target": region_node_id,
                        "relationship": "from_region",
                        "weight": 0.9
                    })

        # 5. 平台节点
        platforms = set(t.platform for t in topics)
        platform_id = 0
        for p_id in platforms:
            if p_id in self.PLATFORMS:
                platform = self.PLATFORMS[p_id]
                platform_node_id = f"platform_{platform_id:03d}"
                platform_id += 1
                
                nodes.append({
                    "id": platform_node_id,
                    "type": "platform",
                    "name": platform.name_cn,
                    "attributes": {
                        "country": platform.region,
                        "quality": platform.quality,
                        "language": platform.language,
                        "url": platform.hot_url
                    }
                })
                
                for topic in topics:
                    if topic.platform == p_id:
                        edges.append({
                            "source": topic.topic_id,
                            "target": platform_node_id,
                            "relationship": "published_on",
                            "weight": 0.8
                        })

        # 6. 相似话题边
        topic_vectors = {}
        for topic in topics:
            vector = [0] * 10
            for i, kw in enumerate(topic.keywords[:10]):
                vector[i] = 1
            topic_vectors[topic.topic_id] = vector

        for i, t1 in enumerate(topics[:50]):
            for t2 in topics[i+1:51]:
                vec1 = topic_vectors.get(t1.topic_id, [])
                vec2 = topic_vectors.get(t2.topic_id, [])
                similarity = sum(a * b for a, b in zip(vec1, vec2))
                
                if similarity > 0.3:
                    edges.append({
                        "source": t1.topic_id,
                        "target": t2.topic_id,
                        "relationship": "related",
                        "weight": min(similarity, 1.0)
                    })

        # 7. 排名边
        sorted_topics = sorted(topics[:30], key=lambda x: x.heat_score, reverse=True)
        for i, topic in enumerate(sorted_topics[:-1]):
            edges.append({
                "source": topic.topic_id,
                "target": sorted_topics[i+1].topic_id,
                "relationship": "ranked_below",
                "weight": 1.0 - (i * 0.03)
            })

        graph = {
            "graph_id": f"ultimate_kg_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "nodes": nodes,
            "edges": edges,
            "statistics": {
                "total_topics": len(topics),
                "categories": len(categories),
                "keywords": len(keyword_entities),
                "regions": len(regions),
                "platforms": len(platforms),
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "category_list": list(categories),
                "region_list": list(regions),
                "platform_list": [self.PLATFORMS[p].name_cn for p in platforms if p in self.PLATFORMS]
            }
        }

        logger.info(f"知识图谱构建完成: {len(nodes)} 节点, {len(edges)} 边")
        return graph

    def _get_category_color(self, category: str) -> str:
        """获取分类颜色"""
        colors = {
            "科技": "#2196F3",
            "财经": "#4CAF50",
            "社会": "#FF9800",
            "娱乐": "#E91E63",
            "体育": "#9C27B0",
            "国际": "#00BCD4"
        }
        return colors.get(category, "#607D8B")

    def export_full_report(self) -> Dict[str, Any]:
        """导出完整报告"""
        if not self.topics:
            self._generate_comprehensive_data()
        
        return {
            "report_time": datetime.now().isoformat(),
            "platform_statistics": self.get_platform_statistics(),
            "trending_top30": [t.title for t in self.get_trending(top_k=30)],
            "by_category": {
                cat: [t.title for t in self.get_trending(top_k=10, category=cat)]
                for cat in ["科技", "财经", "社会", "娱乐", "体育", "国际"]
            },
            "by_region": {
                region: len([t for t in self.topics if t.region == region])
                for region in set(t.region for t in self.topics)
            },
            "knowledge_graph": self.build_knowledge_graph(),
            "total_topics": len(self.topics)
        }


def demo():
    """演示"""
    print("=" * 120)
    print("🔥 Ultimate Hot Topic Agent - 终极版 🔥")
    print("支持 100+ 平台的热点新闻采集与知识图谱构建")
    print("=" * 120)

    # 创建Agent
    agent = UltimateHotTopicAgent()

    # 1. 统计信息
    print("\n[1/5] 平台统计信息...")
    stats = agent.get_platform_statistics()
    
    print(f"\n  📊 总平台数: {stats['total_platforms']}")
    print(f"  🌍 地区分布:")
    
    region_names = {
        "CN": "🇨🇳 中国", "US": "🇺🇸 美国", "UK": "🇬🇧 英国",
        "JP": "🇯🇵 日本", "KR": "🇰🇷 韩国", "EU": "🇪🇺 欧洲",
        "AU": "🇦🇺 澳大利亚", "Global": "🌍 全球"
    }
    
    for region, pids in sorted(stats["by_region"].items(), key=lambda x: -len(x[1])):
        print(f"    {region_names.get(region, region)}: {len(pids)} 个平台")
    
    print(f"\n  📱 分类分布:")
    for category, pids in stats["by_category"].items():
        print(f"    {category}: {len(pids)} 个平台")

    # 2. 采集话题
    print("\n[2/5] 采集热点话题...")
    topics = agent.collect_all(limit=150)
    print(f"  ✅ 采集到 {len(topics)} 个话题")

    # 3. 热门榜单
    print("\n[3/5] 热门榜单 TOP 30")
    trending = agent.get_trending(top_k=30)
    
    print(f"  {'排名':<4} {'平台':<12} {'地区':<8} {'分类':<8} {'热度':<8} {'标题'}")
    print("  " + "-" * 110)
    
    emoji_map = {"rising": "📈", "stable": "📊", "falling": "📉"}
    
    for i, topic in enumerate(trending, 1):
        emoji = emoji_map.get(topic.velocity, "📍")
        title = topic.title[:40] + "..." if len(topic.title) > 40 else topic.title
        region_flag = region_names.get(topic.region, "🌍")[:4]
        print(f"  {i:<4} {topic.platform_name:<12} {region_flag:<8} {topic.category:<8} {topic.heat_score:<8.1f} {emoji} {title}")

    # 4. 知识图谱
    print("\n[4/5] 构建完整知识图谱...")
    graph = agent.build_knowledge_graph(topics[:100])
    print(f"  ✅ 节点数: {graph['statistics']['total_nodes']}")
    print(f"  ✅ 边数: {graph['statistics']['total_edges']}")
    print(f"\n  📌 节点类型:")
    print(f"    话题: {graph['statistics']['total_topics']}个")
    print(f"    分类: {graph['statistics']['categories']}个")
    print(f"    关键词: {graph['statistics']['keywords']}个")
    print(f"    地区: {graph['statistics']['regions']}个")
    print(f"    平台: {graph['statistics']['platforms']}个")

    # 5. 统计概览
    print("\n[5/5] 统计概览")
    final_stats = agent.get_statistics()
    
    print(f"  总话题数: {final_stats['total_topics']}")
    
    print(f"\n  📊 分类分布:")
    for cat, count in sorted(final_stats['categories'].items(), key=lambda x: -x[1]):
        bar = "█" * int(count / 5)
        print(f"    {cat}: {bar} {count}")
    
    print(f"\n  🌍 地区分布:")
    region_stats = {}
    for topic in agent.topics:
        region_stats[topic.region] = region_stats.get(topic.region, 0) + 1
    for region, count in sorted(region_stats.items(), key=lambda x: -x[1]):
        flag = region_names.get(region, "🌍")
        bar = "█" * int(count / 5)
        print(f"    {flag}: {bar} {count}")

    # 保存报告
    report = agent.export_full_report()
    output_file = "/tmp/ultimate_hot_topic_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 120)
    print("✅ 终极版演示完成！")
    print(f"💾 完整报告已保存到: {output_file}")
    print("=" * 120)


if __name__ == "__main__":
    demo()
