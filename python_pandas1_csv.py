import pandas as pd

df_students = pd.read_csv('students.csv')
print(df_students)
print(df_students.head(3))
print(df_students.columns)
print(df_students.at[2, 'name'])
print(df_students.at[10, 'age'] if 10 in df_students.index else 'Lỗi')
print(df_students[['name', 'score']])
df_students['Pass'] = df_students['score'] >= 5
print("\nDataFrame sau khi thêm cột 'Pass':")
print(df_students)
df_sorted = df_students.sort_values(by='score', ascending=False)
print("\nDataFrame sau khi sắp xếp theo score giảm dần:")
print(df_sorted)