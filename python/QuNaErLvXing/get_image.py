from asyncore import file_dispatcher
from time import sleep
import re
from pygame import HWACCEL
import requests
import csv
from bs4 import BeautifulSoup
import os


url_list = []
counts = 0
path = 'D:/Work/spider/python/place_info_detail/'
sleep_time = 3
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

def setup():
    file = open('place_detail_url.csv', 'r', encoding='utf-8')
    file_csv = csv.reader(file)
    for i in file_csv:
        for j in i:
            url_list.append(j)
    file.close()
    global counts
    counts = len(url_list)
    # 获取景点链接列表


def web_data(url): 
    # 访问链接
    web_data = requests.get(url, headers=headers)
    if web_data.status_code != 200:
        print('访问错误')
    re_web_data = BeautifulSoup(web_data.text, 'lxml')
    return re_web_data



def get_data(data, i):
    # 获取网页数据

    # file = open('web_detail.html', 'r', encoding='utf-8')
    # web_data = BeautifulSoup(file.read(), 'lxml')
    # file.close()
    web_data = BeautifulSoup(data, 'lxml')

    li_item = web_data.find_all(name='li', class_='imgbox')
    img_url = re.findall('<img.*?src=\"(.*?)\"/>', str(li_item), re.S)
    # 获取景点图片链接

    p_item = web_data.find_all(name='p', class_='inset-p')
    detail = re.findall('<p.*?>\s*(.*?)\s*</p>', str(p_item), re.S)
    # 获取景点简介

    td_item = web_data.find_all(name='td', class_='td_l')
    address = re.findall('<dt>.*?地址.*?<span>\s*(.*?)\s*</span>', str(td_item), re.S)
    # 获取景点地址

    write_file(img_url, detail, address, i)



def write_file(img_url, detail, address, i):
    # 数据写入文件
    file = open(path+str(i)+'detail.txt', 'w',encoding='utf-8')
    for p in detail:
        file.write(p)
    file.write(address[0])
    file.close()
    # 写入txt文件

    for q, url in img_url:
        file_img = open(path+str(i)+str(q)+'jpg', 'w')
        img = requests.get(url, headers=headers)
        file_img.write(img.content)
        file_img.close()
    # 下载图片


########
#主程序#
#######
def main():
    setup()
    for i in range(1, counts+1):
        os.mkdir(path+str(i))
        webdata = web_data(url_list[i-1])
        get_data(webdata, i)
        sleep(sleep_time)
        print('已完成第'+str(i)+'页内容...')

main()