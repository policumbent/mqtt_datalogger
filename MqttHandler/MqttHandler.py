from paho.mqtt import client as mqtt_client
import random
import time
import logging


class MqttHandler:

    def __init__(self, client_id: str, host: str, port: int, topics: list, callback: callable, pswd="", usr=""):
        self._broker_hostname = host
        self._port = port
        self._topic_list = topics
        self._client_id = client_id + str(random.randint(1, 100))
        self._pswd = pswd
        self._usr = usr

        self.client = self.connectMqtt(callback)

    def on_connect(self, client, userdata, flags, rc):
        print(flags)
        if rc == 0:
            logging.info(f"connected to {self._broker_hostname}")
        else:
            logging.info("failed to connect, return code %d\n", rc)

    def on_disconnect(self, client, usrdata, rc):
        logging.info(f"disconnected with result code {rc}")

        reconnect_count, reconnect_delay = 0, 1
        while reconnect_count < 10:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.info("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= 1
            reconnect_delay = min(reconnect_delay, 10)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


    def connectMqtt(self, callback: callable):

        client = mqtt_client.Client(self._client_id)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.username_pw_set(self._usr, self._pswd)
        client.on_message = callback

        # connecting to the mqtt broker
        client.connect(self._broker_hostname, self._port)


        for t in self._topic_list:
            client.subscribe(topic=t)
        return client