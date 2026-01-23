import asyncio
from pprint import pprint


class SensorScheduler:

    def __init__(self, mqtt_publisher):
        self.mqtt = mqtt_publisher

    async def run_sensor(self, sensor):
        while True:
            metric_payload = await sensor.read()
            metrics = metric_payload["metrics"]

            alerts = await sensor.check_alerts(metrics)
            print(f"{sensor.device} =>")
            pprint(metric_payload)
            self.mqtt.publish_metric(device=sensor.device, payload=metric_payload)

            ts = metric_payload["ts"]

            for alert in alerts:
                alert_payload = sensor.build_alert_payload(alert, ts)
                pprint(alert_payload)
                self.mqtt.publish_alert(device=sensor.device, payload=alert_payload)
            await asyncio.sleep(sensor.interval)
