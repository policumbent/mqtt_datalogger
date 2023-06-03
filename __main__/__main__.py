from Logger import *
from Logger.Logger import Logger
from MqttHandler.MqttHandler import MqttHandler
import logging
import time


topics = {
    "Taurus/bikedata/latitude": '-1',
    "Taurus/bikedata/longitude": '-1',
    "Taurus/bikedata/altitude": '-1',
    "Taurus/bikedata/distance/gps": '-1',
    "Taurus/bikedata/speed_gps": '-1',
    "Taurus/bikedata/timestamp": '-1',
    "Taurus/bikedata/timestamp_net": '-1',
    "Taurus/bikedata/CO2": '-1',
    "Taurus/bikedata/temp": '-1',
    "Taurus/bikedata/TVOC": '-1',
    "Taurus/bikedata/power": '-1',
    "Taurus/bikedata/heartrate": '-1',
    "Taurus/bikedata/rpm/wheel": '-1',
    "Taurus/bikedata/rpm/pedal": '-1',
    "Taurus/bikedata/distance/hall": '-1',
    "Taurus/bikedata/speed_hall": '-1',
    "Taurus/bikedata/gear": '-1',
    "Taurus/bikedata/receiver": '-1',
    "Taurus/bikedata/error": '-1',
    "Taurus/bikedata/limit_switch": '-1'
}




def mqtt_callback(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    logging.info(f"received {payload} on {topic}")
    topics[topic] = payload


def main():
    datalogger = Logger("../log/miriam_datalogger", list(topics.keys()))
    connection = MqttHandler("miriam_datalogger_01", "broker.hivemq.com", 1883, [(t, 0) for t in topics.keys()], mqtt_callback)

    start = time.time()
    while True:
        end = time.time()
        if end - start >= 5:
            start = end
            datalogger.log(list(topics.values()))
        connection.client.loop()


if __name__ == '__main__':
    main()