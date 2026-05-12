# 🎯 智能自适应能力测评系统

基于IRT（项目反应理论）的智能测评智能体，能够根据被测者的实时表现动态生成题目，实现真正的个性化评估。

## ✨ 核心特性

### 🚀 智能自适应测评
- **动态题目生成**：不是从固定题库选题，而是根据被测者表现实时生成新题目
- **IRT自适应策略**：基于项目反应理论智能调整题目难度
- **情境化出题**：结合真实生活和工作场景，增强测评趣味性

### 📊 支持的测评类型

#### 心理测量类
- 抑郁水平测评 (BDI)
- 焦虑水平测评 (SAS)
- 情绪稳定性评估
- 人格特质分析

#### 能力测试类
- 逻辑推理能力
- 数学能力
- 言语理解能力
- 空间想象力
- 记忆力评估
- 注意力测试

#### 职业规划类
- 职业兴趣倾向
- 职业性格分析
- 职业能力评估
- 团队合作能力

#### 社会能力类
- 情绪智力
- 沟通能力
- 领导力评估
- 社会适应性

### 🎨 题目类型
- **选择题**：4选项递进式评分
- **情境判断题**：真实场景决策能力测试
- **开放性题目**：深入分析和创造性思维评估

## 🛠️ 技术栈

- **框架**：LangGraph + LangChain
- **模型**：Doubao-Seed-1.8（支持多模态Agent优化）
- **语言**：Python 3.10+
- **依赖管理**：uv

## 📦 安装使用

### 1. 克隆项目
```bash
git clone <your-github-repo-url>
cd your-repo-name
```

### 2. 安装依赖
```bash
uv sync
```

### 3. 配置环境变量
```bash
# 设置必要的环境变量
export COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
export COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

### 4. 运行测试
```bash
# 本地测试
uv run python src/main.py -m agent

# 或使用 pytest
uv run pytest tests/
```

## 🔧 项目结构

```
.
├── config/                      # 配置文件
│   └── agent_llm_config.json    # 模型配置和系统提示词
├── src/
│   ├── agents/                  # Agent核心逻辑
│   │   └── agent.py
│   ├── tools/                   # 工具定义
│   │   └── question_generator.py  # 智能题目生成工具
│   ├── storage/                 # 存储模块
│   │   └── memory/              # 记忆系统
│   └── main.py                  # 主入口
├── tests/                       # 测试文件
├── assets/                      # 资源文件
├── .gitignore
├── pyproject.toml
└── README.md
```

## 🎯 使用方式

### 快速开始
1. 启动Agent
2. 直接告诉Agent您想测评什么，例如：
   - "我想做逻辑推理测评"
   - "测测我的情绪智力"
   - "我想了解职业兴趣"

3. Agent会自动：
   - 生成第一道中等难度的题目
   - 根据您的回答动态调整难度
   - 生成专业的评估报告

### 对话示例
```
用户：你好，我想做数学能力测评
Agent：🎯 智能自适应能力测评中心
      您好！请直接告诉我您想测评什么...
      
用户：我想做数学能力测评
Agent：好的，我们现在开始数学能力测评。
      第1题（选择题）：某书店推出促销活动...
      请告诉我您的选择（A/B/C/D）
      
用户：B
Agent：回答正确！🎉
      看来您的数学基础很扎实！
      第2题（情境判断题）：...
```

## 📖 文档

- [AGENT.md](./AGENT.md) - Agent设计规范
- [docs/](./docs/) - 详细技术文档

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

[Your Name]

## 🙏 致谢

- 感谢所有心理学量表原作者的贡献
- 基于先进的IRT自适应测评理论
