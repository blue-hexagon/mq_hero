import asyncio

from src.v2.edge_agent.device_runner import DeviceRunner


class FarmRunner:

    def __init__(self, device_runner: DeviceRunner):
        self.device_runner = device_runner

    async def run(self, farm):
        tasks = [
            asyncio.create_task(self.device_runner.run(device))
            for device in farm.devices.values()
            if hasattr(device, "sensors")
        ]
        await asyncio.gather(*tasks)
