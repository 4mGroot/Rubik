import cv2
import numpy as np
import time
from adafruit_pca9685 import PCA9685
import board
import busio
import threading
from picamera2 import Picamera2, Controls
import kociemba


data_front = []
data_right = []
data_back = []
data_left = []
data_up = []
data_bottom = []
datalist_RBL=[data_right,data_back,data_left]

# สร้าง I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# สร้าง PCA9685 object
pca = PCA9685(i2c)
pca.frequency = 60  # ตั้งความถี่ที่ 60Hz (ค่ามาตรฐานสำหรับ servo)


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
    time.sleep(0.06)
    stop_rotation(channel)

def rotate_to_180_cw(channel):
    pca.channels[channel].duty_cycle = 4000  # ค่าเฉพาะสำหรับมุม 90° ตามเข็ม
    time.sleep(0.3)  
    stop_rotation(channel)

# ฟังก์ชันหมุนไปที่มุม 90° ทวนเข็ม
def rotate_to_180_ccw(channel):
    pca.channels[channel].duty_cycle = 8000  # ค่าเฉพาะสำหรับมุม 90° ทวนเข็ม
    time.sleep(0.3)
    stop_rotation(channel)


# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี RGB: {r}, {g}, {b}")  # แสดงค่าสี BGR ก่อนการแปลง
    if r > 120 and r <175 and g < 80 and b < 80:  # สีแดง
        return "R"
    elif r < 100 and g > 45 and b < 100:  # สีเขียว
        return "G"
    elif r < 60 and g < 100 and b > 70:  # สีน้ำเงิน
        return "B"
    elif r > 175 and g < 120 and b < 20:  # สีส้ม
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

def rotate_RBL():
    for _ in range(5):
        if _ == 0: 
            frame = picam2.capture_array()
            colors = capture(frame, circle_positions)
            data_front.extend(colors)
            print(f"Colors front face: {data_front}")
            time.sleep(2)
        elif _ < 4:  # รอบที่ 2-3 เก็บใน datalist
            rotate_to_90_ccw(3)
            time.sleep(3)
            rotate_to_90_cw(6)
            time.sleep(3)
            print('Detecting colors . . .')
            time.sleep(3)
            frame = picam2.capture_array()
            colors = capture(frame, circle_positions_1)
            datalist_RBL[_ - 1].extend(colors)  
            print(f"The colors on the side{_}: {colors}")
            time.sleep(2)
        elif _ == 4:
            rotate_to_90_ccw(3)
            time.sleep(3)
            rotate_to_90_cw(6)
            time.sleep(3)

def rotate_UD():
     #บน
    rotate_to_90_ccw(3)
    time.sleep(3)
    rotate_to_90_cw(2)
    time.sleep(3)
    rotate_to_90_ccw(5)
    print('Detecting colors . . .')
    time.sleep(5)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_2)
    data_up.extend(colors)
    print(f"Colors Up face: {data_up}")
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
    print('Detecting colors . . .')
    time.sleep(5)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_2)
    data_bottom.extend(colors)
    print(f"Colors Bottom face: {data_bottom}")
    time.sleep(3)

    # ย้อนกลับ
    rotate_to_90_cw(2)
    time.sleep(3)
    rotate_to_90_ccw(5)
    time.sleep(3)
    rotate_to_90_cw(6)
    
    print("All Colors:")
    print("Front:", data_front)
    print("Right:", data_right)
    print("Back:", data_back)
    print("Left:", data_left)
    print("up:", data_up)
    print("bottom:", data_bottom)

def rotate_fourfive_RBLUD():
    global data_right
    global data_back
    global data_left
    global data_up
    global data_bottom

    # right
    rotate_to_90_cw(4)
    time.sleep(4)
    rotate_to_90_ccw(7)
    time.sleep(4)
    rotate_to_90_ccw(3)
    time.sleep(4)
    rotate_to_90_cw(2)
    time.sleep(4)
    rotate_to_90_ccw(5)
    print('Detecting colors . . .')
    time.sleep(3)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_3)
    middle = len(data_right) // 2
    data_right = data_right[:middle] + colors + data_right[middle:]
    print(f"colors data_right after insert: {data_right}")
    time.sleep(4)
    
    # reverse
    rotate_to_90_ccw(2)
    time.sleep(4)
    rotate_to_90_cw(5)
    time.sleep(4)
    rotate_to_90_cw(3)
    time.sleep(4)
    rotate_to_90_cw(7)
    time.sleep(4)
    rotate_to_90_ccw(4)
    time.sleep(4)

    # back
    rotate_to_180_cw(2)
    time.sleep(4)
    rotate_to_180_ccw(5)
    time.sleep(4)
    rotate_to_180_cw(4)
    print('Detecting colors . . .')
    time.sleep(4)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_3)
    middle = len(data_back) // 2
    data_back = data_back[:middle] + colors + data_back[middle:]
    print(f"colors data_back after insert: {data_back}")
    time.sleep(4)

    # reverse
    rotate_to_180_ccw(4)
    time.sleep(4)
    rotate_to_180_cw(5)
    time.sleep(4)
    rotate_to_180_ccw(2)
    time.sleep(4)

    # left
    rotate_to_90_ccw(4)
    time.sleep(4)
    rotate_to_90_cw(7)
    time.sleep(4)
    rotate_to_90_cw(3)
    time.sleep(4)
    rotate_to_90_cw(2)
    time.sleep(4)
    rotate_to_90_ccw(5)
    time.sleep(4)
    print('Detecting colors . . .')
    time.sleep(4)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_3)
    middle = len(data_left) // 2
    data_left = data_left[:middle] + colors + data_left[middle:]
    print(f"colors data_left after insert: {data_left}")

    # reverse
    time.sleep(4)
    rotate_to_90_cw(5)
    time.sleep(4)
    rotate_to_90_ccw(2)
    time.sleep(4)
    rotate_to_90_ccw(3)
    time.sleep(4)
    rotate_to_90_ccw(7)
    time.sleep(4)
    rotate_to_90_cw(4)
    time.sleep(4)

    # Up
    rotate_to_90_cw(2)
    time.sleep(4)
    rotate_to_90_ccw(5)
    time.sleep(4)
    print('Detecting colors . . .')
    time.sleep(4)
    frame = picam2.capture_array()
    colors = capture(frame, circle_positions_3)
    middle = len(data_up) // 2
    data_up = data_up[:middle] + colors + data_up[middle:]
    print(f"colors in data_up after insert: {data_up}")
    time.sleep(4)
    rotate_to_180_cw(2)
    time.sleep(4)
    rotate_to_180_ccw(5)
    print('Detecting colors . . .')
    time.sleep(4)
    frame = picam2.capture_array()
    colors = capture(frame,circle_positions_3)
    middle =len(data_bottom) //2
    data_bottom = data_bottom[:middle] + colors + data_bottom[middle:]
    print(f"colors data_bottom after insert: {data_bottom}")
    time.sleep(4)
    rotate_to_90_cw(2)
    time.sleep(4)
    rotate_to_90_ccw(5)

def U():  
    print("rotate U ccw")
    rotate_to_90_ccw(3)
    time.sleep(3)

def U_prime():
    print("rotate U cw")
    rotate_to_90_cw(3)
    time.sleep(3)

def U2():
    print("rotate U 180 ")
    rotate_to_180_ccw(3)
    time.sleep(3)

def R():  
    print("rotate R ccw")
    rotate_to_90_ccw(2)
    time.sleep(3)

def R_prime():  
    print("rotate R cw")
    rotate_to_90_cw(2)
    time.sleep(3)

def R2():  
    print("rotate R 180 ccw")
    rotate_to_180_ccw(2)
    time.sleep(3)

def F():  
    print("rotate F ccw")
    rotate_to_90_ccw(4)
    time.sleep(3)

def F_prime():  
    print("rotate F cw")
    rotate_to_90_cw(4)
    time.sleep(3)

def F2():  
    print("rotate F 180")
    rotate_to_180_ccw(4)
    time.sleep(3)

def L():  
    print("rotate L ccw")
    rotate_to_90_ccw(5)
    time.sleep(3)

def L_prime():  
    print("rotate L cw")
    rotate_to_90_cw(5)
    time.sleep(3)

def L2():  
    print("rotate L 180")
    rotate_to_180_ccw(5)
    time.sleep(3)

def D():  
    print("rotate R ccw")
    rotate_to_90_ccw(6)
    time.sleep(3)

def D_prime():  
    print("rotate R cw")
    rotate_to_90_cw(6)
    time.sleep(3)

def D2():  
    print("rotate R 180 ")
    rotate_to_180_ccw(6)
    time.sleep(3)

def B():  
    print("rotate F ccw")
    rotate_to_90_ccw(7)
    time.sleep(3)

def B_prime():  
    print("rotate F cw")
    rotate_to_90_cw(7)
    time.sleep(3)

def B2():  
    print("rotate F 180")
    rotate_to_180_ccw(7)
    time.sleep(3)


# ฟังก์ชันหลักที่อ่านคำแนะนำในการหมุนจาก kociemba
def execute_solution(solution):
    moves = solution.split()  # แยกคำสั่งหมุนโดยช่องว่าง
    for move in moves:
        if move == "U":
            U()
        elif move == "U'":
            U_prime()
        elif move == "U2":
            U2()
        elif move == "R":
            R()
        elif move == "R'":
            R_prime()
        elif move == "R2":
            R2()
        elif move == "F":
            F()
        elif move == "F'":
            F_prime()
        elif move == "F2":
            F2()
        elif move == "L":
            L()
        elif move == "L'":
            L_prime()
        elif move == "L2":
            L2()
        elif move == "D":
            D()
        elif move == "D'":
            D_prime()
        elif move == "D2":
            D2()
        elif move == "B":
            B()
        elif move == "B'":
            B_prime()
        elif move == "B2":
            B2()
        else:
            print(f"ไม่รู้จักคำสั่ง: {move}")


def insert_center():
    global data_front
    global data_left
    global data_back
    global data_bottom
    global data_right
    global data_up
    data_front.insert(len(data_front) // 2, "B")
    data_right.insert(len(data_right) // 2, "O")
    data_back.insert(len(data_back) // 2, "G")
    data_left.insert(len(data_left) // 2, "R")
    data_up.insert(len(data_up) // 2, "W")
    data_bottom.insert(len(data_bottom) // 2, "Y")
    
    print(f"The front color : {data_front}")
    print(f"The right color : {data_right}")
    print(f"The back color  : {data_back}")
    print(f"The left color  : {data_left}")
    print(f"The up color    : {data_up}")
    print(f"The bottom color  : {data_bottom}")

def Solve_Rubik():
    global data_front
    global data_left
    global data_back
    global data_bottom
    global data_right
    global data_up

    cube_array = data_up + data_right + data_front + data_bottom + data_left + data_back
    cube = "".join(cube_array)
    print("ข้อมูลสีในต้นฉบับ:", cube)
    cube = cube.replace('R', 'L')  # สีแดง -> R
    cube = cube.replace('Y', 'D')  # สีเหลือง -> U
    cube = cube.replace('B', 'F')  # สีน้ำเงิน -> F
    cube = cube.replace('O', 'R')  # สีส้ม -> L
    cube = cube.replace('W', 'U')  # สีขาว -> D
    cube = cube.replace('G', 'B')  # สีเขียว -> B
    print("Converted color data: ", cube)
    solution = kociemba.solve(str(cube))
    print("Rotation instructions: ", solution)
    execute_solution(solution)


def all():
    rotate_RBL()
    print("go next solution . . .")
    time.sleep(5)
    rotate_UD()
    print("go next solution  . . .")
    time.sleep(5)
    rotate_fourfive_RBLUD()
    time.sleep(5)
    insert_center()
    print("go solution solve Rubik ")
    time.sleep(5)
    Solve_Rubik()
    print('finish ')
    
# หน้านึง
circle_positions = [ 
    (588, 64), (772, 74), (940,102),
    (578, 317),           (968, 377),
    (598, 572), (779, 556), (950, 533)  
]
#แถวบนและล่างแนวนอน
circle_positions_1 = [
   (588, 64), (772, 74), (940,102),
    (598, 572), (779, 556), (950, 533)  
]
#แถวซ้ายขวาเรียงลงมา
circle_positions_2 = [
      (940,102),(968, 377),(950, 533),(588, 64),(578, 317),(598, 572)
]
circle_positions_3 =[
    (578, 317),(968, 377)
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
