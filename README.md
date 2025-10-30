#  WeatherFlow - 动态天气卡片与钉钉推送平台

WeatherFlow 是一个基于 **Python Flask** 构建的前后端一体应用。它巧妙地结合了实时数据展示与后台定时任务：

1.  **前端展示 (Web UI)**: 提供一个美观、动态的天气卡片网页，任何人都可以访问以获取最新的 3 天天气预报。
2.  **后端推送 (Backend)**: 在后台静默运行一个定时任务 (使用 **APScheduler**)，在每天指定的时间自动将天气预报推送到钉钉群。


## 🚀 主要功能

* **动态天气卡片**：使用 HTML/CSS/JS 构建的现代化前端界面，通过 `fetch` 异步调用后端 API。
* **API 服务**：内置 `/api/weather` 端点，提供 JSON 格式的实时天气数据。
* **后台定时推送**：使用 APScheduler，可灵活配置 CRON 表达式（例如每天早上 8:30）。
* **钉钉集成**：使用 Markdown 格式发送消息，排版清晰，体验良好。
* **配置灵活**：所有 API 密钥和配置均可通过环境变量设置，完美支持容器化部署。
* **轻量高效**：基于 Flask 框架，占用资源少，启动速度快。

## 📁 项目结构

项目采用了标准的 Flask 应用结构，将前端与后端逻辑清晰分离。

```
weather_pusher/
│
├── app.py             # 🚀 Flask 主应用 (Web路由, API, 调度器)
├── weather_service.py # 🛠️ 核心服务 (获取天气, 发送钉钉)
├── config.py          # 🔑 配置文件 (读取环境变量)
├── requirements.txt   # 📦 Python 依赖
│
├── templates/         # 📄【前端】存放 HTML 模板
│   └── index.html
│
├── static/            # 🎨【前端】存放 CSS 和 JS
│   ├── style.css      # (天气卡片样式与动态效果)
│   └── script.js      # (API 调用与 DOM 操作)
│
├── LICENSE            # 📜 许可证 (MIT)
└── README.md          # (本项目)
```

## 🛠️ 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zixiwangluo/weather_pusher.git
cd weather_pusher
```

### 2. 安装依赖

推荐在 Python 虚拟环境中安装：

```bash
# 创建并激活虚拟环境 (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# (Windows)
# python -m venv venv
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置密钥

本项目依赖高德地图 API 和钉钉机器人。**强烈推荐使用环境变量进行配置**。

| 环境变量 | 说明 | 示例 |
| :--- | :--- | :--- |
| `AMAP_API_KEY` | **[必需]** 高德地图 Web 服务 Key | `your_amap_api_key` |
| `DINGTALK_WEBHOOK`| **[必需]** 钉钉机器人 Webhook | `https://oapi.dingtalk.com/robot/send?access_token=...` |
| `DINGTALK_SECRET` | **[必需]** 钉钉机器人加签密钥 | `SEC...` |
| `CITY_CODE` | *[可选]* 城市编码 (默认 `330109` 萧山区) | `110101` (北京东城) |
| `CRON_SCHEDULE` | *[可选]* CRON 表达式 (默认 `30 8 * * *`) | `0 9 * * *` (每天 9:00) |

**设置环境变量 (Linux/macOS):**
```bash
export AMAP_API_KEY="你的高德Key"
export DINGTALK_WEBHOOK="你的钉钉Webhook"
export DINGTALK_SECRET="你的钉钉Secret"
```

> **快速测试**：你也可以直接修改 `config.py` 文件来填入你的密钥，但这不推荐用于生产环境。

## 🏃 运行与使用

1.  **启动应用**

    ```bash
    python app.py
    ```

2.  **服务启动**

    启动后，程序会同时做两件事：
    * **[前端]** 启动一个 Web 服务器在 `http://0.0.0.0:5000`。
    * **[后端]** 启动后台调度器，并根据 `CRON_SCHEDULE` 设定开始等待下一次推送。

3.  **访问前端**

    打开浏览器，访问 **`http://127.0.0.1:5000/`**。
    
    你将看到动态天气卡片。页面会自动向 `/api/weather` 发起请求并渲染数据。

4.  **查看后台**

    后台推送任务将根据你的 CRON 表达式自动在后台运行，准时发送钉钉消息。

## 📄 许可协议 (License)

本项目采用 [MIT 许可证](LICENSE)。