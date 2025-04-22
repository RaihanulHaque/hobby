# Python code to predict garbage in video from file using ultralytics and yolov8 model
import cv2
import numpy as np
from ultralytics import YOLO
import time
import matplotlib.pyplot as plt

model = YOLO("/Users/rahi/Code/hobby/nimra-paper.pt")
model.device = "mps"
print(model.names)

cap = cv2.VideoCapture(0)

def get_prediction(image):
    results = model.predict(image,)
    result = results[0]
    class_names = result.names
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        probability = round(box.conf[0].item(), 2)
        if(probability < 0.45):
            continue
        output.append({
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "class_name": class_names[class_id],
            "probability": probability
        })
        # print(output)
    return output
   

# For Live Video
while True:
    ret, frame = cap.read()
    # cv2.imshow("Frame", frame)
    # try:
    output = get_prediction(frame)
    for box in output:
        cv2.rectangle(frame, (box["x1"], box["y1"]), (box["x2"], box["y2"]), (255, 0, 0), 2)
        cv2.putText(frame, box["class_name"], (box["x1"], box["y1"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        print(box["class_name"], box["probability"])
 

    cv2.imshow("Frame", frame)
    time.sleep(0.05)
        # out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()




# # For Single Image
# image = cv2.imread("dataset/images.jpeg")
# output = get_prediction(image)
# for box in output:
#     cv2.rectangle(image, (box["x1"], box["y1"]), (box["x2"], box["y2"]), (255, 0, 0), 2)
#     cv2.putText(image, box["class_name"], (box["x1"], box["y1"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     print(box["class_name"], box["probability"])

# # cv2.imshow("Frame", image)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# plt.imshow(image)
# plt.show()

