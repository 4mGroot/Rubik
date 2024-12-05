
import time
# from adafruit_pca9685 import PCA9685
# import board
# import busio

# # สร้าง I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)

# # สร้าง PCA9685 object
# pca = PCA9685(i2c)
# pca.frequency = 50 



def angle_to_duty_cycle(angle):
    min_duty = 1500 
    max_duty = 6000  
    return int(min_duty + (angle / 180) * (max_duty - min_duty))

def rotate_to_angle(channel, angle):
    duty_cycle = angle_to_duty_cycle(angle)
    print(f'servo ตัวที่ {channel} หมุนไปที่มุม {angle} โดย Duty Cycle = {duty_cycle}')
    time.sleep(0.5)

try:
    rotate_to_angle(0, 90)
    rotate_to_angle(1)

finally:
    print("ปิด PCA9685 (ไม่มีการเชื่อมต่อกับฮาร์ดแวร์)")
