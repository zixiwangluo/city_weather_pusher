// static/script.js

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    fetchWeather();
});

async function fetchWeather() {
    // 获取 HTML 元素
    const loadingSpinner = document.getElementById('loadingSpinner');
    const weatherContent = document.getElementById('weatherContent');
    const cityEl = document.getElementById('city');
    const reportTimeEl = document.getElementById('reportTime');
    const currentIconEl = document.getElementById('currentIcon');
    const currentTempEl = document.getElementById('currentTemp');
    const currentDescEl = document.getElementById('currentDesc');
    const forecastContainer = document.getElementById('forecastContainer');

    try {
        // 1. 调用后端的 API
        const response = await fetch('/api/weather');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }
        
        // 2. 解析和填充数据
        const today = data.casts[0];

        cityEl.textContent = data.city;
        reportTimeEl.textContent = `发布于 ${data.reporttime}`;

        // 填充今日天气
        currentIconEl.textContent = getWeatherIcon(today.dayweather);
        currentTempEl.textContent = `${today.daytemp}°C`;
        currentDescEl.textContent = `${today.dayweather} / ${today.nightweather}`;

        // 3. 动态创建3天预报
        forecastContainer.innerHTML = ''; // 清空
        data.casts.forEach(day => {
            const dayOfWeek = getChineseWeekday(day.date);
            const dayCard = document.createElement('div');
            dayCard.className = 'forecast-day';
            dayCard.innerHTML = `
                <div class="date">${dayOfWeek}</div>
                <div class="icon">${getWeatherIcon(day.dayweather)}</div>
                <div class="desc">${day.dayweather}</div>
                <div class="temp">${day.nighttemp}°C / ${day.daytemp}°C</div>
            `;
            forecastContainer.appendChild(dayCard);
        });

        // 4. 显示内容，隐藏加载
        loadingSpinner.style.display = 'none';
        weatherContent.style.display = 'block';

    } catch (error) {
        console.error("获取天气失败:", error);
        loadingSpinner.innerHTML = `<p style="color: #ff6b6b;">获取天气数据失败: ${error.message}</p>`;
    }
}

/**
 * 根据天气描述返回一个 Emoji 图标
 * @param {string} weather - 天气描述 (e.g., "晴", "多云", "雷阵雨")
 * @returns {string} - Emoji
 */
function getWeatherIcon(weather) {
    if (weather.includes('晴')) return '☀️';
    if (weather.includes('多云')) return '☁️';
    if (weather.includes('阴')) return '🌥️';
    if (weather.includes('雷阵雨')) return '⛈️';
    if (weather.includes('雨')) return '🌧️';
    if (weather.includes('雪')) return '❄️';
    if (weather.includes('雾')) return '🌫️';
    if (weather.includes('霾')) return '🌫️';
    return '🌬️'; // 默认 风
}

/**
 * 根据日期字符串 (YYYY-MM-DD) 获取中文星期
 * @param {string} dateStr 
 * @returns {string} (e.g., "星期一")
 */
function getChineseWeekday(dateStr) {
    const weekdays = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    const date = new Date(dateStr);
    return weekdays[date.getDay()];
}
