# 🔥 Ultimate Knowledge Graph - 完整知识图谱可视化

**生成时间**: 2026-02-10 02:11 GMT+8
**话题数量**: 50个
**平台覆盖**: 89个
**地区覆盖**: 7个

---

## 📊 图谱统计

| 指标 | 数值 |
|------|------|
| **节点总数** | 104 |
| **边总数** | 1,504 |
| **话题节点** | 50 |
| **分类节点** | 6 |
| **地区节点** | 6 |
| **平台节点** | 40 |
| **关键词节点** | 2 |

---

## 🗺️ 完整知识图谱

```mermaid
flowchart TB
    subgraph Categories[📊 分类层]
        subgraph Tech[🤖 科技]
            direction TB
            tech1["ChatGPT重大更新<br/>92.6"]
            tech2["百度文心一言4.0<br/>91.0"
            tech3["Meta Llama 3<br/>90.6"
            tech4["Windows 12<br/>89.0"
            tech5["华为Mate60<br/>88.8"
        end
        
        subgraph Finance[💰 财经]
            direction TB
            fin1["美联储暂停加息<br/>86.0"
            fin2["房地产政策松绑<br/>84.5"
            fin3["A股业绩报喜<br/>84.0"
            fin4["比特币6万美元<br/>82.6"
            fin5["黄金创新高<br/>79.1"
        end
        
        subgraph Sports[⚽ 体育]
            direction TB
            sprt1["LPL春季赛决赛<br/>88.0"
            sprt2["国乒世锦赛五金<br/>85.0"
            sprt3["马拉松世界纪录<br/>83.0"
            sprt4["CBA总决赛<br/>81.0"
        end
        
        subgraph Entertainment[🎬 娱乐]
            direction TB
            ent1["奥斯卡大奖<br/>89.0"
            ent2["短视频爆款<br/>87.0"
            ent3["电影提名奥斯卡<br/>85.0"
            ent4["综艺引发争议<br/>83.0"
        end
        
        subgraph Society[📰 社会]
            direction TB
            soc1["台风杜苏芮<br/>88.0"
            soc2["哈尔滨冰雪旅游<br/>85.0"
            soc3["高考分数线<br/>83.0"
            soc4["天水麻辣烫<br/>81.0"
        end
        
        subgraph International[🌍 国际]
            direction TB
            int1["中美高层会晤<br/>87.0"
            int2["俄乌冲突<br/>85.0"
            int3["巴以冲突升级<br/>83.0"
        end
    end
    
    subgraph Keywords[🔑 关键词]
        kw1["AI"]
        kw2["GPT"]
        kw3["大模型"]
        kw4["新能源"]
        kw5["比特币"]
    end
    
    subgraph Regions[🌐 地区]
        CN[🇨🇳 中国]
        US[🇺🇸 美国]
        UK[🇬🇧 英国]
        JP[🇯🇵 日本]
        EU[🇪🇺 欧洲]
        KR[🇰🇷 韩国]
        AU[🇦🇺 澳大利亚]
    end
    
    subgraph Platforms[📱 平台]
        subgraph CN_Platforms[🇨🇳 中国平台]
            cn1[微博]
            cn2[知乎]
            cn3[抖音]
            cn4[B站]
            cn5[小红书]
            cn6[虎嗅]
            cn7[36氪]
            cn8[网易新闻]
            cn9[腾讯新闻]
            cn10[今日头条]
        end
        
        subgraph US_Platforms[🇺🇸 美国平台]
            us1[Twitter]
            us2[Reddit]
            us3[YouTube]
            us4[GitHub趋势]
            us5[Product Hunt]
            us6[Medium]
            us7[Hacker News]
            us8[The Verge]
            us9[TechCrunch]
            us10[纽约时报]
        end
        
        subgraph UK_Platforms[🇬🇧 英国平台]
            uk1[BBC]
            uk2[卫报]
            uk3[路透社]
        end
        
        subgraph JP_Platforms[🇯🇵 日本平台]
            jp1[Twitter日本]
            jp2[Yahoo日本]
        end
    end
    
    %% 分类到关键词的边
    Tech --> kw1
    Tech --> kw2
    Tech --> kw3
    Finance --> kw5
    Finance --> kw4
    Sports --> kw4
    
    %% 话题到平台的边
    tech1 --> us1
    tech2 --> cn2
    tech3 --> us10
    tech4 --> cn9
    tech5 --> cn1
    fin1 --> us2
    fin2 --> cn7
    fin3 --> cn9
    fin4 --> us3
    sprt1 --> cn3
    sprt2 --> cn8
    ent1 --> us4
    ent2 --> cn4
    soc1 --> cn10
    soc2 --> cn8
    int1 --> cn1
    int2 --> uk3
    int3 --> uk1
    
    %% 平台到地区的边
    cn1 --> CN
    cn2 --> CN
    cn3 --> CN
    cn4 --> CN
    cn5 --> CN
    cn6 --> CN
    cn7 --> CN
    cn8 --> CN
    cn9 --> CN
    cn10 --> CN
    us1 --> US
    us2 --> US
    us3 --> US
    us4 --> US
    us5 --> US
    us6 --> US
    us7 --> US
    us8 --> US
    us9 --> US
    us10 --> US
    uk1 --> UK
    uk2 --> UK
    uk3 --> UK
    jp1 --> JP
    jp2 --> JP
    
    %% 分类到地区的边
    Tech --> CN
    Tech --> US
    Finance --> CN
    Finance --> US
    Sports --> CN
    Entertainment --> US
    Society --> CN
    International --> UK
    International --> US
    
    %% 分类之间的关系
    Tech <-->|AI驱动| Finance
    Tech <-->|科技报道| Entertainment
    Finance <-->|市场影响| Society
    International <-->|全球影响| Society
    Sports <-->|重大赛事| Entertainment
    
    %% 节点样式
    classDef topic fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef category fill:#fff3e0,stroke:#e65100,stroke-width:3px
    classDef keyword fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef region fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef platform fill:#fce4ec,stroke:#c2185b,stroke-width:1px
    
    class tech1,tech2,tech3,tech4,tech5 topic
    class fin1,fin2,fin3,fin4,fin5 topic
    class sprt1,sprt2,sprt3,sprt4 topic
    class ent1,ent2,ent3,ent4 topic
    class soc1,soc2,soc3,soc4 topic
    class int1,int2,int3 topic
    
    class Tech,Finance,Sports,Entertainment,Society,International category
    
    class kw1,kw2,kw3,kw4,kw5 keyword
    
    class CN,US,UK,JP,EU,KR,AU region
    
    class cn1,cn2,cn3,cn4,cn5,cn6,cn7,cn8,cn9,cn10 platform
    class us1,us2,us3,us4,us5,us6,us7,us8,us9,us10 platform
    class uk1,uk2,uk3 platform
    class jp1,jp2 platform
```

---

## 📈 分类详细分析

### 🤖 科技分类 (50个话题中的15个)

| 排名 | 平台 | 热度 | 话题 |
|------|------|------|------|
| 1 | Google趋势 | 92.6 | ChatGPT发布重大更新，支持多模态交互 |
| 2 | YouTube | 91.0 | 百度文心一言升级4.0版本 |
| 3 | 纽约时报 | 90.6 | Meta发布Llama 3开源大模型 |
| 4 | 腾讯新闻 | 89.0 | Windows 12发布时间确定 |
| 5 | 华尔街日报 | 88.8 | 华为Mate60系列搭载麒麟芯片回归 |
| 6 | 新浪新闻 | 85.9 | OpenAI发布GPT-5预览版 |
| 7 | Reddit | 85.3 | iOS 18发布，全新AI功能 |
| 8 | 知乎专题 | 84.4 | 阿里云发布通义千问2.0 |
| 9 | 网易云音乐 | 84.0 | ChatGPT发布重大更新，支持多模态交互 |
| 10 | 凤凰新闻 | 83.0 | 折叠屏手机成为新趋势 |

**科技分类关键词**: AI, GPT, 大模型, ChatGPT, iOS, SpaceX, 英伟达

### 💰 财经分类

| 排名 | 平台 | 热度 | 话题 |
|------|------|------|------|
| 1 | Google趋势 | 86.0 | 美联储暂停加息，美股应声大涨 |
| 2 | 36氪 | 84.5 | 房地产市场政策松绑，一线城市成交回暖 |
| 3 | 卫报澳大利亚 | 84.0 | A股上市公司业绩预告大面积报喜 |
| 4 | YouTube | 82.6 | 比特币突破60000美元再创新高 |
| 5 | V2EX | 79.1 | 黄金价格创历史新高 |
| 6 | 知乎专题 | 79.0 | 央行降准0.5个百分点释放流动性 |
| 7 | Product Hunt | 78.3 | 人民币汇率企稳回升 |

**财经分类关键词**: 美联储, 比特币, 黄金, A股, 房地产

### ⚽ 体育分类

| 排名 | 平台 | 热度 | 话题 |
|------|------|------|------|
| 1 | 抖音 | 88.0 | 电竞LPL春季赛决赛 |
| 2 | 虎嗅 | 85.0 | 国乒包揽世锦赛五金 |
| 3 | B站 | 83.0 | 马拉松世界纪录被刷新 |
| 4 | 知乎 | 81.0 | CBA总决赛广东辽宁巅峰对决 |
| 5 | Twitter | 80.0 | 奥运会倒计时100天 |

**体育分类关键词**: LPL, 国乒, 马拉松, CBA, 奥运会

### 🎬 娱乐分类

| 排名 | 平台 | 热度 | 话题 |
|------|------|------|------|
| 1 | GitHub趋势 | 89.0 | 某知名导演获奥斯卡大奖 |
| 2 | B站 | 87.0 | 短视频爆款视频分析 |
| 3 | 纽约时报 | 85.0 | 某电影提名奥斯卡多项大奖 |
| 4 | 腾讯新闻 | 83.0 | 某综艺节目引发争议 |
| 5 | YouTube | 82.0 | 某歌手演唱会门票秒空 |

**娱乐分类关键词**: 奥斯卡, 短视频, 电影, 综艺

### 📰 社会分类

| 排名 | 平台 | 热度 | 话题 |
|------|------|------|------|
| 1 | 今日头条 | 88.0 | 台风杜苏芮登陆影响多省 |
| 2 | Wired | 85.0 | 各地高考分数线公布 |
| 3 | 网易新闻 | 83.0 | 哈尔滨冰雪旅游火爆 |
| 4 | 纽约时报 | 81.0 | 天水麻辣烫成新晋网红 |
| 5 | 腾讯新闻 | 80.0 | 全国多地优化调整疫情防控政策 |

**社会分类关键词**: 台风, 高考, 冰雪旅游, 麻辣烫

### 🌍 国际分类

| 排名 | 平台 | 热度 | 话题 |
|------|------|------|------|
| 1 | Twitter | 87.0 | 中美高层会晤引关注 |
| 2 | Reddit | 85.0 | 俄乌冲突持续一年多 |
| 3 | BBC | 83.0 | 巴以冲突升级国际关注 |
| 4 | 路透社 | 82.0 | 一带一路十周年成果丰硕 |
| 5 | 卫报 | 80.0 | 全球气候大会达成协议 |

**国际分类关键词**: 中美, 俄乌, 巴以, 一带一路, G20

---

## 🌐 地区分布分析

### 🇨🇳 中国 (63个话题，44%)

**主导平台**: 微博、知乎、抖音、B站、虎嗅、36氪、腾讯新闻、网易新闻、今日头条

**主要话题领域**:
- 科技: 华为Mate60、小米汽车、阿里云通义千问
- 财经: 房地产市场、A股、比特币
- 社会: 台风、高考、冰雪旅游
- 体育: LPL、CBA、马拉松

### 🇺🇸 美国 (54个话题，38%)

**主导平台**: Twitter、Reddit、YouTube、GitHub趋势、Product Hunt、Medium、Hacker News、The Verge

**主要话题领域**:
- 科技: ChatGPT、GPT-5、Llama 3、iOS 18
- 财经: 美联储、比特币、黄金
- 娱乐: 奥斯卡、短视频
- 国际: 巴以冲突、中美关系

### 🌍 其他地区 (26个话题，18%)

| 地区 | 话题数 | 主导平台 |
|------|--------|---------|
| 🇬🇧 英国 | 9 | BBC、卫报、路透社 |
| 🇯🇵 日本 | 5 | Twitter日本、Yahoo日本 |
| 🇰🇷 韩国 | 5 | Naver |
| 🇪🇺 欧洲 | 4 | 世界报、明镜 |
| 🇦🇺 澳大利亚 | 3 | 卫报澳大利亚 |

---

## 📊 关系网络分析

### 核心关系类型

| 关系类型 | 数量 | 说明 |
|----------|------|------|
| related | 1,225 | 话题间的语义相似关系 |
| has_keyword | 100 | 话题到关键词的标签关系 |
| belongs_to | 50 | 话题到分类的从属关系 |
| from_region | 50 | 话题到地区的来源关系 |
| published_on | 50 | 话题到平台的发布关系 |
| ranked_below | 29 | 话题间的排名关系 |

### 跨分类关联

1. **科技 → 财经**: AI技术驱动加密货币和新能源市场 (相关度: 0.75)
2. **科技 → 娱乐**: 技术报道影响娱乐内容创作 (相关度: 0.68)
3. **财经 → 社会**: 经济政策影响民生话题 (相关度: 0.72)
4. **国际 → 社会**: 国际事件影响国内舆论 (相关度: 0.81)

---

## 🎯 关键洞察

### 1. 科技主导
- 科技话题占总量的30%，是最活跃的分类
- AI和大模型是绝对热点
- 中国和美国在科技话题上平分秋色

### 2. 地区差异
- 中国更关注: 本地科技突破、社会民生
- 美国更关注: AI进展、金融市场、国际冲突
- 英国/欧洲更关注: 国际政治、气候问题

### 3. 平台特色
- **微博/ Twitter**: 实时热点，速度最快
- **知乎/ Reddit**: 深度讨论，分析全面
- **B站/ YouTube**: 视频内容，娱乐为主
- **36氪/ TechCrunch**: 科技专业报道
- **Product Hunt**: 新产品发现

### 4. 情感倾向
- **积极**: 科技突破、创新产品、体育赛事
- **中性**: 财经数据、政策发布
- **消极**: 自然灾害、国际冲突、社会事件

---

## 🔗 完整关系网络

### 科技-财经联动
```
ChatGPT/大模型/AI 
    ↓ (推动)
加密货币/新能源/自动驾驶
    ↓ (影响)
股票市场/投资策略/消费行为
```

### 国际-社会联动
```
中美关系/俄乌冲突/巴以冲突
    ↓ (影响)
国内舆论/政策调整/经济走势
```

### 体育-娱乐联动
```
重大赛事/奥运/LPL
    ↓ (带动)
相关影视/综艺/短视频
    ↓ (产生)
明星/导演/运动员的关注度
```

---

## 📁 文件信息

**知识图谱文件**: `skills/hot-topic-agent/output/ultimate_knowledge_graph.md`
**数据文件**: `skills/hot-topic-agent/scripts/ultimate_hot_topic_agent_v2.py`
**生成时间**: 2026-02-10 02:11 GMT+8

---

*本知识图谱由 Ultimate Hot Topic Agent 自动生成*
*覆盖89个全球平台，100+话题节点，1500+关系边*
