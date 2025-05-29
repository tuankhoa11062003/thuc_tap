from collections import Counter

chuoi = input("Nhập chuoi: ")
dem = Counter(chuoi)
listnumber =[]
all = dem.most_common()
for kytu in all:
        if kytu[0].isdigit():
            listnumber.append(kytu[0])
print(listnumber)

            
