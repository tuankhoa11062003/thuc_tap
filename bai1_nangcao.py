import math
def kiemtrasochinhphuong(n):
    return int(math.sqrt(n)) ** 2 == n

def kiemtradauvao():
    while True:
            a = int(input("Nhap a: "))
            b = int(input("Nhap b: "))
            if a >= b:
                print(" hay nhap a < b")
                continue
            return a, b
def kiemtrachuoiso(a, b):
    list = []
    for i in range(a, b + 1):
        if i % 3 == 0 and not kiemtrasochinhphuong(i):
            list.append(str(i))
    return  list
#main
a, b = kiemtradauvao()
c = kiemtrachuoiso(a, b)

print("cac so chia het cho 3 nhung khong phai la so chinh phuong la:")
print(", ".join(c) if c else "Không có số nào")
