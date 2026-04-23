"""
智能题目生成工具

支持基于IRT理论动态生成适应性的测评题目。
可以根据被测者的回答历史，实时调整题目难度、类型和内容。
"""

from langchain.tools import tool
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


def _generate_question_with_llm(
    domain: str,
    difficulty: str,
    question_type: str,
    context: str = "",
    previous_answers: list = None
) -> str:
    """
    使用LLM生成题目的内部函数

    Args:
        domain: 测评领域（如：抑郁、焦虑、逻辑推理、数学能力等）
        difficulty: 难度级别（easy/medium/hard）
        question_type: 题目类型（multiple_choice/situational/open_ended）
        context: 上下文信息
        previous_answers: 之前的回答历史

    Returns:
        生成的题目内容（JSON格式）
    """
    ctx = request_context.get() or new_context(method="generate_question")
    client = LLMClient(ctx=ctx)

    # 构建提示词
    previous_answers_str = ""
    if previous_answers:
        previous_answers_str = "\n".join([
            f"题目{i+1}: {ans.get('question', '')}\n回答: {ans.get('answer', '')}\n得分: {ans.get('score', '')}"
            for i, ans in enumerate(previous_answers)
        ])

    prompt = f"""你是一位专业的心理测评和学科能力测评专家，擅长根据IRT（项目反应理论）动态生成适应性测评题目。

## 任务
根据以下要求生成一道测评题目：

## 测评信息
- 测评领域：{domain}
- 题目难度：{difficulty}
- 题目类型：{question_type}
- 上下文：{context}

## 被测者回答历史
{previous_answers_str if previous_answers_str else "（这是第一道题目，无历史记录）"}

## 题目类型说明
1. **multiple_choice（选择题）**：
   - 包含题目描述和4个选项
   - 选项难度递进（从易到难）
   - 适合心理测量、基础知识测试

2. **situational（情境判断题）**：
   - 描述一个真实情境
   - 设置3-5个可能的应对选项
   - 适合能力测评、决策能力测试

3. **open_ended（开放性题目）**：
   - 提出开放性问题
   - 引导被测者详细阐述
   - 适合深入分析、创造性思维测试

## IRT自适应策略
- 如果被测者之前回答表现优秀 → 生成更具挑战性的题目（hard）
- 如果被测者之前回答表现一般 → 生成中等难度题目（medium）
- 如果被测者之前回答表现较差 → 生成相对简单题目（easy）

## 输出要求
请以JSON格式输出题目，格式如下：

```json
{{
    "question": "题目描述",
    "options": [
        {{"id": "A", "text": "选项A内容", "score": 1}},
        {{"id": "B", "text": "选项B内容", "score": 2}},
        {{"id": "C", "text": "选项C内容", "score": 3}},
        {{"id": "D", "text": "选项D内容", "score": 4}}
    ],
    "difficulty": "{difficulty}",
    "domain": "{domain}",
    "reasoning": "生成这道题目的原因和逻辑"
}}
```

注意：
- 题目要有创新性，避免照搬陈旧题目
- 题目内容要符合测评领域的专业知识
- 情境判断题要贴近实际生活
- 开放性题目要有明确的引导性

现在开始生成题目："""

    from langchain_core.messages import HumanMessage
    messages = [HumanMessage(content=prompt)]

    response = client.invoke(
        messages=messages,
        model="doubao-seed-1-8-251228",
        temperature=0.7,
        max_completion_tokens=2000
    )

    # 处理响应内容
    if isinstance(response.content, str):
        return response.content
    elif isinstance(response.content, list):
        if response.content and isinstance(response.content[0], str):
            return " ".join(response.content)
        else:
            text_parts = [item.get("text", "") for item in response.content
                         if isinstance(item, dict) and item.get("type") == "text"]
            return " ".join(text_parts)
    return str(response.content)


@tool
def generate_adaptive_question(
    domain: str,
    difficulty: str,
    question_type: str = "multiple_choice",
    context: str = "",
    previous_answers_json: str = "[]"
) -> str:
    """
    基于IRT理论生成自适应测评题目

    根据被测者的回答历史，动态生成适合其能力水平的题目。
    支持多种测评领域和题目类型。

    Args:
        domain: 测评领域，如：
            - 心理测量类：depression（抑郁）、anxiety（焦虑）、emotion_stability（情绪稳定性）
            - 能力测试类：logic_reasoning（逻辑推理）、math_ability（数学能力）、verbal（言语能力）
            - 职业规划类：career_interest（职业兴趣）、work_ability（职业能力）
        difficulty: 难度级别，可选值：
            - easy：简单
            - medium：中等（默认）
            - hard：困难
        question_type: 题目类型，可选值：
            - multiple_choice：选择题（默认）
            - situational：情境判断题
            - open_ended：开放性题目
        context: 上下文或情境描述（用于情境判断题）
        previous_answers_json: 之前的回答历史，JSON字符串格式
            示例：'[{"question":"题目1","answer":"选项A","score":1}]'

    Returns:
        JSON格式的题目内容，包含题目描述、选项、难度、评分标准等

    Examples:
        生成一道抑郁测评的简单选择题：
        >>> generate_adaptive_question("depression", "easy", "multiple_choice")

        生成一道逻辑推理的情境判断题：
        >>> generate_adaptive_question("logic_reasoning", "medium", "situational", "工作中遇到冲突")

        基于历史回答生成题目：
        >>> generate_adaptive_question(
        ...     domain="depression",
        ...     difficulty="medium",
        ...     previous_answers_json='[{"question":"第1题","answer":"2","score":2}]'
        ... )
    """
    import json

    # 解析历史回答
    try:
        previous_answers = json.loads(previous_answers_json) if previous_answers_json else []
    except json.JSONDecodeError:
        previous_answers = []

    # 生成题目
    question_json = _generate_question_with_llm(
        domain=domain,
        difficulty=difficulty,
        question_type=question_type,
        context=context,
        previous_answers=previous_answers
    )

    return question_json


@tool
def estimate_ability_level(previous_answers_json: str, domain: str) -> str:
    """
    基于IRT理论估计被测者的能力水平

    根据被测者的回答历史，估计其在特定领域的能力水平（θ值），
    并推荐下一道题目的难度。

    Args:
        previous_answers_json: 之前的回答历史，JSON字符串格式
            示例：'[{"question":"题目1","answer":"选项A","score":2,"difficulty":"medium"}]'
        domain: 测评领域

    Returns:
        JSON格式的能力评估结果，包含：
        - estimated_ability: 估计的能力水平（easy/medium/hard）
        - average_score: 平均得分
        - total_questions: 总答题数
        - recommended_difficulty: 推荐的下一题难度
        - analysis: 分析说明

    Examples:
        >>> estimate_ability_level(
        ...     '[{"question":"第1题","answer":"2","score":2,"difficulty":"medium"}]',
        ...     "depression"
        ... )
    """
    import json

    # 解析历史回答
    try:
        previous_answers = json.loads(previous_answers_json) if previous_answers_json else []
    except json.JSONDecodeError:
        previous_answers = []

    if not previous_answers:
        return """{
    "estimated_ability": "unknown",
    "average_score": 0,
    "total_questions": 0,
    "recommended_difficulty": "medium",
    "analysis": "这是第一道题目，建议使用中等难度作为起点。"
}"""

    # 计算平均得分
    total_score = sum(ans.get("score", 0) for ans in previous_answers)
    total_questions = len(previous_answers)
    average_score = total_score / total_questions if total_questions > 0 else 0

    # 根据平均得分和能力题目估计能力水平
    # 假设题目难度：easy=2分以下，medium=2-3分，hard=3分以上
    if average_score < 1.5:
        ability = "low"
        recommended = "easy"
        analysis = f"被测者平均得分{average_score:.1f}分，显示能力偏低，建议降低题目难度。"
    elif average_score < 2.5:
        ability = "medium"
        recommended = "medium"
        analysis = f"被测者平均得分{average_score:.1f}分，能力处于中等水平，建议保持当前难度。"
    else:
        ability = "high"
        recommended = "hard"
        analysis = f"被测者平均得分{average_score:.1f}分，显示能力较强，建议增加题目难度。"

    result = {
        "estimated_ability": ability,
        "average_score": round(average_score, 2),
        "total_questions": total_questions,
        "recommended_difficulty": recommended,
        "analysis": analysis
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
