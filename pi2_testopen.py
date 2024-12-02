import cv2
import numpy as np
from picamera2 import Picamera2

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี RGB: {r}, {g}, {b}")  # แสดงค่าสี BGR ก่อนการแปลง
    if r > 80 and r < 145 and g < 84 and b < 100:  # สีแดง
        return "R"
    elif r < 100 and g > 45 and b < 100:  # สีเขียว
        return "G"
    elif r < 90 and g < 90 and b > 50:  # สีน้ำเงิน
        return "B"
    elif r > 150 and g > 30 and b < 100:  # สีส้ม
        return "O"
    elif r > 80 and g > 80 and b > 80:  # สีขาว
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

# กำหนดตำแหน่งจุด 8 จุดในรูปแบบวงกลม
circle_positions = [
    (440, 341), (579, 226), (774, 73),
    (412, 478),           (764, 236),
    (379, 675), (566, 569), (773, 437),
    (1000, 80), (1208, 188), (1357, 281),
    (1000, 233),           (1422, 433),
    (1030, 402), (1298, 533), (1468, 608),
    (504, 815), (674, 720), (915, 604),
    (707, 871),           (1223, 682),
    (891, 932), (1223, 842), (1389, 757)
]

# เปิดกล้องด้วย Picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1920, 1080)})
picam2.configure(config)
picam2.start()

current_color = "?"
current_position = (0, 0)

def mouse_callback(event, x, y, flags, param):
    global current_color, current_position
    if event == cv2.EVENT_MOUSEMOVE:  # เมื่อเมาส์เคลื่อนไหว
        current_position = (x, y)  # ตำแหน่งเมาส์ปัจจุบัน
        # อ่านค่าสีจากตำแหน่งเมาส์
        bgr = frame[y, x] if y < frame.shape[0] and x < frame.shape[1] else (0, 0, 0)
        current_color = convert_bgr_to_color(bgr)

cv2.namedWindow("Rubik Color Capture", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Rubik Color Capture", cv2.WND_PROP_FULLSCREEN, 1)  # เปิดเป็นเต็มจอ
cv2.setMouseCallback("Rubik Color Capture", mouse_callback)

try:
    while True:
        # อ่านภาพจาก Picamera2
        frame = picam2.capture_array()

        # ปรับขนาดภาพให้พอดีกับหน้าจอ
        frame_resized = cv2.resize(frame, (1920, 1080))

        # วาดวงกลมบนเฟรม
        draw_guidelines(frame_resized, circle_positions)

        # แสดงค่าสีและตำแหน่งปัจจุบัน
        cv2.putText(frame_resized, f"Position: {current_position}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_resized, f"Color: {current_color}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # แสดงผลเฟรม
        cv2.imshow("Rubik Color Capture", frame_resized)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):  # กด 'e' เพื่อบันทึกค่าสี
            captured_colors = get_colors(frame_resized, circle_positions)
            print("สีที่จับได้:", captured_colors)  # พิมพ์ตัวอักษรสีที่จับได้
        elif key == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
            break
finally:
    picam2.stop()
    cv2.destroyAllWindows()
