# VIDEODA ILGILENDIĞIMIZ ALANA (ROI) AIT KOORDINATLARA (X1,Y1)=(150,100) VE (X2,Y2)=(350,400) GÖRE VIDEOYU KIRPMA
import cv2

cap = cv2.VideoCapture("boyutlandiririlmis_video.mp4") # videoyu yükle
x1, y1, x2, y2 = 150, 100, 350, 400 # ROI koordinatları
w, h = x2 - x1, y2 - y1 # ROI boyutları
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # çıktısı alınacak videonun codec'i
out = cv2.VideoWriter("kirpilmis_video.mp4", fourcc, 30, (w, h)) # çıktı video objesi

while True:
    ret, frame = cap.read() # videoyu frame-by-frame oku
    if ret:
        roi = frame[y1:y2, x1:x2] # ROI'yi kırp
        out.write(roi) # çıktı videoya yazdır
        cv2.imshow("KIRPILMIS VİDEO", roi) # ROI'yi göster
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()