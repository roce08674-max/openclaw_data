# 图文Agent - 智能配图生成

**创建时间**: 2026-02-08 20:56 GMT+8
**最后更新**: 2026-02-08 20:56 GMT+8
**用途**: 基于华为云Gitee AI的智能配图生成

---

## Agent概述

### 核心能力

图文Agent专注于为公众号文章生成高质量配图，具有以下核心能力：

智能配图生成：根据文章内容自动生成匹配的图片，支持多种风格和尺寸定制。

使用量监控：严格遵循每日100张的限制，自动跟踪使用量并提醒。

高质量输出：支持1024x1024高清分辨率，满足公众号配图需求。

### 技术架构

| 组件 | 技术 |
|------|------|
| **API提供商** | 华为云Gitee AI |
| **模型** | Z-Image |
| **接口方式** | OpenAI兼容API |
| **语言** | Python |
| **依赖** | openai, requests, base64 |

---

## API配置

### ⚠️ 安全说明

**重要**: API密钥是敏感数据，请勿直接写入代码！

### 安全配置方法

**方法1：使用环境变量（推荐）**

```python
import os
from dotenv import load_dotload

load_dotenv()
api_key = os.environ.get("GITEE_AI_API_KEY")
```

**方法2：创建.env文件**

在项目根目录创建 `.env` 文件：

```bash
# .env 文件内容
GITEE_AI_API_KEY=your_api_key_here
```

**方法3：运行时传入**

```python
agent = ImageAgent(
    api_key="your_api_key_here",
    base_url="https://ai.gitee.com/v1"
)
```

### 基础配置（示例，不含真实密钥）

```python
# API配置
BASE_URL = "https://ai.gitee.com/v1"
MODEL_NAME = "Z-Image"

# 默认参数
DEFAULT_SIZE = "1024x1024"
DEFAULT_GUIDANCE_SCALE = 5
DEFAULT_STEPS = 30
```

### 初始化客户端

```python
from openai import OpenAI
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class ImageAgent:
    """图文Agent - 智能配图生成"""
    
    def __init__(self, api_key=None, base_url=None):
        # 从环境变量获取API密钥
        if api_key is None:
            api_key = os.environ.get("GITEE_AI_API_KEY")
        
        self.client = OpenAI(
            base_url=base_url or "https://ai.gitee.com/v1",
            api_key=api_key
        )
        
        # 默认参数
        self.default_params = {
            "size": "1024x1024",
            "guidance_scale": 5,
            "num_inference_steps": 30
        }
        
        # 使用量跟踪
        self.usage_tracker = ImageUsageTracker(daily_limit=100)
```

---

## 使用规则

### 每日限制

| 规则 | 值 | 说明 |
|------|-----|------|
| **每日上限** | 100张 | UTC 0:00重置 |
| **单次请求** | 1张 | 默认为1张 |
| **超出处理** | 拒绝请求 | 返回友好错误 |

### 速率限制

遵循NVIDIA API规则：

| 限制项 | 值 | 应对策略 |
|--------|-----|---------|
| **RPS** | 1-2 | 控制请求间隔≥0.5秒 |
| **RPM** | 60 | 足够日常使用 |
| **并发数** | ≤5 | 使用信号量控制 |
| **HTTP 429** | 速率限制 | 指数退避（1s→2s→4s→8s） |

---

## 核心功能

### 1. 生成单张图片

```python
def generate_image(self, prompt, size=None, guidance_scale=None, 
                   num_inference_steps=None, save_path=None):
    """
    生成单张图片
    
    参数:
        prompt: 图片描述提示词
        size: 图片尺寸，默认1024x1024
        guidance_scale: 引导比例，默认5
        num_inference_steps: 推理步数，默认30
        save_path: 保存路径，为None则不保存
    
    返回:
        dict: 包含图片URL或base64数据
    """
    # 检查使用量
    if not self.usage_tracker.can_generate():
        return {
            "status": "error",
            "message": "今日配图生成已达上限（100张），请明天再试",
            "remaining": 0
        }
    
    # 设置参数
    params = {
        "model": "Z-Image",
        "prompt": prompt,
        "size": size or self.default_params["size"],
        "extra_body": {
            "guidance_scale": guidance_scale or self.default_params["guidance_scale"],
            "num_inference_steps": num_inference_steps or self.default_params["num_inference_steps"]
        }
    }
    
    try:
        # 调用API
        response = self.client.images.generate(**params)
        
        # 记录使用量
        self.usage_tracker.record_generation()
        
        # 处理结果
        result = {
            "status": "success",
            "usage": self.usage_tracker.get_remaining(),
            "images": []
        }
        
        for i, image_data in enumerate(response.data):
            image_info = {}
            
            if image_data.url:
                # 从URL下载
                ext = image_data.url.split('.')[-1].split('?')[0] or "jpg"
                filename = f"Z-Image-output-{i}.{ext}"
                
                img_response = requests.get(image_data.url, timeout=30)
                img_response.raise_for_status()
                
                image_info = {
                    "source": "url",
                    "url": image_data.url,
                    "filename": filename,
                    "data": img_response.content
                }
                
                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(img_response.content)
                        
            elif image_data.b64_json:
                # Base64解码
                image_bytes = base64.b64decode(image_data.b64_json)
                filename = f"Z-Image-output-{i}.jpg"
                
                image_info = {
                    "source": "base64",
                    "filename": filename,
                    "data": image_bytes
                }
                
                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(image_bytes)
            
            result["images"].append(image_info)
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"图片生成失败: {str(e)}",
            "usage": self.usage_tracker.get_remaining()
        }
```

### 2. 批量生成图片

```python
def generate_batch(self, prompts, size=None, delay=1):
    """
    批量生成图片
    
    参数:
        prompts: 提示词列表
        size: 图片尺寸
        delay: 请求间隔（秒），默认1秒
    
    返回:
        list: 生成结果列表
    """
    results = []
    
    for i, prompt in enumerate(prompts):
        # 检查是否超出限制
        if not self.usage_tracker.can_generate():
            results.append({
                "status": "error",
                "message": f"第{i+1}张：今日已达上限",
                "remaining": 0
            })
            break
        
        # 生成图片
        result = self.generate_image(prompt, size=size)
        results.append(result)
        
        # 添加延迟，避免触发速率限制
        if i < len(prompts) - 1:
            time.sleep(delay)
    
    return results
```

### 3. 提示词优化

```python
def optimize_prompt(self, article_context, style="general"):
    """
    根据文章内容优化生成提示词
    
    参数:
        article_context: 文章内容或主题
        style: 风格（general, tech, lifestyle, business）
    
    返回:
        str: 优化后的提示词
    """
    style_prompts = {
        "general": "high quality, detailed, professional",
        "tech": "futuristic, clean, technology-themed, digital",
        "lifestyle": "warm, cozy, lifestyle photography style",
        "business": "corporate, professional, clean design",
        "artistic": "artistic, creative, unique style"
    }
    
    # 基础优化
    optimized = f"{article_context}, {style_prompts.get(style, style_prompts['general'])}"
    
    # 添加质量标签
    quality_tags = ", 4K resolution, sharp focus, beautiful lighting"
    optimized += quality_tags
    
    return optimized
```

---

## 使用流程

### 标准工作流

```
1. 输入文章内容或主题
   ↓
2. 自动优化提示词
   ↓
3. 生成配图
   ↓
4. 监控使用量（每日≤100）
   ↓
5. 保存或返回图片
   ↓
6. 记录生成日志
```

### 示例调用

```python
# 初始化Agent
agent = ImageAgent()

# 输入文章主题
article_topic = "AI Agent成为2026年科技圈热点话题"

# 生成配图
result = agent.generate_image(
    prompt=agent.optimize_prompt(article_topic, style="tech"),
    save_path="output/ai-agent-cover.jpg"
)

# 检查结果
if result["status"] == "success":
    print(f"生成成功！剩余{result['usage']}张配额")
    print(f"图片已保存: {result['images'][0]['filename']}")
else:
    print(f"生成失败: {result['message']}")
```

---

## 提示词模板

### 公众号配图常用模板

#### 科技类文章
```
A modern technology workspace with AI elements, clean and professional, 
4K resolution, sharp focus, beautiful lighting, abstract digital patterns
```

#### 商业财经类
```
Professional business setting, clean corporate design, modern office environment,
high quality photography, 4K resolution, sharp focus
```

#### 生活方式类
```
Cozy lifestyle photography, warm tones, comfortable atmosphere,
natural lighting, high quality, 4K resolution
```

#### 热点新闻类
```
Breaking news illustration, professional design, clean layout,
high impact visual, 4K resolution, sharp focus
```

#### 教程指南类
```
Educational illustration, clear and concise, step-by-step visual guide,
clean design, 4K resolution, professional graphics
```

---

## 监控与告警

### 使用量监控

```python
def get_usage_status(self):
    """获取当前使用状态"""
    remaining = self.usage_tracker.get_remaining()
    percentage = (remaining / 100) * 100
    
    if remaining <= 0:
        level = "critical"
        message = "已达每日上限，请明天再试"
    elif percentage <= 20:
        level = "warning"
        message = f"剩余{remaining}张（{percentage:.0f}%），请注意使用"
    else:
        level = "normal"
        message = f"已使用{100-remaining}张，剩余{remaining}张"
    
    return {
        "level": level,
        "message": message,
        "used": 100 - remaining,
        "remaining": remaining,
        "reset_time": self.usage_tracker.reset_time.isoformat()
    }
```

### 告警配置

| 级别 | 阈值 | 动作 |
|------|------|------|
| **正常** | 剩余>20张 | 无特殊动作 |
| **警告** | 剩余≤20张 | 发送提醒 |
| **严重** | 剩余=0张 | 拒绝请求 |

---

## 常见问题

### Q1: 生成失败怎么办？

**检查步骤**:
1. 检查API密钥是否正确
2. 检查网络连接
3. 查看错误消息
4. 实施指数退避重试

**重试示例**:
```python
for attempt in range(3):
    try:
        result = agent.generate_image(prompt)
        if result["status"] == "success":
            break
    except Exception as e:
        wait_time = (2 ** attempt)
        time.sleep(wait_time)
```

### Q2: 图片质量不佳怎么调整？

**参数调优建议**:
- 增加`num_inference_steps`到50-100（更精细）
- 调整`guidance_scale`到7-10（更贴合提示词）
- 使用更详细的提示词描述

### Q3: 如何提高生成速度？

**优化建议**:
- 使用默认尺寸1024x1024
- 减少`num_inference_steps`到20-30
- 避免并发请求（速率限制）

---

## 最佳实践

### ✅ 推荐做法

- 使用提示词模板提高效率
- 定期检查使用量，避免达上限
- 保存成功案例的提示词
- 实施退避策略处理速率限制

### ❌ 避免做法

- 短时间内发送大量并发请求（触发429）
- 忽略每日100张的限制
- 不检查生成结果直接使用
- 将API密钥暴露在代码中

---

## 相关文档

- [NVIDIA API使用规则](nvidia-api-rules.md)
- [免费图片生成API汇总](free-image-generation-apis.md)
- [直接API调用项目](direct-api-image-generation.md)
- [公众号Agent使用指南](../docs/公众号文章agent使用指南.md)

---

**文档更新时间**: 2026-02-08 20:56 GMT+8
**维护者**: OpenClaw Agent
**API配置**: ✅ 已配置华为云Gitee AI
**每日限制**: ✅ 100张/天
**下次更新**: 规则变更时
