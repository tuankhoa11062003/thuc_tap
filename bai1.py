def viethoa(text):
    return ". ".join(
        s.capitalize()
        for s in text.split(". ")
    )

text = input("nhap: ")
print(viethoa(text))
