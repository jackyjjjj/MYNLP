import time
import subprocess
import os

EXECUTION_TIME = "11:20:00"  # 设定执行时间（24小时制，例如14:30）
COMMAND = "java -jar .\wtu-booking.jar 羽毛球 04号场 2025-03-08 13:30-15:00 fcfd3c0ffaff11efb3790242ac110002"  # Windows CMD 命令
WORKING_DIRECTORY = r"E:\reserve"  # 目标执行目录


def run_command():
    try:
        os.chdir(WORKING_DIRECTORY)  # 切换到目标目录
        result = subprocess.run(COMMAND, shell=True, capture_output=True, text=True)
        print("Command Output:")
        print(result.stdout)
        print("Command Errors:")
        print(result.stderr)
    except Exception as e:
        print(f"Error executing command: {e}")

# 计算等待时间
current_time = time.strftime("%H:%M:%S")
while current_time != EXECUTION_TIME:
    time.sleep(1)  # 每秒检查一次
    current_time = time.strftime("%H:%M:%S")

# 到达指定时间后执行命令
run_command()
