import asyncio
from bme280_sensor import Sensor
from discord_bot import Bot

async def main():
    aobayama_sensor = Sensor()
    bot = Bot()

    token = "supersecrettoken"
    bot_task = asyncio.create_task(bot.client.start(token))

    await aobayama_sensor.wifi_check()

    while True:
        if aobayama_sensor.time_since_last_wifi_check > 5:
            await aobayama_sensor.wifi_check()
        
        aobayama_sensor.time_since_last_wifi_check += 1

        await asyncio.sleep(1)

asyncio.run(main())

