import easygui as g
import os


def codecount(file):
    count = 0
    try:
        with open (file, 'r', encoding='utf-8') as f:
            for i in f:
                if i:
                    count += 1
    except UnicodeDecodeError:
        try:
            with open (file, 'r', encoding='gb2312') as f:
                for i in f:
                    if i:
                        count += 1
        except UnicodeDecodeError:
            print('UnicodeDecodeError on file {}'.format(file))
            return -1
    return count

def main():    
    targets = {'.c':0, '.py':0, }
    errorcount = {'.c':0, '.py':0,}
    res = 0
    
    dir1 = g.diropenbox(msg=r'统计哪个目录下的代码量:')
    paths = os.walk(top = dir1)
    for dirpath,_,pathlist in paths:
        for path in pathlist:
            ext = os.path.splitext(path)[1]
            if  ext in targets:
                num = codecount(dirpath+os.sep+path)
                if num >= 0:
                    targets[ext] += 1
                    res += num
                else:
                    errorcount[ext] += 1
                
    restext = '共 {} 行\n'.format(res)
    for i in targets:
        restext += '{} 格式文件共 {} 个\n'.format(i,targets[i])
    restext += '\n\n解码错误文件数量:\n'
    for i in errorcount:
        restext += '{} 格式文件共 {} 个\n'.format(i,errorcount[i])
    g.msgbox(title='结果如下:', msg=restext)

if __name__ == '__main__':
    main()
            
        
