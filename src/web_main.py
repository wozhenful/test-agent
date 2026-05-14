"""
Web应用主入口
提供HTTP服务，支持语音交互
"""
import os
import json
import base64
import asyncio
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# 导入Agent和工具
from agents.agent import build_agent
from tools.voice_tools import text_to_speech
from coze_coding_dev_sdk import ASRClient
from coze_coding_utils.runtime_ctx.context import new_context

app = FastAPI(title="智能自适应能力测评中心", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储对话历史
conversations = {}


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回Web界面"""
    with open("web_app.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    处理对话请求
    """
    try:
        session_id = request.session_id or "default"
        
        # 初始化Agent（如果还没有）
        if session_id not in conversations:
            conversations[session_id] = {
                "agent": build_agent(),
                "history": []
            }
        
        # 调用Agent（这里简化处理，实际需要使用graph.run等）
        # 暂时返回模拟响应
        response_text = f"收到您的消息：{request.message}\n\n正在处理中..."
        
        # 生成语音（如果需要）
        audio_url = None
        if len(request.message) > 0:
            try:
                audio_url = text_to_speech.invoke(response_text)
            except Exception as e:
                print(f"TTS error: {e}")
        
        return JSONResponse({
            "text": response_text,
            "audio_url": audio_url,
            "session_id": session_id
        })
        
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)


@app.post("/api/asr")
async def asr(audio: UploadFile = File(...)):
    """
    处理语音识别请求
    """
    try:
        # 读取音频文件
        audio_data = await audio.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        
        # 调用ASR
        ctx = new_context(method="asr.recognize")
        client = ASRClient(ctx=ctx)
        
        text, data = client.recognize(
            uid="web_user",
            base64_data=audio_base64
        )
        
        return JSONResponse({
            "text": text,
            "duration": data.get("result", {}).get("duration", 0)
        })
        
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)


@app.get("/api/health")
async def health():
    """健康检查"""
    return {"status": "ok", "service": "assessment-agent"}


def main():
    """启动服务"""
    print("=" * 50)
    print("🎯 智能自适应能力测评中心")
    print("=" * 50)
    print("📍 访问地址：http://localhost:9000")
    print("=" * 50)
    
    uvicorn.run(
        "web_main:app",
        host="0.0.0.0",
        port=9000,
        reload=False
    )


if __name__ == "__main__":
    main()
