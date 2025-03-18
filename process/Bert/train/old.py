import os



import pandas as pd

from sklearn.model_selection import train_test_split

from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, \
DataCollatorWithPadding

from datasets import Dataset

from transformers import Trainer, TrainingArguments, AdamW, get_linear_schedule_with_warmup







dataPath = r'E:\project\process\Bert\baidu-api'

savePath = r'E:\project\process\Bert\train'

modelSavePath = r'E:\project\process\Bert\bert-trained'



fileName = 'comments.xlsx'

excel_file_path = os.path.join(savePath,fileName)

df = pd.read_excel(excel_file_path)

# 2. 数据预处理
# 假设 DataFrame 中有 'text' 和 'label' 两列

df = df[['comment', 'label']]
# 3. 切分训练集和验证集

train_df, test_df = train_test_split(df, test_size=0.2) # 80% 训练，20% 测试

# 4. 将 DataFrame 转换为 Hugging Face 数据集
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# 5. 加载中文 BERT tokenizer 和模型

tokenizer = BertTokenizer.from_pretrained(r'/root/MyData/process/bert-trained-base-chinese')

model = BertForSequenceClassification.from_pretrained(r'/root/MyData/process/bert-trained-base-chinese',

num_labels=3) # 假设是二分类任务
# 6. 数据预处理函数

def tokenize_function(examples):
    return tokenizer(examples['comment'], truncation=True)

# 7. 对训练集和验证集进行分词
train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# 8. 设置数据格式
# train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'sentiment'])
# test_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'sentiment'])

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
# 配置训练参数
training_args = TrainingArguments(
output_dir='../bert-trained/results', # 输出目录
evaluation_strategy="epoch", # 每个 epoch 后评估一次
learning_rate=2e-5, # 初始学习率
per_device_train_batch_size=16, # 每个设备训练批次大小
per_device_eval_batch_size=64, # 每个设备评估批次大小
num_train_epochs=10, # 训练 epoch 数
weight_decay=0.01, # 权重衰减
lr_scheduler_type='linear', # 使用线性学习率调度器
warmup_steps=500, # 预热步数，学习率从 0 线性增加到初始学习率
logging_dir='./logs', # 日志保存路径
)



# 如果需要自定义优化器 AdamW（默认的），可以按如下方式设置

optimizer = AdamW(model.parameters(), lr=training_args.learning_rate)
# 获取学习率调度器
num_training_steps = len(train_dataset) * training_args.num_train_epochs // training_args.per_device_train_batch_size
lr_scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=training_args.warmup_steps,
    num_training_steps=num_training_steps
)



# 使用 Trainer 进行训练

trainer = Trainer(

model=model, # 你训练的模型

args=training_args, # 训练配置

optimizer=optimizer, # 优化器

lr_scheduler=lr_scheduler, # 学习率调度器

train_dataset=train_dataset, # 训练数据

eval_dataset=test_dataset, # 验证数据

)



# 开始训练

trainer.train()



# 12. 保存微调后的模型



model.save_pretrained(os.path.join(modelSavePath,"./bert_trained_by_20000"))

tokenizer.save_pretrained(os.path.join(modelSavePath,"./bert_trained_by_20000"))



# 13. 评估模型

eval_results = trainer.evaluate()



# 14. 打印评估结果

print(f"评估结果: {eval_results}")



# 15. 计算准确度

predictions = trainer.predict(test_dataset)

preds = predictions.predictions.argmax(-1)

labels = predictions.label_ids



# 计算准确度

accuracy = (preds == labels).mean()

print(f"模型准确度: {accuracy:.4f}")