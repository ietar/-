#2 不过可以重写下昨天那个 乌龟抓鱼
def t_catch_f():
    from random import randint
    #errorinfo =[]
    limitx1,limitx2,limity1,limity2,fishnum,apmax,apreg = 0,10,0,10,10,100,20
    mode = input('快速模式【无需输入】,自定义模式【1】：')
    
    
    
    def Setsize():
        nonlocal limitx1,limitx2,limity1,limity2,fishnum,apmax,apreg
        while 1:
            try:
                limitx1,limitx2 = int(input('输入池塘横轴尺寸(下界):')),int(input('输入池塘横轴尺寸(上界):'))
                limity1,limity2 = int(input('输入池塘纵轴尺寸(下界):')),int(input('输入池塘纵轴尺寸(上界):'))
                pass
            except:
                print('输入的不是整数,重新输入...')
                continue
            try:
                fishnum = int(input('请输入鱼的数量:'))
                pass
            except:
                print('鱼群数量输入错误')
                continue
            try:
                apmax = int(input('请输入乌龟最大体力:'))
                pass
            except:
                print('乌龟最大体力输入错误')
                continue
            try:
                apreg = int(input('请输入成功抓鱼恢复体力值:'))
                pass
            except:
                print('成功抓鱼恢复体力值输入错误')
                continue
            break
            
        if limitx1 > limitx2 :
            (limitx1,limitx2) = (limitx2,limitx1)
            print('上下界顺序错误,已将其互换')
        if limity1 > limity2 :
            (limity1,limity2) = (limity2,limity1)
            print('上下界顺序错误,已将其互换')
            
        print('自定义模式参数输入完成')
        #防呆设计zzzzz
        return
    
    if mode =='1':
        Setsize()
        
    assert limitx1 < limitx2#
    assert limity1 < limity2#
    class Turtle:
        def __init__(self):
            self.x = randint(limitx1,limitx2)
            self.y = randint(limity1,limity2)
            self.ap = apmax
        def move(self):
            self.step = randint(1,2)
            direction = Dire()
            self.x += self.step * direction[0]
            self.y += self.step * direction[1]
            #尝试移动
            if self.x > limitx2:
                self.x = 2*limitx2 - self.x
            if self.x < limitx1:
                self.x = -self.x + 2*limitx1
            assert self.x in range(limitx1,limitx2 + 1)#
            if self.y > limity2:
                self.y = 2*limity2 - self.y
            if self.y < limity1:
                self.y = -self.y + 2*limity1
            assert self.y in range(limity1,limity2 + 1)#
            #越界补正
            self.ap -= 1
        def catch(self):
            self.ap = self.ap + apreg if self.ap <= (apmax-apreg) else apmax

    class Fish:
        def __init__(self):
            self.x = randint(limitx1,limitx2)
            self.y = randint(limity1,limity2)
        def move(self):
            direction = Dire()
            self.x += direction[0]
            self.y += direction[1]
            #尝试移动
            if self.x > limitx2:
                self.x = 2*limitx2 - self.x
            if self.x < limitx1:
                self.x = -self.x + 2*limitx1
            assert self.x in range(limitx1,limitx2 + 1)#test
            #if self.x not in range(limitx1,limitx2 + 1):#test
                #print('x,limitx1,limitx2=({},{},{})'.format(self.x,limitx1,limitx2))#test
                #raise AssertionError#test
            if self.y > limity2:
                self.y = 2*limity2 - self.y
            if self.y < limity1:
                self.y = -self.y + 2*limity1
            assert self.y in range(limity1,limity2 + 1)#
            #越界补正
            
    def Dire():
        d1=[[-1,0],[1,0],[0,1],[0,-1]]
        return d1[randint(0,3)]
    
    turtle = Turtle()
    fish = []     
    for i in range(0,fishnum):
        afish = Fish()
        fish.append(afish)
    #创建1龟n鱼完成

        
    while 1:
        combo = 0
        try:
            fish[0]
            pass
        except IndexError:
            print('鱼全都抓完了,嗯?!')
            break
        if turtle.ap == 0:
            print('一共抓到【{}/{}】条鱼'.format(fishnum-len(fish),fishnum))
            print('乌龟体力用尽,睡觉去了zzzZZ')
            break
        turtle.move()
        for i in fish[:]:#迭代器中删除列表元素危险 原因尚未了解 用fish[:]或fish.copy()写法
            #乌龟先动 先判定是否被抓 之后鱼再动 被抓事件单写成函数 练习下闭包
            def Caught():
                nonlocal turtle,fish,combo
                if (i.x , i.y) == (turtle.x,turtle.y):
                    fish.remove(i)
                    turtle.catch()
                    print('1条倒霉小鱼被抓了T_T')
                    combo += 1
                return
            Caught()
            i.move()
        #每条鱼都移动完成了
        if combo > 1:
            print('nb啊 一次抓了【{}】条鱼！！'.format(combo))
    #主程序完成        
    a = input('输入【a】再来一局:')
    if a == 'a':
        t_catch_f()
    return
t_catch_f()

