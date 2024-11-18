import cv2
import numpy as np
import kociemba  # ไลบรารีแก้ปัญหารูบิค

# ฟังก์ชันแปลงค่าเฉลี่ยสี (BGR) เป็นตัวอักษรสี
def convert_bgr_to_color(bgr):
    b, g, r = bgr
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

# ฟังก์ชันควบคุมเซอร์โวให้หมุนตามทิศทาง (ตัวอย่าง)
def rotate_servo(position):
    # โค้ดการหมุนเซอร์โวจะถูกใส่ที่นี่
    print(f"หมุนเซอร์โวไปที่ตำแหน่ง {position}")

# ฟังก์ชันแก้ปัญหารูบิค
def solve_rubik(cube_string):
    solution = kociemba.solve(cube_string)  # ใช้ไลบรารี Kociemba เพื่อหาคำแนะนำในการหมุน
    return solution

# ฟังก์ชันแปลงข้อมูลสีจากแต่ละด้านของรูบิคให้เป็นสตริงที่ Kociemba สามารถใช้ได้
def create_cube_string(rubik_colors):
    # แปลงข้อมูลสีที่เก็บไว้ใน rubik_colors ให้เป็นสตริง
    cube_string = "".join(rubik_colors['top']) + \
                  "".join(rubik_colors['front']) + \
                  "".join(rubik_colors['bottom']) + \
                  "".join(rubik_colors['back']) + \
                  "".join(rubik_colors['left']) + \
                  "".join(rubik_colors['right'])
    return cube_string

# กำหนดตำแหน่งจุด 8 จุดในรูปแบบวงกลม
circle_positions = [
    (200, 150), (300, 150), (400, 150),  # แถวบน
    (200, 250),           (400, 250),  # แถวกลาง
    (200, 350), (300, 350), (400, 350)   # แถวล่าง
]

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# เก็บข้อมูลสีจากแต่ละด้านของรูบิค
rubik_colors = {
    'front': [],  # ด้านหน้า
    'back': [],   # ด้านหลัง
    'left': [],   # ด้านซ้าย
    'right': [],  # ด้านขวา
    'top': [],    # ด้านบน
    'bottom': []  # ด้านล่าง
}

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถเปิดกล้องได้")
        break

    # วาดวงกลมบนเฟรม
    draw_guidelines(frame, circle_positions)

    # แสดงผลเฟรม
    cv2.imshow("Rubik Color Capture", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('e'):  # กด 'e' เพื่อบันทึกค่าสี
        captured_colors = get_colors(frame, circle_positions)
        print("สีที่จับได้:", captured_colors)  # พิมพ์ตัวอักษรสีที่จับได้

        # เก็บสีที่จับได้ในแต่ละด้านของรูบิค
        rubik_colors['front'] = captured_colors[:3]
        rubik_colors['back'] = captured_colors[3:6]
        rubik_colors['left'] = captured_colors[6:9]
        rubik_colors['right'] = captured_colors[9:12]
        rubik_colors['top'] = captured_colors[12:15]
        rubik_colors['bottom'] = captured_colors[15:18]

        # แปลงข้อมูลสีเป็นสตริงสำหรับ Kociemba
        rubik_string = create_cube_string(rubik_colors)

        # แก้ปัญหาด้วย Kociemba
        solution = solve_rubik(rubik_string)
        print("คำแนะนำในการหมุน:", solution)  # แสดงคำแนะนำในการหมุน

        # ตัวอย่างการหมุนเซอร์โว (สามารถเชื่อมกับฟังก์ชันหมุนเซอร์โวจริงได้)
        for move in solution:
            rotate_servo(move)  # หมุนเซอร์โวตามคำแนะนำ

    elif key == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
        break

# ปิดกล้องและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
