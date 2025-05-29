import time

def randomnumber():
    miligiay = int((time.time() * 1000)) % 1000
    if miligiay == 0:
        miligiay = 1
    return miligiay

def doanso():
    while True:
            so = int(input("hay doan so tu 1 den 999: "))
            if 1 <= so <= 999:
                return so
            else:
                print("Vui lòng nhập số trong khoảng 1 đến 999.")

def game():
    youdone = randomnumber()
    youfail = 0

    while True:
        doan = doanso()
        
        if doan == youdone:
            print(f"ban da doan dung so {youdone}!")
            break
        else:
            youfail += 1
            if abs(doan - youdone) <= 10:
                print("ban doan gan dung roi!")

            print(f"da doan sai {youfail} lần.")

            if youfail == 5:
                print("Ban da doan sai 5 lan, xin hay doan lai.")
                youdone = randomnumber()
                youfail = 0  # Reset số lần sai

# Bắt đầu trò chơi
game()
