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
df = pd.read_excel(r"comments.xlsx")
df.dropna(inplace=True)
# 获取Access Token
access_token = get_access_token()

# 对每个词语进行情感分析并保存结果

flag = 0

# 继续检查label为-1的评论并重新请求API
for i in tqdm(range(len(df)), desc="Retrying Failed Requests"):
    if df.at[i, 'label']  == -1:
        result = sentiment_analysis(df['comment'][i], access_token)
        if 'items' in result and len(result['items']) > 0:
            sentiment = result['items'][0]['sentiment']
            sentiment_cn = map_sentiment(sentiment)
            df.at[i, 'sentiment'] = sentiment_cn
            df.at[i, 'label'] = sentiment
        else:
            df.at[i, 'sentiment'] = "未知"
            df.at[i, 'label'] = -1
            
df = df[df['label']!=-1]


df.to_excel(r'comments.xlsx', index=False)  # 保存到原文件