import asyncio
import bme280
import smbus2
import RPi.GPIO as GPIO
import subprocess

class Sensor:
    def __init__(self, port=1, address=0x76):
        # BME280 config
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(port)
        bme280.load_calibration_params(self.bus, self.address)

        # GPIO config
        self.sampling_led = 17
        self.wlan_led = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.sampling_led, GPIO.OUT)
        GPIO.setup(self.wlan_led, GPIO.OUT)

        # wifi check config
        self.time_since_last_wifi_check = 0

    async def read(self):
        self.data = bme280.sample(self.bus, self.address)
        self.humidity = self.data.humidity
        self.pressure = self.data.pressure
        self.ambient_temperature = self.data.temperature
        self.atm_pressure = self.pressure / 1013.25
        print(f"Humidity: {self.humidity}%, Pressure: {self.atm_pressure} atm, Temperature: {self.ambient_temperature} C")

        # Blink sampling LED once
        GPIO.output(self.sampling_led, GPIO.HIGH)
        await asyncio.sleep(0.2)
        GPIO.output(self.sampling_led, GPIO.LOW)

        return round(self.humidity, 2), round(self.atm_pressure, 2), round(self.ambient_temperature, 2)

    async def wifi_check(self):
        try:
            ps = subprocess.Popen(["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # Connected to WLAN.
            output = subprocess.check_output(("grep", "ESSID"), stdin=ps.stdout)
            print("[LOG: RASPBERRY PI]", output)
            if GPIO.input(27) == 0:
                # Turns on LED if it was previously off
                GPIO.output(self.wlan_led, GPIO.HIGH)
        except subprocess.CalledProcessError:
            # Not connected to WLAN.
            print("[LOG: RASPBERRY PI] Not connected to wireless LAN.")
            if GPIO.input(27) == 1:
                # Turns off LED if it was previously on
                GPIO.output(self.wlan_led, GPIO.LOW)

        self.time_since_last_wifi_check = 0

