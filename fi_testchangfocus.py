from picamera2 import Picamera2, Controls
import cv2
import numpy as np

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี RGB: {r}, {g}, {b}")  # แสดงค่าสี BGR ก่อนการแปลง
    if r > 130 and r <190 and g < 80 and b < 80:  # สีแดง
        return "R"
    elif r < 100 and g > 45 and b < 100:  # สีเขียว
        return "G"
    elif r < 60 and g < 100 and b > 70:  # สีน้ำเงิน
        return "B"
    elif r > 190 and g < 120 and b < 20:  # สีส้ม
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
        cv2.circle(frame, (x, y), 10, (0, 255, 0), 2)  # วาดวงกลมขนาด 10 px

# ฟังก์ชันอ่านค่าสีจากตำแหน่งที่กำหนด
def get_colors(frame, points):
    colors = []
    for (x, y) in points:
        roi = frame[y-5:y+5, x-5:x+5]  # เลือกบริเวณเล็ก ๆ รอบจุด
        avg_color = cv2.mean(roi)[:3]  # ค่าเฉลี่ยสี (BGR)
        color_letter = convert_bgr_to_color(avg_color)  # แปลงเป็นตัวอักษร
        colors.append(color_letter)
    return colors

# กำหนดตำแหน่งจุด
circle_positions = [
    (588, 77), (772, 74), (940,102),
    (578, 317),           (968, 377),
    (598, 572), (779, 556), (950, 533)
]

# เปิดกล้องด้วย Picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)})
picam2.configure(config)
picam2.start()

# ปรับระยะโฟกัสเริ่มต้น
focus_position = 10  # ค่าเริ่มต้นสำหรับโฟกัส (0-1000)

# ฟังก์ชันปรับโฟกัส
def set_focus(position):
    picam2.set_controls({"LensPosition": position})
    print(f"Focus set to: {position}")

# ตั้งโฟกัสเริ่มต้น
set_focus(focus_position)

current_color = "?"
current_position = (0, 0)


# ฟังก์ชันจับตำแหน่งเมาส์
def mouse_callback(event, x, y, flags, param):
    global current_color, current_position
    if event == cv2.EVENT_MOUSEMOVE:  # เมื่อเมาส์เคลื่อนไหว
        current_position = (x, y)  # ตำแหน่งเมาส์ปัจจุบัน
        # อ่านค่าสีจากตำแหน่งเมาส์
        bgr = frame[y, x] if y < frame.shape[0] and x < frame.shape[1] else (0, 0, 0)
        current_color = convert_bgr_to_color(bgr)

cv2.namedWindow("Rubik Color Capture", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Rubik Color Capture", 1280, 720)
cv2.setMouseCallback("Rubik Color Capture", mouse_callback)

try:
    while True:
        # อ่านภาพจาก Picamera2
        frame = picam2.capture_array()

        # ปรับขนาดภาพให้พอดีกับหน้าจอ
        frame_resized = cv2.resize(frame, (1280, 720))

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
        elif key == ord('f'):  # กด 'f' เพื่อเพิ่มโฟกัส
            focus_position = min(1000, focus_position + 10)
            set_focus(focus_position)
        elif key == ord('d'):  # กด 'd' เพื่อลดโฟกัส
            focus_position = max(0, focus_position - 10)
            set_focus(focus_position)

finally:
    picam2.stop()
    cv2.destroyAllWindows()
