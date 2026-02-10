# 增强版知识图谱: 热点事件分析（含浏览器采集）
**生成时间**: 2026-02-10T00:32:16.912247
**节点数**: 18 | **边数**: 80
**浏览器采集**: 12 条 (100.0%)

```mermaid
graph TB
    phenomenon_0("技术普及")
    phenomenon_1("市场关注")
    phenomenon_2("政策支持")
    phenomenon_3("资本投入")
    emotion_0<"积极乐观">
    emotion_1<"期待">
    emotion_2<"兴奋">
    emotion_3<"焦虑">
    event_0["为什么越来越多的人开始关注心理健康？..."]
    event_1["娱乐头条：#某电影定档#..."]
    event_2["热搜第一：#某地突发地震#..."]
    event_3["今日头条：#A股大涨#..."]
    event_4["[B站热门] 某UP主耗时三年制作的视频..."]
    event_5["房价下跌对年轻人意味着什么？..."]
    event_6["网友热议：#某明星恋情曝光#..."]
    event_7["AI会取代哪些职业？..."]
    event_8["微博热搜：#某明星离婚#..."]
    event_9["[B站热门] 美食探店：网红餐厅实测..."]

    %% 边关系
    event_0 -.->|leads_to| phenomenon_0
    event_0 -.->|leads_to| phenomenon_1
    event_0 -.->|leads_to| phenomenon_2
    event_0 -.->|leads_to| phenomenon_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3
    event_1 -.->|leads_to| phenomenon_0
    event_1 -.->|leads_to| phenomenon_1
    event_1 -.->|leads_to| phenomenon_2
    event_1 -.->|leads_to| phenomenon_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3
    event_2 -.->|leads_to| phenomenon_0
    event_2 -.->|leads_to| phenomenon_1
    event_2 -.->|leads_to| phenomenon_2
    event_2 -.->|leads_to| phenomenon_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3
    event_3 -.->|leads_to| phenomenon_0
    event_3 -.->|leads_to| phenomenon_1
    event_3 -.->|leads_to| phenomenon_2
    event_3 -.->|leads_to| phenomenon_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3
    event_4 -.->|leads_to| phenomenon_0
    event_4 -.->|leads_to| phenomenon_1
    event_4 -.->|leads_to| phenomenon_2
    event_4 -.->|leads_to| phenomenon_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3
    event_5 -.->|leads_to| phenomenon_0
    event_5 -.->|leads_to| phenomenon_1
    event_5 -.->|leads_to| phenomenon_2
    event_5 -.->|leads_to| phenomenon_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3
    event_6 -.->|leads_to| phenomenon_0
    event_6 -.->|leads_to| phenomenon_1

    %% 节点样式
    classDef event fill:#e1f5fe,stroke:#01579b
    classDef phenomenon fill:#fff3e0,stroke:#e65100
    classDef psychology fill:#f3e5f5,stroke:#4a148c
    class event_0,event_1,event_2,event_3,event_4,event_5,event_6,event_7,event_8,event_9 event
    class phenomenon_0,phenomenon_1,phenomenon_2,phenomenon_3 phenomenon
    class emotion_0,emotion_1,emotion_2,emotion_3 psychology
```

---

## 📊 嵌入分析结果

### 事件相似度 TOP 10

| 事件1 | 事件2 | 相似度 |
|-------|-------|--------|
| 娱乐头条：#某电影定档# | 微博热搜：#某明星离婚# | 0.9965 |
| 热搜第一：#某地突发地震# | 网友热议：#某明星恋情曝光# | 0.9641 |
| 娱乐头条：#某电影定档# | 热搜第一：#某地突发地震# | 0.9611 |
| 热搜第一：#某地突发地震# | 微博热搜：#某明星离婚# | 0.9592 |
| 为什么越来越多的人开始关注心理健康？ | [B站热门] 某UP主耗时三年制作的视频 | 0.9554 |
| [B站热门] 某UP主耗时三年制作的视频 | [B站热门] 美食探店：网红餐厅实测 | 0.9374 |
| 今日头条：#A股大涨# | AI会取代哪些职业？ | 0.9367 |
| 为什么越来越多的人开始关注心理健康？ | 房价下跌对年轻人意味着什么？ | 0.9354 |
| 网友热议：#某明星恋情曝光# | 微博热搜：#某明星离婚# | 0.9242 |
| 娱乐头条：#某电影定档# | 网友热议：#某明星恋情曝光# | 0.9228 |

### 事件聚类

- **cluster_0**: 娱乐头条：#某电影定档#, 热搜第一：#某地突发地震#, 今日头条：#A股大涨#, 房价下跌对年轻人意味着什么？, 网友热议：#某明星恋情曝光#, AI会取代哪些职业？, 微博热搜：#某明星离婚#
- **cluster_1**: 为什么越来越多的人开始关注心理健康？, [B站热门] 某UP主耗时三年制作的视频, [B站热门] 美食探店：网红餐厅实测

### 链接预测

| 预测事件 | 分数 |
|---------|------|
| [B站热门] 某UP主耗时三年制作的视频 | 0.9554 |
| 房价下跌对年轻人意味着什么？ | 0.9354 |
| [B站热门] 美食探店：网红餐厅实测 | 0.9122 |