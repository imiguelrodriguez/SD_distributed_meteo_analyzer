from meteo_utils import MeteoDataDetector
import time
import datetime

generator = MeteoDataDetector()
while True:
    time.sleep(2)
    timestamp = datetime.datetime().now()
    data = generator.analyze_pollution()
    # send data
