import kociemba

# รับค่าในแต่ละด้านของรูบิค
print("กรุณาพิมพ์สีของแต่ละช่องในแต่ละด้าน (r=แดง, y=เหลือง, b=น้ำเงิน, o=ส้ม, w=ขาว, g=เขียว):")

# รับสีสำหรับแต่ละด้าน (เก็บในรูปแบบ array)
front = list(input("ด้านหน้า (น้ำเงิน) - กรอก 9 ช่อง (เช่น 'rrrbrrbrr'): "))
back = list(input("ด้านหลัง (เขียว) - กรอก 9 ช่อง: "))
left = list(input("ด้านซ้าย (ส้ม) - กรอก 9 ช่อง: "))
right = list(input("ด้านขวา (แดง) - กรอก 9 ช่อง: "))
up = list(input("ด้านบน (เหลือง) - กรอก 9 ช่อง: "))
down = list(input("ด้านล่าง (ขาว) - กรอก 9 ช่อง: "))

# รวมสีทั้งหมดในลำดับที่ kociemba ต้องการ
cube_array = up + right + front + down + left + back
cube = "".join(cube_array)

print("ข้อมูลสีในต้นฉบับ:", cube)

# แทนที่สีในสตริงให้ตรงกับไลบรารี Kociemba
cube = cube.replace('r', 'R')  # สีแดง -> R
cube = cube.replace('y', 'U')  # สีเหลือง -> U
cube = cube.replace('b', 'F')  # สีน้ำเงิน -> F
cube = cube.replace('o', 'L')  # สีส้ม -> L
cube = cube.replace('w', 'D')  # สีขาว -> D
cube = cube.replace('g', 'B')  # สีเขียว -> B

print("ข้อมูลสีที่แปลงแล้ว:", cube)

# แก้ปัญหาด้วยไลบรารี Kociemba
solution = kociemba.solve(str(cube))
test = solution.split
print("คำแนะนำในการหมุน:", solution)
