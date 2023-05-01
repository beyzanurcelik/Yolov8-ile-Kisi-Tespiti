# VİDEO OKUMA VE YENİDEN BOYUTLANDIRMA

import cv2

# Giriş video dosyası
giris_video = "Istiklal_Caddesi_Yuruyen _Insanlar.mp4"

# Yeni boyut
new_width, new_height = 640, 480

# Çıktı video dosyası
cikis_video = "boyutlandiririlmis_video.mp4"

# Video dosyasını oku
cap = cv2.VideoCapture(giris_video)

# Video codec ve FPS değerleri
codec = cv2.VideoWriter_fourcc(*"mp4v")
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Yeni boyuta göre video dosyasını yeniden boyutlandırma
out = cv2.VideoWriter(cikis_video, codec, fps, (new_width, new_height))
while True:
    ret, frame = cap.read()
    if ret:
        # Yeni boyuta göre yeniden boyutlandır
        resized_frame = cv2.resize(frame, (new_width, new_height))
        # Yeni boyutlu kareyi çıktı dosyasına yaz
        out.write(resized_frame)
        cv2.imshow('boyutlandiririlmis_video', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Video dosyalarını serbest bırak
cap.release()
out.release()
cv2.destroyAllWindows()




