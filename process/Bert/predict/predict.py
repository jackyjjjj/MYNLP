import os

import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from tqdm import tqdm  # 导入tqdm库

#训练好的模型路径
modelPath = r''
#待预测的评论数据的路径
dataPath = r''
#待预测的评论数据文件名字
fileName = r''


# 加载中文BERT分词器和情感分析模型
tokenizer = BertTokenizer.from_pretrained(modelPath)
model = BertForSequenceClassification.from_pretrained(modelPath ,num_labels=3)

filePath = os.path.join(dataPath,fileName)
df = pd.read_excel(filePath)


# 定义一个函数来进行情感分析
def sentiment_analysis(text):
    # 编码输入文本
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)

    # 设置模型为评估模式
    model.eval()
    # 进行推理
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    # 获取预测类别
    prediction = torch.argmax(logits, dim=-1).item()
    # 返回情感标签
    return prediction


# 使用 tqdm 显示进度条
tqdm.pandas(desc="正在进行情感分析...")

# 对评论数据进行情感分析，并显示进度条
df['sentiment'] = df['comment'].progress_apply(sentiment_analysis)

# 将结果保存到新的Excel文件（例如 'comments_with_sentiment.xlsx'）
df.to_excel(f'{filePath}-predicted.xlsx', index=False)

print(f"情感分析完成，结果已保存到 f'{filePath}-predicted.xlsx'")
