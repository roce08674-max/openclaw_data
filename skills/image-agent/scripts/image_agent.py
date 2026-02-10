#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图文Agent - 智能配图生成

基于华为云Gitee AI的智能配图生成
遵循每日100张限制

作者: OpenClaw Agent
创建时间: 2026-02-08
"""

import os
import time
import json
import base64
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum

try:
    from openai import OpenAI
    import requests
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请安装: pip install openai requests")
    exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImageStyle(Enum):
    """图片风格枚举"""
    GENERAL = "general"
    TECH = "tech"
    LIFESTYLE = "lifestyle"
    BUSINESS = "business"
    ARTISTIC = "artistic"


@dataclass
class ImageConfig:
    """图片生成配置"""
    size: str = "1024x1024"
    guidance_scale: int = 5
    num_inference_steps: int = 30
    save_dir: str = "./generated_images"


@dataclass 
class GenerationResult:
    """生成结果"""
    status: str  # "success" or "error"
    message: str
    remaining_quota: int
    images: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.images is None:
            self.images = []


class UsageTracker:
    """每日使用量跟踪器"""
    
    def __init__(self, daily_limit: int = 100):
        self.daily_limit = daily_limit
        self.state_file = "./image_usage_state.json"
        self.state = self._load_state()
        
    def _load_state(self) -> Dict[str, Any]:
        """加载状态"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载状态失败: {e}")
        return {
            "count": 0,
            "last_reset": datetime.utcnow().strftime("%Y-%m-%d")
        }
    
    def _save_state(self):
        """保存状态"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"保存状态失败: {e}")
    
    def _is_new_day(self) -> bool:
        """检查是否是新的一天"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return self.state["last_reset"] != today
    
    def reset_if_needed(self):
        """必要时重置"""
        if self._is_new_day():
            self.reset()
    
    def reset(self):
        """重置计数"""
        self.state = {
            "count": 0,
            "last_reset": datetime.utcnow().strftime("%Y-%m-%d")
        }
        self._save_state()
        logger.info(f"使用量已重置，今日可生成{self.daily_limit}张")
    
    def can_generate(self) -> bool:
        """检查是否可以生成"""
        self.reset_if_needed()
        return self.state["count"] < self.daily_limit
    
    def record_generation(self) -> bool:
        """记录一次生成"""
        self.reset_if_needed()
        if self.state["count"] < self.daily_limit:
            self.state["count"] += 1
            self._save_state()
            return True
        return False
    
    def get_remaining(self) -> int:
        """获取剩余生成次数"""
        self.reset_if_needed()
        return max(0, self.daily_limit - self.state["count"])
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        self.reset_if_needed()
        used = self.state["count"]
        remaining = self.daily_limit - used
        percentage = (remaining / self.daily_limit) * 100
        
        if remaining <= 0:
            level = "critical"
            message = "已达每日上限（100张），请明天再试"
        elif percentage <= 20:
            level = "warning"
            message = f"剩余{remaining}张（{percentage:.0f}%），请注意使用"
        else:
            level = "normal"
            message = f"已使用{used}张，剩余{remaining}张"
        
        return {
            "level": level,
            "message": message,
            "used": used,
            "remaining": remaining,
            "reset_time": self.state["last_reset"]
        }


class ImageAgent:
    """图文Agent - 智能配图生成"""
    
    # 默认配置
    DEFAULT_CONFIG = ImageConfig(
        size="1024x1024",
        guidance_scale=5,
        num_inference_steps=30,
        save_dir="./generated_images"
    )
    
    # 风格提示词
    STYLE_PROMPTS = {
        ImageStyle.GENERAL: "high quality, detailed, professional",
        ImageStyle.TECH: "futuristic, clean, technology-themed, digital",
        ImageStyle.LIFESTYLE: "warm, cozy, lifestyle photography style",
        ImageStyle.BUSINESS: "corporate, professional, clean design",
        ImageStyle.ARTISTIC: "artistic, creative, unique style"
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        daily_limit: int = 100,
        config: Optional[ImageConfig] = None
    ):
        """
        初始化图文Agent
        
        参数:
            api_key: API密钥，为None则使用环境变量或默认配置
            base_url: API基础URL
            daily_limit: 每日生成限制
            config: 图片生成配置
        """
        # API配置
        self.api_key = api_key or os.environ.get("GITEE_AI_API_KEY")
        self.base_url = base_url or os.environ.get(
            "GITEE_AI_BASE_URL",
            "https://ai.gitee.com/v1"
        )
        
        # 验证API密钥是否已配置
        if self.api_key is None:
            raise ValueError(
                "API密钥未配置！请设置环境变量 GITEE_AI_API_KEY\n"
                "方法: export GITEE_AI_API_KEY='your_api_key_here'\n"
                "或创建 .env 文件添加 GITEE_AI_API_KEY=your_api_key_here"
            )
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        # 配置
        self.config = config or self.DEFAULT_CONFIG
        
        # 确保保存目录存在
        Path(self.config.save_dir).mkdir(parents=True, exist_ok=True)
        
        # 使用量跟踪器
        self.usage_tracker = UsageTracker(daily_limit=daily_limit)
        
        logger.info(f"图文Agent初始化完成")
        logger.info(f"API: {self.base_url}")
        logger.info(f"每日限制: {daily_limit}张")
    
    def _optimize_prompt(self, context: str, style: ImageStyle = ImageStyle.GENERAL) -> str:
        """优化提示词"""
        style_prompt = self.STYLE_PROMPTS.get(style, self.STYLE_PROMPTS[ImageStyle.GENERAL])
        
        # 组合提示词
        optimized = f"{context}, {style_prompt}"
        
        # 添加质量标签
        quality_tags = ", 4K resolution, sharp focus, beautiful lighting"
        optimized += quality_tags
        
        return optimized
    
    def _download_image(self, url: str, filename: str) -> bytes:
        """从URL下载图片"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 保存图片
        save_path = os.path.join(self.config.save_dir, filename)
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        return response.content
    
    def _save_image(self, image_bytes: bytes, filename: str) -> str:
        """保存图片到本地"""
        save_path = os.path.join(self.config.save_dir, filename)
        with open(save_path, "wb") as f:
            f.write(image_bytes)
        return save_path
    
    def generate(
        self,
        prompt: str,
        size: Optional[str] = None,
        guidance_scale: Optional[int] = None,
        num_inference_steps: Optional[int] = None,
        save: bool = True,
        style: Optional[ImageStyle] = None
    ) -> GenerationResult:
        """
        生成单张图片
        
        参数:
            prompt: 图片描述提示词
            size: 图片尺寸，默认1024x1024
            guidance_scale: 引导比例，默认5
            num_inference_steps: 推理步数，默认30
            save: 是否保存图片
            style: 图片风格
        
        返回:
            GenerationResult: 生成结果
        """
        # 检查使用量
        if not self.usage_tracker.can_generate():
            return GenerationResult(
                status="error",
                message=f"今日配图生成已达上限（100张），请明天再试",
                remaining_quota=0
            )
        
        # 优化提示词
        if style:
            prompt = self._optimize_prompt(prompt, style)
        
        # 设置参数
        params = {
            "model": "Z-Image",
            "prompt": prompt,
            "size": size or self.config.size,
            "extra_body": {
                "guidance_scale": guidance_scale or self.config.guidance_scale,
                "num_inference_steps": num_inference_steps or self.config.num_inference_steps
            }
        }
        
        try:
            logger.info(f"开始生成图片...")
            logger.info(f"提示词: {prompt[:100]}...")
            
            # 调用API
            response = self.client.images.generate(**params)
            
            # 记录使用量
            self.usage_tracker.record_generation()
            
            # 处理结果
            result = GenerationResult(
                status="success",
                message="图片生成成功",
                remaining_quota=self.usage_tracker.get_remaining(),
                images=[]
            )
            
            for i, image_data in enumerate(response.data):
                image_info = {
                    "index": i,
                    "filename": None,
                    "url": None,
                    "data": None
                }
                
                if image_data.url:
                    # 确定文件扩展名
                    ext = image_data.url.split('.')[-1].split('?')[0] or "jpg"
                    filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.{ext}"
                    
                    # 下载并保存
                    if save:
                        image_bytes = self._download_image(image_data.url, filename)
                        image_info["filename"] = filename
                        image_info["url"] = image_data.url
                        image_info["data"] = "saved"
                        logger.info(f"图片已保存: {filename}")
                    
                elif image_data.b64_json:
                    # Base64解码
                    image_bytes = base64.b64decode(image_data.b64_json)
                    filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.jpg"
                    
                    # 保存图片
                    if save:
                        save_path = self._save_image(image_bytes, filename)
                        image_info["filename"] = filename
                        image_info["data"] = "saved"
                        logger.info(f"图片已保存: {filename}")
                
                result.images.append(image_info)
            
            return result
            
        except Exception as e:
            logger.error(f"图片生成失败: {e}")
            return GenerationResult(
                status="error",
                message=f"图片生成失败: {str(e)}",
                remaining_quota=self.usage_tracker.get_remaining()
            )
    
    def generate_batch(
        self,
        prompts: List[str],
        size: Optional[str] = None,
        guidance_scale: Optional[int] = None,
        num_inference_steps: Optional[int] = None,
        delay: float = 1.0,
        style: Optional[ImageStyle] = None
    ) -> List[GenerationResult]:
        """
        批量生成图片
        
        参数:
            prompts: 提示词列表
            size: 图片尺寸
            guidance_scale: 引导比例
            num_inference_steps: 推理步数
            delay: 请求间隔（秒）
            style: 图片风格
        
        返回:
            List[GenerationResult]: 生成结果列表
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            # 检查是否超出限制
            if not self.usage_tracker.can_generate():
                results.append(GenerationResult(
                    status="error",
                    message=f"第{i+1}张：今日已达上限",
                    remaining_quota=0
                ))
                break
            
            # 生成图片
            logger.info(f"生成第{i+1}/{len(prompts)}张...")
            result = self.generate(
                prompt=prompt,
                size=size,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                style=style
            )
            results.append(result)
            
            # 添加延迟，避免触发速率限制
            if i < len(prompts) - 1:
                time.sleep(delay)
        
        return results
    
    def get_usage_status(self) -> Dict[str, Any]:
        """获取当前使用状态"""
        return self.usage_tracker.get_status()
    
    def reset_usage(self):
        """重置使用量（谨慎使用）"""
        self.usage_tracker.reset()


def demo():
    """演示"""
    print("=" * 60)
    print("图文Agent演示")
    print("=" * 60)
    
    # 初始化Agent
    agent = ImageAgent()
    
    # 显示当前状态
    status = agent.get_usage_status()
    print(f"\n当前状态: {status['message']}")
    
    # 生成测试图片
    print("\n生成测试图片...")
    
    result = agent.generate(
        prompt="A cute orange cat sitting on a windowsill, warm sunlight",
        size="1024x1024",
        style=ImageStyle.GENERAL
    )
    
    if result.status == "success":
        print(f"✅ 生成成功！")
        print(f"剩余配额: {result.remaining_quota}张")
        for img in result.images:
            print(f"  - 文件: {img['filename']}")
    else:
        print(f"❌ 生成失败: {result.message}")
    
    # 显示最终状态
    print(f"\n最终状态: {agent.get_usage_status()['message']}")


if __name__ == "__main__":
    demo()
