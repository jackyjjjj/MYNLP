import os
import pandas as pd
from tqdm import tqdm  # 导入 tqdm 库

# 文件夹路径，包含所有的Excel文件
folder_path = r'E:\project\data'  # 请替换为你的文件夹路径

# 获取文件夹中所有Excel文件的列表
file_list = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 初始化一个空的DataFrame，用于存储合并后的数据
all_data = pd.DataFrame()

# 使用 tqdm 显示进度条
tqdm.pandas(desc="正在合并文件...")

# 遍历每个文件，将其数据读取并合并到all_data中
for file in tqdm(file_list, desc="处理文件", unit="文件"):
    # 构造文件的完整路径
    file_path = os.path.join(folder_path, file)

    # 读取当前Excel文件
    df = pd.read_excel(file_path)

    # 只保留 `likes`, `comment`, `ip`, `rating` 四列
    df = df[['likes', 'comment', 'ip', 'rating']]
    df.dropna(inplace=True)  # 删除包含缺失值的行

    # 将当前文件的数据追加到 all_data 中
    all_data = pd.concat([all_data, df], ignore_index=True)

# 将合并后的数据保存到新的Excel文件中
all_data.to_excel(r'E:\project\data\combine.xlsx', index=False)

print("所有文件已合并，结果已保存到 'combine.xlsx'")
