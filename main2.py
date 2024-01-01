import cv2
import time
import hand as htm
import math
import autopy
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0)

# Chiều dài và chiều cao của Camera
wCam = 10000
hCam = 10000
cap.set(3, hCam)
cap.set(4, wCam)
pTime = 0




detector = htm.handDetector(detectionCon= 1)

fingerID = [4, 8, 12, 16, 20]
# fingerID Một mảng chứa đầu các ngón tay theo thư viện mediapipe 4 là cái, 8 là trỏ, 12 là giữa, 16 là áp út và 20 là út


volumeValue = 0 # Khởi tạo giá trị âm thanh ban đầu là 0

menu = 0 # Khởi tạo giá trị menu ban đầu là 0

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    # lmList sẽ trả về 20 mảng, mỗi mãng chứa 3 phần tử: phần tử 0 là điểm trên mắt bàn tay, phần tử 1 là trục x mà phần tử 0 đang đứng
    # và phần tử 2 là trục y mà phần tử 0 đang đứng
    lmList = detector.findPosition(frame, draw= False)

    if menu == 0:
        cv2.putText(frame, f"Menu chuc nang", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"1.Mau xanh: Nhan dien ban tay va dem ngon tay.", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2)
        cv2.putText(frame, f"2.Mau cam: Dieu khien am thanh.", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2)
        cv2.putText(frame, f"3.Mau hong: Di chuyen va click chuot.", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2)
        cv2.putText(frame, f"4.Mau den: Thoat chuong trinh", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Dung ngon cai de bam vao cac mau tren ban tay", (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2)
    fingers = [] # Tạo mãng chứa chỉ số 1 và 0, 1 là ngón tay dơ và 0 là ngón tay úp

    if len(lmList) != 0:
        # Kiểm tra ngón tay cái dơ lên hay úp (Điểm 4 nằm bên trái hay bên phải của điểm 3 đối với bàn tay phải)
        # lmList[fingerID[0]][1]] là tọa độ trục x điểm 4 của ngón cái,
        # lmList[fingerID[0] - 1][1] là tọa độ trục x điểm 3 của ngón cái,
        # nếu như trục x điểm 4 nhỏ hơn trục x điểm 1 ngón cái => đang úp
        if lmList[fingerID[0]][1] < lmList[fingerID[0] - 1][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        # Tương tự như ngón cái kiểm tra ngón dài
        # lmList[fingerID[id]][2]] là tọa độ điểm cao nhất trục y của ngón tay  dài,
        # lmList[fingerID[id] - 2][2] là tọa điểm cao nhất - 2 trục y của ngón cái,
        # nếu như trục y điểm cao nhất nhỏ hơn trục y điểm cao nhất - 2 => đang úp
        for id in range(1, 5):
            if lmList[fingerID[id]][2] < lmList[fingerID[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        cv2.circle(frame, (lmList[20][1], lmList[20][2]), 10, (0, 0, 0), cv2.FILLED)

        if menu == 0:
            # Vẽ màu
            for i in [4, 8, 12, 16]:
                if i == 4:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (0, 0, 255), cv2.FILLED)
                elif i == 8:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (0, 255, 0), cv2.FILLED)
                elif i == 12:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (0, 165, 255), cv2.FILLED)
                elif i == 16:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (255, 0, 255), cv2.FILLED)
            # Chọn chức năng
            x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa dộ x và y điểm 4 trên bàn tay
            x2, y2 = lmList[8][1], lmList[8][2]  # Lấy tọa dộ x và y điểm 8 trên bàn tay
            x3, y3 = lmList[12][1], lmList[12][2]  # Tọa tọa độ x và y điểm 12 trên bàn tày
            x4, y4 = lmList[16][1], lmList[16][2]  # Tọa độ x và y điểm 16 trên bàn tày
            x5, y5 = lmList[20][1], lmList[20][2]  # Tọa độ x và y điểm 20 trên bàn tày
            # Em sử dụng công thức toán học căn bậc hai của tổng hai bình phương của hiệu giữa hai tọa dộ x2 và x1 và y2 và y1
            # Tính khoảng cách giữa đầu ngón cái và đầu ngón trỏ
            caiVaTro = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            caiVaGiua = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
            caiVaApUt = math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2)
            caiVaUt = math.sqrt((x5 - x1) ** 2 + (y5 - y1) ** 2)
            if caiVaTro < 35: # Nhận dạng bàn tay, số ngón tay, tên ngón tay
                menu = 1
            elif caiVaGiua < 35:  # Điều chỉnh âm thanh.
                menu = 2
            elif caiVaApUt < 35: # Di chuyển và click chuột.
                menu = 3



        elif menu == 1: # Nhận dạng bàn tay, hiển thị số ngón tay tên ngón tay
            # Chèn chữ hiển thị số ngón tay đang dơ lên
            cv2.putText(frame, f"So ngon tay do: {fingers.count(1)} ", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),                            2)

            # Chèn chữ hiển thị số ngón tay đang dơ lên
            cv2.putText(frame, f"Ten ngon tay:", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 0), 2)

            # Hiện tên ngón tay đang dơ lên
            if len(fingers) != 0:  # Kiểm tra độ dài của mảng khác 0 thì mới tiếp tục
                if fingers[0] == 1:
                    cv2.putText(frame, f"Ngon cai", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
                if fingers[1] == 1:
                    cv2.putText(frame, f"Ngon tro", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
                if fingers[2] == 1:
                    cv2.putText(frame, f"Ngon giua", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
                if fingers[3] == 1:
                    cv2.putText(frame, f"Ngon ap ut", (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
                if fingers[4] == 1:
                    cv2.putText(frame, f"Ngon ut", (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
                    # Module thoát chương trình
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa dộ x và y điểm 4 trên bàn tay
                x2, y2 = lmList[20][1], lmList[20][2]  # Tọa tọa độ x và y điểm 20 trên bàn tày
                # Em sử dụng công thức toán học căn bậc hai của tổng hai bình phương của hiệu giữa hai tọa dộ x2 và x1 và y2 và y1
                # Tính khoảng cách giữa đầu ngón cái và đầu ngón trỏ
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < 35:  # Kiểm tra nếu khoảng cách nhỏ hơn 35 thì sẽ thoát chương trình
                    menu = 0

        # Module điều khiển âm thanh
        elif menu == 2:
            for i in [4, 8]:
                x, y = lmList[i][1], lmList[i][2]  # Lấy tọa độ trục x và y của ngón cái và ngón trỏ
                cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)  # Vẽ đoạn thẳng từ ngón cái đến ngón trỏ
            lenLine = math.hypot(x2 - x1, y2 - y1)  # math.hypot là công thức toán học dùng để tính độ dài của 2 điểm ở đây là ngón trỏ và ngón cái

            # Vì do khi đưa tay xa hoặc gần thì giá trị sẽ thay đổi
            # Nên em sử dụng max và min để có định giá trị luôn trong khoản 0 đến 100
            volumeValue = int(max(0, min((lenLine - 30) / (400 - 100) * 100, 100)))
            cv2.putText(frame, f"Gia tri am luong: {volumeValue}%", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 0, 0), 2)
            # Sử dụng thư viện pycaw để điều chỉnh âm lượng
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            # Lấy giá trị âm lượng hiện tại
            current_volume = volume.GetMasterVolumeLevelScalar()

            # Áp dụng giá trị âm lượng mới
            volume.SetMasterVolumeLevelScalar(volumeValue / 100.0, None)


            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa dộ x và y điểm 4 trên bàn tay
                x2, y2 = lmList[20][1], lmList[20][2]  # Tọa tọa độ x và y điểm 20 trên bàn tày
                # Em sử dụng công thức toán học căn bậc hai của tổng hai bình phương của hiệu giữa hai tọa dộ x2 và x1 và y2 và y1
                # Tính khoảng cách giữa đầu ngón cái và đầu ngón trỏ
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < 35:  # Kiểm tra nếu khoảng cách nhỏ hơn 35 thì sẽ thoát chương trình
                    menu = 0

        # Module điều khiển và di chuyển chuột
        if menu == 3:
            for i in [4, 5, 8, 12]:
                if i == 4:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (0, 255, 0), cv2.FILLED)
                elif i == 5:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (0, 165, 255), cv2.FILLED)
                elif i == 8 or i == 12:
                    cv2.circle(frame, (lmList[i][1], lmList[i][2]), 10, (0, 0, 255), cv2.FILLED)

            # Điều kiện khi chỉ có ngón trỏ và ngón cái dơ thì mới thực hiện đoạn mã phía trong
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                xMouse = (lmList[8][1] + lmList[12][1]) / 2  # Lấy tọa độ x ngón tay trỏ hiện tại
                yMouse = (lmList[8][2] + lmList[12][2]) / 2  # Lấy tọa độ y ngón tay trỏ hiện tại
                autopy.mouse.move(xMouse, yMouse)  # Di chuyển con trỏ chuột
                cv2.putText(frame, f"Di chuyen chuot", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                2)

            # Module Click chuột trái
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa dộ x và y điểm 4 trên bàn tay
                x2, y2 = lmList[5][1], lmList[5][2]  # Tọa tọa độ x và y diêm 5 trên bàn tày
                # Em sử dụng công thức toán học căn bậc hai của tổng hai bình phương của hiệu giữa hai tọa dộ x2 và x1 và y2 và y1
                # Tính khoảng cách giữa đầu ngón cái và đầu ngón trỏ
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < 35:  # Kiểm tra nếu khoảng cách nhỏ hơn 35 thì sẽ click chuột
                    autopy.mouse.click()
                    cv2.putText(frame, f"Click chuot trai", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)

            # Module Click chuột phải
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa dộ x và y điểm 4 trên bàn tay
                x2, y2 = lmList[5][1], lmList[5][2]  # Tọa tọa độ x và y diêm 5 trên bàn tày
                # Em sử dụng công thức toán học căn bậc hai của tổng hai bình phương của hiệu giữa hai tọa dộ x2 và x1 và y2 và y1
                # Tính khoảng cách giữa đầu ngón cái và đầu ngón trỏ
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < 35:  # Kiểm tra nếu khoảng cách nhỏ hơn 35 thì sẽ click chuột phải
                    autopy.mouse.click(autopy.mouse.Button.RIGHT)
                    cv2.putText(frame, f"Click chuot phai", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
            # Về menu
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa dộ x và y điểm 4 trên bàn tay
                x2, y2 = lmList[20][1], lmList[20][2]  # Tọa tọa độ x và y điểm 20 trên bàn tày
                # Em sử dụng công thức toán học căn bậc hai của tổng hai bình phương của hiệu giữa hai tọa dộ x2 và x1 và y2 và y1
                # Tính khoảng cách giữa đầu ngón cái và đầu ngón trỏ
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < 35:  # Kiểm tra nếu khoảng cách nhỏ hơn 35 thì sẽ thoát chương trình
                    menu = 0
            cv2.putText(frame, f"Do ngon cai, tro va giua de di chuyen chuot", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)
            cv2.putText(frame, f"Do ngon tro va ngon giua xanh va cam cham nhau click chuot trai", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)
            cv2.putText(frame, f"Do ngon tro va dung diem xanh va cam cham nhau click chuot phai", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)



        # if volumeControl == 0:
        #     # Vẽ hình tròn lên đầu ngón trỏ và đầu ngón cái
        #     for idx in [4, 5, 8, 12, 16]:
        #         x, y = lmList[idx][1], lmList[idx][2] # Lấy tọa độ trục x và y của ngón cái và ngón trỏ
        #         if idx == 8 or idx == 12: # Thỏa điều kiện này thì sẽ tô màu đỏ
        #             cv2.circle(frame, (x, y), 10, (0, 0, 255), cv2.FILLED)
        #         else: # Còn không sẽ tô màu xanh
        #             cv2.circle(frame, (x, y), 10, (0, 255, 0), cv2.FILLED)
        #
        #
        #
        #     else:
        #         # Khi kích hoạt chức năng điều khiển âm thanh thì sẽ vẽ chỉ vẽ ô tròn cho ngón cái và ngón trỏ
        #         for idx in [4, 8, 12]:
        #             x, y = lmList[idx][1], lmList[idx][2]  # Lấy tọa độ trục x và y của ngón cái và ngón trỏ
        #             if idx == 4 or idx == 8:
        #                 cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
        #             else:
        #                 cv2.circle(frame, (x, y), 10, (0, 255, 0), cv2.FILLED)
        #         x1, y1 = lmList[4][1], lmList[4][2]  # Lấy tọa độ x và y của ngón cái
        #         x2, y2 = lmList[8][1], lmList[8][2]  # Lấy tọa độ x và y của ngón trỏ
        #         cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 4) #Vẽ đoạn thẳng từ ngón cái đến ngón trỏ
        #
        #         lenLine = math.hypot(x2 - x1, y2 - y1) # math.hypot là công thức toán học dùng để tính độ dài của 2 điểm ở đây là ngón trỏ và ngón cái
        #
        #         cv2.putText(frame, f"Gia tri am luong: {volumeValue}%", (800, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #                     (255, 0, 0), 2)
        #
        #         volumeValue = int((lenLine - 30) / (450 - 30) * 100)
        #
        #         if int((lenLine - 30) / (450 - 30) * 100) > 0 and int((lenLine - 30) / (450 - 30) * 100) < 100:
        #             volumeValue = int((lenLine - 30) / (450 - 30) * 100)
        #
        #         devices = AudioUtilities.GetSpeakers()
        #         interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        #         volume = cast(interface, POINTER(IAudioEndpointVolume))
        #         # Lấy giá trị âm lượng hiện tại
        #         current_volume = volume.GetMasterVolumeLevelScalar()
        #         # Áp dụng giá trị âm lượng mới
        #         volume.SetMasterVolumeLevelScalar(volumeValue / 100.0, None)


    cTime = time.time() # Trả về số giây, vào thời điểm bắt đầu thời gian
    fps = 1/(cTime-pTime) # Tính số khung hình trên một giây
    pTime = cTime

    # Hiển thị FPS lên màn hình
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Nhan dien cua chi tay", frame)


    if cv2.waitKey(1) == ord("q"): # độ trễ 1/1000s, nếu bấm q sẽ thoát
        break



cap.release() # Giải phóng camera sau khi dùng xong
cv2.destroyWindow() # Thoát tất cả các cửa sổ
