import time
import adafruit_dht
import board
from os import environ
import shortuuid
import json

from awscrt import mqtt
from awsiot import mqtt_connection_builder

dht_device = adafruit_dht.DHT11(board.D22)

mqtt_endpoint = environ["MQTT_ENDPOINT"]
cert_filepath = environ["CERT_FILEPATH"]
pri_key_filepath = environ["PRI_KEY_FILEPATH"]
ca_filepath = environ["CA_FILEPATH"]
client_id  = environ["CLIENT_ID"]
mqtt_topic = environ["MQTT_TOPIC"]

if __name__ == '__main__':

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=mqtt_endpoint,
        cert_filepath=cert_filepath,
        pri_key_filepath=pri_key_filepath,
        ca_filepath=ca_filepath,
        client_id=client_id)

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")


    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature != None and humidity != None:
                payload = {
                        "version": "1",
                        "type": "air",
                        "temperature": temperature,
                        "humidity": humidity, 
                        "uuid": shortuuid.uuid()
                    }

                print("Temp:{:.1f} C /  Hum: {}%".format(temperature,humidity))
                
                message_json = json.dumps(payload)
                mqtt_connection.publish(
                    topic=mqtt_topic,
                    payload=message_json,
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                time.sleep(5)
            else: 
                time.sleep(1)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(1)