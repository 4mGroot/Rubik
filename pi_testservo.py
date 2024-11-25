import time
from adafruit_pca9685 import PCA9685
import board
import busio

# สร้าง I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# สร้าง PCA9685 object
pca = PCA9685(i2c)
pca.frequency = 60  # ตั้งความถี่ที่ 60Hz (ค่ามาตรฐานสำหรับ servo)

# ฟังก์ชันหมุนไปข้างหน้า
def rotate_forward(channel, duty_cycle):
    pca.channels[channel].duty_cycle = duty_cycle  # หมุนไปข้างหน้า

# ฟังก์ชันหมุนถอยหลัง
def rotate_backward(channel, duty_cycle):
    pca.channels[channel].duty_cycle = duty_cycle  # หมุนถอยหลัง

# ฟังก์ชันหยุดการหมุน
def stop_rotation(channel):
    pca.channels[channel].duty_cycle = 0  # หยุดการหมุน

def rotate_to_90(channel):
    pca.channels[channel].duty_cycle = 2000 # ค่าเฉลี่ยสำหรับมุม 90°
    time.sleep(0.1)  # รอให้เซอร์โวหมุนไปที่มุม 90°

def rotate_to_180(channel):
    pca.channels[channel].duty_cycle = 2000 # ค่าเฉลี่ยสำหรับมุม 90°
    time.sleep(0.4)  # รอให้เซอร์โวหมุนไปที่มุม 90°

rotate_to_180(0)
stop_rotation(0)
# time.sleep(1)

# rotate_to_90(1)
# stop_rotation(1)
# time.sleep(1)

# rotate_to_90(2)
# stop_rotation(2)
# time.sleep(1)

# rotate_to_90(3)
# stop_rotation(3)
# time.sleep(1)

# rotate_to_90(4)
# stop_rotation(4)
# time.sleep(1)

# rotate_to_90(5)
# stop_rotation(5)
# time.sleep(1)



# rotate_forward(0, 3000)  
# time.sleep(1)  
# stop_rotation(0)  

# หมุนตัวที่สอง (Servo 2) ไปข้างหน้า
# rotate_forward(1, 1000)
# time.sleep(2)  
# stop_rotation(1)  
