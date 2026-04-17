# ADK Skills Agent

基于 [Google Agent Development Kit (ADK)](https://github.com/google/adk-python) 构建的示例 Agent，演示如何使用 `SkillToolset` 加载和组合多个技能模块，并通过 OpenAI 兼容接口接入自定义 LLM。

## 项目结构

```
adk-skills/
├── skills_agent/
│   ├── agent.py              # Agent 主入口，定义 root_agent
│   ├── .env                  # 环境变量配置（模型地址、Key、模型名）
│   ├── __init__.py
│   └── skills/
│       └── weather-skill/    # 天气技能模块
│           ├── SKILL.md      # 技能定义（指令 + 元数据）
│           ├── references/
│           │   └── weather_info.md   # 天气参考数据
│           └── scripts/
│               └── get_humidity.py  # 湿度查询脚本
└── README.md
```

## 环境要求

- Python 3.10+
- pip

## 安装

```bash
pip install google-adk python-dotenv litellm
```

> Windows 用户建议额外设置 UTF-8 编码，避免 LiteLLM 读取缓存文件时出现编码错误：
> ```powershell
> $env:PYTHONUTF8 = "1"
> ```

## 配置

编辑 `skills_agent/.env`，填入你的模型服务信息：

```dotenv
# LLM Config
OPENAI_BASE_URL=https://your-endpoint/v1
OPENAI_API_KEY=your-api-key
LLM_MODEL=gpt-4o
```

| 变量 | 说明 |
|------|------|
| `OPENAI_BASE_URL` | OpenAI 兼容接口的 Base URL |
| `OPENAI_API_KEY` | API 密钥 |
| `LLM_MODEL` | 模型名称，默认 `gpt-4o` |

## 运行

**必须从项目根目录运行**，否则 ADK 无法正确识别 agent 目录：

```bash
# 在 adk-skills/ 根目录下执行
adk web
```

启动后访问 **http://127.0.0.1:8000**，在左侧下拉菜单选择 `skills_agent` 即可开始对话。

## Agent 能力

Agent 加载了以下技能和工具：

### 技能（Skills）

| 技能 | 描述 |
|------|------|
| `greeting-skill` | 向指定用户打招呼 |
| `weather-skill` | 查询天气信息、湿度、风速 |

### 内置工具（Tools）

| 工具 | 描述 |
|------|------|
| `get_timezone` | 返回指定地点的时区 |
| `get_wind_speed` | 返回指定地点的当前风速 |

### 测试示例

```
Say hello to Alice
What's the weather in Beijing?
What's the humidity in Shanghai?
What's the wind speed in London?
What timezone is Tokyo in?
```

## 技术说明

- **模型接入**：通过 [LiteLLM](https://github.com/BerriAI/litellm) 的 `LiteLlm` 封装，支持任意 OpenAI 兼容接口
- **代码执行**：使用 `UnsafeLocalCodeExecutor` 执行技能脚本（⚠️ 仅限本地开发，不可用于生产环境）
- **技能加载**：`greeting-skill` 以代码方式内联定义，`weather-skill` 从目录文件加载

## 许可证

[Apache License 2.0](LICENSE)
