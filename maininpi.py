import cv2
import numpy as np
import time
from adafruit_pca9685 import PCA9685
import board
import busio
import threading
from picamera2 import Picamera2, Controls


data_font = []
data_right = []
data_back = []
data_left = []
data_up = []
data_down = []

# สร้าง I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# สร้าง PCA9685 object
pca = PCA9685(i2c)
pca.frequency = 60  # ตั้งความถี่ที่ 60Hz (ค่ามาตรฐานสำหรับ servo)

# ฟังก์ชันหยุดการหมุน
def stop_rotation(channel):
    pca.channels[channel].duty_cycle = 0  # หยุดการหมุน

# ฟังก์ชันหมุนไปที่มุม 90° ตามเข็ม
def rotate_to_90_cw(channel):
    pca.channels[channel].duty_cycle = 10200  # ค่าเฉพาะสำหรับมุม 90° ตามเข็ม
    time.sleep(0.1)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

# ฟังก์ชันหมุนไปที่มุม 90° ทวนเข็ม
def rotate_to_90_ccw(channel):
    pca.channels[channel].duty_cycle = 1250  # ค่าเฉพาะสำหรับมุม 90° ทวนเข็ม
    time.sleep(0.1)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

def rotate_to_180_cw(channel):
    pca.channels[channel].duty_cycle = 10200  # ค่าเฉพาะสำหรับมุม 90° ตามเข็ม
    time.sleep(0.4)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

# ฟังก์ชันหมุนไปที่มุม 90° ทวนเข็ม
def rotate_to_180_ccw(channel):
    pca.channels[channel].duty_cycle = 1300  # ค่าเฉพาะสำหรับมุม 90° ทวนเข็ม
    time.sleep(0.4)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี RGB: {r}, {g}, {b}")  # แสดงค่าสี BGR ก่อนการแปลง
    if r > 180 and g < 50 and b < 50:  # สีแดง
        return "R"
    elif r < 100 and g > 45 and b < 100:  # สีเขียว
        return "G"
    elif r < 60 and g < 100 and b > 100:  # สีน้ำเงิน
        return "B"
    elif r > 200 and g < 120 and b < 100:  # สีส้ม
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

# ฟังก์ชันวางค่าสี
def capture(frame, circle_positions):
    captured_colors = get_colors(frame, circle_positions)
    print("สีที่จับได้:", captured_colors)


# ฟังก์ชันที่เรียก rotate_RBL แบบ Background Thread
def run_rotate_rbl_in_thread():
    thread = threading.Thread(target=rotate_RBL)
    thread.start()

def run_rotate_UD_in_thread():
    thread = threading.Thread(target=rotate_UD)
    thread.start()


def rotate_RBL():
    for _ in range(4):
        thread_up = threading.Thread(target=rotate_to_90_cw, args=(4,))
        thread_down = threading.Thread(target=rotate_to_90_ccw, args=(1,))
        thread_up.start()
        thread_down.start()
        thread_up.join()
        thread_down.join()

        if _ < 3:  # ตรวจสอบว่ารอบปัจจุบันไม่ใช่รอบที่ 4
            frame = picam2.capture_array()
            capture(frame, circle_positions_1)
            print("จับภาพเสร็จแล้วในรอบที่:", _ + 1)

        # พักระหว่างการหมุนแต่ละรอบ (ปรับเวลาได้ตามต้องการ)
        time.sleep(2)

def rotate_UD():
    #บน
    rotate_to_90_cw(4)
    time.sleep(1)
    thread_left = threading.Thread(target=rotate_to_90_cw, args=(6,))
    thread_right = threading.Thread(target=rotate_to_90_ccw, args=(2,))
    thread_left.start()
    thread_right.start()
    thread_left.join()
    thread_right.join()
    frame = picam2.capture_array()
    capture(frame, circle_positions_2)
    time.sleep(2)
    thread_left_return = threading.Thread(target=rotate_to_90_ccw, args=(6,))
    thread_right_return = threading.Thread(target=rotate_to_90_cw, args=(2,))
    thread_left_return.start()
    thread_right_return.start()
    thread_left_return.join()
    thread_right_return.join()
    time.sleep(1)
    rotate_to_90_ccw(4)

    print('เสจข้างบนแล้วว')
    time.sleep(2)
    #ล่าง
    rotate_to_90_cw(1)
    time.sleep(1)
    thread_left = threading.Thread(target=rotate_to_90_ccw, args=(6,))
    thread_right = threading.Thread(target=rotate_to_90_cw, args=(2,))
    thread_left.start()
    thread_right.start()
    thread_left.join()
    thread_right.join()
    frame = picam2.capture_array()
    capture(frame, circle_positions_2)
    time.sleep(2)
    thread_left_return = threading.Thread(target=rotate_to_90_cw, args=(6,))
    thread_right_return = threading.Thread(target=rotate_to_90_ccw, args=(2,))
    thread_left_return.start()
    thread_right_return.start()
    thread_left_return.join()
    thread_right_return.join()
    time.sleep(1)
    rotate_to_90_ccw(1)


    # time.sleep(2)
    # rotate_to_90_ccw(6)
    # time.sleep(1)
    # rotate_to_90_ccw(4)

    # rotate_to_90_cw(1)
    # time.sleep(1)
    # rotate_to_90_cw(6)


    
# หน้านึง
circle_positions = [ 
    (440, 220), (640, 220), (840,220 ),
    (440, 320),           (840, 320),
    (440, 420), (640, 420), (840, 420)  
]
#แถวบนและล่างแนวนอน
circle_positions_1 = [
    (440, 220), (640, 220), (840,220),  
    (440, 420), (640, 420), (840, 420)
]
#แถวซ้ายขวาเรียงลงมา
circle_positions_2 = [
       (440, 220), (840,220 ),
    (440, 320), (840, 320),
    (440, 420), (840, 420) 
]

# เปิดกล้องด้วย PiCamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)})
picam2.configure(config)
picam2.start()

focus_position = 10

def set_focus(position):
    picam2.set_controls({"LensPosition": position})
    print(f"Focus set to: {position}")
    set_focus(focus_position)

cv2.namedWindow("Rubik Color Capture", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Rubik Color Capture", 1280, 720)  # กำหนดขนาดหน้าต่างให้ตรงกับขนาดภาพที่แสดง

try:
    while True:
        # รับภาพจาก PiCamera2
        frame = picam2.capture_array()
        
        frame_resized = cv2.resize(frame, (1280, 720))

        draw_guidelines(frame_resized, circle_positions)
        
        # แสดงภาพ
        cv2.imshow("Rubik Color Capture", frame_resized)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  
            break
        elif key == ord('e'):  # กด 'e' เพื่อบันทึกค่าสี
            # run_rotate_rbl_in_thread()
            run_rotate_UD_in_thread()

finally:
    picam2.stop()
    cv2.destroyAllWindows()
