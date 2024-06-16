import time
import adafruit_dht
import board

dht_device = adafruit_dht.DHT11(board.D22)

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print("Temp:{:.1f} C /  Hum: {}%".format(temperature,humidity))
    except RuntimeError as error:
        print(error.args[0])
    time.sleep(2.0)