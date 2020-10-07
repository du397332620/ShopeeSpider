import requests
import time
from fake_useragent import UserAgent
from urllib import parse
import csv

class XiaPi(object):
    def __init__(self):
        # self.ua = UserAgent()
        # self.url = 'https://shopee.co.th/api/v2/search_items/?by=relevancy&categoryids=13024&keyword=%E0%B8%AB%E0%B8%A1%E0%B9%89%E0%B8%AD%E0%B8%97%E0%B8%AD%E0%B8%94%E0%B9%84%E0%B8%9F%E0%B8%9F%E0%B9%89%E0%B8%B2&limit=50&newest={}&order=desc&page_type=search&skip_autocorrect=1&version=2'
        self.url = 'https://th.xiapibuy.com/api/v2/search_items/?by=relevancy&keyword={}&limit=50&newest={}&order=desc&page_type=search&price_max={}&price_min={}&rating_filter=1&skip_autocorrect=1&version=2'
        # self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}
        # self.url = 'https://xiapi.xiapibuy.com/api/v2/search_items/?by=pop&fe_categoryids=2561&limit=50&newest={}&order=desc&page_type=search&version=2'
        self.count = 0
    def one_html(self,url):
        ua = UserAgent()
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}
        proxies = {
            'http': 'http://t19555111313413:123456@tps186.kdlapi.com:15818',
            'https': 'https://t19555111313413:123456@tps186.kdlapi.com:15818'
        }
        for i in range(3):
            try:
                html = requests.get(url=url,headers=headers,proxies=proxies,timeout=50).json()
                # print(html)
                print('********************************',url)
                # print(html['items'])ผ้าห่ม
                for item in html['items']:
                    href = str(item['name']) + '-i.' + str(item['shopid']) + '.' + str(item['itemid'])
                    shangpin_link = 'https://xiapi.xiapibuy.com/' + href

                    master_map = 'https://cf.shopee.com.my/file/' + item['image']
                    name = item['name']
                    print(shangpin_link)
                    print(master_map)
                    self.count+=1
                    print("**********",self.count)
                    with open('shopee.csv','a',newline='',encoding='utf8') as f:
                        csv_writer = csv.writer(f)
                        csv_writer.writerow((self.count,name))
                        f.close()
                    # with open('name.txt','a',encoding='utf8') as f:
                    #     f.write(name + '\n')
                    # tow_url = 'https://xiapi.xiapibuy.com/api/v2/item/get?itemid={}&shopid={}'.format(item['itemid'],item['shopid'])
                    # try:
                    #     self.two_html(tow_url)
                    #     self.count += 1
                    #     print("**********",self.count)
                    #     time.sleep(1)
                    # except:
                    #     print('下一条')
                # self.count +=50
                break
            except Exception as e:

                print('连接超时 重试',e)
                continue

    def two_html(self,url):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        data = requests.get(url=url,headers=headers,timeout=8).json()
        price = str(data['item']['price_min'])[:-5]
        print(price)
        print(data['image'])
    def run(self):
        start = time.time()
        word = input("爬取的名称：")
        min_price = input('最低价:')
        max_price = input('最高价:')
        page = int(input("输入页数:"))
        word = parse.quote(word)
        # print(word)
        for i in range(0,page*50,50):
            url = self.url.format(word,i,max_price,min_price)
            self.one_html(url)
            time.sleep(5)
        end = time.time()
        spend = end-start
        minutes = int(spend // 60)
        second = int(spend % 60)
        print('程序运行时间为{}分{}秒'.format(minutes,second))
        print(self.count)
if __name__ == '__main__':
    xiapi = XiaPi()
    xiapi.run()
