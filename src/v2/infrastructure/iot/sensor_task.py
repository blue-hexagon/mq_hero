import asyncio
import random
import time


async def sensor_task(sensor):
    interval = sensor.interval

    # optional startup jitter
    await asyncio.sleep(random.uniform(0, interval * 0.1))

    while True:
        start = time.time()

        try:
            data = await sensor.read()
            # publish_sensor_data(sensor, data)
        except Exception as e:
            pass  # handle_sensor_error(sensor, e)

        await asyncio.sleep(max(0, interval - (time.time() - start)))
