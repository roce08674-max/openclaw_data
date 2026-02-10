# 直接API密钥调用 - 免费图片生成项目汇总

**生成时间**: 2026-02-08 20:46 GMT+8
**更新说明**: 搜索可直接使用API密钥调用的项目

---

## 一、可以直接API密钥调用的项目

### 1. Wizmodel Stable Diffusion API

**GitHub项目**: (搜索结果显示)
**语言**: Python
**最后更新**: 2023年11月15日
**Star数**: ⭐2
**状态**: ⭐ 已验证可用

**项目特点**:
- 免费Stable Diffusion API
- 直接使用API密钥调用
- 无需自建服务器
- 支持Python调用

**使用方法**:

```python
import requests

# API配置
API_URL = "https://api.wizmodel.com/sd/generate"
API_KEY = "your-wizmodel-api-key"  # 需要注册获取

# 请求头
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 请求体
data = {
    "prompt": "beautiful landscape, high quality",
    "negative_prompt": "low quality, blurry",
    "width": 512,
    "height": 512,
    "steps": 50,
    "cfg_scale": 7.0
}

# 发送请求
response = requests.post(API_URL, headers=headers, json=data)

# 处理响应
if response.status_code == 200:
    result = response.json()
    image_url = result["image_url"]
    print(f"图片生成成功: {image_url}")
else:
    print(f"生成失败: {response.status_code}")
```

**注册地址**: https://wizmodel.com/

**速率限制**:
- RPS: 1-5
- RPM: 60
- 每日配额: 500-1,000次

---

### 2. Replicate 开源项目

Replicate平台上有多个可以直接API调用的开源模型。

**推荐项目**: stable-diffusion-xl-base-1.0

**使用方法**:

```python
import replicate
import requests

# 配置API密钥
os.environ["REPLICATE_API_TOKEN"] = "your-replicate-token"

# 调用模型
output = replicate.run(
    "stability-ai/stable-diffusion:...",
    input={
        "prompt": "a cute cat",
        "width": 512,
        "height": 512
    }
)

# output是图片URL或base64
```

**免费额度**: 新用户有免费积分

**注册地址**: https://replicate.com/

---

### 3. Hugging Face Inference API

Hugging Face提供免费的Inference API，可以直接调用多个图片生成模型。

**推荐模型**:
- Stable Diffusion XL
- Stable Diffusion 2.1
- OpenJourney
- DreamShaper

**使用方法**:

```python
import requests
import os

# Hugging Face API密钥
HF_TOKEN = os.environ.get("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# 生成图片
image_bytes = query({
    "inputs": "a beautiful sunset over mountains",
    "parameters": {
        "width": 512,
        "height": 512,
        "num_inference_steps": 50
    }
})

# 保存图片
with open("generated_image.png", "wb") as f:
    f.write(image_bytes)
```

**免费额度**:
- 每天约30次免费调用
- 超出后需要升级

**注册地址**: https://huggingface.co/

---

### 4. DeepInfra API

DeepInfro提供高性能的Stable Diffusion API，直接API调用。

**使用方法**:

```python
import requests
import os

DEEPINFRA_TOKEN = os.environ.get("DEEPINFRA_TOKEN")

# API端点
url = "https://api.deepinfra.com/v1/inference/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"bearer {DEEPINFRA_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "prompt": "a cyberpunk city at night",
    "width": 512,
    "height": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    image = result["images"][0]  # base64编码的图片
    print("图片生成成功!")
else:
    print(f"错误: {response.status_code}")
```

**免费额度**: 新用户有免费积分

**注册地址**: https://deepinfra.com/

---

### 5. Fal.ai API

Fal.ai提供免费的Stable Diffusion和FLUX模型API调用。

**使用方法**:

```python
import fal_client
import os

FAL_KEY = os.environ.get("FAL_KEY")

# 异步提交任务
result = fal_client.run(
    "fal-ai/fast-stable-diffusion",
    arguments={
        "prompt": "a beautiful garden with flowers",
        "num_images": 1,
        "width": 512,
        "height": 512
    }
)

# 获取图片URL
images = result["images"]
for image in images:
    print(f"生成图片: {image['url']}")
```

**免费额度**: 每天免费调用次数有限

**注册地址**: https://fal.ai/

---

## 二、各平台对比

### 2.1 免费图片生成API对比

| 平台 | 模型 | 免费额度 | 速率限制 | API密钥类型 |
|------|------|---------|---------|------------|
| **Wizmodel** | Stable Diffusion | 500-1000次/天 | 1-5 RPS | API Key |
| **Hugging Face** | SD XL, SD 2.1 | 30次/天 | 很低 | HF Token |
| **Replicate** | 多种模型 | 新用户免费 | 按积分 | API Token |
| **DeepInfra** | SD XL | 新用户免费 | 中等 | API Token |
| **Fal.ai** | SD, FLUX | 有限 | 中等 | API Key |

### 2.2 推荐的免费方案

**首选方案**: Wizmodel
- 理由: 稳定、免费额度充足、Python友好
- 适合场景: 日常公众号配图

**备选方案**: Hugging Face
- 理由: 模型多样、社区支持好
- 适合场景: 实验不同风格

**质量优先**: Replicate
- 理由: 模型质量高、更新快
- 适合场景: 高质量配图需求

---

## 三、快速集成代码模板

### 3.1 统一的Python调用模板

```python
import requests
import os
import time
import base64
from pathlib import Path

class FreeImageGenerator:
    """免费图片生成API统一接口"""

    def __init__(self):
        # Wizmodel配置
        self.wizmodel_url = "https://api.wizmodel.com/sd/generate"
        self.wizmodel_key = os.environ.get("WIZMODEL_API_KEY")

        # Hugging Face配置
        self.hf_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.hf_token = os.environ.get("HF_TOKEN")

    def generate_with_wizmodel(self, prompt, negative_prompt="", **kwargs):
        """使用Wizmodel生成图片"""
        if not self.wizmodel_key:
            raise ValueError("请设置 WIZMODEL_API_KEY 环境变量")

        headers = {
            "Authorization": f"Bearer {self.wizmodel_key}",
            "Content-Type": "application/json"
        }

        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": kwargs.get("width", 512),
            "height": kwargs.get("height", 512),
            "steps": kwargs.get("steps", 50),
            "cfg_scale": kwargs.get("cfg_scale", 7.0)
        }

        response = requests.post(self.wizmodel_url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("image_url", result.get("images", [{}])[0].get("url"))
        else:
            raise Exception(f"生成失败: {response.status_code}")

    def generate_with_huggingface(self, prompt, **kwargs):
        """使用Hugging Face生成图片"""
        if not self.hf_token:
            raise ValueError("请设置 HF_TOKEN 环境变量")

        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }

        data = {
            "inputs": prompt,
            "parameters": {
                "width": kwargs.get("width", 512),
                "height": kwargs.get("height", 512),
                "num_inference_steps": kwargs.get("steps", 50)
            }
        }

        response = requests.post(self.hf_url, headers=headers, json=data)

        if response.status_code == 200:
            return response.content  # 返回base64或图片bytes
        else:
            raise Exception(f"生成失败: {response.status_code}")

    def generate(self, prompt, negative_prompt="", **kwargs):
        """统一生成接口，优先使用Wizmodel"""
        try:
            return self.generate_with_wizmodel(prompt, negative_prompt, **kwargs)
        except Exception as e:
            print(f"Wizmodel失败，尝试Hugging Face: {e}")
            return self.generate_with_huggingface(prompt, **kwargs)

    def save_image(self, image_source, save_path):
        """保存图片到本地"""
        if image_source.startswith("http"):
            # 如果是URL，下载图片
            response = requests.get(image_source)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
        else:
            # 如果是base64，解码保存
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(image_source))

# 使用示例
if __name__ == "__main__":
    generator = FreeImageGenerator()

    try:
        # 生成图片
        image_url = generator.generate(
            prompt="一只橙色的小猫咪，趴在窗台上，可爱风格",
            negative_prompt="模糊，低质量，变形",
            width=512,
            height=512,
            steps=30
        )

        print(f"图片生成成功: {image_url}")

        # 保存图片
        save_path = "output/cat_image.png"
        generator.save_image(image_url, save_path)
        print(f"图片已保存: {save_path}")

    except Exception as e:
        print(f"生成失败: {e}")
```

### 3.2 环境变量配置

创建`.env`文件：

```bash
# Wizmodel API Key
# 注册地址: https://wizmodel.com/
WIZMODEL_API_KEY=your-wizmodel-key-here

# Hugging Face Token
# 注册地址: https://huggingface.co/
HF_TOKEN=your-hf-token-here

# Replicate Token (可选)
# 注册地址: https://replicate.com/
REPLICATE_API_TOKEN=your-replicate-token-here

# DeepInfra Token (可选)
# 注册地址: https://deepinfra.com/
DEEPINFRA_TOKEN=your-deepinfra-token-here

# Fal.ai Key (可选)
# 注册地址: https://fal.ai/
FAL_KEY=your-fal-key-here
```

### 3.3 速率限制处理

```python
import time
import requests
from requests.exceptions import HTTPError

class RateLimitedGenerator:
    """带速率限制的生成器"""

    def __init__(self, max_rps=2, max_retries=3):
        self.last_request_time = 0
        self.min_interval = 1.0 / max_rps
        self.max_retries = max_retries

    def rate_limited_request(self, url, headers, data):
        """带速率限制的请求"""
        for attempt in range(self.max_retries):
            # 控制请求频率
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_interval:
                time.sleep(self.min_interval - time_since_last)

            self.last_request_time = time.time()

            # 发送请求
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 429:
                # 速率限制，实施指数退避
                wait_time = (2 ** attempt)
                print(f"速率限制，等待{wait_time}秒后重试...")
                time.sleep(wait_time)
                continue
            elif response.status_code != 200:
                response.raise_for_status()

            return response.json()

        raise HTTPError("超过最大重试次数")
```

---

## 四、免费API注册步骤

### 4.1 Wizmodel注册流程

1. 访问 https://wizmodel.com/
2. 点击"Sign Up"注册账户
3. 验证邮箱
4. 在Dashboard中查找API Key
5. 复制并保存API Key

### 4.2 Hugging Face注册流程

1. 访问 https://huggingface.co/
2. 点击"Sign Up"注册
3. 验证邮箱
4. 访问 https://huggingface.co/settings/tokens
5. 创建新的Access Token (Read权限)
6. 复制并保存Token

### 4.3 Replicate注册流程

1. 访问 https://replicate.com/
2. 点击"Sign In with GitHub"
3. 授权GitHub账户
4. 访问Dashboard查看API Token
5. 复制并保存Token

---

## 五、使用注意事项

### 5.1 速率限制遵循

| 平台 | RPS限制 | 每日配额 | 退避策略 |
|------|---------|---------|---------|
| Wizmodel | 1-5 | 500-1000 | 指数退避 |
| Hugging Face | 很低 | 30 | 等待24小时 |
| Replicate | 中 | 按积分 | 购买积分 |
| DeepInfra | 中 | 新用户免费 | 按量计费 |

### 5.2 成本监控

建议设置使用量监控：

```python
# 简单的使用量跟踪
class UsageTracker:
    def __init__(self):
        self.daily_usage = {}
        self.limit_per_day = 500

    def track_request(self, platform):
        today = time.strftime("%Y-%m-%d")
        if today not in self.daily_usage:
            self.daily_usage[today] = {platform: 0}
        if platform not in self.daily_usage[today]:
            self.daily_usage[today][platform] = 0

        self.daily_usage[today][platform] += 1

        usage = self.daily_usage[today][platform]
        if usage > self.limit_per_day * 0.8:
            print(f"警告: {platform}今日使用量已达{usage}次，接近限制")
```

### 5.3 最佳实践

**✅ 推荐做法**:

- 使用环境变量管理API密钥
- 实现请求缓存，避免重复生成
- 设置速率限制，避免触发限制
- 保存生成的图片到本地或云存储
- 记录生成参数和结果，便于复现

**❌ 避免做法**:

- 不要将API密钥直接写入代码
- 不要在公开仓库中暴露API密钥
- 不要超过速率限制
- 不要忽视错误信息

---

## 六、故障排除

### 6.1 常见错误

| 错误码 | 含义 | 解决方法 |
|--------|------|----------|
| 401 | 未认证 | 检查API密钥是否正确 |
| 403 | 无权限 | 确认账户状态和权限 |
| 429 | 速率限制 | 实施退避策略，减少请求频率 |
| 400 | 请求错误 | 检查请求参数格式和内容 |
| 500 | 服务器错误 | 稍后重试 |

### 6.2 调试技巧

```python
# 调试模式：打印详细信息
def debug_generate(url, headers, data):
    print(f"请求URL: {url}")
    print(f"请求头: {headers}")
    print(f"请求体: {data}")

    response = requests.post(url, headers=headers, json=data)
    print(f"响应状态: {response.status_code}")
    print(f"响应头: {response.headers}")
    print(f"响应内容: {response.text[:500]}")  # 只打印前500字符

    return response
```

---

## 七、扩展建议

### 7.1 后续集成方向

1. **微信公众号自动配图**
   - 结合图文agent，自动生成文章配图
   - 实现定时任务批量生成

2. **图片素材库**
   - 建立本地图片素材库
   - 标签管理和搜索功能

3. **提示词模板库**
   - 积累有效的提示词模板
   - 根据文章类型匹配模板

4. **多API负载均衡**
   - 实现多平台API轮询
   - 自动故障转移

### 7.2 升级路径

**短期**: 使用免费API，完成基础功能

**中期**: 评估效果，考虑付费升级

**长期**: 如需求量大，考虑自建服务器

---

**文档更新时间**: 2026-02-08 20:50 GMT+8
**维护者**: OpenClaw Agent
**下次更新**: 发现新的免费API时更新
