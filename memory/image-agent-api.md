# 图文Agent API配置

**配置时间**: 2026-02-08 20:56 GMT+8
**用途**: 图文生成Agent专用API

---

## API基本信息

| 配置项 | 值 |
|--------|-----|
| **API提供商** | 华为云Gitee AI |
| **基础URL** | https://ai.gitee.com/v1 |
| **API密钥** | 🔒 **敏感数据** - 请在 `.env` 文件中配置 |
| **模型名称** | Z-Image |
| **默认尺寸** | 1024x1024 |
| **guidance_scale** | 5 |
| **num_inference_steps** | 30 |

---

## ⚠️ 安全说明

**API密钥是敏感数据**，请勿直接写入代码或文档！

### 安全配置方法

**方法1：使用环境变量（推荐）**

```bash
# 在终端中设置
export GITEE_AI_API_KEY="your_api_key_here"

# 或添加到 .env 文件
echo 'GITEE_AI_API_KEY="your_api_key_here"' > .env
```

**方法2：在代码中使用**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件
api_key = os.environ.get("GITEE_AI_API_KEY")
```

### 环境变量配置

创建 `.env` 文件：

```bash
# 文件名: .env
# 路径: 项目根目录

# Gitee AI API配置
GITEE_AI_API_KEY=your_api_key_here
```

**重要提示**:
- ✅ 将 `.env` 添加到 `.gitignore`
- ❌ 不要将 `.env` 推送到GitHub
- ✅ 定期轮换API密钥
- ❌ 不要在代码中硬编码API密钥

---

## 使用规则

### 每日限制

| 限制类型 | 限制值 | 监控方式 |
|---------|--------|---------|
| **每日生成数量** | ≤100张 | 自动计数+告警 |
| **每日凌晨重置** | 是 | UTC 0:00重置 |
| **超出处理** | 拒绝请求+提示 | 返回友好错误 |

### 速率限制（遵循NVIDIA API规则）

| 限制项 | 值 | 说明 |
|--------|-----|------|
| **RPS** | 1-2 | 每秒1-2次请求 |
| **RPM** | 60 | 每分钟最多60次 |
| **并发数** | 5 | 最多5个并发请求 |
| **错误处理** | 指数退避 | 1s→2s→4s→8s... |

---

## 监控配置

### 使用量跟踪

```python
class ImageUsageTracker:
    """每日图片生成量跟踪器"""
    
    def __init__(self, daily_limit=100):
        self.daily_limit = daily_limit
        self.reset_time = get_next_reset_utc()  # UTC 0:00
        self.count = 0
        self.last_reset = None
        
    def can_generate(self):
        """检查是否可以生成"""
        if self.is_new_day():
            self.reset()
        return self.count < self.daily_limit
    
    def record_generation(self):
        """记录一次生成"""
        if self.can_generate():
            self.count += 1
            return True
        return False
    
    def get_remaining(self):
        """获取剩余生成次数"""
        if self.is_new_day():
            self.reset()
        return max(0, self.daily_limit - self.count)
    
    def is_new_day(self):
        """检查是否是新的一天"""
        now = datetime.utcnow()
        if self.last_reset is None:
            return True
        return now >= self.reset_time
```

---

## 告警配置

| 告警级别 | 阈值 | 通知方式 |
|---------|------|---------|
| **信息** | 生成完成后 | 提示剩余数量 |
| **警告** | 剩余<20%时 | 发送提醒 |
| **严重** | 达到限制时 | 阻止生成+提示 |

---

**API信息来源**: 用户于2026-02-08提供
**配置状态**: ✅ 已保存
**下次更新**: 规则变更时
