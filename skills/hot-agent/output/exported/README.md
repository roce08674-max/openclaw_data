# 📦 知识图谱导出文件说明

**生成时间**: 2026-02-10 02:20 GMT+8
**数据来源**: Ultimate Hot Topic Agent (89个平台)
**话题数量**: 50个话题
**关系数量**: 1,504条边

---

## 📁 导出文件列表

| 文件名 | 大小 | 格式 | 用途 |
|--------|------|------|------|
| `knowledge_graph.json` | 229 KB | JSON | 程序处理、API集成 |
| `knowledge_graph.csv` | 62 KB | CSV | Excel打开、电子表格分析 |
| `knowledge_graph.graphml` | 184 KB | GraphML | Gephi、Cytoscape等专业软件 |
| `knowledge_graph.ttl` | 82 KB | Turtle/RDF | 语义网、知识图谱数据库 |

**输出目录**: `skills/hot-agent/output/exported/`

---

## 📄 格式详细说明

### 1. JSON 格式 (`knowledge_graph.json`)

**用途**: 程序处理、API集成、数据存储

**结构**:
```json
{
  "metadata": {
    "graph_id": "ultimate_kg_20260210022055",
    "export_time": "2026-02-10T02:20:55.294927",
    "statistics": {...}
  },
  "nodes": [
    {
      "id": "topic_00115",
      "type": "topic",
      "name": "巴以冲突升级国际关注",
      "attributes": {
        "category": "国际",
        "region": "CN",
        "platform": "腾讯新闻",
        "heat_score": 95.0,
        "sentiment": "positive",
        "keywords": ["热点", "热门"]
      }
    }
  ],
  "edges": [
    {
      "source": "topic_00115",
      "target": "category_000",
      "relationship": "belongs_to",
      "weight": 1.0
    }
  ]
}
```

**使用示例**:
```python
import json

with open('knowledge_graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
# 处理节点
for node in data['nodes']:
    print(node['name'], node['attributes']['heat_score'])

# 处理边
for edge in data['edges']:
    print(f"{edge['source']} --[{edge['relationship']}]--> {edge['target']}")
```

---

### 2. CSV 格式 (`knowledge_graph.csv`)

**用途**: Excel打开、表格分析、统计处理

**结构**:
```csv
=== 节点 (Nodes) ===
id,type,name,category,region,platform,heat_score,sentiment,velocity,keywords
topic_00115,topic,巴以冲突升级国际关注,国际,CN,腾讯新闻,95.0,positive,stable,"热点|热门"

=== 边 (Edges) ===
source,target,relationship,weight
topic_00115,category_000,belongs_to,1.0
```

**使用示例**:
```python
import pandas as pd

# 读取节点
nodes_df = pd.read_csv('knowledge_graph.csv', skiprows=1, nrows=50)
print(nodes_df[['name', 'category', 'heat_score']].head(10))

# 筛选科技话题
tech_topics = nodes_df[nodes_df['category'] == '科技']
print(tech_topics.sort_values('heat_score', ascending=False))
```

**Excel打开**:
1. 打开Excel
2. 导入CSV文件
3. 使用数据透视表分析
4. 创建图表

---

### 3. GraphML 格式 (`knowledge_graph.graphml`)

**用途**: 专业图分析软件、Gephi、Cytoscape、yEd

**结构**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="name" for="node" attr.name="name" attr.type="string"/>
  <key id="type" for="node" attr.name="type" attr.type="string"/>
  <key id="heat_score" for="node" attr.name="heat_score" attr.type="double"/>
  
  <graph id="G" edgedefault="directed">
    <node id="topic_00115">
      <data key="name">巴以冲突升级国际关注</data>
      <data key="type">topic</data>
      <data key="heat_score">95.0</data>
    </node>
    ...
  </graph>
</graphml>
```

**使用软件**:

**Gephi (推荐)**:
1. 下载Gephi: https://gephi.org/
2. 打开 `knowledge_graph.graphml`
3. 使用布局算法（ForceAtlas2、Yifan Hu）
4. 按分类着色节点
5. 导出PNG/SVG

**Cytoscape**:
1. 下载Cytoscape: https://cytoscape.org/
2. File → Import → Network from File
3. 选择 `knowledge_graph.graphml`
4. 使用分析功能

**yEd**:
1. 下载yEd: https://yed.yworks.com/
2. File → Open
3. 选择 `knowledge_graph.graphml`
4. 自动布局

---

### 4. Turtle/RDF 格式 (`knowledge_graph.ttl`)

**用途**: 语义网、链接数据、知识图谱数据库

**结构**:
```turtle
@prefix kg: <http://knowledge-graph.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# 话题节点
kg:topic_00115 rdf:type kg:topic .
kg:topic_00115 rdfs:label "巴以冲突升级国际关注" .
kg:topic_00115 kg:category "国际" .
kg:topic_00115 kg:region "CN" .
kg:topic_00115 kg:platform "腾讯新闻" .
kg:topic_00115 kg:heatScore 95.0 .

# 关系
kg:topic_00115 kg:belongs_to kg:category_000 .
```

**使用软件**:

**Apache Jena**:
```bash
# 安装
wget https://dlcdn.apache.org/jena/binaries/apache-jena-4.9.0.tar.gz
tar -xzf apache-jena-4.9.0.tar.gz

# 查询
./apache-jena-4.9.0/bin/tdbquery --dataset=/path/to/tdb --query "
PREFIX kg: <http://knowledge-graph.org/>
SELECT ?topic ?score WHERE {
  ?topic kg:heatScore ?score .
}
ORDER BY DESC(?score)
LIMIT 10
"
```

**Protégé**:
1. 下载Protégé: https://protege.stanford.edu/
2. File → Open
3. 选择 `knowledge_graph.ttl`
4. 推理和分析

---

## 📊 数据统计

### 节点统计

| 类型 | 数量 | 说明 |
|------|------|------|
| 话题节点 | 50 | 热点话题 |
| 分类节点 | 6 | 科技、财经、社会、娱乐、体育、国际 |
| 关键词节点 | 2 | 热点、热门 |
| 地区节点 | 5 | CN、US、UK、JP、EU |
| 平台节点 | 37 | 发布平台 |

### 边统计

| 关系类型 | 数量 | 说明 |
|----------|------|------|
| related | 1,225 | 话题相似关系 |
| has_keyword | 50 | 话题-关键词 |
| belongs_to | 50 | 话题-分类 |
| from_region | 50 | 话题-地区 |
| published_on | 50 | 话题-平台 |
| ranked_below | 29 | 排名关系 |

---

## 🎯 使用场景推荐

| 场景 | 推荐格式 | 原因 |
|------|----------|------|
| 程序处理 | JSON | 结构化、易解析 |
| 统计分析 | CSV | Excel兼容、数据透视 |
| 可视化展示 | HTML | 交互式、浏览器打开 |
| 专业分析 | GraphML | Gephi/Cytoscape |
| 语义查询 | Turtle | RDF、SPARQL查询 |
| 知识库 | Turtle | 链接数据标准 |

---

## 📥 下载文件

**文件位置**: `skills/hot-agent/output/exported/`

```bash
# 查看文件
ls -lh skills/hot-agent/output/exported/

# 复制到本地
cp skills/hot-agent/output/exported/knowledge_graph.json .
cp skills/hot-agent/output/exported/knowledge_graph.csv .
cp skills/hot-agent/output/exported/knowledge_graph.graphml .
cp skills/hot-agent/output/exported/knowledge_graph.ttl .
```

---

## 🔗 相关文件

- **知识图谱可视化**: `skills/hot-agent/output/ultimate_knowledge_graph_visualization.md`
- **源代码**: `skills/hot-topic-agent/scripts/ultimate_hot_topic_agent_v2.py`
- **导出工具**: `skills/hot-topic-agent/scripts/export_knowledge_graph.py`

---

*生成时间: 2026-02-10 02:20 GMT+8*
*Powered by Ultimate Hot Topic Agent*
