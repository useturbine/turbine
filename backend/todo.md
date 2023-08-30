milvus-standalone  | [2023/08/30 09:36:36.798 +00:00] [INFO] [config/etcd_source.go:145] ["start refreshing configurations"]
turbine-daemon     | Traceback (most recent call last):
turbine-daemon     |   File "/turbine-api/daemon.py", line 15, in <module>
turbine-daemon     |     debezium = DebeziumDataSource(
turbine-daemon     |   File "/turbine-api/src/datasource/debezium/debezium.py", line 21, in __init__
turbine-daemon     |     self.consumer = KafkaConsumer(
turbine-daemon     |   File "/usr/local/lib/python3.10/site-packages/kafka/consumer/group.py", line 356, in __init__
turbine-daemon     |     self._client = KafkaClient(metrics=self._metrics, **self.config)
turbine-daemon     |   File "/usr/local/lib/python3.10/site-packages/kafka/client_async.py", line 244, in __init__
turbine-daemon     |     self.config['api_version'] = self.check_version(timeout=check_timeout)
turbine-daemon     |   File "/usr/local/lib/python3.10/site-packages/kafka/client_async.py", line 927, in check_version
turbine-daemon     |     raise Errors.NoBrokersAvailable()
turbine-daemon     | kafka.errors.NoBrokersAvailable: NoBrokersAvailable
turbine-daemon exited with code 1


- "dependency" does not check if the services are ready, and not just container is up (docker compose health check)
- need to add dependency on container health check