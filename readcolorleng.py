import cv2
import time

# ฟังก์ชันวาดวงกลมสำหรับตำแหน่ง mark
def draw_guidelines(frame, points):
    for (x, y) in points:
        cv2.circle(frame, (x, y), 10, (0, 255, 0), 2)  # วาดวงกลม

# ฟังก์ชันอ่านค่าสี BGR จากตำแหน่ง mark
def get_bgr_colors(frame, points):
    colors = []
    for (x, y) in points:
        b, g, r = frame[y, x]  # อ่านค่าพิกเซล BGR ตรงตำแหน่ง
        colors.append((b, g, r))
    return colors

# กำหนดตำแหน่ง mark ที่ต้องการ
circle_positions = [
    (200, 150), (300, 150), (400, 150),  # แถวบน
    (200, 250),           (400, 250),  # แถวกลาง
    (200, 350), (300, 350), (400, 350)   # แถวล่าง
]

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# กำหนดเวลาเริ่มต้น
last_read_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("ไม่สามารถเปิดกล้องได้")
        break

    # วาดวงกลมบนเฟรม
    draw_guidelines(frame, circle_positions)

    # ตรวจสอบเวลาเพื่ออ่านค่าสีทุกๆ 10 วินาที
    current_time = time.time()
    if current_time - last_read_time >= 10:  # ถ้าผ่านไป 10 วินาที
        captured_colors = get_bgr_colors(frame, circle_positions)
        print("ค่าสี BGR ที่จับได้:", captured_colors)  # แสดงผล BGR ในคอนโซล
        last_read_time = current_time  # อัปเดตเวลาเริ่มต้นใหม่

    # แสดงผลเฟรม
    cv2.imshow("Rubik Color Capture", frame)

    # กด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดกล้องและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
