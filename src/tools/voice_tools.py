"""
语音合成工具 - 将文本转换为语音
"""
from langchain.tools import tool
from coze_coding_dev_sdk import TTSClient
from coze_coding_utils.runtime_ctx.context import new_context
import requests


def _synthesize_speech(
    text: str,
    voice_type: str = "zh_female_xiaohe_uranus_bigtts",
    speech_rate: int = 0,
    loudness_rate: int = 0
) -> str:
    """
    内部函数：执行语音合成
    """
    try:
        # 创建上下文用于追踪
        ctx = new_context(method="text_to_speech")
        
        # 初始化TTS客户端
        client = TTSClient(ctx=ctx)
        
        # 调用语音合成
        audio_url, audio_size = client.synthesize(
            uid="assessment_agent",
            text=text,
            speaker=voice_type,
            audio_format="mp3",
            sample_rate=24000,
            speech_rate=speech_rate,
            loudness_rate=loudness_rate
        )
        
        return audio_url
        
    except Exception as e:
        return f"语音合成失败: {str(e)}"


@tool
def text_to_speech(
    text: str,
    voice_type: str = "zh_female_xiaohe_uranus_bigtts",
    speech_rate: int = 0,
    loudness_rate: int = 0
) -> str:
    """
    将文本转换为语音并返回音频URL。
    
    Args:
        text: 要转换的文本内容
        voice_type: 语音类型，可选值：
            - zh_female_xiaohe_uranus_bigtts: 晓荷（女声，默认）
            - zh_female_vv_uranus_bigtts: Vivi（女声，中英双语）
            - zh_male_m191_uranus_bigtts: 云舟（男声）
            - zh_male_taocheng_uranus_bigtts: 晓天（男声）
            - zh_female_xueayi_saturn_bigtts: 儿童故事（女声）
            - zh_male_dayi_saturn_bigtts: 大义（男声，视频配音）
            - zh_female_mizai_saturn_bigtts: 迷仔（女声，视频配音）
        speech_rate: 语速调节，范围 -50 到 100，默认0（正常语速）
        loudness_rate: 音量调节，范围 -50 到 100，默认0（正常音量）
    
    Returns:
        str: 生成的语音文件URL
        
    Example:
        >>> audio_url = text_to_speech("欢迎使用能力测评系统！")
        >>> print(f"音频URL: {audio_url}")
    """
    return _synthesize_speech(text, voice_type, speech_rate, loudness_rate)


@tool
def generate_intro_speech() -> str:
    """
    生成开场白语音。
    
    Returns:
        str: 开场白语音URL
    """
    intro_text = """欢迎使用智能自适应能力测评中心！
    
    我是您的智能测评助手，采用先进的项目反应理论自适应测评技术。
    
    我能为您提供多种测评服务，包括心理测量、能力测试、职业规划和情绪智力等多个领域的评估。
    
    我的特点是动态生成题目，根据您的表现实时调整难度，为您提供精准的能力评估。
    
    请直接告诉我您想进行什么类型的测评，我会为您安排合适的测试。
    
    让我们开始吧！"""
    
    return _synthesize_speech(intro_text, voice_type="zh_female_xiaohe_uranus_bigtts")


@tool
def generate_question_speech(question: str, options: str = "") -> str:
    """
    生成测评题目语音。
    
    Args:
        question: 题目内容
        options: 选项内容（可选）
    
    Returns:
        str: 题目语音URL
    """
    full_text = question
    if options:
        full_text = f"题目是：{question}。{options}"
    
    return _synthesize_speech(full_text, voice_type="zh_female_xiaohe_uranus_bigtts")


@tool
def generate_report_summary_speech(summary: str) -> str:
    """
    生成测评报告摘要语音。
    
    Args:
        summary: 报告摘要内容
    
    Returns:
        str: 报告语音URL
    """
    # 截取摘要的前500字，避免语音过长
    truncated_summary = summary[:500] if len(summary) > 500 else summary
    
    return _synthesize_speech(truncated_summary, voice_type="zh_female_xiaohe_uranus_bigtts")
