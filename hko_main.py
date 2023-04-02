import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

from constant import *


# 获取指定路径页面内容字节流
def get_response_bytes(url='', uri='') -> bytes:
    return requests.get(url + uri).content


# 获取指定路径页面内容字符串
def get_response_text(url='', uri='') -> str:
    return requests.get(url + uri).text


# 获取BeautifulSoup
def get_soup(cont: bytes) -> BeautifulSoup:
    return BeautifulSoup(cont, 'html.parser')


# 获取当前路径
def get_current_loc() -> str:
    return os.path.dirname(os.path.abspath(__file__))


# 创建文件夹
def creat_dir(basedir: str, cdir: str) -> str:
    full_dir = basedir + "\\" + cdir
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)
    return full_dir


# 获取图片
def get_img_and_write(html: str, base_url='', reg=''):
    # 匹配图片链接的正则表达式
    reg = re.compile(reg)  #
    opp_link = reg.findall(html)  # 在html文档中查找所有的图片链接

    # 去掉相对路径前缀并拼接绝对路径
    abs_link = []
    for surl in opp_link:
        abs_link.append(base_url + surl[12:])

    write_image(abs_link)


# 保存图片
def write_image(abs_link):
    # 逐个获取图片并保存
    for img in abs_link:
        names = img.split('/')[-1]
        dir_name = names.split('_')[0]
        img_strs = requests.get(img)
        with open(creat_dir(get_current_loc(), dir_name) + '\\' + names, 'wb') as f:
            f.write(img_strs.content)  # 将图片写入文件


# 爬取1到12月的所有图片并保存
def crawl_all_images():
    for month in range(1, 13):
        crawl_images(month)


# 爬取单月图片并保存
def crawl_images(month):
    t_uri = trans_month(month)
    get_img_and_write(get_response_text(url, t_uri), root_url, regulars)


# 对齐长度
def trans_month(month) -> str:
    t_uri = ''
    if month < 10:
        t_uri = '0' + str(month) + '.htm'
    else:
        t_uri = str(month) + '.htm'
    return t_uri


# 爬取1到12月的所有表格
def crawl_all_tables():
    for month in range(1, 13):
        crawl_tables(month)


# 爬取单月的表格
def crawl_tables(month):
    tables = get_soup(get_response_bytes(url, trans_month(month))).findAll('tbody')
    content = get_table_lines(tables)

    max_len = get_max_len(content)
    # 不显示观测地点，对齐最后一行
    for elem in content:
        while len(content[elem]) == max_len:
            content[elem].pop()
    trans_to_chinese_head(content, month)


# 获取表格里的列内容
def get_table_lines(tables):
    content = {}
    for th in table_h1:
        line = []
        for con in tables[0].findAllNext(headers=th):
            line.append(con.get_text())
        content[th] = line
    for th in table_h2:
        line = []
        for con in tables[1].findAllNext(headers=th):
            line.append(con.get_text())
        content[th] = line
    return content


# 转换汉字表头并保存
def trans_to_chinese_head(content, month):
    for elem in content:
        if [elem in table_header]:
            table_header[elem] = content[elem]
    write_to_csv(table_header, creat_dir(get_current_loc(), 'csv_files') + '\\' + trans_month(month) + '.csv')


def get_max_len(content) -> int:
    max_len = 0
    for i in content:
        max_len = max(len(content[i]), max_len)
    return max_len


# 将表格内容写到csv中
def write_to_csv(write_content={}, write_to_file='./weather.csv'):
    weather = pd.DataFrame(write_content)
    weather.to_csv(write_to_file)


if __name__ == '__main__':
    # 获取1到12月的所有表格数据并保存
    crawl_all_tables()
    # 获取所有十月份的天气表格
    # crawl_tables(10)
    # 想获取1到12月的所有图片并保存就取消下面的注释
    # crawl_all_images()
