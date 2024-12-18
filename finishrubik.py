import cv2
import numpy as np
import time
from adafruit_pca9685 import PCA9685
import board
import busio
import threading
from picamera2 import Picamera2, Controls


data_front = []
data_right = []
data_back = []
data_left = []
data_up = []
data_down = []
datalist_RBL=[data_right,data_back,data_left]

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
    pca.channels[channel].duty_cycle = 4000 # ค่าเฉพาะสำหรับมุม 90° ตามเข็ม
    time.sleep(0.06)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

# ฟังก์ชันหมุนไปที่มุม 90° ทวนเข็ม
def rotate_to_90_ccw(channel):
    pca.channels[channel].duty_cycle = 8000 # ค่าเฉพาะสำหรับมุม 90° ทวนเข็ม
    time.sleep(0.06)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

def rotate_to_180_cw(channel):
    pca.channels[channel].duty_cycle = 4000  # ค่าเฉพาะสำหรับมุม 90° ตามเข็ม
    time.sleep(0.3)  # รอให้เซอร์โวหมุนเสร็จ
    stop_rotation(channel)

# ฟังก์ชันหมุนไปที่มุม 90° ทวนเข็ม
def rotate_to_180_ccw(channel):
    pca.channels[channel].duty_cycle = 8000  # ค่าเฉพาะสำหรับมุม 90° ทวนเข็ม
    time.sleep(0.3)  # รอให้เซอร์โวหมุนเสร็จ
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
    return captured_colors  # คืนค่าข้อมูลสีที่จับได้

def testt():
    rotate_to_90_ccw(3)
    time.sleep(3)
    rotate_to_90_ccw(3)
    time.sleep(3)
    rotate_to_90_ccw(3)
    time.sleep(3)
    rotate_to_90_ccw(3)
    time.sleep(3)
    rotate_to_90_ccw(6)
    time.sleep(3)
    rotate_to_90_ccw(6)
    time.sleep(3)
    rotate_to_90_ccw(6)
    time.sleep(3)
    rotate_to_90_ccw(6)
    time.sleep(3)


def rotate_RBL():
    for _ in range(5):
        if _ == 0:  # รอบแรกเก็บใน data_front
            frame = picam2.capture_array()
            colors = capture(frame, circle_positions)
            data_front.extend(colors)
            print(f"ข้อมูลในด้าน Front: {data_front}")
            time.sleep(2)
        elif _ < 4:  # รอบที่ 2-3 เก็บใน datalist
            rotate_to_90_ccw(3)
            time.sleep(3)
            rotate_to_90_cw(6)
            time.sleep(3)
            print('กำลังถ่ายรูป')
            time.sleep(3)
            frame = picam2.capture_array()
            colors = capture(frame, circle_positions_1)
            datalist_RBL[_ - 1].extend(colors)  
            print(f"ข้อมูลในด้านที่ {_}: {colors}")
            time.sleep(2)
        elif _ == 4:  # รอบที่ 4 หมุนแต่ไม่ถ่ายภาพ
            rotate_to_90_ccw(3)
            time.sleep(3)
            rotate_to_90_cw(6)
            time.sleep(3)
            print("หมุนรอบที่ 4 สำเร็จ (ไม่ถ่ายภาพ)")

def rotate_UD():
    rotate_to_90_ccw(3) #บน
    time.sleep(3)
    rotate_to_90_cw(2)
    time.sleep(3)
    rotate_to_90_ccw(5)
    print('กำลังถ่ายภาพ')
    time.sleep(3)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_2)
    data_up.extend(colors)
    print(f"ข้อมูลในด้าน Front: {data_up}")
    time.sleep(3)
    # ย้อนกับ
    rotate_to_90_ccw(2)
    time.sleep(3)
    rotate_to_90_cw(5)
    time.sleep(3)
    rotate_to_90_cw(3)
    time.sleep(3)

    #ล่าง
    rotate_to_90_ccw(6)
    time.sleep(3)
    rotate_to_90_ccw(2)
    time.sleep(3)
    rotate_to_90_cw(5)
    print('กำลังถ่ายภาพ')
    time.sleep(3)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_2)
    data_down.extend(colors)
    print(f"ข้อมูลในด้าน Front: {data_down}")
    time.sleep(3)

    # ย้อนกลับ
    rotate_to_90_cw(2)
    time.sleep(3)
    rotate_to_90_ccw(5)
    time.sleep(3)
    rotate_to_90_cw(6)
    
    print("ข้อมูลที่เก็บได้ทั้งหมด:")
    print("Front:", data_front)
    print("Right:", data_right)
    print("Back:", data_back)
    print("Left:", data_left)
    print("up:", data_up)
    print("down:", data_down)

def rotate_ffiRBL():
    rotate_to_90_cw(2)
    time.sleep(3)
    rotate_to_90_ccw(5)
    time.sleep(3)
    rotate_to_90_cw(3)
#     thread_left = threading.Thread(target=rotate_to_90_ccw, args=(4,))
#     thread_right = threading.Thread(target=rotate_to_90_cw, args=(7,))
#     thread_left.start()
#     thread_right.start()
#     thread_left.join()
#     thread_right.join()
#     time.sleep(5)
#     frame = picam2.capture_array()
#     colors = capture(frame, circle_positions_2)
# # คำนวณตำแหน่งที่จะแทรกข้อมูล (กลางของ data_left)
#     middle = len(data_right) // 2
# # แทรกข้อมูลใหม่ในตำแหน่งกลาง
#     data_right = data_right[:middle] + colors + data_right[middle:]
#     print(f"ข้อมูลใน data_right หลังแทรก: {data_right}")
#     thread_left_return = threading.Thread(target=rotate_to_90_cw, args=(4,))
#     thread_right_return = threading.Thread(target=rotate_to_90_ccw, args=(7,))
#     thread_left_return.start()
#     thread_right_return.start()
#     thread_left_return.join()
#     thread_right_return.join()
#     rotate_to_90_ccw(3)
    
#     # เสจด้านขวา

#     thread_left1 = threading.Thread(target=rotate_to_180_ccw, args=(4,))
#     thread_right1 = threading.Thread(target=rotate_to_180_cw, args=(7,))
#     thread_left1.start()
#     thread_right1.start()
#     thread_left1.join()
#     thread_right1.join()
#     time.sleep(3)
#     frame = picam2.capture_array()
#     colors = capture(frame, circle_positions_2)
#     middle = len(data_back) // 2
#     data_back = data_back[:middle] + colors + data_back[middle:]
#     print(f"ข้อมูลใน data_back หลังแทรก: {data_back}")
#     time.sleep(3)
#     thread_left_return1 = threading.Thread(target=rotate_to_180_cw, args=(4,))
#     thread_right_return1 = threading.Thread(target=rotate_to_180_ccw, args=(7,))
#     thread_left_return1.start()
#     thread_right_return1.start()
#     thread_left_return1.join()
#     thread_right_return1.join()
#     time.sleep(3)

#     # เสจหลัง

#     thread_fontb= threading.Thread(target=rotate_to_90_ccw, args=(2,))
#     thread_blackb = threading.Thread(target=rotate_to_90_cw, args=(5,))
#     thread_fontb.start()
#     thread_blackb.start()
#     thread_fontb.join()
#     thread_blackb.join()
#     time.sleep(3)
#     rotate_to_90_cw(3)
#     thread_leftb = threading.Thread(target=rotate_to_90_ccw, args=(4,))
#     thread_rightb = threading.Thread(target=rotate_to_90_cw, args=(7,))
#     thread_leftb.start()
#     thread_rightb.start()
#     thread_leftb.join()
#     thread_rightb.join()
#     time.sleep(5)
#     frame = picam2.capture_array()
#     colors = capture(frame, circle_positions_2)
# # คำนวณตำแหน่งที่จะแทรกข้อมูล (กลางของ data_left)
#     middle = len(data_right) // 2
# # แทรกข้อมูลใหม่ในตำแหน่งกลาง
#     data_right = data_right[:middle] + colors + data_right[middle:]
#     print(f"ข้อมูลใน data_right หลังแทรก: {data_right}")
#     thread_left_returnb = threading.Thread(target=rotate_to_90_cw, args=(4,))
#     thread_right_returnb = threading.Thread(target=rotate_to_90_ccw, args=(7,))
#     thread_left_returnb.start()
#     thread_right_returnb.start()
#     thread_left_returnb.join()
#     thread_right_returnb.join()
#     time.sleep(3)
#     rotate_to_90_ccw(3)
#     time.sleep(3)
#     thread_font_returnb= threading.Thread(target=rotate_to_90_ccw, args=(2,))
#     thread_black_returnb = threading.Thread(target=rotate_to_90_cw, args=(5,))
#     thread_font_returnb.start()
#     thread_black_returnb.start()
#     thread_font_returnb.join()
#     thread_black_returnb.join()
#     time.sleep(3)


def all():
    # rotate_RBL()
    # print("go solution")
    # time.sleep(5)
    # rotate_UD()
    rotate_ffiRBL

 
# หน้านึง
circle_positions = [ 
    (588, 77), (772, 74), (940,102),
    (578, 317),           (968, 377),
    (598, 572), (779, 556), (950, 533)  
]
#แถวบนและล่างแนวนอน
circle_positions_1 = [
   (588, 77), (772, 74), (940,102),
    (598, 572), (779, 556), (950, 533)  
]
#แถวซ้ายขวาเรียงลงมา
circle_positions_2 = [
      (588, 77), (940,102),
    (578, 317), (968, 377),
    (598, 572),  (950, 533) 
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
            rotation_thread = threading.Thread(target=all)
            rotation_thread.start()  # ทำงานการหมุนใน Background
            
            

finally:
    picam2.stop()
    cv2.destroyAllWindows()
