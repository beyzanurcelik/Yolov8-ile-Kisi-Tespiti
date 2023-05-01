from ultralytics import YOLO
import cv2
import cvzone
import math
import time
from sort import *

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

mask = cv2.imread("mask.jpg")

# takip
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

prev_frame_time = 0
new_frame_time = 0

cap = cv2.VideoCapture("kirpilmis_video.mp4") # okunacak video dosyasının belirtilmesi 

# video kayıt için fourcc ve VideoWriter tanımlama
cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
success, img = cap.read()
#print(img.shape)
#cv2.imwrite("ornek_resim.jpg", img)
size = list(img.shape)
del size[2]
size.reverse()
video = cv2.VideoWriter("kaydedilen_video.mp4", cv2_fourcc, 24, size)

# modelin yüklenmesi
model = YOLO("yolov8n.pt")

limits = [70, 0, 70, 293]   # videoda sınır olarak belirlenen cizginin koordinatları
totalCount = [] # tutulacak kişi sayısını ifade eden liste

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    
    imgRegion = cv2.bitwise_and(img, mask) #videodan alınan görüntü üzerine maskeleme isleminin yapılması


    results = model(imgRegion, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls == 0:    # 0 kişi için sınıf indeksidir
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                # nesnenin güven skorunun belirlenmesi
                conf = math.ceil((box.conf[0] * 100)) / 100
            currentArray = np.array([x1, y1, x2, y2, conf])
            detections = np.vstack((detections, currentArray))
           
    resultsTracker = tracker.update(detections)   # yukarıda olusturulan numpy dizisindeki nesnelerin izlenmesini saglar 
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (255, 255, 255), 4)   # img üzerindeki çizginin çizilmesi

    # bu for döngüsüyle izlenen nesnelerin konumları güncellenir ve bu nesneler ekrana çizilir
    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))    # img üzerine dikdörtgen çizilmesi
        cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                           scale=1, thickness=1, offset=10)     # izlenen nesnenin id değeri ekrana yazılır

        cx, cy = x1 + w // 2, y1 + h // 2   # izlenen nesnenin merkez koordinatlarının hesaplanması
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) # img üzerine merkez koordinata göre daire cizilmesi

        # bu if koşuluyla cizdirilen çizgiden gecen kisilerin saydırılması amaclanmıstır. 
        if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
            if totalCount.count(id) == 0:
                totalCount.append(id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 3)

    cv2.putText(img, str(len(totalCount)), (80, 280), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 8)    # hesaplanan kişi sayısının ekrana yazdırılması 
    
    # video kayıt
    video.write(img)

    cv2.imshow("Kisi Tespiti", img)
    if cv2.waitKey(1) == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()

