import asyncio
from bme280_sensor import Sensor
from discord_bot import Bot

async def main():
    aobayama_sensor = Sensor()
    bot = Bot()

    token = "supersecrettokeniwontgiveyou"
    bot_task = asyncio.create_task(bot.client.start(token))

    while True:
        # humidity, pressure, temperature = await aobayama_sensor.read()
        
        # Comment below line if intermittent reading is used
        aobayama_sensor.time_since_last_wifi_check += 1

        if aobayama_sensor.time_since_last_wifi_check > 5:
            aobayama_sensor.wifi_check()

        await asyncio.sleep(1)

asyncio.run(main())