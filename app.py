# app.py
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

from weather_service import push_weather_job
from config import CRON_SCHEDULE

# 1. 初始化 Flask 应用
app = Flask(__name__)

# 2. 初始化后台调度器
scheduler = BackgroundScheduler(daemon=True)

@app.route('/')
def index():
    """提供一个简单的访问端点，用于检查服务是否存活"""
    return "Weather Pushing Service is running. Task is scheduled."

def start_scheduler():
    """启动定时任务"""
    try:
        # 3. 添加定时任务
        # 我们使用 CronTrigger 来精确控制时间
        trigger = CronTrigger.from_crontab(CRON_SCHEDULE)
        scheduler.add_job(
            func=push_weather_job,
            trigger=trigger,
            id='daily_weather_push',
            name='Daily Weather Push Job',
            replace_existing=True
        )
        
        # 4. 启动调度器
        scheduler.start()
        print(f"调度器已启动，任务计划: {CRON_SCHEDULE}")
        
        # 注册退出处理器，确保程序退出时调度器能正确关闭
        atexit.register(lambda: scheduler.shutdown())
        
    except Exception as e:
        print(f"启动调度器失败: {e}")

if __name__ == '__main__':
    # 5. 立即执行一次任务（可选，用于测试）
    print("立即执行一次推送任务（用于启动测试）...")
    push_weather_job()
    
    # 6. 启动调度器
    start_scheduler()
    
    # 7. 运行 Flask 应用
    # use_reloader=False 是必须的，否则调度器会执行两次
    app.run(host='0.0.0.0', port=5000, use_reloader=False)