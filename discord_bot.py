import discord
from bme280_sensor import Sensor

class Bot:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)

        self.aobayama_sensor = Sensor()

        @self.client.event
        async def on_ready():
            print(f"[LOG: DISCORD BOT] Successfully logged in as {self.client.user}")

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith("$hello"):
                await message.channel.send("Hello!")

            if message.content.startswith("$weather"):
                # Get sensor readings from aobayama sensor
                humidity, pressure, temperature = await self.aobayama_sensor.read()

                reply = f"Current weather conditions:\nTemperature: {temperature}°C\nHumidity = {humidity}%\nPressure = {pressure} atm."
                await message.channel.send(reply)