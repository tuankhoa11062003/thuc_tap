from collections import Counter

chuoi = input("Nhập chuoi: ")
dem = Counter(chuoi)
kytu, solan = dem.most_common(1)[0]

print(f"max la ky tu '{kytu}' xuat hien {solan} lan.")
