#!/usr/bin/env bash
set -e

export OTEL_PORT=4318
export PROM_PORT=8889

TMP_FILE=$(mktemp -p /tmp otel-collector-config.yml.XXXXXXX)
trap "rm -f $TMP_FILE" EXIT
chmod a+r $TMP_FILE

cat <<EOF >> $TMP_FILE
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:${OTEL_PORT}
exporters:
  debug:
    verbosity: detailed
  prometheus:
    endpoint: 0.0.0.0:${PROM_PORT}
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      exporters: [debug, prometheus]
    logs:
      receivers: [otlp]
      exporters: [debug]
EOF

docker run \
  --rm \
  -p ${OTEL_PORT}:${OTEL_PORT} \
  -p ${PROM_PORT}:${PROM_PORT} \
   -v ${TMP_FILE}:/etc/otelcol/config.yaml \
   otel/opentelemetry-collector
