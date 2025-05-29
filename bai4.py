from collections import Counter

chuoi = input("Nhập chuoi: ")
dem = Counter(chuoi)
all = dem.most_common()
for kytu, solan in all:
    if solan >= 0:
        if kytu == ' ':
            print(f"ky tu 'space' xuat hien {solan} lan.")
        else:
            print(f"ky tu '{kytu}' xuat hien {solan} lan.")
