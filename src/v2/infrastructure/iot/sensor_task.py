import asyncio
import random
import time

from src.v2.infrastructure.iot.errors import SensorReadError


async def sensor_task(sensor):
    interval = sensor.interval

    # optional startup jitter
    await asyncio.sleep(random.uniform(0, interval * 0.1))

    while True:
        start = time.time()

        try:
            data = await sensor.read()  # noqa
            # publish_sensor_data(sensor, data)
        except SensorReadError as e:  # noqa
            pass  # handle_sensor_error(sensor, e)

        await asyncio.sleep(max(0, interval - (time.time() - start)))
