import os
import requests


# =========================
# 基本設定
# =========================

# 指定地點：桃園市
LATITUDE = 24.9937
LONGITUDE = 121.3010

# 從 GitHub Secrets 取得 Telegram 資訊
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# =========================
# 取得天氣資料
# =========================

def get_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": [
            "temperature_2m_max",
            "precipitation_probability_max"
        ],
        "timezone": "Asia/Taipei",
        "forecast_days": 1
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"天氣 API 請求失敗，HTTP 狀態碼："
            f"{response.status_code}"
        )

    data = response.json()

    max_temperature = data["daily"]["temperature_2m_max"][0]

    rain_probability = data["daily"][
        "precipitation_probability_max"
    ][0]

    return max_temperature, rain_probability


# =========================
# 取得 AQI
# =========================

def get_aqi():

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "us_aqi",
        "timezone": "Asia/Taipei",
        "forecast_days": 1
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"AQI API 請求失敗，HTTP 狀態碼："
            f"{response.status_code}"
        )

    data = response.json()

    aqi_list = data["hourly"]["us_aqi"]

    valid_aqi = [
        aqi for aqi in aqi_list
        if aqi is not None
    ]

    if not valid_aqi:
        raise Exception("找不到 AQI 資料")

    max_aqi = max(valid_aqi)

    return max_aqi


# =========================
# 建立通勤建議
# =========================

def create_advice(
    max_temperature,
    rain_probability,
    aqi
):

    advice = []

    # 降雨機率達 60%
    if rain_probability >= 60:
        advice.append(
            "☔ 降雨機率達 60%，請記得攜帶雨傘。"
        )

    # 最高溫達 33°C
    if max_temperature >= 33:
        advice.append(
            "☀️ 最高溫達 33°C，請注意防曬並適時補充水分。"
        )

    # AQI 達 100
    if aqi >= 100:
        advice.append(
            "😷 AQI 達 100，空氣品質較差，建議配戴口罩。"
        )

    # 所有條件正常
    if not advice:
        advice.append(
            "✅ 今日天氣與空氣品質正常，適合外出通勤。"
        )

    return advice


# =========================
# 發送 Telegram
# =========================

def send_telegram(message):

    if not TELEGRAM_BOT_TOKEN:
        raise Exception(
            "找不到 TELEGRAM_BOT_TOKEN，"
            "請確認 GitHub Secrets 是否設定。"
        )

    if not TELEGRAM_CHAT_ID:
        raise Exception(
            "找不到 TELEGRAM_CHAT_ID，"
            "請確認 GitHub Secrets 是否設定。"
        )

    url = (
        "https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(
        url,
        data=payload,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"Telegram 發送失敗，"
            f"HTTP 狀態碼：{response.status_code}\n"
            f"{response.text}"
        )

    print("Telegram 訊息發送成功")


# =========================
# 主程式
# =========================

def main():

    print("開始取得天氣與空氣品質資料...")

    max_temperature, rain_probability = get_weather()

    print(f"最高溫度：{max_temperature}°C")
    print(f"最高降雨機率：{rain_probability}%")

    aqi = get_aqi()

    print(f"最高 AQI：{aqi}")

    advice = create_advice(
        max_temperature,
        rain_probability,
        aqi
    )

    message = (
        "🚨 智慧通勤風險通知 🚨\n"
        "\n"
        "📍 地點：桃園市\n"
        f"🌡️ 最高溫度：{max_temperature}°C\n"
        f"🌧️ 最高降雨機率：{rain_probability}%\n"
        f"🌫️ AQI：{aqi}\n"
        "\n"
        "📢 今日通勤建議：\n"
    )

    for item in advice:
        message += f"{item}\n"

    print("\n" + message)

    send_telegram(message)


if __name__ == "__main__":
    main()
