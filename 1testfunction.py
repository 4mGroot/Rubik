
import time
from adafruit_pca9685 import PCA9685
import board
import busio

# สร้าง I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# สร้าง PCA9685 object
pca = PCA9685(i2c)
pca.frequency = 50 


def angle_to_duty_cycle(angle):
    min_duty = 1500 
    max_duty = 6000  
    return int(min_duty + (angle / 180) * (max_duty - min_duty))

def rotate_to_angle(channel, angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pca.channels[channel].duty_cycle = duty_cycle
    print('ตัวที่  '+channel+'หมุนไป' +angle)
    time.sleep(0.5)

try:
   
    print("หมุนเซอร์โวช่อง 0 ไปที่ 90°")
    rotate_to_angle(0, 90)

    
    print("หมุนเซอร์โวช่อง 1 ไปที่ 45°")
    rotate_to_angle(1, 45)

    
    print("หมุนเซอร์โวช่อง 2 ไปที่ 180°")
    rotate_to_angle(2, 180)
    print("หมุนเซอร์โวช่อง 2 กลับไปที่ 0°")
    rotate_to_angle(2, 0)

    # ตัวอย่าง 4: หมุนเซอร์โวทุกช่องไปที่มุม 90°
    print("หมุนเซอร์โวทุกช่องไปที่ 90°")
    for channel in range(6):  # ช่อง 0 ถึง 5
        rotate_to_angle(channel, 90)

    # ตัวอย่าง 5: หมุนวนทุกช่องไปที่มุม [0°, 90°, 180°, 90°, 0°]
    print("หมุนเซอร์โวทุกช่องตามลำดับมุม [0°, 90°, 180°, 90°, 0°]")
    angles = [0, 90, 180, 90, 0]
    for channel in range(6):
        for angle in angles:
            rotate_to_angle(channel, angle)

finally:
   print("ปิด PCA9685")
pca.deinit()  # ปิดการทำงานของ PCA9685
