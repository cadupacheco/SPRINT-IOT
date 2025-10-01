import json
import time
import threading
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, JSON as SA_JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import paho.mqtt.client as mqtt

DATABASE_URL = 'sqlite:///./detections.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Detection(Base):
    __tablename__ = 'detections'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Float, index=True)
    payload = Column(SA_JSON)  # SQLAlchemy will handle JSON for SQLite as text

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mottu - Detections API")

class DetectionIn(BaseModel):
    timestamp: float
    detections: List[dict]

@app.post('/detections/')
def receive_detection(d: DetectionIn):
    db = SessionLocal()
    row = Detection(timestamp=d.timestamp, payload=d.dict())
    db.add(row)
    db.commit()
    db.close()
    return {'status': 'ok'}

@app.get('/health')
def health():
    return {'status': 'running'}

# MQTT bridge: subscribe to topic and persist messages into DB
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "mottu/detections"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker, subscribing to topic:", MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        db = SessionLocal()
        row = Detection(timestamp=payload.get('timestamp', time.time()), payload=payload)
        db.add(row)
        db.commit()
        db.close()
    except Exception as e:
        print("Error persisting MQTT message:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt_loop():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

# Start MQTT listener in background thread (daemon so process can exit)
threading.Thread(target=start_mqtt_loop, daemon=True).start()
