import asyncio
from typing import Dict, Any
import requests
from maxapi import Dispatcher, Router, Message

# --- Конфигурация ---
OPENWEATHER_API_KEY = "ТВОЙ_OPENWEATHER_KEY"
CITY = "Moscow"  # можно позже заменить на ввод пользователя
UNITS = "metric"  # metric = °C, imperial = °F
LANG = "ru"      # язык описания погоды

dp = Dispatcher()
router = Router()
dp.include_router(router)

def get_detailed_weather_openweathermap() -> Dict[str, Any]:
    """Получает текущую погоду + прогноз на 5 дней (3‑часовой шаг) от OpenWeatherMap"""
    # Текущая погода
    url_current = "https://api.openweathermap.org/data/2.5/weather"
    params_current = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": UNITS,
        "lang": LANG,
    }
    resp_current = requests.get(url_current, params=params_current, timeout=10)
    resp_current.raise_for_status()
    current_data = resp_current.json()

    # Прогноз на 5 дней (каждые 3 часа)
    url_forecast = "https://api.openweathermap.org/data/2.5/forecast"
    params_forecast = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": UNITS,
        "lang": LANG,
    }
    resp_forecast = requests.get(url_forecast, params=params_forecast, timeout=10)
    resp_forecast.raise_for_status()
    forecast_data = resp_forecast.json()

    return {
        "current": current_data,
        "forecast": forecast_data,
    }


def format_detailed_forecast_openweathermap(data: Dict[str, Any]) -> str:
    """Формирует красивый HTML-текст для MAX"""
    current = data["current"]
    forecast = data["forecast"]

    main = current["main"]
    wind = current["wind"]
    weather = current["weather"][0]

    text = (
        f"🌤 <b>Погода в {current['name']} сейчас</b>\n\n"
        f"Температура: <b>{main['temp']}°C</b>\n"
        f"Ощущается как: <b>{main.get('feels_like', '?')}°C</b>\n"
        f"Влажность: {main['humidity']}%\n"
        f"Давление: {main['pressure']} гПа\n"
        f"Ветер: {wind.get('speed', '?')} м/с, направление {wind.get('deg', '?')}°\n"
        f"Состояние: {weather['description'].capitalize()}\n\n"
    )

    text += "<b>📅 Прогноз на ближайшие дни (каждые 3 ч):</b>\n\n"

    # Берём первые 8 записей (это примерно сутки), чтобы не превысить лимит сообщения
    for item in forecast["list"][:8]:
        dt_txt = item["dt_txt"]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"].capitalize()
        text += f"🕒 {dt_txt}: <b>{temp}°C</b>, {desc}\n"

    return text


@router.message_created("/weather")
async def handle_weather(message: Message):
    try:
        data = get_detailed_weather_openweathermap()
        text = format_detailed_forecast_openweathermap(data)
        await message.answer(text=text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении погоды: {e}")


if __name__ == "__main__":
    asyncio.run(dp.start_polling())
