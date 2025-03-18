import pandas as pd

col = ['您认为西藏文创促销活动哪种形式更吸引您？',' 您认为西藏文创产品最需要改进的方面是？',' 您希望西藏景区/文创店提供哪些附加服务？','您更倾向于文创产品中包含以下哪些元素？','您更倾向于哪种产品形式？','您认为西藏文创产品最吸引您的包装风格是？',
       '您购买文创产品的主要用途是？','您通常通过什么渠道购买西藏文创产品？','您通过哪些渠道了解到西藏文创产品？','若去过西藏，您去过的地市包括以下哪些？']

# 读取 Excel 文件
df = pd.read_excel("comments_data.xlsx")

for c in col:

    # 假设需要处理的列名为 'tags'
    column_name = c
    # 拆分该列，并创建新的独热编码列
    split_values = df[column_name].str.get_dummies(sep='┋')

    # 重命名列名，添加前缀（旧列名+下划线）
    split_values = split_values.add_prefix(f"{column_name}_")

    # 将新列追加到原 DataFrame 的指定位置（旧列后）
    col_index = df.columns.get_loc(column_name)  # 获取该列索引
    df = pd.concat([df.iloc[:, :col_index+1], split_values, df.iloc[:, col_index+1:]], axis=1)

    # 保存处理后的 Excel 文件
df.to_excel("output.xlsx", index=False)
