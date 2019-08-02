import urllib.request

print("""-------------这个是一个只能保存图片的爬虫------------""")

s = int(input('请输入下载次数:'))

for i in range(s):
    url=str(input('请输入网址:'))
    flie=str(input('文件名:'))
    try:
        response = urllib.request.urlopen(url)
        img=response.read()

        with open(flie,'wb') as f:
            f.write(img)
    except URLExit:
        print('出错啦~~~,无法处理本网站')
        input()
    except:
        print('出错啦~~~,网址输入不正确')
        input()

