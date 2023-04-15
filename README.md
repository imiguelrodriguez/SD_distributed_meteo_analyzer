# SD_distributed_meteo_analyzer
Task 1 of SD (Sistemes Distribuïts) subject. The system analyzes fictional meteorogical data and communicates with servers which process and store the data. It explores both direct and indirect communication. The results will be shown as a real-time plot in a terminal. 

The system has been developed using the PyCharm IDE and a virtual environment. The required installed modules are: `grpcio`, `pika`, `pickle`, `json`, `redis`, `pytz` and `matplotlib`. The rest of the modules are supposed to be installed by default.

Please, make sure that a **Redis** server is running on default port 6379, and a **RabbitMQ** server is running on default port 5672.
## Direct communication
In order to run the direct communication system, follow the next steps:
1. Run `loadBalancer.py` in the **lb** folder.
2. Run several `airSensor.py` and `pollutionSensor.py` in the **sensors** folder.
3. Run several `processingServer.py` in the **ps** folder.
4. Run `proxy.py` in the **proxy** folder.
5. Run several `model.py` inside the **terminal/model** folder.

## Indirect communication
In order to run the indirect communication system, follow the next steps:
1. Run several `airSensorIndirect.py` and `pollutionSensorIndirect.py` in the **sensors** folder.
2. Run several `processingServerIndirect.py` in the **ps** folder.
3. Run `proxyIndirect.py` in the **proxy** folder.
4. Run several `modelIndirect.py` inside the **terminal/model** folder.

