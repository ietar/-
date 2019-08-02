import re,os
from urllib import request
from bs4 import BeautifulSoup
def open_url(url):
    req = request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36')
    page = request.urlopen(req)
    html = page.read()

    return html

def get_img(html):
    soup = BeautifulSoup(html.decode('utf-8'),features='lxml')
    for i in soup.find(class_='chartcontainer').find_all('img'):
        filename = i['src'].split('/')[-1]
        print(filename)#test
        with open(filename,'wb') as f:
            f.write(open_url(i['src']))
    return

def main():
    folder = '北京空气质量报告爬虫存图'
    try:
        os.mkdir(folder)
    except:
        print('文件夹已存在')
        pass
    os.chdir(folder)
    url = 'http://www.beijing-air.com/'
    get_img(open_url(url))
    return

if __name__ == '__main__':
    main()
    
