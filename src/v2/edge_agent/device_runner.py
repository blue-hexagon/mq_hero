import asyncio


class DeviceRunner:

    def __init__(self, scheduler):
        self.scheduler = scheduler

    async def run(self, device):
        tasks = [
            asyncio.create_task(self.scheduler.run_sensor(sensor))
            for sensor in device.sensors
        ]
        await asyncio.gather(*tasks)