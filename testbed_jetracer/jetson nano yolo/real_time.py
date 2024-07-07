import torch
import cv2
import time
import numpy as np

# Model
model = torch.hub.load("/home/jetson/yolov5/", "custom", path="/home/jetson/yolov5/yolov5s.pt", source="local")  # or yolov5n - yolov5x6, custom

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    start_time = time.time()
    results = model(frame)  # Perform object detection
    current_time = time.time()
    elapsed_time = current_time - start_time
    fps = 1 / np.round(elapsed_time, 2)
    fps_text = f"FPS: {fps:.2f}"
    
    # Convert the rendered frame to a compatible format for cv2.imshow
    rendered_frame = results.render()[0]  # Assuming that render() returns a list
    #rendered_frame = np.array(rendered_frame[:, :, ::-1])  # Convert from RGB to BGR
    
    cv2.putText(rendered_frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("fps_frame", rendered_frame)
    
    with open("fps_values_battery.txt", "a") as file:
        file.write(f"{fps:.2f}\n")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
