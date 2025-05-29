def docso(so):
    chu_so = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    t = so // 100
    c = (so % 100) // 10
    d = so % 10
    res = f"{chu_so[t]} trăm"
    if c == 0 and d != 0:
        res += " lẻ " + chu_so[d]
    elif c == 1:
        res += " mười" + ("" if d == 0 else " " + ("lăm" if d == 5 else chu_so[d]))
    elif c > 1:
        res += " " + chu_so[c] + " mươi"
        if d == 1:
            res += " mốt"
        elif d == 4:
            res += " tư"
        elif d == 5:
            res += " lăm"
        elif d != 0:
            res += " " + chu_so[d]
    return res

num = input("nhap so: ")
print(docso(int(num)))
