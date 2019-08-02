import os

def video(d0):
    '''ignorelist = [r'$RECYCLE.BIN',r'Config.Msi']
    for i in ignorelist:#刺头就别管了 
        if i in d0:
            return'''
    try:    
        for i in os.listdir(d0):
            d1=d0+os.sep+i
            if os.path.isdir(d1):#是文件夹就打开    
                video(d1)
            else:#是文件就检测扩展名
                ext = os.path.splitext(i)[-1]
                if ext and ext in ['.avi','.mp4','.rmvb']:#有些无扩展名的倒霉文件
                    #print('i=',i)#test
                    print(d0+os.sep+i)
    except PermissionError:#刺头就别管了
        return

video(input('file:'))

