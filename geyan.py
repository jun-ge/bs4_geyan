from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.geyanw.com"

#获取主类目的名称和链接
def get_main_categories(base_url):
    categories_list = []#定义一个空的列表存放，主类目
    res = requests.get(base_url)#通过requests获取响应后的结果（包含，网页内容，状态码，和url信息）
    html_doc = res.content#获取网页的源码
    soup = BeautifulSoup(html_doc, 'lxml')#创建一个BeautifulSoup对象，方便定位
    nav_li_list = soup.select("#nav > ul > li")#定位到id为nav下的url--li节点,选择出所有的li标签，返回列表
    for li in nav_li_list:
        link = base_url + li.a.get('href')#获取li标签的href 并且和base_url拼接
        text = li.get_text()#获取主目类的文本
        categories_list.append([text, link])#存放
    return categories_list[1:]#剔除第一个，



if __name__ == '__main__':
    for cate in get_main_categories(BASE_URL):
        print(cate)#打印出所有类目的名称和网址
