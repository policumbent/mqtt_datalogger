from Logger.Logger import Logger
from Uploader.Uploader import Uploader
from MqttHandler.MqttHandler import MqttHandler
from random import randint
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

topics_miriam_csv = [
    "latitude",
    "longitude",
    "altitude",
    "distance/gps",
    "speed_gps",
    "timestamp",
    "timestamp_net",
    "CO2",
    "temp",
    "TVOC",
    "power",
    "heartrate",
    "rpm/wheel",
    "rpm/pedal",
    "distance/hall",
    "speed_hall",
    "gear",
    "receiver",
    "error",
    "limit_switch"
]

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

topics_sara_csv = [
    "timestamp",
    "temperature",
    "humidity",
    "pressure",
    "speed",
    "direction",
    "latitude",
    "longitude",
    "altitude"
]


def mqtt_callback_miriam(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    logging.info(f"received {payload} on {topic}")
    topics_miriam[topic] = payload


def mqtt_callback_sara(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    logging.info(f"received {payload} on {topic}")
    topics_sara[topic] = payload


def main():
    datalogger_miriam = Logger("./log/miriam/miriam_datalogger", list(topics_miriam.keys()), topics_miriam_csv)
    connection_miriam = MqttHandler("miriam_datalogger_"+str(randint(0, 100)), "broker.hivemq.com", 1883, [(t, 0) for t in topics_miriam.keys()], mqtt_callback_miriam)

    datalogger_sara = Logger("./log/sara/sara_datalogger", list(topics_sara.keys()), topics_sara_csv)
    connection_sara = MqttHandler("sara_datalogger_"+str(randint(0, 100)), "broker.hivemq.com", 1883,
                                    [(t, 0) for t in topics_sara.keys()], mqtt_callback_sara)
    #database path:
    db = r"./test.db"
    uploader = Uploader(db)
    conn = uploader.create_connection(db)
    if conn is not None:
        miriam_table = uploader.generate_table(db, topics_miriam_csv, "Miriam")
        sara_table = uploader.generate_table(db, topics_sara_csv, "Sara")
    else:
        print(f"no connection established.")
    #generate miriam and sara table
    
    connection_miriam.client.loop_start()
    connection_sara.client.loop_start()
    

    
    start = time.time()
    while True and conn:
        end = time.time()
        if end - start >= 1:
            start = end
            #uploading data in db and csv file for Miriam
            datalogger_miriam.log(list(topics_miriam.values()))
            print("Miriam -> " + str(list(list(topics_miriam.values()))))
            uploader.insert_table(topics_miriam_csv,topics_miriam.values(),"Miriam")
            
            #uploading data in db and csv file for Sara
            datalogger_sara.log(list(topics_sara.values()))
            print("Sara -> " + str(list(list(topics_sara.values()))))
            uploader.insert_table(topics_sara_csv,topics_sara.values(),"Sara")
        if not connection_miriam.client.is_connected():
            print("attempting reconnection")
            connection_miriam.client.reconnect()
        if not connection_sara.client.is_connected():
            print("attempting reconnection")
            connection_sara.client.is_connected()
        

    connection_miriam.client.loop_stop()
    connection_sara.client.loop_stop()


if __name__ == '__main__':
    main()