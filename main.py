import const
from data import rower_data
from utils import datalog
import asyncio
from bleak import BleakScanner, BleakClient
import datetime
import requests
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

class RowingTrainerClient:
    def __init__(self):
        self.selected_device = None
        self.device = None
        self.device_name = None
        self.device_address = None
        self.connected = False
        self.data_log = []

    async def discover_devices(self):
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        for idx, device in enumerate(devices):
            print(f"{idx + 1}. {device.name} - {device.address}")
            if device.name == const.TARGET_DEVICE_NAME:
                self.selected_device = device
                print(f"Target found: {idx + 1}. {device.name} - {device.address}")

        return devices

    async def select_device(self):
        devices = await self.discover_devices()
        
        if not devices:
            print("No devices found.")
            return None
        
        if not self.selected_device:
            device_index = int(input("Select the device index: ")) - 1
            self.selected_device = devices[device_index]
        
        self.device_name = self.selected_device.name
        self.device_address = self.selected_device.address
        print(f"Selected device: {self.device_name} - {self.device_address}")
        return self.selected_device

    async def connect(self):
        print(f"Connecting to {self.device_name}...")
        try:
            self.device = BleakClient(self.device_address)
            await self.device.connect()
            self.connected = True
            print(f"Connected to {self.device_name}")
        except Exception as e:
            print(f"Error connecting to device: {e}")
            self.connected = False

    async def disconnect(self):
        if self.device and self.device.is_connected:
            await self.device.disconnect()
            self.connected = False
            print(f"Disconnected from {self.device_name}")

    async def start_notifications(self):
        def callback(sender, data):
            self.process_data(data)

        if self.device:
            await self.device.start_notify(const.ROWING_TRAINER_CHARACTERISTIC_UUID, callback)
        else:
            print("Device not connected")

    def process_data(self, data):
        timestamp = datetime.datetime.now()
        rowing_data = self.interpret_rowing_data(data)
        log_entry = {'timestamp': timestamp, 'data': rowing_data}
        self.data_log.append(log_entry)
        print(f"Data received at {timestamp}: {rowing_data}")

    def interpret_rowing_data(self, val):
        return rower_data.parse_rower_data(val)

    async def reconnect(self):
        print("Attempting to reconnect...")
        await self.disconnect()
        await self.connect()
        if self.connected:
            await self.start_notifications()

    async def run(self):
        selected_device = await self.select_device()
        if selected_device:
            await self.connect()
            if self.connected:
                await self.start_notifications()
            else:
                print("Initial connection failed. Retrying in 10 seconds...")
                await asyncio.sleep(10)
                await self.reconnect()

    async def main_loop(self):
        while True:
            try:
                if not self.connected:
                    await self.reconnect()
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error in main loop: {e}")
                await asyncio.sleep(10)
                await self.reconnect()

    def save_log(self, filename='rowing_data_log.txt'):
        datalog.save_log(self.data_log, filename)

    def save_log_to_tcx(self, filename='rowing_data_log.tcx'):
        datalog.save_log_to_tcx(self.data_log, filename)

    def upload_to_strava(self, filename):
        datalog.upload_strava(filename)

client = RowingTrainerClient()

async def main():
    await client.run()
    await client.main_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print("Program stopped. Saving data log...")
    try:
        filename = datalog.generate_unique_filename()
        client.save_log(f"{filename}.txt")
        client.save_log_to_tcx(f"{filename}.tcx")
        print("\nProgram interrupted. Would you like to upload the results to Strava? (y/n): ")
        choice = input().strip().lower()
        if choice == 'y':
            if client.data_log:
                client.upload_to_strava(f"{filename}.tcx")
            else:
                print("No data to upload.")
        else:
            print("Upload canceled.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Exiting...")
finally:
    loop.close()