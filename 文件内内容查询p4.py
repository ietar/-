#0
import os
def countf():
    list1 = os.listdir(os.curdir)
    dic1={}
    for i in list1:
        if os.path.isdir(i):
            dic1.setdefault('文件夹',0)
            dic1['文件夹'] += 1
        else:
            ext = os.path.splitext(i)[1]
            dic1.setdefault(ext,0)
            dic1[ext] += 1
    for i in dic1.keys():
        print('该文件夹下共有类型为【{}】的文件 {} 个'.format(i,dic1[i]))
#countf()

#1
def p1():
    list1 = os.listdir(os.curdir)
    for i in list1:
        if os.path.isfile(i):
            size=os.path.getsize(i)
            print(i,'【{} Bytes】'.format(size))
        else:
            list1.remove(i)
    return
#p1()

#2
def p2():
    targetfile = input('请输入需要查找的目标文件:')
    inidir = input('请输入待查找的初始目录:')
    def p2_1(tar,dir0):
        for i in os.listdir(dir0):
            if os.path.isfile(i) and i == tar:#是文件且同名 找到啦！
                print(dir0)
            if os.path.isdir(i):#是文件夹就打开
                dir0=dir0 + os.sep + i
                p2_1(tar,dir0)
    return p2_1(targetfile,inidir)
#p2()

#3
def p3():#查找.mp4 .rmvb .avi格式文件
    dir0 = input('请输入待查找的初始目录:')
    while not os.path.isdir(dir0):
        dir0 = input('输入的不是目录，重新输入:')
    def p3_1(d0):
        targetype = ['.mp4','.rmvb','.avi']
        for i in os.listdir(d0):
            if os.path.isdir(i):#是文件夹
                return p3_1(d0 + os.sep +i)
            else:#是个文件
                if os.path.splitext (i)[1].lower() in targetype:#扩展名匹配上了
                    print(d0 + os.sep + i) 
    return p3_1(dir0)
#p3()
#这个查找速度和系统的查找比 效率如何

#4
def pos_in_line(line,key):
    pos = []
    beg = line.find(key)
    while beg != -1:
        pos.append(beg+1)
        beg = line.find(key,beg+1)
    return pos

def p4():
    key = input('请将该脚本放于待查找的文件夹内,请输入关键字:')
    
    sp = input('请问是否需要打印关键字【{}】在文件中的具体\
位置(YES/NO):'.format(key))
    while sp.lower() not in('yes','no'):
        sp = input('输入错误，请重新选择(YES/NO):')
    os.chdir(r'C:\Users\ietar1\Desktop\py')
    f1 = os.walk(os.getcwd())
    svdir = []

    for i in f1:
        for i1 in i[2]:
            if os.path.splitext(i1)[1] == '.py':
            #if os.path.splitext(i1)[1] == '.txt':
                i1 = os.path.join(i[0],i1)
                svdir.append(i1)
    #.txt格式文件路径已存入svdir列表
    for i in svdir:
        f = open(i,encoding='utf-8',errors='ignore')
        count = 0 #记录行数
        dict1 ={}
        for i1 in f:
            count += 1
            if key in i1:
                pos = pos_in_line(i1,key)
                dict1[count] = pos
        #记录xx行key出现的各个位置x1,x2,x3... 存入dict1{xx:[x1,x2,x3...]}
        f.close()
        if dict1:
            print(''.center(60,'='))
            print('在文件【{}】中找到关键字【{}】'.format(i,key))
            if sp.upper()== 'YES':
                keys = dict1.keys()
                keys = sorted(keys)
                for i1 in keys:
                    print('关键字出现在第{}行，第{}个位置'.format(i1,dict1[i1]))
    return
#p4()
    






                


