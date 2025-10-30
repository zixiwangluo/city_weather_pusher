# config.py
import os

# --- 高德地图 API 配置 ---
# 在 https://console.amap.com/dev/key/app 申请
AMAP_API_KEY = os.environ.get('AMAP_API_KEY', 'YOUR_AMAP_API_KEY_HERE')

# --- 城市代码 ---
# 示例: '330109' 是 杭州市萧山区
# 可以在 https://a.amap.com/lbs/static/api/javascript/demo/citypicker/index.html 查询
CITY_CODE = os.environ.get('CITY_CODE', '330109')


# --- 钉钉机器人配置 ---
# 机器人的 Webhook 地址
DINGTALK_WEBHOOK = os.environ.get('DINGTALK_WEBHOOK', 'YOUR_DINGTALK_WEBHOOK_URL_HERE')

# 机器人的安全设置（加签）密钥
DINGTALK_SECRET = os.environ.get('DINGTALK_SECRET', 'YOUR_DINGTALK_SECRET_HERE')


# --- 定时任务配置 ---
# CRON 表达式 (示例: 每天早上 8:30)
# 格式: 分 时 日 月 周
CRON_SCHEDULE = os.environ.get('CRON_SCHEDULE', '30 8 * * *')