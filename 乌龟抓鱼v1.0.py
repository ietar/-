'''
0
多态性？

1
继承 原类Exception
class MyError(Exception):

2
指代对象自己

3
用那个骗自己的私有方式 属性/方法名之前加'__'

4
__init__方法吧

5
MyClass.myfun(MyClass) 即可
'''
#0
def ticket():
    class Ticket:
        def __init__(self,guest='a',day='a',num=1):#默认成人平日1人票
            self.price = 0
            self.guest = guest
            self.day = day
            self.num = num
        def setguest(self):#多余了 随便提供个接口
            a = input('请输入门票类型:成人【a】/儿童【b】:')
            while 1:
                if a.lower() in 'ab':
                    self.guest = a
                    break
                else:
                    a=input('输入错误,请输入成人【a】/儿童【b】:')
        def setday(self):#多余了 随便提供个接口
            a = input('请输入门票类型:平时【a】/周末【b】:')
            while 1:
                if a.lower() in 'ab':
                    self.guest = a
                    break
                else:
                    a=input('输入错误,请输入平时【a】/周末【b】:')
        def calprice(self):
            self.price = 100 if self.guest == 'a' else 50
            if self.day == 'b':
                self.price *= 1.2
            return self.price*self.num
    t1=Ticket(num=2)
    t2=Ticket(guest='b')
    print('2个成人+1个小孩平日票价为 {} 元'.format(t1.calprice()+t2.calprice()))
#ticket()

#1
from random import *
def Turtle_catch_fish():
    class Turtle:#1 turtle
        def __init__(self):
            self.ap=100
            self.x=randint(0,10)
            self.y=randint(0,10)
            
        def move(self):
            step = randint(1,2)
            d = Dire()
            self.x += step*d[0]
            self.y += step*d[1]
            #尝试移动
            if self.x < 0:
                self.x = -self.x
            if self.x > 10:
                self.x = 20-self.x
            if self.y < 0:
                self.y = -self.y
            if self.y > 10:
                self.y = 20-self.y
            #越界补正
            self.ap -= 1
            return self.x,self.y

        def catch(self):
            self.ap += 20
            if self.ap > 100:
                self.ap = 100

        
    class Fish:#10 fishes
        def __init__(self):
            self.x=randint(0,10)
            self.y=randint(0,10)

        def move(self):
            d = Dire()
            self.x += d[0]
            self.y += d[1]
            #尝试移动
            if self.x < 0:
                self.x = -self.x
            if self.x > 10:
                self.x = 20-self.x
            if self.y < 0:
                self.y = -self.y
            if self.y > 10:
                self.y = 20-self.y
            #越界补正
            return self.x,self.y

                
    def Dire():
        a=randint(0,3)
        if a == 0:
            direction = [1,0]
        if a == 1:
            direction = [-1,0]
        if a == 2:
            direction = [0,1]
        if a == 3:
            direction = [0,-1]
        #随机生成移动方向
        return direction
    

    turtle = Turtle()
    fish = []
    for i in range(0,10):
        fish_n = Fish()
        fish.append(fish_n)
    #创建1龟10鱼

    fishleft = 10
    while 1:
        if not len(fish):
            print('鱼都没啦,over')
            break
        if not turtle.ap:
            print('还剩【{}】条,乌龟没体力累死啦,over'.format(fishleft))
            break
        pos = turtle.move()
        combo = 0#存在一次抓到多条鱼的可能
        for i in fish.copy():#为什么不让在迭代器中删除列表元素?
            if i.move() == pos:#鱼也动动
                turtle.catch()
                fish.remove(i)
                print('抓到1条')
                fishleft -= 1
                combo += 1
        if combo > 1:
            print('nb啊 一次移动抓到{}条鱼！！'.format(combo))
    return
Turtle_catch_fish()
#真的不好抓 体力100太少了
#突然发现写了个[-10,10]的池子 那确实是不太好抓...
    
        

    
        
    
        
                
        
