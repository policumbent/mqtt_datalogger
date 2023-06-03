from paho.mqtt import client as mqtt_client
import time
import logging


class MqttHandler:

    def __init__(self, client_id: str, host: str, port: int, topics: list, callback: callable, pswd="", usr=""):
        self._broker_hostname = host
        self._port = port
        self._topic_list = topics
        self._client_id = client_id
        self._pswd = pswd
        self._usr = usr

        self.client = self.connectMqtt(callback)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"connected to {self._broker_hostname}")
        else:
            logging.info("failed to connect, return code %d\n", rc)

    def on_disconnect(self, client, usrdata, rc):
        logging.info(f"disconnected with result code {rc}")

        while True:
            try:
                client.reconnect()
                logging.info("successfully reconnected")
                return
            except Exception as e:
                logging.error(f"{e} --> reconnection attempt")
                time.sleep(1)

    def connectMqtt(self, callback: callable):

        client = mqtt_client.Client(self._client_id)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.username_pw_set(self._usr, self._pswd)

        # connecting to the mqtt broker
        client.connect(self._broker_hostname, self._port)
        client.subscribe(topic=self._topic_list)
        client.on_message = callback
        return client