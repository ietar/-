# 爬取妹子图
import requests
from bs4 import BeautifulSoup
import time
# 得到每个页面的链接
def get_url():
    for i in range(1,51):
        url = 'http://www.mzitu.com/116519/' + str(i)  #基本上这个图片网站都可以以这种形式下载，所有是半自动，图片的网址你需要自己输入，就看你喜欢哪种类型
        yield url
# 得到妹子图片的链接
def get_girl_url(url_list):
    for url in url_list:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
                   'Referer': 'http://wwww.mzitu.com'}
        res = requests.get(url,headers=headers)
        html = res.text
        soup = BeautifulSoup(html,'lxml')
        img_url = soup.find(class_='main-image').find('img').get('src')
        yield img_url
# 存储妹子图片到本地
def save_img(img_url_list):
    for img_url in img_url_list:
        Picreferer = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
                      'Referer':'http://i.meizitu.net'}  #加Referer属性是防止盗链图的产生，目的是告诉服务器当前请求是从哪个页面请求过来的
        res = requests.get(img_url,headers=Picreferer)
        html = res.content
        filename =  'MM/' + img_url.split('/')[-1] #这里保存文件路径请依据自己的电脑位置来存放
        with open(filename,'wb') as f:
            f.write(html)

list1 = get_url()
print('list1=',list1)#test
list2 = get_girl_url(list1)
save_img(list2)
