def cutname(name):
    parts = name.strip().split()
    ho_lot = " ".join(parts[0:-1])  
    ten = parts[-1]
    return ho_lot, ten

ho_lot, ten = cutname("Giap huynh khoa")
print("Họ lot:", ho_lot)
print("Ten:", ten)
