import json
from tqdm import tqdm
import pandas as pd

from aliyunsdkalinlp.request.v20200629.GetSaChGeneralRequest import GetSaChGeneralRequest
from aliyunsdkalinlp.request.v20200629 import GetSaChGeneralRequest
from aliyunsdkcore.client import AcsClient



AccessKey_ID = 'LTAI5tLDGdLysuXcon847FkU'
AccessKey_Secret = 'o3SdSFDurlJZZaqGOI9YqUNttNEfW3'
Region_id = 'cn-hangzhou'

file_path = r'/process/Bert/baidu-api/words-freq/comments.xlsx'

client = AcsClient(AccessKey_ID, AccessKey_Secret, Region_id)
df = pd.read_excel(file_path)

def analyze_sentiment(text):
    request = GetSaChGeneralRequest.GetSaChGeneralRequest()
    request.set_ServiceCode('alinlp')
    request.set_Text(text)
    response = client.do_action_with_exception(request)
    result = json.loads(response)
    if 'Data' in result:
        data = json.loads(result['Data'])
        return data.get('sentiment')
    else:
        return None


tqdm.pandas(desc="Processing comments")
df['sentiment-ali'] = df['comment'].progress_apply(lambda x: analyze_sentiment(x) if pd.notna(x) else None)

# 将结果保存到新的Excel文件
df.to_excel('comments-ali.xlsx', index=False)