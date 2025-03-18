import time

import requests
import pandas as pd
from tqdm import tqdm

# 百度API的APP_ID、API_KEY和SECRET_KEY
APP_ID = '117246480'
API_KEY = 'duPaS4px10QeBpk11gNRpIaB'
SECRET_KEY = 'Dt4Owv3wv9LwnBBXWZhaIIhIFunvAc4s'


# 获取Access Token
def get_access_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
    response = requests.get(url)
    return response.json().get('access_token')


# 情感分析函数
def sentiment_analysis(text, access_token):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'access_token': access_token,
    }
    data = {
        'text': text,
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    # print(response.json())
    return response.json()


# 映射情感极性为中文
def map_sentiment(sentiment):
    if sentiment == 0:
        return "负向"
    elif sentiment == 1:
        return "中性"
    elif sentiment == 2:
        return "正向"
    else:
        return "未知"


# 读取Excel文件
df = pd.read_excel(r"E:\project\data\combine.xlsx")
df.dropna(inplace=True)
# 获取Access Token
access_token = get_access_token()

# 对每个词语进行情感分析并保存结果


# 假设 sentiment_analysis 和 map_sentiment 函数已经定义

sentiments = []
labels = []

# 记录已发送请求的次
request_count = 0

# 初始请求，获取情感分析结果
for comment in tqdm(df['comment'], desc="Analyzing Sentiments"):
    result = sentiment_analysis(comment, access_token)

    if 'items' in result and len(result['items']) > 0:
        sentiment = result['items'][0]['sentiment']
        sentiment_cn = map_sentiment(sentiment)
        sentiments.append(sentiment_cn)
        labels.append(sentiment)
    else:
        sentiments.append("未知")  # 标记为未知
        labels.append(-1)  # 设置label为-1，表示需要重新请求

    # 每发送两次请求后，等待0.2秒
    request_count += 1
    if request_count == 2:
        time.sleep(0.2)
        request_count = 0  # 重置计数器

# 持续检查并请求API，直到所有label不为-1
while -1 in labels:
    for i in tqdm(range(len(df)), desc="Retrying Failed Requests"):
        if labels[i] == -1:
            # 如果label为-1，重新请求API
            result = sentiment_analysis(df['comment'][i], access_token)

            if 'items' in result and len(result['items']) > 0:
                sentiment = result['items'][0]['sentiment']
                sentiment_cn = map_sentiment(sentiment)
                sentiments[i] = sentiment_cn
                labels[i] = sentiment
            else:
                sentiments[i] = "未知"  # 如果仍然失败，标记为未知
                labels[i] = -1

        # 每发送两次请求后，等待0.2秒
        request_count += 1
        if request_count == 2:
            time.sleep(0.2)
            request_count = 0  # 重置计数器

# 将最终结果添加到DataFrame中
df['label'] = labels
df['sentiment'] = sentiments


# df = df[df['sentiment'] != "未知"]

# 保存结果到原文件
df.to_excel(r"comments.xlsx", index=False)

print("情感分析完成，结果已保存到文件！")
