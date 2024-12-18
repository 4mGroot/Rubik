data_font = []
data_right = []
data_back = []
data_left = []
data_up = []
data_down = []
datalist1 = [data_right,data_back,data_left,data_up,data_down]
count = 0

value = input("พิมมาเลย1 : ")
data_font.append(value)
first_list = False

while True :
    value = input("พิมมาเลย2 : ")
    if not first_list:
        datalist1[count].append(value)
        print(f'ข้อมูลใน data_{count +1} : {datalist1[count]}')
        count = (count+1) % len(datalist1)
        print(count)

        if all(len(data) > 0 for data in datalist1):
            print("ครบ")
            first_list = True
            
    else:
        print('มาแล้ว')
        if len(datalist1[count]) > 0:
            datalist1[count].insert(3,value)
            print(f'ข้อมูลใน data_{count +1} : {datalist1[count]}')
        count = (count+1) % len(datalist1)
        print(count)

        if all(len(data) >6 for data in datalist1):
            print("ครบทุกลิสต์แล้ว! เลิกการทำงาน")
            break


print("font ",data_font)
print("left ",data_left)
print("back ",data_back)
print("up ",data_up)
print("down ",data_down)

