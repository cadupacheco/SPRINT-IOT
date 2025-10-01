import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "mottu/sensors"

def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    while True:
        payload = {
            'timestamp': time.time(),
            'sensor_id': 'sim01',
            'gps': {'lat': -23.55 + random.random()*0.001, 'lon': -46.63 + random.random()*0.001},
            'battery': random.randint(30, 100),
            'status': random.choice(['ok', 'idle', 'moving'])
        }
        client.publish(TOPIC, json.dumps(payload))
        print("published simulated sensor:", payload)
        time.sleep(1)

if __name__ == "__main__":
    main()
