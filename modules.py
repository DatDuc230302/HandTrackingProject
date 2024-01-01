import cv2
import numpy as np
import HandTrackingModule as htm
import autopy

# Chiều dài và chiều cao của Camera
wCam = 1920
hCam = 1080
# Khung hình
frameR = 100
# Độ mượt
smoothening = 6

# Đặt chiều dài và chiều rộng cho Camera
camera = cv2.VideoCapture(0)
camera.set(3, wCam)
camera.set(4, hCam)



def nhan_dien_ban_tay():
    detector = htm.handDetector()
    while True:
        # 1. Tìm các điểm trên bàn tay
        success, img = camera.read()
        img = detector.findHands(img)
        detector.findPosition(img)
        # 2. Đếm giá trị các ngón đang đưa lên hoặc không đưa lên
        fingers = detector.fingersUp()
        num_fingers = fingers.count(1)
        cv2.putText(img, f'So ngon tay: {num_fingers}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
        # 4. Kiểm tra: Nếu khống có ngón nào đưa lên thì sẽ xuất không có ngón nào còn lại thì sẽ hiện tên theo ngón đưa lên
        if(fingers.count(1) == 0):
            cv2.putText(img, f'Khong co ngon nao', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
        else:
            if(fingers[0] == 1):
                cv2.putText(img, f'Ngon cai', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
            if(fingers[1] == 1):
                cv2.putText(img, f'Ngon tro', (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
            if(fingers[2] == 1):
                cv2.putText(img, f'Ngon giua', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
            if(fingers[3] == 1):
                cv2.putText(img, f'Ngon ap ut', (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
            if(fingers[4] == 1):
                cv2.putText(img, f'Ngon ut', (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
        # 5. Hiển thị hình ảnh
        cv2.imshow("Nhan dien ban tay", img)
        cv2.waitKey(1)
def di_chuyen_chuot():
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    detector = htm.handDetector(maxHands=1)
    wScr, hScr = autopy.screen.size()

    while True:
        # 1. Tìm điểm trên bàn tay
        success, img = camera.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        # 2. Get the tip of the index and middle fingers
        cv2.putText(img, f'Hanh dong', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

        # 3. Kiểm tra các ngon tay đang đưa lên
        fingers = detector.fingersUp()
        # 4. Di chuyển con trỏ chuột chỉ khi ngón cái đưa lên
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr - clocX, clocY)  # Di chuyển con trỏ chuột
            plocX, plocY = clocX, clocY  # Cập nhật vị trí trước đó cho việc làm mịn
            cv2.putText(img, f'Di chuyen', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)

        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            autopy.mouse.click()
            cv2.putText(img, f'Click', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 0, 0), 2)
        # 14. Hien thi hinh anh
        cv2.imshow("Nhan dien cu chi tay", img)
        cv2.waitKey(1)