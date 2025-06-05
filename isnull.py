import pandas as pd

df = pd.DataFrame([['ant', 'bee', 'cat'], ['dog', None , 'fly']])

# isnull() trả về DataFrame với True cho các giá trị null
print(df)
print(df.isnull())

# dropna() loại bỏ các hàng có giá trị null
print(df.dropna())

# fillna() thay thế giá trị null bằng giá trị khác
print(df.fillna(10))
