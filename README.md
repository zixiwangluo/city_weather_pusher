# 天气预报钉钉推送助手

这是一个基于 Python Flask 和 APScheduler 构建的后台服务。它会定时从高德地图 API 获取天气预报，并将其格式化后推送到指定的钉钉机器人。

## ✨ 主要功能

* **定时推送**：使用 APScheduler，可灵活配置 CRON 表达式（例如每天早上 8:30）。
* **3 天预报**：获取今天、明天、后天（共3天）的详细天气。
* **钉钉集成**：使用 Markdown 格式发送消息，排版清晰。
* **配置灵活**：所有 API 密钥和配置均可通过环境变量设置，方便部署。
* **Web 服务**：内置一个简单的 Flask Web 服务，用于检查服务是否存活。

## 📁 项目结构

```
weather_pusher/
│
├── app.py             # Flask 主应用和调度器配置
├── weather_service.py # 封装所有业务逻辑（获取天气、发送钉钉）
├── config.py          # 存放所有配置信息（API Key 等）
├── requirements.txt   # 项目依赖
└── README.md          # (本项目)
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zixiwangluo/city_weather_pusher.git
cd weather_pusher
```

### 2. 安装依赖

建议在虚拟环境中安装：

```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### 3. 配置密钥

本项目依赖高德地图 API 和钉钉机器人。**推荐使用环境变量进行配置**。

| 环境变量 | 说明 | 示例 |
| :--- | :--- | :--- |
| `AMAP_API_KEY` | **[必需]** 高德地图 Web 服务 Key | `your_amap_api_key` |
| `DINGTALK_WEBHOOK`| **[必需]** 钉钉机器人 Webhook | `https://oapi.dingtalk.com/robot/send?access_token=...` |
| `DINGTALK_SECRET` | **[必需]** 钉钉机器人加签密钥 | `SEC...` |
| `CITY_CODE` | *[可选]* 城市编码 (默认 `330109`) | `110101` (北京东城) |
| `CRON_SCHEDULE` | *[可选]* CRON 表达式 (默认 `30 8 * * *`) | `0 9 * * *` (每天 9:00) |

**设置环境变量 (Linux/macOS):**
```bash
export AMAP_API_KEY="你的高德Key"
export DINGTALK_WEBHOOK="你的钉钉Webhook"
export DINGTALK_SECRET="你的钉钉Secret"
```

**设置环境变量 (Windows):**
```powershell
$env:AMAP_API_KEY="你的高德Key"
$env:DINGTALK_WEBHOOK="你的钉钉Webhook"
$env:DINGTALK_SECRET="你的钉钉Secret"
```

> **快速测试**：你也可以直接修改 `config.py` 文件来填入你的密钥，但这不推荐用于生产环境。

### 4. 运行服务

```bash
python app.py
```

服务启动后：
1.  会立即执行一次推送（用于测试）。
2.  Flask 服务会运行在 `http://0.0.0.0:5000`。
3.  后台定时任务会根据 `CRON_SCHEDULE` 设定的时间自动执行。

## 📄 许可协议 (License)


本项目采用 [MIT 许可证](LICENSE)。