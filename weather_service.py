# weather_service.py
import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import requests
from datetime import datetime
from config import AMAP_API_KEY, CITY_CODE, DINGTALK_WEBHOOK, DINGTALK_SECRET

def get_chinese_weekday(date_str: str) -> str:
    """根据日期字符串 (YYYY-MM-DD) 获取中文星期"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return weekdays[date_obj.weekday()]

def get_weather_forecast() -> dict | None:
    """
    使用高德 API 获取天气预报
    (使用 requests 库重构)
    """
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={AMAP_API_KEY}&city={CITY_CODE}&extensions=all"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败 (非 2xx 状态码) 则抛出异常
        data = response.json()

        if data.get('status') == '1' and data.get('count') == '1':
            return data['forecasts'][0]
        else:
            print(f"高德 API 返回错误: {data.get('info', '未知错误')}")
            return None
    except requests.RequestException as e:
        print(f"获取天气预报失败: {e}")
        return None

def format_weather_message(forecast_data: dict) -> str:
    """格式化天气预报为钉钉消息"""
    city = forecast_data['city']
    forecasts = forecast_data['casts'][:3]  # 只取3天
    
    # 获取当前时间（北京时间）
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    
    message_lines = [
        f"### 🏙️ {city} 天气预报",
        f"**播报日期：** {date_str} {get_chinese_weekday(now.strftime('%Y-%m-%d'))}\n"
    ]

    for day in forecasts:
        date = day['date']
        weekday = get_chinese_weekday(date)
        
        message_lines.append(
            f"--- \n"
            f"**日期：** {date} ({weekday})\n"
            f"**白天：** {day['dayweather']} ( {day['daytemp']}°C / {day['daywind']}风 {day['daypower']}级 )\n"
            f"**夜间：** {day['nightweather']} ( {day['nighttemp']}°C / {day['nightwind']}风 {day['nightpower']}级 )"
        )
    
    return "\n".join(message_lines)


def send_dingtalk_message(message: str) -> bool:
    """
    发送钉钉机器人消息
    (使用 requests 库重构)
    """
    timestamp = str(round(time.time() * 1000))
    secret_enc = DINGTALK_SECRET.encode('utf-8')
    string_to_sign = f'{timestamp}\n{DINGTALK_SECRET}'
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    # 完整的 Webhook URL
    webhook_url = f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"

    headers = {
        'Content-Type': 'application/json'
    }
    
    # 我们使用 Markdown 格式，体验更好
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "天气预报",
            "text": message
        }
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get('errcode') == 0:
            print(f"[{datetime.now()}] 钉钉消息发送成功")
            return True
        else:
            print(f"[{datetime.now()}] 钉钉消息发送失败: {result.get('errmsg')}")
            return False
            
    except requests.RequestException as e:
        print(f"发送钉钉消息异常: {e}")
        return False

# --- 调度器要执行的主任务 ---
def push_weather_job():
    """定时推送任务的主函数"""
    print(f"[{datetime.now()}] 开始执行天气推送任务...")
    
    if not all([AMAP_API_KEY, CITY_CODE, DINGTALK_WEBHOOK, DINGTALK_SECRET]):
        print("错误：配置不完整。请检查 config.py 或环境变量。")
        return

    weather_data = get_weather_forecast()
    
    if weather_data:
        message = format_weather_message(weather_data)
        send_dingtalk_message(message)
    else:
        print("未能获取天气数据，取消推送。")