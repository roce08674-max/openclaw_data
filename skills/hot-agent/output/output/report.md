# 知识图谱: 热点事件知识图谱
**生成时间**: 2026-02-09 22:22:40
**节点数**: 18 | **边数**: 56

```mermaid
graph TB
    %% 节点定义
    subgraph 事件层
        event_https://www.theverge.com/?p=875309["Discord will require..."]
        event_https://techcrunch.com/?p=3090538["Gather AI, maker of ..."]
        event_https://www.theverge.com/?p=875692["PlayStation’s next b..."]
        event_-5681179609737676210["语音问一问上线，小红书为何发力问搜？..."]
        event_https://www.theverge.com/?p=874895["Animal Crossing star..."]
        event_4711335956247921672["克罗格任命沃尔玛前高管为新任首席执行官..."]
        event_2639416489023408832["金螳螂：联合中标2.42亿元装修及智能化..."]
        event_5845899813940419802["谷歌母公司Alphabet启动七批美元债..."]
        event_-7251073919150803577["热门中概股美股盘前多数下跌，哔哩哔哩跌超..."]
        event_6565944244376916220["美股大型科技股盘前涨跌不一，甲骨文涨超2..."]
    end

    subgraph 现象层
        phenomenon_0("技术普及")
        phenomenon_1("市场关注")
        phenomenon_2("政策支持")
        phenomenon_3("资本投入")
    end

    subgraph 心理层
        emotion_0<"积极乐观">
        emotion_1<"期待">
        emotion_2<"兴奋">
        emotion_3<"焦虑">
    end

    %% 边关系
    event_https://www.theverge.com/?p=875309 -.->|leads_to| phenomenon_0
    event_https://www.theverge.com/?p=875309 -.->|leads_to| phenomenon_1
    event_https://www.theverge.com/?p=875309 -.->|leads_to| phenomenon_2
    event_https://www.theverge.com/?p=875309 -.->|leads_to| phenomenon_3
    event_https://techcrunch.com/?p=3090538 -.->|leads_to| phenomenon_0
    event_https://techcrunch.com/?p=3090538 -.->|leads_to| phenomenon_1
    event_https://techcrunch.com/?p=3090538 -.->|leads_to| phenomenon_2
    event_https://techcrunch.com/?p=3090538 -.->|leads_to| phenomenon_3
    event_https://www.theverge.com/?p=875692 -.->|leads_to| phenomenon_0
    event_https://www.theverge.com/?p=875692 -.->|leads_to| phenomenon_1
    event_https://www.theverge.com/?p=875692 -.->|leads_to| phenomenon_2
    event_https://www.theverge.com/?p=875692 -.->|leads_to| phenomenon_3
    event_-5681179609737676210 -.->|leads_to| phenomenon_0
    event_-5681179609737676210 -.->|leads_to| phenomenon_1
    event_-5681179609737676210 -.->|leads_to| phenomenon_2
    event_-5681179609737676210 -.->|leads_to| phenomenon_3
    event_https://www.theverge.com/?p=874895 -.->|leads_to| phenomenon_0
    event_https://www.theverge.com/?p=874895 -.->|leads_to| phenomenon_1
    event_https://www.theverge.com/?p=874895 -.->|leads_to| phenomenon_2
    event_https://www.theverge.com/?p=874895 -.->|leads_to| phenomenon_3
    event_4711335956247921672 -.->|leads_to| phenomenon_0
    event_4711335956247921672 -.->|leads_to| phenomenon_1
    event_4711335956247921672 -.->|leads_to| phenomenon_2
    event_4711335956247921672 -.->|leads_to| phenomenon_3
    event_2639416489023408832 -.->|leads_to| phenomenon_0
    event_2639416489023408832 -.->|leads_to| phenomenon_1
    event_2639416489023408832 -.->|leads_to| phenomenon_2
    event_2639416489023408832 -.->|leads_to| phenomenon_3
    event_5845899813940419802 -.->|leads_to| phenomenon_0
    event_5845899813940419802 -.->|leads_to| phenomenon_1
    event_5845899813940419802 -.->|leads_to| phenomenon_2
    event_5845899813940419802 -.->|leads_to| phenomenon_3
    event_-7251073919150803577 -.->|leads_to| phenomenon_0
    event_-7251073919150803577 -.->|leads_to| phenomenon_1
    event_-7251073919150803577 -.->|leads_to| phenomenon_2
    event_-7251073919150803577 -.->|leads_to| phenomenon_3
    event_6565944244376916220 -.->|leads_to| phenomenon_0
    event_6565944244376916220 -.->|leads_to| phenomenon_1
    event_6565944244376916220 -.->|leads_to| phenomenon_2
    event_6565944244376916220 -.->|leads_to| phenomenon_3
    phenomenon_0 -.->|influences| emotion_0
    phenomenon_0 -.->|influences| emotion_1
    phenomenon_0 -.->|influences| emotion_2
    phenomenon_0 -.->|influences| emotion_3
    phenomenon_1 -.->|influences| emotion_0
    phenomenon_1 -.->|influences| emotion_1
    phenomenon_1 -.->|influences| emotion_2
    phenomenon_1 -.->|influences| emotion_3
    phenomenon_2 -.->|influences| emotion_0
    phenomenon_2 -.->|influences| emotion_1
    phenomenon_2 -.->|influences| emotion_2
    phenomenon_2 -.->|influences| emotion_3
    phenomenon_3 -.->|influences| emotion_0
    phenomenon_3 -.->|influences| emotion_1
    phenomenon_3 -.->|influences| emotion_2
    phenomenon_3 -.->|influences| emotion_3

    %% 节点样式
    classDef event fill:#e1f5fe,stroke:#01579b
    classDef phenomenon fill:#fff3e0,stroke:#e65100
    classDef psychology fill:#f3e5f5,stroke:#4a148c

    class event_https://www.theverge.com/?p=875309,event_https://techcrunch.com/?p=3090538,event_https://www.theverge.com/?p=875692,event_-5681179609737676210,event_https://www.theverge.com/?p=874895,event_4711335956247921672,event_2639416489023408832,event_5845899813940419802,event_-7251073919150803577,event_6565944244376916220 event
    class phenomenon_0,phenomenon_1,phenomenon_2,phenomenon_3 phenomenon
    class emotion_0,emotion_1,emotion_2,emotion_3 psychology
```
