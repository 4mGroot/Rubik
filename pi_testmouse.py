import cv2
import numpy as np

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี BGR: {b:.2f}, {g:.2f}, {r:.2f}")  # แสดงค่าสี BGR ก่อนการแปลง
    if r > 120 and g < 100 and b < 100:  # สีแดง
        return "R"
    elif r < 100 and g > 120 and b < 100:  # สีเขียว
        return "G"
    elif r < 100 and g < 100 and b > 120:  # สีน้ำเงิน
        return "B"
    elif r > 200 and g > 150 and b < 100:  # สีส้ม
        return "O"
    elif r > 200 and g > 200 and b > 200:  # สีขาว
        return "W"
    elif r > 160 and g > 160 and b < 100:  # สีเหลือง
        return "Y"
    else:
        return "?"

# ฟังก์ชันเมื่อเมาส์เคลื่อนไหวหรือคลิก
def mouse_callback(event, x, y, flags, param):
    global current_color, current_position
    if event == cv2.EVENT_MOUSEMOVE:  # เมื่อเมาส์เคลื่อนไหว
        current_position = (x, y)  # ตำแหน่งเมาส์ปัจจุบัน
        # อ่านค่าสีจากตำแหน่งเมาส์
        bgr = frame[y, x] if y < frame.shape[0] and x < frame.shape[1] else (0, 0, 0)
        current_color = convert_bgr_to_color(bgr)

# เปิดกล้อง
cap = cv2.VideoCapture(1)
cv2.namedWindow("Rubik Color Capture", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Rubik Color Capture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# กำหนดตัวแปรสำหรับการแสดงตำแหน่งเมาส์และสี
current_color = "?"
current_position = (0, 0)

# กำหนด Callback
cv2.setMouseCallback("Rubik Color Capture", mouse_callback)

# กำหนดความละเอียดของหน้าจอ
screen_width, screen_height = 1920, 1080

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถเปิดกล้องได้")
        break

    # ปรับขนาดภาพให้เป็น 1920x1080
    frame = cv2.resize(frame, (screen_width, screen_height))

    # วาดข้อมูลสีและตำแหน่งบนเฟรม
    cv2.putText(frame, f"Position: {current_position}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Color: {current_color}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # แสดงผลเฟรม
    cv2.imshow("Rubik Color Capture", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
        break

# ปิดกล้องและหน้าต่าง
cap.release()
cv2.destroyAllWindows() 
