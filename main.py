import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# =========================
# 設定（好きな場所に変えてOK）
# =========================
LAT = 35.681236
LON = 139.767125
TZ = "Asia/Tokyo"

# =========================
# Open-Meteo 天気取得
# =========================
def fetch_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,precipitation,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": TZ,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

# =========================
# 天気データを人間向けに整形
# =========================
def format_weather(data: dict) -> str:
    cur = data["current"]
    daily = data["daily"]

    text = (
        f"時刻: {cur['time']}\n"
        f"気温: {cur['temperature_2m']}°C（体感 {cur['apparent_temperature']}°C）\n"
        f"降水量(直近): {cur['precipitation']} mm\n"
        f"風速: {cur['wind_speed_10m']} km/h\n"
        f"weather_code: {cur['weather_code']}\n\n"
        f"【今日】最高 {daily['temperature_2m_max'][0]}°C / 最低 {daily['temperature_2m_min'][0]}°C\n"
        f"降水量合計: {daily['precipitation_sum'][0]} mm"
    )
    return text

# =========================
# GPTで短い要約を作る
# =========================
def summarize_with_gpt(raw_weather_text: str) -> str:
    client = OpenAI()
    prompt = f"""
あなたは天気通知ボットです。以下の天気情報を、日本語でLINE通知向けに短く要約してください。
条件:
- 3〜5行
- 数値（気温/降水/風/最高最低）は残す
- 推奨する服装

天気情報:
{raw_weather_text}
""".strip()

    resp = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )
    return resp.output_text.strip()

# =========================
# LINE Push 通知
# =========================
def push_text_to_line(message: str):
    channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}],
    }

    r = requests.post(url, headers=headers, json=payload, timeout=10)
    r.raise_for_status()

# =========================
# main
# =========================
def main():
    # 1) .env 読み込み
    load_dotenv()

    # 2) 天気取得
    data = fetch_weather(LAT, LON)

    # 3) 整形
    raw_text = format_weather(data)

    # 4) GPT要約
    summary = summarize_with_gpt(raw_text)

    # 5) LINE送信（要約 + 生データちょい）
    message = "【今日の天気】\n" + summary
    push_text_to_line(message)

    print("OK: LINEに通知しました")
    print("----送信内容----")
    print(message)

if __name__ == "__main__":
    main()



