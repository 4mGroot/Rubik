import cv2
import numpy as np

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี BGR: {b}, {g}, {r}")  # แสดงค่าสี BGR ก่อนการแปลง
    if 110 < r < 145 and g < 84 and b < 100:  # สีแดง
        return "R"
    elif r < 100 and g > 70 and b < 100:  # สีเขียว
        return "G"
    elif r < 90 and g < 90 and b > 50:  # สีน้ำเงิน
        return "B"
    elif r > 150 and g > 50 and b < 70:  # สีส้ม
        return "O"
    elif r > 90 and g > 90 and b > 90:  # สีขาว 
        return "W"
    elif r > 120 and g > 120 and b < 100:  # สีเหลือง
        return "Y"
    else:
        return "?"

# ฟังก์ชันวาดวงกลมสำหรับจุด
def draw_guidelines(frame, points):
    for (x, y) in points:
        cv2.circle(frame, (x, y), 10, (0, 255, 0), 2)  # วาดวงกลมขนาด 20 px

# ฟังก์ชันอ่านค่าสีจากตำแหน่งที่กำหนด
def get_colors(frame, points):
    colors = []
    for (x, y) in points:
        roi = frame[y-5:y+5, x-5:x+5]  # เลือกบริเวณเล็ก ๆ รอบจุด
        avg_color = cv2.mean(roi)[:3]  # ค่าเฉลี่ยสี (BGR)
        color_letter = convert_bgr_to_color(avg_color)  # แปลงเป็นตัวอักษร
        colors.append(color_letter)
    return colors

# ฟังก์ชันปรับแสงสะท้อนโดยการใช้ Histogram Equalization
def preprocess_frame(frame):
    # แปลงภาพจาก BGR เป็น HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ทำ Histogram Equalization ที่ช่อง V (Value) เพื่อปรับแสงสะท้อน
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])

    # แปลงกลับเป็น BGR
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return frame

# กำหนดตำแหน่งจุดในรูปแบบวงกลม
circle_positions = [
   (440, 341), (579, 226), (774, 73), (1000, 80), (1208, 188), (1357, 281),  # แถวบน
    (412, 478),           (764, 236), (1000, 233),           (1422, 433),  # แถวกลาง
    (379, 675), (566, 569), (773, 437), (1030, 402), (1298, 533), (1468, 608),   # แถวล่าง
                        (504, 815), (674, 720), (915, 604),
                        (707, 871),           (1223, 682),
                        (891, 932), (1223, 842), (1389, 757)
]

# เปิดกล้อง
cap = cv2.VideoCapture(1)
cv2.namedWindow("Rubik Color Capture", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Rubik Color Capture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ดึงขนาดหน้าจอเพื่อปรับภาพ
screen_width = 1920  # ปรับตามขนาดหน้าจอของคุณ
screen_height = 1080

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถเปิดกล้องได้")
        break

    # ปรับขนาดภาพให้พอดีกับหน้าจอ
    resized_frame = cv2.resize(frame, (screen_width, screen_height))

    # ใช้การปรับแสงสะท้อนด้วย Histogram Equalization
    processed_frame = preprocess_frame(resized_frame)

    # วาดวงกลมบนเฟรม
    draw_guidelines(processed_frame, circle_positions)

    # แสดงผลเฟรม
    cv2.imshow("Rubik Color Capture", processed_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('e'):  # กด 'e' เพื่อบันทึกค่าสี
        captured_colors = get_colors(processed_frame, circle_positions)
        print("สีที่จับได้:", captured_colors)  # พิมพ์ตัวอักษรสีที่จับได้
    elif key == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
        break

# ปิดกล้องและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
