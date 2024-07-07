from ultralytics import YOLO
import cv2
import time
import numpy as np

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)  


while True:
    ret, frame = cap.read()
    start_time = time.time()
    if not ret:
        break

    results = model.predict(frame, show=True)

    current_time = time.time()
    elapsed_time = current_time - start_time
    fps = 1 / np.round(elapsed_time,2)

    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("YOLO Object Detection", frame)

    with open("fps_values.txt", "a") as file:
        file.write(f"{fps:.2f}\n")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
