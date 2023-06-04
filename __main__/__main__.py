from Logger import *
from Logger.Logger import Logger
from MqttHandler.MqttHandler import MqttHandler
import logging
import time


topics_miriam = {
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

topics_sara = {
    "Policumbent/weather/ws1/timestamp": '-1',
    "Policumbent/weather/ws1/temperature": '-1',
    "Policumbent/weather/ws1/humidity": '-1',
    "Policumbent/weather/ws1/pressure": '-1',
    "Policumbent/weather/ws1/speed": '-1',
    "Policumbent/weather/ws1/direction": '-1',
    "Policumbent/weather/ws1/latitude": '-1',
    "Policumbent/weather/ws1/longitude": '-1',
    "Policumbent/weather/ws1/altitude": '-1',
}




def mqtt_callback(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    logging.info(f"received {payload} on {topic}")
    topics_miriam[topic] = payload


def main():
    datalogger_miriam = Logger("../log/miriam/miriam_datalogger", list(topics_miriam.keys()))
    connection_miriam = MqttHandler("miriam_datalogger_01", "broker.hivemq.com", 1883, [(t, 0) for t in topics_miriam.keys()], mqtt_callback)

    datalogger_sara = Logger("../log/sara/miriam_datalogger", list(topics_sara.keys()))
    connection_sara = MqttHandler("sara_datalogger_01", "broker.hivemq.com", 1883,
                                    [(t, 0) for t in topics_sara.keys()], mqtt_callback)

    start = time.time()
    while True:
        end = time.time()
        if end - start >= 5:
            start = end
            datalogger_miriam.log(list(topics_miriam.values()))
            datalogger_sara.log(list(topics_sara.values()))
        connection_miriam.client.loop()
        connection_sara.client.loop()


if __name__ == '__main__':
    main()