import csv
import os
import re

from appium.options.android import UiAutomator2Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
from appium import webdriver

save_path = r"E:\project\data"
pattern = re.compile(
    r"(?P<userName>.*?)\n"  # 昵称
    r"(?P<rating>\d+星)\n"  # 评分
    r"(?P<content>.*?)\n"  # 评论内容
    r"(?P<date>\d{4}-\d{2}-\d{2});"  # 日期
    r"(?P<region>.*?);"  # 地区
    r"来自(?P<device>.*?);"  # 设备
    r"点赞(?P<likes>\d+)"  # 点赞数
)

categories = ['资讯阅读','摄影美图','社交通讯','音乐电台']
Apps = ['QQ']


def getComments(driver):
    time.sleep(1)
    name = driver.find_element(By.XPATH,
                               '//android.widget.TextView[@resource-id="com.bbk.appstore:id/package_detail_title"]')
    appName = name.text
    #点击评论
    driver.tap([(450, 510)])
    # for _ in range(3):
    #     driver.swipe(500, 1200, 500, 700)
    # 定义存储评论数据的列表
    comments_data = []
    time.sleep(1)

    time.sleep(0.5)

    scroll_time = 700  # 设置滑动次数
    for _ in range(scroll_time):
        try:
            # 滑动屏幕（根据实际情况调整坐标）
            driver.swipe(500, 1200, 500, 620)
            time.sleep(0.2)  # 给页面加载时间
            # 获取评论元素
            infos = driver.find_elements(By.CLASS_NAME, 'android.widget.LinearLayout')
            # 遍历每个评论项
            for info in infos:
                try:
                    # 获取 content-desc 属性
                    content_desc = info.get_attribute('content-desc')
                    if not content_desc:
                        # print("警告：未找到 content-desc 属性")
                        continue

                    # 替换换行符和 HTML 实体
                    content_desc = content_desc.replace("&#10;", "\n").strip()

                    # 正则匹配
                    match = pattern.search(content_desc)
                    if not match:
                        print("警告：未匹配到有效数据")
                        continue

                    # 转换成字典
                    data = match.groupdict()

                    # 将点赞数转换为整数
                    data["likes"] = int(data["likes"])

                    # 打印解析结果
                    print("解析结果：")
                    print(data)

                    # 将数据添加到列表中
                    comments_data.append({
                        'rating': data['rating'],
                        'comment': data['content'],
                        'ip': data['region'],  # 注意：这里可能是地区，而不是 IP 地址
                        'likes': data['likes']
                    })
                    print('添加数据成功')

                except AttributeError as e:
                    print(f"错误：元素属性获取失败 - {e}")
                except ValueError as e:
                    print(f"错误：数据转换失败（如点赞数不是数字） - {e}")
                except Exception as e:
                    print(f"未知错误：{e}")

                    # 打印最终解析的评论数据
            # print("所有解析的评论数据：")
            # print(comments_data)

        except Exception as e:
            print(f"发生错误: {e}")

    file_name = f"{appName}.xlsx"
    #评论数据去重
    unique_comments = [dict(t) for t in {frozenset(item.items()) for item in comments_data}]
    if len(unique_comments) == 0:
        print(f'{appName}最新评论为空')

    #保存文件的路径
    excel_file_name = os.path.join(save_path, file_name)
    # 如果文件已存在，读取数据并追加
    if os.path.isfile(excel_file_name):
        # 如果文件存在，则追加数据
        df_existing = pd.read_excel(excel_file_name)
        df_new = pd.DataFrame(unique_comments)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(excel_file_name, index=False)  # 保存合并后的数据
    else:
        # 如果文件不存在，则创建新文件并写入数据
        df_new = pd.DataFrame(unique_comments)
        df_new.to_excel(excel_file_name, index=False)  # 保存新数据

    print(f"评论数据已保存到 {excel_file_name}")



#导航到评论
def find_comment(driver):
    time.sleep(3)
    # 点击分类

    time.sleep(2)

    driver.find_element(By.XPATH,
                        '(//android.widget.LinearLayout[@resource-id="com.bbk.appstore:id/ll_info"])[1]').click()
    time.sleep(1)


if __name__ == "__main__":
    desired_caps = {
        'platformName': 'Android',  # 被测手机是安卓
        'platformVersion': '12',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
        'deviceName': 'vivo',  # 设备名，安卓手机可以随意填写
        'appPackage': 'com.bbk.appstore',  # 启动APP Package名称
        'appActivity': '.ui.AppStore',  # 启动Activity名称
        'unicodeKeyboard': True,  # 自动化需要输入中文时填True
        'resetKeyboard': True,  # 执行完程序恢复原来输入法
        'noReset': True,  # 不要重置App
        'newCommandTimeout': 6000,
        'automationName': 'UiAutomator2'
        # 'app': r'd:\apk\bili.apk',
    }


    driver = webdriver.Remote('http://localhost:4723/wd/hub',
                              options=UiAutomator2Options().load_capabilities(desired_caps))
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '//android.widget.TextSwitcher[@resource-id="com.bbk.appstore:id/ts_key_label_new"]').click()
    for app in Apps:

        time.sleep(0.5)

        driver.find_element(By.XPATH,'//android.widget.EditText[@content-desc="应用搜索框"]').send_keys(app)
        time.sleep(2)
        driver.find_element(By.XPATH,'//android.widget.TextView[@resource-id="com.bbk.appstore:id/search_box"]').click()

        time.sleep(1)

        driver.find_element(By.XPATH,'(//android.widget.RelativeLayout[@resource-id="com.bbk.appstore:id/package_list_item_info_layout"])[1]').click()
        getComments(driver)
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//android.widget.ImageButton[@content-desc="返回"]').click()



    # 关闭驱动
    driver.quit()
