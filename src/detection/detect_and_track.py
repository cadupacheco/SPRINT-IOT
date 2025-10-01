import time
import json
import argparse
from ultralytics import YOLO
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from collections import OrderedDict
from typing import List, Tuple

class CentroidTracker:
    def __init__(self, max_disappeared=50):
        self.next_object_id = 0
        self.objects = OrderedDict()       # id -> (centroid, bbox)
        self.disappeared = OrderedDict()   # id -> disappeared_count
        self.max_disappeared = max_disappeared

    def register(self, centroid: Tuple[int,int], bbox: Tuple[int,int,int,int]):
        self.objects[self.next_object_id] = (centroid, bbox)
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id: int):
        if object_id in self.objects:
            del self.objects[object_id]
        if object_id in self.disappeared:
            del self.disappeared[object_id]

    def update(self, rects: List[Tuple[int,int,int,int]]):
        # rects: list of bbox (x1,y1,x2,y2)
        if len(rects) == 0:
            for oid in list(self.disappeared.keys()):
                self.disappeared[oid] += 1
                if self.disappeared[oid] > self.max_disappeared:
                    self.deregister(oid)
            return self.objects

        input_centroids = []
        for (x1, y1, x2, y2) in rects:
            cX = int((x1 + x2) / 2.0)
            cY = int((y1 + y2) / 2.0)
            input_centroids.append((cX, cY))

        if len(self.objects) == 0:
            for i, c in enumerate(input_centroids):
                self.register(c, rects[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = [v[0] for v in self.objects.values()]

            D = np.linalg.norm(np.array(object_centroids)[:, None] - np.array(input_centroids)[None, :], axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (r, c) in zip(rows, cols):
                if r in used_rows or c in used_cols:
                    continue
                oid = object_ids[r]
                self.objects[oid] = (input_centroids[c], rects[c])
                self.disappeared[oid] = 0
                used_rows.add(r)
                used_cols.add(c)

            unused_rows = set(range(0, D.shape[0])) - used_rows
            for r in unused_rows:
                oid = object_ids[r]
                self.disappeared[oid] += 1
                if self.disappeared[oid] > self.max_disappeared:
                    self.deregister(oid)

            unused_cols = set(range(0, D.shape[1])) - used_cols
            for c in unused_cols:
                self.register(input_centroids[c], rects[c])

        return self.objects

def publish_mqtt(client, topic: str, payload: dict):
    client.publish(topic, json.dumps(payload))

def main(args):
    model = YOLO(args.model)
    cap = cv2.VideoCapture(args.video if args.video else 0)
    tracker = CentroidTracker()

    # MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.connect(args.mqtt_host, args.mqtt_port, 60)

    last_print = time.time()
    frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames += 1
        # run inference (ultralytics returns results objects)
        results = model(frame)[0]

        bboxes = []
        # results.boxes.data is tensor-like: [x1,y1,x2,y2,conf,class]
        if hasattr(results, 'boxes') and len(results.boxes) > 0:
            for r in results.boxes.data.tolist():
                x1, y1, x2, y2, conf, cls = r
                # Optionally filter by class (e.g., motorbike). For generality we include all detections.
                bboxes.append((int(x1), int(y1), int(x2), int(y2)))

        objects = tracker.update(bboxes)

        detections_payload = {"timestamp": time.time(), "detections": []}
        for oid, (centroid, bbox) in objects.items():
            x1, y1, x2, y2 = bbox
            detections_payload["detections"].append({
                "id": int(oid),
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "centroid": [int(centroid[0]), int(centroid[1])]
            })
            # draw on frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {oid}", (x1, max(y1-10,0)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # publish detections if any (or publish empty to indicate heartbeat)
        publish_mqtt(mqtt_client, args.mqtt_topic, detections_payload)

        # display FPS occasionally
        if time.time() - last_print >= 1.0:
            print(f"FPS ~ {frames/(time.time()-last_print):.2f} (approx)")
            frames = 0
            last_print = time.time()

        cv2.imshow('detections', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='yolov8n.pt', help='ultralytics model (pt or yaml)')
    parser.add_argument('--video', default=None, help='path to video or omit for webcam')
    parser.add_argument('--mqtt_host', default='localhost', help='MQTT broker host')
    parser.add_argument('--mqtt_port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--mqtt_topic', default='mottu/detections', help='MQTT topic to publish detections')
    args = parser.parse_args()
    main(args)
