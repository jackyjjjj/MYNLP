import os
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, \
    DataCollatorWithPadding, EarlyStoppingCallback
from datasets import Dataset
from transformers import Trainer, TrainingArguments, AdamW, get_linear_schedule_with_warmup
import matplotlib.pyplot as plt
import json

config_path = r'/root/autodl-tmp/MyData/path-config.json'

with open(config_path,"r",encoding='utf-8') as f:
    config = json.load(f)


modelSavePath = config['model_save_path']
excel_file_path = config['train_data']
pretrained_model_path = config['pretrained_model_path']

# 读取数据
df = pd.read_excel(excel_file_path)

# 数据预处理
df = df[['comment', 'label']]

# 切分训练集和验证集
train_df, test_df = train_test_split(df, test_size=0.2)

# 转换为 Hugging Face 数据集格式
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# 加载 BERT tokenizer 和模型
tokenizer = BertTokenizer.from_pretrained(pretrained_model_path)
model = BertForSequenceClassification.from_pretrained(pretrained_model_path, num_labels=3)

# 数据预处理函数
def tokenize_function(examples):
    return tokenizer(examples['comment'], padding=True, truncation=True, max_length=128)

# 对训练集和验证集进行分词
train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# 设置数据格式
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# 配置训练参数
training_args = TrainingArguments(
    output_dir='../bert-trained/results',  # 输出目录
    evaluation_strategy="epoch",  # 每个 epoch 后评估一次
    learning_rate=2e-5,  # 初始学习率
    per_device_train_batch_size=16,  # 每个设备训练批次大小
    per_device_eval_batch_size=64,  # 每个设备评估批次大小
    num_train_epochs=10,  # 训练 epoch 数
    weight_decay=0.01,  # 权重衰减
    lr_scheduler_type='linear',  # 使用线性学习率调度器
    warmup_steps=500,  # 预热步数，学习率从 0 线性增加到初始学习率
    logging_dir='./logs',  # 日志保存路径
    logging_steps=10,  # 每 10 步记录一次日志
    save_strategy="epoch",  # 每个 epoch 后保存模型
    load_best_model_at_end=True,  # 加载验证集上表现最好的模型
    metric_for_best_model="eval_loss",  # 监控验证集上的损失
    greater_is_better=False,  # 损失越小越好
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

# 添加提前停止回调
early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=3)  # 3 个 epoch 没有提升就停止

# 使用 Trainer 进行训练
trainer = Trainer(
    model=model,  # 你训练的模型
    args=training_args,  # 训练配置
    optimizer=optimizer,  # 优化器
    lr_scheduler=lr_scheduler,  # 学习率调度器
    train_dataset=train_dataset,  # 训练数据
    eval_dataset=test_dataset,  # 验证数据
    callbacks=[early_stopping_callback]  # 添加提前停止回调
)

# 开始训练
train_result = trainer.train()

# 12. 保存微调后的模型
model.save_pretrained(os.path.join(modelSavePath, "./bert_trained_by_20000"))
tokenizer.save_pretrained(os.path.join(modelSavePath, "./bert_trained_by_20000"))

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

# 16. 可视化训练过程
# 提取训练和验证损失
train_loss = [log['loss'] for log in trainer.state.log_history if 'loss' in log]
eval_loss = [log['eval_loss'] for log in trainer.state.log_history if 'eval_loss' in log]
epochs = range(1, len(train_loss) + 1)

# 绘制损失曲线
plt.plot(epochs, train_loss, label='Training Loss')
plt.plot(range(1, len(eval_loss) + 1), eval_loss, label='Evaluation Loss')
plt.title('Training Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# 提取学习率
learning_rates = [log['learning_rate'] for log in trainer.state.log_history if 'learning_rate' in log]
steps = range(1, len(learning_rates) + 1)

# 绘制学习率曲线
plt.plot(steps, learning_rates)
plt.title('Learning Rate Schedule')
plt.xlabel('Step')
plt.ylabel('Learning Rate')
plt.show()