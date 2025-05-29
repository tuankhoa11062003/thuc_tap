def kiem_tra_doi_xung(chuoi):
    chuoi = chuoi.strip()
    return chuoi == chuoi[::-1]
char = input("Nhap chuoi: ")
if kiem_tra_doi_xung(char):
    print("doi xung.")
else:
    print("khong doi xung.")
