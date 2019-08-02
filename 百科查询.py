from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import re

def main():
    keyword_r=input('请输入需要搜索的关键词:')
    keyword = parse.quote(keyword_r)
    url = ''.join(['https://baike.baidu.com/search/word?word=',keyword])
    res = request.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html,features='lxml')

    #如果没找到
    if soup.find(text=re.compile('抱歉，没有找到与')):
        print('没找到这个词条')
        return

    #词条名和副标题
    print(soup.h1.text,soup.h2.text,'\n')
    #尝试打印简介
    if soup.find(class_ = "para"):
        print(soup.find(class_ = "para").text)

    def polysemant():
        '''寻找义项并打印'''
        count = 0
        if soup.find(class_="polysemantList-wrapper cmn-clearfix"):#有多义词
            print(soup.find(class_="polysemantList-header-title").text[:-7])
            for i in soup.find(class_="polysemantList-wrapper cmn-clearfix").find_all(href=re.compile('view')):
                count += 1
                if count == 5:#现在义项没那么多了吧
                    count = 0
                    confirm = input('输入任意字符继续打印或输入q退出:')
                    if confirm == 'q':
                        break
                content = i.text

                '''地址由前半部分不用改的 和 结尾可能出现的中文 组成
                    找出中文字符 parse.quote改造之 然后接到原位置
                '''
                urlcn = i['href']
                if not urlcn.isascii():#判断用不用处理中文
                    for i1 in urlcn[::-1]:
                        if not ord(i1)<256:
                            urlcn = urlcn.replace(i1,parse.quote(i1))
                        else:#从后向前发现不是中文了
                            if urlcn.isascii():
                                break

                url_2 = ''.join(['http://baike.baidu.com',urlcn])
                res_2 = request.urlopen(url_2)
                soup2 = BeautifulSoup(res_2.read(),features='lxml')
                
                if soup2.h2:
                    content = ''.join([content,soup2.h2.text])
                print(content,'->',''.join(['http://baike.baidu.com',i['href']])) 
        else:
            print('百科没有认定其为多义词')
        return
    polysemant()
    print('\n以上为本词条及相关义项内容\n')
    return

while 1:
    main()
