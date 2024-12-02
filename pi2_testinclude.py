data_font = []
data_right = []
data_back = []
data_left = []
data_up = []
data_down = []
datalist1 = [data_font,data_right,data_back,data_left,data_up,data_down]
count = 0
first_list = False

while True :
    value = input("พิมมาเลย2 : ")
    if not first_list:
        datalist1[count].append(value)
        print(f'ข้อมูลใน data_{count +1} : {datalist1[count]}')
        count = (count+1) % len(datalist1)
        print(count)
        print(first_list)

        if all(len(data) >0 for data in datalist1):
            print("ครบ")
            first_list = True
            print(data_font)
            print(data_right)
            print(data_back)
            print(data_left)
            print(data_up)
            print(data_down)
            print(count)
            
            
    else:
        print('มาแล้ว')
        if count == 0:
            count = 1
        datalist1[count][0] = datalist1[count][0][:3] + value + datalist1[count][0][3:]
        print(f'ข้อมูลใน data_{count + 1} : {datalist1[count]}')
        count = (count+1)

        if all(len(data[0]) == 8 for data in datalist1[1:] if len(data) > 0):
            print("ครบทุกลิสต์แล้ว! เลิกการทำงาน")
            break



print("font ",data_font)
print("left ",data_left)
print("back ",data_back)
print("up ",data_up)
print("down ",data_down)

