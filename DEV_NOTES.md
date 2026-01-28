# Telegraf Config

```
[[inputs.mqtt_consumer.topic_parsing]]
  topic = "+/+/+/metrics"
  measurement = "iot_metrics"
  tags = "_/_/_/_"
```

# Schema Documentation

generate-schema-doc .\src\v2\assets\schemas\tenant.schema.yaml ./docs/schema.html

# Docker

docker compose up -d
docker exec -it grafana ls /var/lib/grafana/dashboards

## Nuke (W/O Images)

docker compose down -v
docker system prune --volumes
<Y>

```json
{
  'amperage': 51.81,
  'area': 'barn',
  'device_id': 'electricity-01',
  'farm': 'tagensgaard',
  'lat': 55.40375,
  'lng': 11.3542,
  'schema': 'sensor.metric.v1',
  'ts': 1769534617,
  'voltage': 404.51,
  'wattage': 26996.85
}
```