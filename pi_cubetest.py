import cv2

# เปิดการเชื่อมต่อกับกล้อง (0 หมายถึงกล้องแรก)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: ไม่สามารถเปิดกล้องได้")
    exit()

while True:
    # อ่านภาพจากกล้อง
    ret, frame = cap.read()

    if not ret:
        print("Error: ไม่สามารถรับข้อมูลจากกล้องได้")
        break

    # แสดงภาพจากกล้อง
    cv2.imshow('Camera Feed', frame)

    # กด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดการเชื่อมต่อกับกล้องและหน้าต่างแสดงผล
cap.release()
cv2.destroyAllWindows()
