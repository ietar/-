import os
import easygui as g

def main():
    
    #遍历文件夹 找出指定格式文件
    # targettype = ['.py','.pyw','.txt']
    targettype = ['.py','.pyw']
    getdir = g.diropenbox()
    mode_strict =  g.ynbox(msg='是否严格检定(筛除注释行)?' ,default_choice='No')

    list1 = os.walk(getdir)
    dict1 ={}#统计各指定格式文件的数量
    dict2 ={}#统计行数

    for i in list1:#i是walk返回的块数 每个最深的walk是一块
        for i1 in i[2]:#i1是文件名 i[2]是文件名列表
            ext = os.path.splitext(i1)[-1]#取到文件扩展名
            if ext and ext in targettype:
                try:
                    dict1[ext] += 1
                except:
                    dict1[ext] = 1
                    #统计各类型文件数量
                path = i[0] + os.sep + i1
                with open(file=path,encoding='utf-8') as f:
                    count1=0
                    count2=0
                    try:
                        for i2 in f:#i2是文件中的一行 
                            i2=i2.strip()
                            def iscode(i2,f,ext,dict2):
                                nonlocal count1,count2
                                try:
                                    dict2[ext]
                                except:
                                    dict2[ext] = 0
                                if i2 == '':
                                    return
                                elif i2.startswith('#') and not count1 and not count2 :#不在引号中的#开头
                                    return


                                elif not count1:
                                    if i2.count("'''")%2:
                                        count1 = 1
                                    else:
                                        dict2[ext] += 1
                                        
                                elif count1:
                                    if i2.count("'''")%2:
                                        count1 = 0

                                elif not count2:
                                    if i2.count("'''")%2:
                                        count2 = 1
                                    else:
                                        dict2[ext] += 1
                                        
                                elif count2:
                                    if i2.count("'''")%2:
                                        count2 = 0   
                                        
    
                            if mode_strict == True:
                                iscode(i2,f,ext,dict2)#iscode()#测试完成！！
                            else:
                                try:
                                    dict2[ext]
                                except:
                                    dict2[ext] = 0
                                dict2[ext]+=1
                        
                    except:
                        print('尝试分析{}失败'.format(path))#test
                        pass
                                

    #已将目标格式文件遍历 并将对应格式及其数量存入dict1
    sumlines = 0
    t1=''
    for i in dict2:#dict2={'.py':xxx,'.txt':yyy}
        lines = dict2[i]
        sumlines += lines
        
        t1 +='【{}】格式文件共{}个,代码量{}行\n'.format(i,dict1[i],lines)
    summary = '各类型代码共{}行,完成进度{}%,离10万行还差{}'.format(\
            sumlines , sumlines/1000 , 100000-sumlines)
    g.textbox(msg= summary , text=t1)

    return

if __name__ == '__main__':
    main()
