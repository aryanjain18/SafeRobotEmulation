import torch
import cv2
import time
import numpy as np

# Model
model = torch.hub.load("/home/jetson/yolov5/", "custom", path="/home/jetson/yolov5/yolov5s.pt", source="local")  # or yolov5n - yolov5x6, custom

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    results = model(frame) 

    for det in results.pred[0]:
        x1,y1,x2,y2,conf,cls=det.tolist()
        if cls == 0 and conf>0.5:
            class_name = model.names[int(cls)]
            roi = frame[int(y1):int(y2),int(x1):int(x2)]
            avging = cv2.blur(roi,(21,21))
            #blur = cv2.GaussianBlur(roi,(9,9),cv2.BORDER_DEFAULT)
            frame[int(y1):int(y2), int(x1):int(x2)] = avging
            cv2.rectangle(frame,(int(x1),int(y1),int(x2),int(y2)),(0,0,0),2)
            #print(results.pred[0])
            cv2.putText(frame,f"{class_name}{conf:.2f}",(int(x1),int(y1)-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

           

    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
