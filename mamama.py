import cv2
import numpy as np
import time

def angle_to_duty_cycle(angle):
    min_duty = 1500 
    max_duty = 6000  
    return int(min_duty + (angle / 180) * (max_duty - min_duty))

def rotate_to_angle(channel, angle):
    duty_cycle = angle_to_duty_cycle(angle)
    print(f'servo ตัวที่ {channel} หมุนไปที่มุม {angle} โดย Duty Cycle = {duty_cycle}')
    time.sleep(0.5)

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
    print(f"ค่าสี BGR: {b}, {g}, {r}")  # แสดงค่าสี BGR ก่อนการแปลง

    if r > 200 and g < 100 and b < 100:  # สีแดง
        return "R"
    elif r < 100 and g > 200 and b < 100:  # สีเขียว
        return "G"
    elif r < 100 and g < 100 and b > 200:  # สีน้ำเงิน
        return "B"
    elif r > 200 and g > 150 and b < 100:  # สีส้ม
        return "O"
    elif r > 200 and g > 200 and b > 200:  # สีขาว
        return "W"
    elif r > 200 and g > 200 and b < 100:  # สีเหลือง
        return "Y"
    else:
        return "?"

# ฟังก์ชันวาดวงกลมสำหรับจุด
def draw_guidelines(frame, points):
    for (x, y) in points:
        cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)  # วาดวงกลมขนาด 20 px

# ฟังก์ชันอ่านค่าสีจากตำแหน่งที่กำหนด
def get_colors(frame, points):
    colors = []
    for (x, y) in points:
        roi = frame[y-5:y+5, x-5:x+5]  # เลือกบริเวณเล็ก ๆ รอบจุด
        avg_color = cv2.mean(roi)[:3]  # ค่าเฉลี่ยสี (BGR)
        color_letter = convert_bgr_to_color(avg_color)  # แปลงเป็นตัวอักษร
        colors.append(color_letter)
    return colors

# ฟังก์ชันจับภาพและเก็บค่าสี
def capture(frame, circle_positions):
    captured_colors = get_colors(frame, circle_positions)
    print("สีที่จับได้:", captured_colors)

def capture_RBL(frame, circle_positions):
    capture(frame, circle_positions)
    rotate_to_angle(1,90) 
    rotate_to_angle(1,90)
    time.sleep(5)
    capture(frame, circle_positions_1)
    rotate_to_angle(1,180) 
    rotate_to_angle(1,180)
    capture(frame, circle_positions_1)



circle_positions = [
    (200, 150), (300, 150), (400, 150), 
    (200, 250),           (400, 250), 
    (200, 350), (300, 350), (400, 350)   
]
circle_positions_1 = [
    (200, 150), (300, 150), (400, 150),  
    (200, 350), (300, 350), (400, 350)   
]

# เปิดกล้อง
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถเปิดกล้องได้")
        break


    draw_guidelines(frame, circle_positions)


    capture(frame, circle_positions)


    cv2.imshow("Rubik Color Capture", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
