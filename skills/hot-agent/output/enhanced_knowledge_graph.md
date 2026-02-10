# 增强版知识图谱: 热点事件分析
**生成时间**: 2026-02-09T23:04:57.168082
**节点数**: 16 | **边数**: 64

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
    event_0["人工智能大模型再获突破，行业迎来新变革..."]
    event_1["新能源汽车销量持续增长，市场格局生变..."]
    event_2["房地产市场政策调整，买房时机引关注..."]
    event_3["科技巨头发布新品，引领行业发展新趋势..."]
    event_4["社会热点事件引发广泛讨论，舆论持续发酵..."]
    event_5["国际形势复杂多变，经济影响逐步显现..."]
    event_6["5G网络商用加速，产业数字化转型..."]
    event_7["互联网平台监管加强，规范行业发展..."]

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
    class event_0,event_1,event_2,event_3,event_4,event_5,event_6,event_7 event
    class phenomenon_0,phenomenon_1,phenomenon_2,phenomenon_3 phenomenon
    class emotion_0,emotion_1,emotion_2,emotion_3 psychology
```

---

## 📊 嵌入分析结果

### 事件相似度 TOP 10

| 事件1 | 事件2 | 相似度 |
|-------|-------|--------|
| 科技巨头发布新品，引领行业发展新趋势 | 国际形势复杂多变，经济影响逐步显现 | 0.997 |
| 科技巨头发布新品，引领行业发展新趋势 | 互联网平台监管加强，规范行业发展 | 0.996 |
| 人工智能大模型再获突破，行业迎来新变革 | 社会热点事件引发广泛讨论，舆论持续发酵 | 0.9952 |
| 人工智能大模型再获突破，行业迎来新变革 | 国际形势复杂多变，经济影响逐步显现 | 0.9944 |
| 社会热点事件引发广泛讨论，舆论持续发酵 | 国际形势复杂多变，经济影响逐步显现 | 0.9944 |
| 人工智能大模型再获突破，行业迎来新变革 | 科技巨头发布新品，引领行业发展新趋势 | 0.9938 |
| 新能源汽车销量持续增长，市场格局生变 | 互联网平台监管加强，规范行业发展 | 0.9938 |
| 人工智能大模型再获突破，行业迎来新变革 | 新能源汽车销量持续增长，市场格局生变 | 0.9935 |
| 国际形势复杂多变，经济影响逐步显现 | 互联网平台监管加强，规范行业发展 | 0.9935 |
| 人工智能大模型再获突破，行业迎来新变革 | 互联网平台监管加强，规范行业发展 | 0.9934 |

### 事件聚类

- **cluster_0**: 
- **cluster_1**: 人工智能大模型再获突破，行业迎来新变革, 新能源汽车销量持续增长，市场格局生变, 房地产市场政策调整，买房时机引关注, 科技巨头发布新品，引领行业发展新趋势, 社会热点事件引发广泛讨论，舆论持续发酵, 国际形势复杂多变，经济影响逐步显现, 5G网络商用加速，产业数字化转型, 互联网平台监管加强，规范行业发展

### 链接预测

| 预测事件 | 分数 |
|---------|------|
| 社会热点事件引发广泛讨论，舆论持续发酵 | 0.9952 |
| 国际形势复杂多变，经济影响逐步显现 | 0.9944 |
| 科技巨头发布新品，引领行业发展新趋势 | 0.9938 |