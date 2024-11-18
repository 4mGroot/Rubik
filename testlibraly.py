import kociemba


cube = "rorrybobogwyrrgwyobryybggoowygwwbrgbyywoogbrrbbgwgwyow"
print("ข้อมูลสีในต้นฉบับ:", cube)


cube = cube.replace('y', 'U')
cube = cube.replace('r', 'R')
cube = cube.replace('b', 'F')
cube = cube.replace('w', 'D')
cube = cube.replace('o', 'L')
cube = cube.replace('g', 'B')

print("ข้อมูลสีที่แปลงแล้ว:", cube)


solution = kociemba.solve(str(cube))
print("คำแนะนำในการหมุน:", solution)
