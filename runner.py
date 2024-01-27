import asyncio
from bme280_sensor import Sensor
from discord_bot import Bot

async def main():
    aobayama_sensor = Sensor()
    bot = Bot()

    token = "supersecrettoken"
    bot_task = asyncio.create_task(bot.client.start(token))

    aobayama_sensor.wifi_check()
    while True:
        # humidity, pressure, temperature = await aobayama_sensor.read()

        if aobayama_sensor.time_since_last_wifi_check > 5:
            aobayama_sensor.wifi_check()

        await asyncio.sleep(1)

asyncio.run(main())