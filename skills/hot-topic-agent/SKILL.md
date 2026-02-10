# Hot Topic Agent Skill

A comprehensive skill for collecting, analyzing, and generating insights from hot topics and trending news across multiple platforms. Supports real-time data collection, trend analysis, sentiment analysis, and knowledge graph generation.

## Features

### Data Collection
- **Multi-source collection**: Gather hot topics from Chinese social media (Weibo, Zhihu, Douyin, Bilibili, Xiaohongshu) and international sources (Twitter, Reddit, Hacker News)
- **Real-time monitoring**: Track trending topics with heat scores and velocity metrics
- **Historical data**: Access historical trending data for trend analysis

### Analysis
- **Trend detection**: Identify rising trends and viral content
- **Sentiment analysis**: Analyze public sentiment on trending topics
- **Topic clustering**: Group similar trending topics automatically
- **Influence scoring**: Measure the spread and impact of trending topics

### Integration
- **Knowledge graph**: Generate knowledge graphs from trending topics
- **Browser tool**: Use OpenClaw browser for direct web data collection
- **MCP compatibility**: Can be extended with MCP servers for specific platforms

## Usage

### Basic Usage

```python
# Collect hot topics from all platforms
from hot_topic_agent import HotTopicAgent

agent = HotTopicAgent()
topics = agent.collect_all(limit=50)

# Filter by platform
weibo_topics = agent.collect_from_platform("weibo", limit=20)

# Get trending topics with heat scores
trending = agent.get_trending(top_k=10)
```

### Advanced Usage

```python
# Sentiment analysis
sentiment = agent.analyze_sentiment(topic_id)

# Trend prediction
predictions = agent.predict_trends(hours_ahead=24)

# Knowledge graph generation
kg = agent.build_knowledge_graph(topics)
```

### Integration with Browser

The skill uses OpenClaw browser tool for web-based data collection:

```bash
# Start browser
browser action=start profile=openclaw

# Collect data from specific platform
browser action=open targetUrl="https://weibo.com/热搜"

# Take snapshot for analysis
browser action=snapshot
```

## Configuration

### Supported Platforms

| Platform | Type | Update Frequency | Data Quality |
|----------|------|------------------|--------------|
| Weibo (微博) | CN Social | Real-time | High |
| Zhihu (知乎) | CN QA | Hourly | High |
| Douyin (抖音) | CN Video | Real-time | High |
| Bilibili (哔哩) | CN Video | Real-time | High |
| Xiaohongshu (小红书) | CN Social | Hourly | Medium |
| Twitter/X | Intl Social | Real-time | High |
| Hacker News | Tech | 10min | High |
| Reddit | Intl Social | Real-time | Medium |

### Environment Variables

```bash
# Optional API configurations
export WEIBO_COOKIE="your_cookie"  # For extended access
export ZHIHU_COOKIE="your_cookie"
export TWITTER_BEARER="your_bearer_token"
```

## Architecture

```
HotTopicAgent
├── DataCollector
│   ├── WeiboCollector
│   ├── ZhihuCollector
│   ├── DouyinCollector
│   ├── BilibiliCollector
│   ├── TwitterCollector
│   └── HackerNewsCollector
├── Analyzer
│   ├── TrendDetector
│   ├── SentimentAnalyzer
│   ├── TopicCluster
│   └── InfluenceScorer
├── KnowledgeGraphBuilder
│   └── GraphGenerator
└── BrowserIntegration
    └── BrowserCollector
```

## Example Output

```json
{
  "topics": [
    {
      "id": "topic_001",
      "title": "AI大模型再获突破",
      "platform": "weibo",
      "heat_score": 95,
      "velocity": "rising",
      "sentiment": "positive",
      "keywords": ["AI", "大模型", "技术突破"],
      "related_topics": ["ChatGPT", "AGI"]
    }
  ],
  "trends": [
    {
      "trend": "人工智能",
      "velocity": "+25%",
      "prediction": "continued_rising"
    }
  ]
}
```

## Best Practices

1. **Rate limiting**: Respect platform rate limits to avoid being blocked
2. **Session management**: Rotate sessions and cookies regularly
3. **Data validation**: Verify collected data quality before analysis
4. **Error handling**: Implement robust error handling for network issues
5. **Caching**: Cache frequently accessed data to reduce API calls

## Integration with Other Skills

### Combined with Knowledge Graph Skill
```python
# Collect topics
agent = HotTopicAgent()
topics = agent.collect_all(limit=20)

# Build knowledge graph
from knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph("Trending Topics")
kg.build_from_events(topics)
```

### Combined with Browser Tool
```python
# Use browser for real-time data
browser action=start profile=openclaw
browser action=open targetUrl="https://www.zhihu.com/hot"
browser action=snapshot
# Parse snapshot for trending topics
```

## Limitations

- Some platforms may require authentication for extended access
- Real-time data collection may be rate-limited
- Sentiment analysis accuracy varies by language and context
- Cross-platform correlation analysis requires sufficient data volume

## Further Reading

- [Anthropics Skills Documentation](https://github.com/anthropics/skills)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Webapp Testing Skill Pattern](./webapp-testing)
- [Knowledge Graph Skill](./knowledge-graph)
