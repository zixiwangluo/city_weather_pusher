# app.py
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

# 🔴 导入 get_weather_forecast
from weather_service import push_weather_job, get_weather_forecast
from config import CRON_SCHEDULE

# 1. 初始化 Flask 应用
app = Flask(__name__)

# 2. 初始化后台调度器
scheduler = BackgroundScheduler(daemon=True)

# --- 🔴 新增前端路由 ---

@app.route('/')
def index():
    """
    渲染前端天气卡片页面
    Flask 会自动在 'templates' 文件夹中寻找 'index.html'
    """
    return render_template('index.html')

@app.route('/api/weather')
def api_weather():
    """
    提供天气数据的 JSON API 端点
    供前端的 script.js 来调用
    """
    weather_data = get_weather_forecast()
    if weather_data:
        # 使用 jsonify 将 Python 字典转换为 JSON 响应
        return jsonify(weather_data)
    else:
        return jsonify({"error": "无法获取天气数据"}), 500

# --- 后台定时任务 (保持不变) ---

def start_scheduler():
    """启动定时任务"""
    try:
        trigger = CronTrigger.from_crontab(CRON_SCHEDULE)
        scheduler.add_job(
            func=push_weather_job,
            trigger=trigger,
            id='daily_weather_push',
            name='Daily Weather Push Job',
            replace_existing=True
        )
        scheduler.start()
        print(f"调度器已启动，任务计划: {CRON_SCHEDULE}")
        atexit.register(lambda: scheduler.shutdown())
        
    except Exception as e:
        print(f"启动调度器失败: {e}")

if __name__ == '__main__':
    # 启动时不再立即执行推送，因为用户可以通过访问网页来测试
    # print("立即执行一次推送任务（用于启动测试）...")
    # push_weather_job()
    
    # 启动调度器
    start_scheduler()
    
    # 运行 Flask 应用
    # 🔴 注意：开发时可以设置 debug=True，但 use_reloader=False 仍然是必须的
    app.run(host='0.0.0.0', port=5000, use_reloader=False, debug=True)