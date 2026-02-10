#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱导出工具

支持导出格式：
1. JSON - 机器可读，用于程序处理
2. HTML - 交互式可视化网页
3. CSV - 电子表格格式
4. GraphML - 专业图数据库格式
5. Turtle - RDF语义网格式

作者: OpenClaw Agent
创建时间: 2026-02-10
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class KnowledgeGraphExporter:
    """知识图谱导出器"""

    def __init__(self, graph_data: Dict[str, Any]):
        self.graph = graph_data
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_json(self, output_path: str = None) -> str:
        """导出为JSON格式"""
        export_data = {
            "metadata": {
                "graph_id": self.graph.get("graph_id", "unknown"),
                "export_time": datetime.now().isoformat(),
                "statistics": self.graph.get("statistics", {})
            },
            "nodes": self.graph.get("nodes", []),
            "edges": self.graph.get("edges", [])
        }

        content = json.dumps(export_data, ensure_ascii=False, indent=2)
        
        if output_path is None:
            output_path = f"/tmp/knowledge_graph_{self.timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path

    def export_html(self, output_path: str = None) -> str:
        """导出为交互式HTML网页"""
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Knowledge Graph - 可视化</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }}
        
        header h1 {{
            font-size: 2.5em;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}
        
        header .subtitle {{
            color: rgba(255,255,255,0.7);
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-card .label {{
            color: rgba(255,255,255,0.7);
            margin-top: 5px;
        }}
        
        #network {{
            width: 100%;
            height: 600px;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }}
        
        .controls {{
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .control-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .control-group label {{
            color: rgba(255,255,255,0.8);
        }}
        
        select, button {{
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        select:hover, button:hover {{
            background: rgba(255,255,255,0.2);
            border-color: #00d4ff;
        }}
        
        button {{
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
        }}
        
        .sections {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        
        @media (max-width: 1000px) {{
            .sections {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .section h2 {{
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        
        .topic-list {{
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .topic-item {{
            padding: 15px;
            margin-bottom: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .topic-item:hover {{
            background: rgba(255,255,255,0.1);
            transform: translateX(5px);
        }}
        
        .topic-item .title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .topic-item .meta {{
            font-size: 0.85em;
            color: rgba(255,255,255,0.6);
        }}
        
        .topic-item .heat {{
            float: right;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: rgba(255,255,255,0.5);
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 30px;
        }}
        
        .legend {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 Ultimate Knowledge Graph</h1>
            <p class="subtitle">完整知识图谱可视化 - 50个话题 · 89个平台 · 7个地区 · 1500+关系</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{len(self.graph.get('nodes', []))}</div>
                <div class="label">节点总数</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(self.graph.get('edges', []))}</div>
                <div class="label">关系总数</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(set(n.get('attributes', {{}}).get('category', '') for n in self.graph.get('nodes', []) if n.get('type') == 'topic'))}</div>
                <div class="label">分类数</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(set(n.get('attributes', {{}}).get('region', '') for n in self.graph.get('nodes', []) if n.get('type') == 'topic'))}</div>
                <div class="label">地区数</div>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #2196F3;"></div>
                <span>科技</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #4CAF50;"></div>
                <span>财经</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FF9800;"></div>
                <span>社会</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #E91E63;"></div>
                <span>娱乐</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #9C27B0;"></div>
                <span>体育</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #00BCD4;"></div>
                <span>国际</span>
            </div>
        </div>
        
        <div id="network"></div>
        
        <div class="controls">
            <div class="control-group">
                <label>布局:</label>
                <select id="layout">
                    <option value="forceDirected">力导向</option>
                    <option value="breadthfirst">广度优先</option>
                    <option value="cose">COSE</option>
                </select>
            </div>
            <div class="control-group">
                <label>分类:</label>
                <select id="categoryFilter">
                    <option value="all">全部</option>
                    <option value="科技">科技</option>
                    <option value="财经">财经</option>
                    <option value="社会">社会</option>
                    <option value="娱乐">娱乐</option>
                    <option value="体育">体育</option>
                    <option value="国际">国际</option>
                </select>
            </div>
            <button onclick="zoomIn()">放大</button>
            <button onclick="zoomOut()">缩小</button>
            <button onclick="fitNetwork()">自适应</button>
            <button onclick="exportPNG()">导出PNG</button>
        </div>
        
        <div class="sections">
            <div class="section">
                <h2>🔥 热门话题 TOP 20</h2>
                <div class="topic-list" id="topicList">
                    <!-- Topics will be populated by JS -->
                </div>
            </div>
            <div class="section">
                <h2>📊 分类分布</h2>
                <div class="topic-list" id="categoryList">
                    <!-- Categories will be populated by JS -->
                </div>
            </div>
        </div>
        
        <footer>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Powered by Ultimate Hot Topic Agent</p>
        </footer>
    </div>
    
    <script>
        // Prepare data for vis.js
        var nodes = new vis.DataSet([]);
        var edges = new vis.DataSet([]);
        
        // Node type colors
        var colors = {{
            'topic': {{
                '科技': '#2196F3',
                '财经': '#4CAF50',
                '社会': '#FF9800',
                '娱乐': '#E91E63',
                '体育': '#9C27B0',
                '国际': '#00BCD4'
            }},
            'category': '#7b2cbf',
            'keyword': '#feca57',
            'region': '#48dbfb',
            'platform': '#ff6b6b'
        }};
        
        // Add nodes
        var topics = {json.dumps(self.graph.get('nodes', []), ensure_ascii=False)};
        topics.forEach(function(node) {{
            var color = colors.topic[node.attributes.category] || '#607D8B';
            if (node.type === 'category') color = colors.category;
            else if (node.type === 'keyword') color = colors.keyword;
            else if (node.type === 'region') color = colors.region;
            else if (node.type === 'platform') color = colors.platform;
            
            nodes.add({{
                id: node.id,
                label: node.name.length > 20 ? node.name.substring(0, 20) + '...' : node.name,
                title: node.name,
                group: node.type,
                value: node.attributes.heat_score || 1
            }});
        }});
        
        // Add edges
        var edgeData = {json.dumps(self.graph.get('edges', []), ensure_ascii=False)};
        edgeData.forEach(function(edge) {{
            edges.add({{
                from: edge.source,
                to: edge.target,
                arrows: 'to',
                width: edge.weight * 2,
                color: {{ opacity: 0.6 }}
            }});
        }});
        
        // Create network
        var container = document.getElementById('network');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            nodes: {{
                shape: 'dot',
                size: 10,
                font: {{
                    size: 12,
                    color: '#ffffff'
                }},
                borderWidth: 2
            }},
            edges: {{
                width: 1,
                color: {{
                    color: '#ffffff',
                    opacity: 0.6
                }},
                smooth: {{
                    type: 'continuous'
                }}
            }},
            physics: {{
                forceAtlas2Based: {{
                    gravitationalConstant: -26,
                    centralGravity: 0.005,
                    springLength: 230,
                    springConstant: 0.18
                }},
                maxVelocity: 146,
                solver: 'forceAtlas2Based',
                timestep: 0.35,
                stabilization: {{ iterations: 150 }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                navigationButtons: true,
                keyboard: true
            }}
        }};
        
        var network = new vis.Network(container, data, options);
        
        // Handle layout change
        document.getElementById('layout').addEventListener('change', function(e) {{
            var options = {{
                layout: {{
                    hierarchical: e.target.value === 'hierarchical' ? {{
                        direction: 'UD',
                        sortMethod: 'directedness'
                    }} : false
                }},
                physics: e.target.value === 'hierarchical' ? {{ enabled: false }} : {{
                    enabled: true
                }}
            }};
            network.setOptions(options);
        }});
        
        // Handle category filter
        document.getElementById('categoryFilter').addEventListener('change', function(e) {{
            var category = e.target.value;
            if (category === 'all') {{
                nodes.forEach(function(node) {{
                    nodes.update({{id: node.id, hidden: false}});
                }});
            }} else {{
                nodes.forEach(function(node) {{
                    var isTopic = node.group === 'topic';
                    var isCorrectCategory = node.group === 'category' || 
                                         (node.title && node.title.includes(category));
                    nodes.update({{id: node.id, hidden: isTopic && !isCorrectCategory}});
                }});
            }}
        }});
        
        // Zoom functions
        function zoomIn() {{
            var scale = network.getScale();
            network.moveTo({{ scale: scale * 1.3 }});
        }}
        
        function zoomOut() {{
            var scale = network.getScale();
            network.moveTo({{ scale: scale / 1.3 }});
        }}
        
        function fitNetwork() {{
            network.fit({{ animation: true }});
        }}
        
        function exportPNG() {{
            var canvas = document.querySelector('#network canvas');
            var link = document.createElement('a');
            link.download = 'knowledge_graph_' + new Date().toISOString().slice(0,10) + '.png';
            link.href = canvas.toDataURL();
            link.click();
        }}
        
        // Populate topic list
        var topicList = document.getElementById('topicList');
        var sortedTopics = topics.filter(function(n) {{ return n.type === 'topic'; }})
            .sort(function(a, b) {{ return (b.attributes.heat_score || 0) - (a.attributes.heat_score || 0); }})
            .slice(0, 20);
        
        sortedTopics.forEach(function(topic, index) {{
            var div = document.createElement('div');
            div.className = 'topic-item';
            div.innerHTML = `
                <span class="heat">${{topic.attributes.heat_score || 0}}</span>
                <div class="title">${{index + 1}}. ${{topic.name}}</div>
                <div class="meta">${{topic.attributes.platform || ''}} · ${{topic.attributes.category || ''}} · ${{topic.attributes.region || ''}}</div>
            `;
            div.onclick = function() {{
                network.focus(topic.id, {{
                    scale: 1.2,
                    animation: true
                }});
            }};
            topicList.appendChild(div);
        }});
        
        // Populate category list
        var categoryList = document.getElementById('categoryList');
        var categories = ['科技', '财经', '社会', '娱乐', '体育', '国际'];
        var categoryCounts = {{}};
        topics.filter(function(n) {{ return n.type === 'topic'; }})
            .forEach(function(topic) {{
                var cat = topic.attributes.category;
                categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
            }});
        
        categories.forEach(function(cat) {{
            var count = categoryCounts[cat] || 0;
            var div = document.createElement('div');
            div.className = 'topic-item';
            div.innerHTML = `
                <span class="heat">${{count}}</span>
                <div class="title">${{cat}}</div>
                <div class="meta">话题数量</div>
            `;
            categoryList.appendChild(div);
        }});
    </script>
</body>
</html>
"""
        
        if output_path is None:
            output_path = f"/tmp/knowledge_graph_{self.timestamp}.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path

    def export_csv(self, output_path: str = None) -> str:
        """导出为CSV格式"""
        lines = []
        
        # 节点CSV
        lines.append("=== 节点 (Nodes) ===")
        lines.append("id,type,name,category,region,platform,heat_score,sentiment,velocity,keywords")
        
        for node in self.graph.get('nodes', []):
            attrs = node.get('attributes', {})
            keywords = '|'.join(attrs.get('keywords', []))
            # Escape quotes in name
            name = node['name'].replace('"', '""')
            line = f"{node['id']},{node['type']},{name},{attrs.get('category','')},{attrs.get('region','')},{attrs.get('platform','')},{attrs.get('heat_score','')},{attrs.get('sentiment','')},{attrs.get('velocity','')},\"{keywords}\""
            lines.append(line)
        
        lines.append("")
        
        # 边CSV
        lines.append("=== 边 (Edges) ===")
        lines.append("source,target,relationship,weight")
        
        for edge in self.graph.get('edges', []):
            line = f"{edge['source']},{edge['target']},{edge['relationship']},{edge['weight']}"
            lines.append(line)
        
        content = '\n'.join(lines)
        
        if output_path is None:
            output_path = f"/tmp/knowledge_graph_{self.timestamp}.csv"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path

    def export_graphml(self, output_path: str = None) -> str:
        """导出为GraphML格式（专业图数据库格式）"""
        
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
            '  <key id="name" for="node" attr.name="name" attr.type="string"/>',
            '  <key id="type" for="node" attr.name="type" attr.type="string"/>',
            '  <key id="category" for="node" attr.name="category" attr.type="string"/>',
            '  <key id="region" for="node" attr.name="region" attr.type="string"/>',
            '  <key id="platform" for="node" attr.name="platform" attr.type="string"/>',
            '  <key id="heat_score" for="node" attr.name="heat_score" attr.type="double"/>',
            '  <key id="sentiment" for="node" attr.name="sentiment" attr.type="string"/>',
            '  <key id="velocity" for="node" attr.name="velocity" attr.type="string"/>',
            '  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>',
            f'  <graph id="G" edgedefault="directed">',
        ]
        
        # 添加节点
        for node in self.graph.get('nodes', []):
            attrs = node.get('attributes', {})
            lines.append(f'    <node id="{node["id"]}">')
            lines.append(f'      <data key="name">{node["name"]}</data>')
            lines.append(f'      <data key="type">{node["type"]}</data>')
            lines.append(f'      <data key="category">{attrs.get("category", "")}</data>')
            lines.append(f'      <data key="region">{attrs.get("region", "")}</data>')
            lines.append(f'      <data key="platform">{attrs.get("platform", "")}</data>')
            lines.append(f'      <data key="heat_score">{attrs.get("heat_score", 0)}</data>')
            lines.append(f'      <data key="sentiment">{attrs.get("sentiment", "")}</data>')
            lines.append(f'      <data key="velocity">{attrs.get("velocity", "")}</data>')
            lines.append(f'    </node>')
        
        # 添加边
        for edge in self.graph.get('edges', []):
            lines.append(f'    <edge source="{edge["source"]}" target="{edge["target"]}">')
            lines.append(f'      <data key="weight">{edge["weight"]}</data>')
            lines.append(f'    </edge>')
        
        lines.append('  </graph>')
        lines.append('</graphml>')
        
        content = '\n'.join(lines)
        
        if output_path is None:
            output_path = f"/tmp/knowledge_graph_{self.timestamp}.graphml"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path

    def export_turtle(self, output_path: str = None) -> str:
        """导出为Turtle格式（RDF语义网格式）"""
        
        lines = [
            '@prefix kg: <http://knowledge-graph.org/> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
            '',
            f'# Knowledge Graph: {self.graph.get("graph_id", "unknown")}',
            f'# Generated: {datetime.now().isoformat()}',
            '',
        ]
        
        # 添加节点
        for node in self.graph.get('nodes', []):
            attrs = node.get('attributes', {})
            node_uri = f'kg:{node["id"]}'
            
            lines.append(f'{node_uri} rdf:type kg:{node["type"]} .')
            lines.append(f'{node_uri} rdfs:label "{node["name"]}" .')
            
            if attrs.get('category'):
                lines.append(f'{node_uri} kg:category "{attrs["category"]}" .')
            if attrs.get('region'):
                lines.append(f'{node_uri} kg:region "{attrs["region"]}" .')
            if attrs.get('platform'):
                lines.append(f'{node_uri} kg:platform "{attrs["platform"]}" .')
            if attrs.get('heat_score'):
                lines.append(f'{node_uri} kg:heatScore {attrs["heat_score"]} .')
            if attrs.get('sentiment'):
                lines.append(f'{node_uri} kg:sentiment "{attrs["sentiment"]}" .')
            
            lines.append('')
        
        # 添加边
        for edge in self.graph.get('edges', []):
            source_uri = f'kg:{edge["source"]}'
            target_uri = f'kg:{edge["target"]}'
            rel = edge['relationship'].replace(' ', '_')
            
            lines.append(f'{source_uri} kg:{rel} {target_uri} .')
        
        content = '\n'.join(lines)
        
        if output_path is None:
            output_path = f"/tmp/knowledge_graph_{self.timestamp}.ttl"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path

    def export_all(self, output_dir: str = "/tmp") -> Dict[str, str]:
        """导出所有格式"""
        results = {}
        
        # JSON
        try:
            path = self.export_json(f"{output_dir}/knowledge_graph.json")
            results['json'] = path
            print(f"✅ JSON: {path}")
        except Exception as e:
            print(f"❌ JSON导出失败: {e}")
        
        # HTML
        try:
            path = self.export_html(f"{output_dir}/knowledge_graph.html")
            results['html'] = path
            print(f"✅ HTML: {path}")
        except Exception as e:
            print(f"❌ HTML导出失败: {e}")
        
        # CSV
        try:
            path = self.export_csv(f"{output_dir}/knowledge_graph.csv")
            results['csv'] = path
            print(f"✅ CSV: {path}")
        except Exception as e:
            print(f"❌ CSV导出失败: {e}")
        
        # GraphML
        try:
            path = self.export_graphml(f"{output_dir}/knowledge_graph.graphml")
            results['graphml'] = path
            print(f"✅ GraphML: {path}")
        except Exception as e:
            print(f"❌ GraphML导出失败: {e}")
        
        # Turtle
        try:
            path = self.export_turtle(f"{output_dir}/knowledge_graph.ttl")
            results['turtle'] = path
            print(f"✅ Turtle: {path}")
        except Exception as e:
            print(f"❌ Turtle导出失败: {e}")
        
        return results


def main():
    """主函数"""
    print("=" * 80)
    print("📦 Knowledge Graph Exporter - 知识图谱导出工具")
    print("=" * 80)
    
    # 导入并生成数据
    import sys
    sys.path.insert(0, '.')
    from ultimate_hot_topic_agent_v2 import UltimateHotTopicAgent
    
    print("\n🔄 生成知识图谱数据...")
    agent = UltimateHotTopicAgent()
    agent._generate_comprehensive_data()
    topics = agent.get_trending(top_k=50)
    graph = agent.build_knowledge_graph(topics)
    
    # 创建导出器
    exporter = KnowledgeGraphExporter(graph)
    
    # 导出所有格式
    print("\n📤 导出知识图谱...")
    results = exporter.export_all("/tmp")
    
    print("\n" + "=" * 80)
    print("✅ 导出完成！")
    print("=" * 80)
    
    print(f"\n📁 导出的文件:")
    for fmt, path in results.items():
        print(f"  {fmt.upper():8s}: {path}")
    
    print(f"\n💡 使用说明:")
    print("  - JSON: 程序处理、API集成")
    print("  - HTML: 浏览器打开交互式可视化")
    print("  - CSV: Excel打开分析")
    print("  - GraphML: Gephi、Cytoscape等专业软件")
    print("  - Turtle: 语义网、知识图谱数据库")


if __name__ == "__main__":
    main()
