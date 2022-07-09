from time import sleep
import re
import requests
import csv
from bs4 import BeautifulSoup

url = 'https://travel.qunar.com/p-cs300133-wuhan-jingdian-3-'
begin = 1
end = 10
sleep_time = 2
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_web_data(i):
    web_data = requests.get(url+str(i), headers=headers)
    if web_data.status_code != 200:
        print('访问错误')
    re_web_data = BeautifulSoup(web_data.text, 'lxml')
    # file = open('web.html', 'w', encoding='utf-8')
    # file.write(re_web_data.prettify())
    # file.close()
    return re_web_data


def get_palce_info(web_data):
    extract_name = web_data.find_all(name='span', class_='cn_tit')
    place_name = re.findall('.*?class=\"cn_tit\">\s*(.*?)\s*<.*?class=\"en_tit\">\s*(.*?)\s*</span>', str(extract_name), re.S)
    # 匹配景点名称

    extract_rank = web_data.find_all(name='span', class_='ranking_sum')
    # print(extract_rank)
    place_rank = []
    for rank in extract_rank:
        res = re.findall('<span.*?ranking_sum\">.*?<span class=\"sum\">\s*(.*?)\s*</span>', str(rank), re.S)
        if res == []:
            res = ['没有排名']
        place_rank.append(res[0])
    # 匹配景点排名

    extract_detail = web_data.find_all(name='div', class_='desbox')
    place_detail = re.findall('<div class=\"desbox\">\s*(.*?)\s*</div>', str(extract_detail), re.S)
    # 匹配景点介绍

    # get_img = web_data.find_all(name='img', class_='img')
    # img_url = re.findall('<img align=\"absmiddle\".*?src=\"(.*?)\".*?/>', str(get_img), re.S)
    # 获取景点图片链接

    target_url = web_data.find_all(name='a', class_='titlink')
    get_url = re.findall('<a.*?data-beacon=\"poi\".*?href=\"(.*?)\" target="_blank\"', str(target_url), re.S)

    file = open('place_detail_url.csv', 'a+', encoding='utf-8', newline='')
    file_csv = csv.writer(file)
    file_csv.writerow(get_url)
    file.close()
    # 获取景点详情链接

    info = []
    i = 0
    for name in place_name:
        info.append([])
        for count in range(0, 1):
            info[i].append(name[0])
            info[i].append(name[1])
        i = i+1
    # 生成景点名称列表

    ranklist = []  # 排名列表
    for rank in place_rank:
        ranklist.append(rank)

    detaillist = []  # 评价列表
    for detail in place_detail:
        detaillist.append(detail)


    for j in range(0, i):
        info[j].append(ranklist[j])
        info[j].append(detaillist[j])
    # 生成景点信息列表

    wite_csv(info)

def wite_csv(list):
    file = open('place_info_new.csv', 'a+', encoding='utf-8', newline='')
    file_csv = csv.writer(file)
    for i in list:
        file_csv.writerow(i)
    file.close()



########
#主程序#
#######
def main():
    file = open('place_info_new.csv', 'w', encoding='utf-8', newline='')
    file_csv = csv.writer(file)
    file_csv.writerow(['景点中文名', '景点英文名', '排名', '简述'])
    file.close()
    for i in range(begin, end+1):
        web_data = get_web_data(i)
        # file = open('web.html', 'r', encoding='utf-8')
        # web_data = BeautifulSoup(file.read(), 'lxml')
        # 获取网页代码
        get_palce_info(web_data)
        sleep(sleep_time)
        # print('已完成第'+str(i)+'页内容...')

    
main()