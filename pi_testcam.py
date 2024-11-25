import cv2
import numpy as np

# เปิดกล้อง
cap = cv2.VideoCapture(0)  # ใช้ 0 สำหรับกล้องตัวแรก หากต้องการใช้กล้องตัวที่สองให้ใช้ 1

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถเปิดกล้องได้")
        break

    # แปลง BGR เป็น LAB
    lab_image = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # แยกส่วนของ L, A, B
    l, a, b = cv2.split(lab_image)

    # ใช้ Median Blur เพื่อปรับภาพให้เรียบ
    l = cv2.medianBlur(l, 15)

    # รวมภาพ LAB กลับเข้าด้วยกัน
    enhanced_lab = cv2.merge([l, a, b])

    # แปลงจาก LAB กลับเป็น BGR
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # แปลง BGR เป็น HSV
    hsv_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)

    # แยกส่วน H, S, V
    h, s, v = cv2.split(hsv_image)

    # เพิ่มความเข้มของสี (Saturation)
    s = cv2.add(s, 75)
    s = cv2.min(s, 255)

    # รวมส่วนต่างๆ ของ HSV กลับเข้าไป
    enhanced_hsv = cv2.merge([h, s, v])

    # แปลงกลับเป็น BGR
    enhanced_image = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

    # แสดงผลเฟรม
    cv2.imshow("Enhanced Image", enhanced_image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
        break

# ปิดกล้องและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
