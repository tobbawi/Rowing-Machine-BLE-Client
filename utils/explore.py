import asyncio
from bleak import BleakScanner, BleakClient

async def discover_devices():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    print("Devices found:")
    for idx, device in enumerate(devices):
        print(f"{idx + 1}. {device.name} - {device.address}")
    return devices

async def explore_device(device):
    async with BleakClient(device) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid} - {service.description}")
            for char in service.characteristics:
                char_info = f"  Characteristic: {char.uuid}, Properties: {char.properties}"
                if char.description:
                    char_info += f", Description: {char.description}"
                print(char_info)
                for descriptor in char.descriptors:
                    desc = await client.read_gatt_descriptor(descriptor.handle)
                    print(f"    Descriptor: {descriptor.uuid}, Value: {desc}")

async def main():
    devices = await discover_devices()
    if not devices:
        print("No devices found.")
        return

    device_index = int(input("Select the device index: ")) - 1
    selected_device = devices[device_index]
    print(f"Selected device: {selected_device.name} - {selected_device.address}")

    await explore_device(selected_device)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
