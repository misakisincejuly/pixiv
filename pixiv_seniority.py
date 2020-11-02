import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import os


# pixiv爬取排行榜前50图片
class download_seniority:

    # 解析排行榜
    def list_resolve(self, url):
        list_url = []
        # 对排行榜链接进行解析
        headers = {"User-Agent": UserAgent().random}
        r = requests.get(url, headers=headers)
        html_doc = r.text
        elector = etree.HTML(html_doc)
        ranking_list = elector.xpath(".//div[@class='ranking-image-item']")
        # print(len(ranking_list))
        # 提取url、标签、和图片数
        for url in ranking_list:
            ranking_url = url.xpath(".//img/@data-src")[0]
            ranking_tag = url.xpath(".//img/@data-tags")[0]
            count = url.xpath(".//div[@class='page-count']/span/text()")

            ranking_url = ranking_url.replace("c/240x480/", "")
            # 处理多p图片
            if len(count) != 0:
                for i in range(1, int(count[0])):
                    dict = {}
                    url_temp = ranking_url
                    dict['url'] = ranking_url
                    dict['tag'] = ranking_tag
                    ranking_url = url_temp.replace("_p{0}".format(i-1), "_p{0}".format(i))
                    list_url.append(dict)
            else:
                dict = {}
                dict['url'] = ranking_url
                dict['tag'] = ranking_tag
                list_url.append(dict)
        return list_url

    # 创建文件夹
    def create_pixiv_dir(self, tag=None):
        # 主文件夹
        if not os.path.isdir('pixiv_download'):
            os.makedirs('pixiv_download')
        # 图片文件夹
        if not os.path.isdir('pixiv_download/Image'):
            os.makedirs('pixiv_download/Image')
        # 漫画文件夹
        if not os.path.isdir('pixiv_download/Cartoon'):
            os.makedirs('pixiv_download/Cartoon')

    # 创建文件查看是否重复
    def create_pixiv_file(self, name, byte_r):
        if not os.path.isfile(name):
            with open(name, "wb")as f:
                f.write(byte_r)

    # 下载图片
    def download(self, url):
        list_url = self.list_resolve(url)
        # 创建文件夹
        self.create_pixiv_dir()
        for item in list_url:
            headers = {"User-Agent": UserAgent().Random, 'Referer': item['url']}
            r = requests.get(item['url'], headers=headers)
            # 漫画下载
            if "漫画" in item['tag']:
                name = item['url'].split("/")[-1].split("_")[0].replace(".jpg", "")
                if not os.path.isdir('pixiv_download/Cartoon/{0}'.format(name)):
                    os.makedirs('pixiv_download/Cartoon/{0}'.format(name))
                self.create_pixiv_file(
                    "pixiv_download/Cartoon/{0}/{1}".format(name, item['url'].split("/")[-1]),
                    r.content)
                print("漫画下载成功")
                time.sleep(5)
                continue
            # 图片下载
            else:
                self.create_pixiv_file("pixiv_download/Image/{0}".format(item['url'].split("/")[-1]), r.content)
                print("图片下载成功")
                time.sleep(5)
f = download_seniority()
# url为排行榜链接地址。可更换周榜及其他
url = "https://www.pixiv.net/ranking.php"
try:
    f.download(url=url)
except:
    print("网络异常")

