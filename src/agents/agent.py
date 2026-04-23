import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver
from tools.question_generator import generate_adaptive_question, estimate_ability_level

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:] # type: ignore

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]

def build_agent(ctx=None):
    """
    构建智能自适应能力测评智能体

    该智能体具备以下核心能力：
    1. 对话式测评管理
    2. 动态生成题目（基于IRT理论，不使用固定题库）
    3. 自适应出题策略（根据被测者表现调整难度）
    4. 情境化题目生成（基于真实场景）
    5. 能力估计（θ值估计）
    6. 答案记录与评分
    7. 测评报告生成

    关键创新点：
    - 每道题目都是根据被测者实时表现动态生成
    - 支持选择题、情境判断题、开放性题目
    - 自动调整题目难度（easy/medium/hard）
    - 多维度测评和能力趋势分析

    Returns:
        Agent: 已配置好的智能体实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[generate_adaptive_question, estimate_ability_level],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
