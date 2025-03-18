import csv
import os
from appium.options.android import UiAutomator2Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
from appium import webdriver

save_path = r"/getComments\OPPO\视频播放"

#获取最热长评论
def getLongComments(driver):
    # 定义存储评论数据的列表
    comments_data = []
    time.sleep(1)
    name = driver.find_element(By.XPATH,
                               '//android.widget.TextView[@resource-id="com.heytap.market:id/header_app_name"]')
    appName = name.text

    driver.find_element(By.XPATH, '//android.widget.TextView[@text="评论"]').click()
    time.sleep(0.5)

    scroll_time = 5  # 设置滑动次数
    for _ in range(scroll_time):
        try:
            # 滑动屏幕（根据实际情况调整坐标）
            driver.swipe(500, 1200, 500, 700)
            time.sleep(1)  # 给页面加载时间
            # 获取评论元素
            infos = driver.find_elements(By.ID, 'rl_comment_item_content_layout')
            # 遍历每个评论项
            for info in infos:
                try:
                    # info.find_element(By.ID,'expand_icon').click()
                    name = info.find_element(By.ID, 'tv_item_username').text
                    # 获取评论内容
                    comment = info.find_element(By.ID, 'collapse_tv').text
                    # 获取发布地点
                    address = info.find_element(By.ID, 'tv_comment_address').text
                    # 提取发布地点的 IP 地址（假设地址的格式从第 4 个字符开始）
                    ip = address[3:].strip()
                    # 存储爬取的数据
                    user_data = {'name': name, 'comment': comment, 'ip': ip}
                    comments_data.append(user_data)
                    # 打印每条评论
                    print(user_data)

                except NoSuchElementException as e:
                    print(f"元素未找到: {e}")
                except StaleElementReferenceException as e:
                    print(f"元素失效: {e}")
                except Exception as e:
                    print(f"发生错误: {e}")

        except Exception as e:
            print(f"发生错误: {e}")

    file_name = f"{appName}_comments.xlsx"
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


#获取最新的短评论
def getShortComments(driver):
    comments_data = []
    time.sleep(1)
    name = driver.find_element(By.XPATH,
                               '//android.widget.TextView[@resource-id="com.heytap.market:id/header_app_name"]')
    appName = name.text

    driver.find_element(By.XPATH, '//android.widget.TextView[@text="评论"]').click()
    time.sleep(0.5)
    driver.find_element(By.XPATH,
                        '//android.widget.ImageView[@resource-id="com.heytap.market:id/expand_indicator"]').click()
    time.sleep(0.5)
    driver.find_element(By.XPATH,
                        '//android.widget.TextView[@resource-id="com.heytap.market:id/popup_list_window_item_title" and @text="最新"]').click()
    scroll_time = 200  # 设置滑动次数
    for _ in range(scroll_time):
        try:
            # 滑动屏幕（根据实际情况调整坐标）
            driver.swipe(500, 1200, 500, 700)
            time.sleep(1)  # 给页面加载时间
            # 获取评论元素
            infos = driver.find_elements(By.ID, 'rl_comment_item_content_layout')
            # 遍历每个评论项
            for info in infos:
                try:
                    name = info.find_element(By.ID, 'tv_item_username').text
                    # 获取评论内容
                    comment = info.find_element(By.ID, 'expand_tv').text
                    # 获取发布地点
                    address = info.find_element(By.ID, 'tv_comment_address').text
                    # 提取发布地点的 IP 地址（假设地址的格式从第 4 个字符开始）
                    ip = address[3:].strip()
                    # 存储爬取的数据
                    user_data = {'name': name, 'comment': comment, 'ip': ip}
                    comments_data.append(user_data)
                    # 打印每条评论
                    print(user_data)


                except NoSuchElementException as e:
                    print(f"元素未找到: {e}")
                except StaleElementReferenceException as e:
                    print(f"元素失效: {e}")
                except Exception as e:
                    print(f"发生错误: {e}")

        except Exception as e:
            print(f"发生错误: {e}")

    file_name = f"{appName}_comments.xlsx"

    excel_file_name = os.path.join(save_path, file_name)
    # 评论数据去重
    unique_comments = [dict(t) for t in {frozenset(item.items()) for item in comments_data}]
    if len(unique_comments) == 0:
        print(f'{appName}最新评论为空')

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



if __name__ == "__main__":
    desired_caps = {
        'platformName': 'Android',  # 被测手机是安卓
        'platformVersion': '12',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
        'deviceName': 'oppo',  # 设备名，安卓手机可以随意填写
        'appPackage': 'com.heytap.market',  # 启动APP Package名称
        'appActivity': '.activity.MainActivity',  # 启动Activity名称
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
    # 点击软件
    driver.find_element(By.XPATH,
                        '(//android.widget.ImageView[@resource-id="com.heytap.market:id/navigation_bar_item_icon_view"])[3]').click()
    time.sleep(0.5)

    #点击分类
    driver.find_element(By.XPATH,
                        '//android.widget.TextView[@text="分类"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//android.widget.TextView[@text="视频播放"]').click()
    count = 6
    for i in range(2, 3):
        time.sleep(1)
        driver.find_element(By.XPATH,f'(//android.view.ViewGroup[@resource-id="com.heytap.market:id/name_label"])[{i}]').click()
        time.sleep(1)
        getShortComments(driver)
        driver.find_element(By.XPATH, '//android.widget.ImageButton[@content-desc="转到上一层级"]').click()
    # 关闭驱动
    driver.quit()
