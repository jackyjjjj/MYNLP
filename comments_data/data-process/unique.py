import pandas as pd

# 读取Excel文件
df = pd.read_excel(r'E:\project\data\喜马拉雅-听书听播客.xlsx')

# 去除重复的行（根据所有列判断重复）
df_no_duplicates = df.drop_duplicates()

# 如果只根据某些列去重，例如 '列1' 和 '列2'
# df_no_duplicates = df.drop_duplicates(subset=['列1', '列2'])
df_no_duplicates.dropna(inplace=True)
# 将去重后的数据保存回Excel文件
df_no_duplicates.to_excel('E:\project\data\喜马拉雅-听书听播客.xlsx', index=False)
