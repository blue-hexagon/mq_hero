# Telegraf Config
```
[[inputs.mqtt_consumer.topic_parsing]]
  topic = "+/+/+/metrics"
  measurement = "iot_metrics"
  tags = "_/_/_/_"
```

# Schema Documentation
generate-schema-doc .\src\v2\assets\schemas\tenant.schema.yaml ./docs/schema.html

