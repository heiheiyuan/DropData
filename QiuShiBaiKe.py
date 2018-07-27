import requests
import json
from lxml import etree


def get_content_list(html_str):
    html = etree.HTML(html_str)
    div_list = html.xpath("//div[@id='content-left']/div")
    content_list = []
    for div in div_list:
        item = {"img": "https:" + div.xpath(".//img/@src")[0] if len(div.xpath(".//img/@src")) > 0 else None,
                "name": div.xpath(".//h2/text()")[0].strip(),
                "age": div.xpath(".//div[@class='author clearfix']/div/text()")[0]
                if len(div.xpath(".//div[@class='author clearfix']/div/text()")) > 0 else None,
                "content": div.xpath(".//div[@class='content']/span/text()")[0].strip()
                if len(div.xpath(".//div[@class='content']/span/text()")) > 0 else None,
                "stats-vote": div.xpath(".//span[@class='stats-vote']/i/text()")[0],
                "stats-comments": div.xpath(".//span[@class='stats-comments']//i/text()")[0]
                if len(div.xpath("//span[@class='stats-comments']//i/text()")) > 0 else None}
        content_list.append(item)
    return content_list


class QiuBaiSpider:

    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like "
                                      "Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        self.file_path = "qiushibaike.txt"

    def run(self):
        # 获取url列表
        urls = self.get_url_list()
        print("获取到的url列表为%s" % urls)
        # 获取数据
        for url in urls:
            html_str = self.get_data(url)
            # 提取数据
            data = get_content_list(html_str)
            # 保存数据
            self.save_data(data)
        print("保存完成")

    def get_url_list(self):
        """
        获取url列表
        :return: url列表
        """
        return [self.start_url.format(i) for i in range(1, 14)]

    def get_data(self, url):
        """
        获取页面数据
        :param url: 网页地址
        :return: 数据
        """
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def save_data(self, data, encoding="UTF-8"):
        """
        保存数据到本地文件
        :param data: 数据
        :param encoding: 编码格式
        """
        with open(self.file_path, "a", encoding=encoding) as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False))
                f.write("\n")


if __name__ == '__main__':
    qiubai = QiuBaiSpider()
    qiubai.run()
