import pandas as pd

# Tạo dataframe và gáng dữ liệu
df_students = (
    pd.DataFrame({
        'Name'  : ['Thành', 'Tuyết', 'Nhi', 'Tú', 'Dũng', 'Khoa', 'Vương', 'Tín', 'Tính', 'Hoàng'],
        'Age'   : [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        'Gender': ['Nam','Nam','Nữ','Nam','Nữ','Nam','Nữ','Nam','Nữ','Nam'],
        'Score' : [7.5,8.0,4.5,6.0,9.0,3.5,5.5,6.5,4.0,8.5]
    })
)

print(df_students)                
print(df_students.head(3))        
print(df_students.at[2, 'Name'])  
print(df_students.at[10, 'Age']    
      if 10 in df_students.index else 'Không có index 10')
print(df_students[['Name','Score']])

df_students['Pass'] = df_students['Score'] >= 5
print("\nDataFrame sau khi thêm cột 'Pass':")
print(df_students)

df_sorted = df_students.sort_values(by='Score', ascending=False)
print("\nDataFrame sau khi sắp xếp theo Score giảm dần:")
print(df_sorted)