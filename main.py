# 这是一个示例 Python 脚本。
import json
import os
import time

import pandas as pd  # 存入csv文件
import requests  # 爬虫发送请求
from bs4 import BeautifulSoup as BS  # 爬虫解析页面


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def get_bilibili_danmu(v_url, url, v_result_file):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}

    print('视频地址是：', url)
    r1 = requests.get(url=v_url, headers=headers).json()
    str1 = str(r1['data'])
    json_str = str1.replace("'", '"')
    # cid = jsonpath(r1, '$..cid')
    r1data = json.loads(json_str)
    cid = r1data[0]['cid']  # 获取视频对应的cid号 保留cid= aid=的中间部分
    print('该视频的cid是:', cid)
    danmu_url = 'http://comment.bilibili.com/{}.xml'.format(cid)  # 弹幕地址
    print('弹幕地址是：', danmu_url)
    r2 = requests.get(danmu_url)
    html2 = r2.text.encode('raw_unicode_escape')
    soup = BS(html2, 'xml')
    danmu_list = soup.find_all('d')
    print('共爬取到{}条弹幕'.format(len(danmu_list)))
    video_url_list = []  # 视频地址
    danmu_url_list = []  # 弹幕地址
    time_list = []  # 弹幕时间
    text_list = []  # 弹幕内容
    for d in danmu_list:
        data_split = d['p'].split(',')  # 按逗号分隔
        temp_time = time.localtime(int(data_split[4]))  # 转换时间格式
        danmu_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time)
        video_url_list.append(url)
        danmu_url_list.append(danmu_url)
        time_list.append(danmu_time)
        text_list.append(d.text)
        print('{}:{}'.format(danmu_time, d.text))
    df = pd.DataFrame()
    df['视频地址'] = video_url_list
    df['弹幕地址'] = danmu_url_list
    df['弹幕时间'] = time_list
    df['弹幕内容'] = text_list
    if os.path.exists(v_result_file):  # 如果文件存在，不需写入字段标题
        header = None
    else:  # 如果文件不存在，说明是第一次新建文件，需写入字段标题
        header = ['视频地址', '弹幕地址', '弹幕时间', '弹幕内容']
    df.to_csv(v_result_file, encoding='utf_8_sig', mode='a+', index=False, header=header)  # 数据保存到csv文件


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print('开始')
    csv_file = '弹幕.csv'
    if os.path.exists(csv_file):  # 如果文件存在，不需写入字段标题
        print('{}已存在，删除文件'.format(csv_file))
        os.remove(csv_file)
    bv_list = ['BV14E411y7MW']
    # 开始爬取
    for bv in bv_list:
        try:
            get_bilibili_danmu('https://api.bilibili.com/x/player/pagelist?bvid={}'.format(bv) + '&jsonp=jsonp', 'https://www.bilibili.com/video/{}'.format(bv),
                               '弹幕.csv')
        except KeyboardInterrupt:
            print('KeyboardInterrupt! ')

    print('爬虫程序执行完毕! ')

    # 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
