import asyncio
import aiohttp
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

bot = Bot(token=BOT_TOKEN)

ALERTS_API = "https://alerts.in.ua/api/states"
MAP_URL = "https://alerts.in.ua/map.png"

last_states = {}

def format_threat(info):
    threats = []
    if info.get("aircraft"):
        threats.append("✈️ Авіація")
    if info.get("missile"):
        threats.append("🚀 Ракетна загроза")
    if info.get("drone"):
        threats.append("🛩 Shahed / БПЛА")
    return "\n".join(threats)

async def send_map():
    await bot.send_photo(
        chat_id=CHANNEL,
        photo=MAP_URL,
        caption="🗺 Карта повітряних тривог"
    )

async def check_alerts():
    global last_states

    async with aiohttp.ClientSession() as session:
        async with session.get(ALERTS_API) as r:
            data = await r.json()

    for region, info in data.items():
        alert = info.get("alert", False)

        if region not in last_states:
            last_states[region] = alert
            continue

        if alert and not last_states[region]:
            text = f"🚨 ПОВІТРЯНА ТРИВОГА\n📍 {region}"
            threat = format_threat(info)
            if threat:
                text += f"\n\nТип загрози:\n{threat}"

            await bot.send_message(chat_id=CHANNEL, text=text)
            await send_map()

        if not alert and last_states[region]:
            await bot.send_message(
                chat_id=CHANNEL,
                text=f"🟢 ВІДБІЙ ТРИВОГИ\n📍 {region}"
            )

        last_states[region] = alert

async def main():
    print("BOT STARTED")
    while True:
        try:
            await check_alerts()
        except Exception as e:
            print("ERROR:", e)
        await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(main())
