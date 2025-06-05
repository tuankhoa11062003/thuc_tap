import pandas  as pd
df_nhanvien = pd.DataFrame({
    'ID'        : [101, 102, 103, 104, 105, 106],
    'Name'      : ['An','Bình', 'Cường', 'Cường', None, 'Hà'], 
    'Age'       : [25,  None, 30, 22, 28, None],
    'Salary'    : [700, 800, 750, None, 710, None],
    'Department': ['HR','IT', 'Marketing', 'Finance', 'HR', None]
})

df_phongban = pd.DataFrame({
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager'   : ['Trang', 'Khoa', 'Minh', 'Lan']
    })
# kieu tra giá trị null trong ban nhanvien
print(df_nhanvien.isnull())
print("_______________________________________________________________________________________________")
# loai bo cac hang co gia tri null trong ban nhanvien
nhan_vien = df_nhanvien.dropna(thresh=df_nhanvien.shape[1] - 2)
print(nhan_vien)
# thay the gia tri null bang gia tri khac
df_nhanvien['Name'] = df_nhanvien['Name'].fillna('chua ro')
df_nhanvien['Age'] = df_nhanvien['Age'].fillna(df_nhanvien['Age'].mean())
df_nhanvien['Salary'] = df_nhanvien['Salary'].fillna(method = 'ffill')
df_nhanvien['Department'] = df_nhanvien['Department'].fillna('unkknown')
print("_______________________________________________________________________________________________")
print(df_nhanvien)
# doi kieu du lieu
print("_______________________________________________________________________________________________")
df_nhanvien['Age'] = df_nhanvien['Age'].astype('int')
df_nhanvien['Salary'] = df_nhanvien['Salary'].astype('int')
print(df_nhanvien.dtypes)
# loc nhan vien it voi do tuoi tren 25
df_nhanvien_it = df_nhanvien[(df_nhanvien['Department'] == 'IT') & (df_nhanvien['Age'] > 25)]
print("_______________________________________________________________________________________________")
print(df_nhanvien_it)
print("_______________________________________________________________________________________________")
# sap xep nhan vien theo luong giam dan
df_nhanvien_sorted = df_nhanvien.sort_values(by='Salary', ascending=False)
print(df_nhanvien_sorted)
# nhom nhan vien theo phong ban
df_grouped = df_nhanvien.groupby('Department')["Salary"].mean().reset_index()
print("_______________________________________________________________________________________________")
print(df_grouped)
# dung merge de ket ban nhan vien voi ban phong ban
df_merged = pd.merge(df_nhanvien, df_phongban, on='Department', how='left')
print("_______________________________________________________________________________________________")
print(df_merged)
# tao ban nhan vien moi gom 2 nhan vien moi va dung concat de noi voi ban nhan vien hien tai
new_employees = pd.DataFrame({
    'ID'        : [107, 108],
    'Name'      : ['Hải', 'Lan'],
    'Age'       : [26, 29],
    'Salary'    : [720, 780],
    'Department': ['IT', 'Marketing']
})
df_nhanvien = pd.concat([df_nhanvien, new_employees], ignore_index=True)
print("_______________________________________________________________________________________________")
print(df_nhanvien)
# tao cot Slary after_tax de tinh luong sau thue
df_nhanvien['Salary_after_tax'] = df_nhanvien['Salary'] * 0.9
print("_______________________________________________________________________________________________")
print(df_nhanvien)