from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.geyanw.com"


# 获取主页主目录的名称和链接
def get_main_categories(base_url):
    """
    :param base_url: 主页面地址
    :return: 主页主目录的名称和链接
    """
    categories_list = []  # 定义一个空的列表存放，主类目
    res = requests.get(base_url)  # 通过requests获取响应后的结果（包含，网页内容，状态码，和url信息）
    html_doc = res.content  # 获取网页的源码
    soup = BeautifulSoup(html_doc, 'lxml')  # 创建一个BeautifulSoup对象，方便定位
    nav_li_list = soup.select("#nav > ul > li")  # 定位到id为nav下的url--li节点,选择出所有的li标签，返回列表
    for li in nav_li_list:
        link = base_url + li.a.get('href')  # 获取li标签的href 并且和base_url拼接
        text = li.get_text()  # 获取主目类的文本
        categories_list.append([text, link])  # 存放
    return categories_list[1:]  # 剔除第一个，


# 获取每个主目录下的所有单页面（获取存在的所有分页）地址
def get_subdirectorys_urls(url):
    """
    :param url: 二级目录页面的地址
    :return:所有分页地址
    """
    urls = []  # 分页1的网址为二级目录网址
    res = requests.get(url)
    html_doc = res.content
    soup = BeautifulSoup(html_doc, 'lxml')
    pages = soup.select('.pageinfo strong')[0].get_text()  # 获取分页的数量
    href = soup.select(".pagelist a")[0]['href']  # 获取到list_33_1.html
    num = href.split('_')[1]  # 截取到“list_33_1.html”中的33
    for page in range(1, int(pages) + 1):
        urls.append(url + 'list_' + num + '_' + str(page) + ".html")  # 拼接分页网址
    return urls


# 获取子页面中单个分页面的二级目录名称和链接
def get_subdirectorys(url):
    """
    :param url: 分页地址
    :return:详情页的名称，和地址
    """
    subdirectorys_list = []
    res = requests.get(url)
    html_doc = res.content
    soup = BeautifulSoup(html_doc, 'lxml')
    subdirectorys = soup.select(".newlist h2")  # 获取所有h2标签
    for sub in subdirectorys:
        subdirectory_text = sub.get_text()  # 获取所有h2标签下a标签的内容
        href = sub.a['href']  # 获取所有h2标签下a标签的href
        subdirectory_url = BASE_URL + href  # 拼接出详情页的地址
        subdirectorys_list.append([subdirectory_text, subdirectory_url])
    return subdirectorys_list


# 获取详情页的多条内容
def get_details(url):
    """
    :param url: 详情页的地址
    :return:详情页的文本内容
    """
    res = requests.get(url)
    html_doc = res.content
    soup = BeautifulSoup(html_doc, 'lxml')
    contents = soup.select('#p_left  p')  # 找到p节点
    contents_list = [contents[i].get_text() for i in range(len(contents)) if i % 2 == 0]  # 排除掉含有空格的p标签，并获取内容
    return contents_list


if __name__ == '__main__':
    from multiprocessing import Pool, Queue
    pool = Pool(processes=8)#开启有8个进程的进程池
    for main_url in get_main_categories(BASE_URL):
        print(main_url)  # 打印出主目录[名称，分页面首页地址]
        for url in pool.apply_async(get_subdirectorys_urls, (main_url[1],)).get():#进程非阻塞执行。并通过get的到结果
            print(url)  # 打印每个分页地址
            for subdirectory in get_subdirectorys(url):
                print(subdirectory)  # 打印出每个分页上面的二级目录的[名称，详情页地址地址】
                for content in get_details(subdirectory[1]):
                    print(content)  # 打印出详情页内容

        pool.close()
        pool.join()
