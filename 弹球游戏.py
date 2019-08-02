import pygame
import sys
import traceback
import time
from pygame.locals import *
from random import *
from math import sqrt
'''
balls 渲染组 balls_active 活动组 group 碰撞组
'''

class SPEED(list):
    def __mul__(self,other):
        self[0] *= other
        self[1] *= other
        return self
    def __truediv__(self,other):
        self[0] /= other
        self[1] /= other
        return self
    
 
        
# 球类继承自Spirte类
class Ball(pygame.sprite.Sprite):
    def __init__(self, grayball_image, greenball_image, position, speed, bg_size, target):
        # 初始化动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.grayball_image = pygame.image.load(grayball_image).convert_alpha()
        self.greenball_image = pygame.image.load(greenball_image).convert_alpha()
        self.rect = self.grayball_image.get_rect()
        # 将小球放在指定位置
        self.rect.left, self.rect.top = position
        #self.side = [choice([-1, 1]), choice([-1, 1])]
        self.speed = speed
        #self.collide = False
        self.target = target
        self.control = False
        self.width, self.height = bg_size[0],bg_size[1]
        self.radius = self.rect.width / 2
        self.stop = False

    def move(self):
        '''if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.side[0] * self.speed[0], \
                                        self.side[1] * self.speed[1]))'''
        

        # 如果小球的左侧出了边界，那么将小球左侧的位置改为右侧的边界
        # 这样便实现了从左边进入，右边出来的效果
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed[0] *= -1

        elif self.rect.right >= self.width:
            self.rect.right = self.width
            self.speed[0] *= -1

        elif self.rect.top <= 0:
            self.rect.top = 0
            self.speed[1] *= -1

        elif self.rect.bottom >= self.height:
            self.rect.bottom = self.height
            self.speed[1] *= -1
        self.rect = self.rect.move(self.speed)
        
    def check(self, motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return False
            

class Glass(pygame.sprite.Sprite):
    def __init__(self, glass_image, mouse_image, bg_size):
        # 初始化动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left, self.glass_rect.top = \
                             (bg_size[0] - self.glass_rect.width) // 2, \
                             bg_size[1] - self.glass_rect.height

        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = \
                              self.glass_rect.left, self.glass_rect.top
        pygame.mouse.set_visible(False)
def Collide_check(b1,b2):
    distance = sqrt((b1.rect.center[0]-b2.rect.center[0])**2 + (b1.rect.center[1]-b2.rect.center[1])**2)
    if distance <= b1.radius*2:
        return True
    else:
        return False

        
def main():
    pygame.init()
    
    diff = 8 #镶嵌难度 0-10
    
    grayball_image = r"C:\Users\ietar1\Desktop\py\img\grayball.png"
    greenball_image = r"C:\Users\ietar1\Desktop\py\img\greenball.png"
    glass_image = r"C:\Users\ietar1\Desktop\py\img\glass.png"
    mouse_image = r"C:\Users\ietar1\Desktop\py\img\mouse1.png"
    bg_image = r"C:\Users\ietar1\Desktop\py\img\background.png"
    fail_image = r'C:\Users\ietar1\Desktop\py\img\fail.png'
    running = True

    # 添加魔性的背景音乐
    pygame.mixer.music.load(r"C:\Users\ietar1\Desktop\py\sound\Cricket.wav")
    pygame.mixer.music.play(loops=36)

    # 添加音效
    loser_sound = pygame.mixer.Sound(r"C:\Users\ietar1\Desktop\py\sound\joinme.wav")
    donesound = pygame.mixer.Sound(r"C:\Users\ietar1\Desktop\py\sound\done1.wav")
    winner_sound = pygame.mixer.Sound(r'C:\Users\ietar1\Desktop\py\sound\Won.ogg')
    button_sound = pygame.mixer.Sound(r"C:\Users\ietar1\Desktop\py\sound\button4.wav")

    # 音乐播放完时游戏结束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    # 根据背景图片指定游戏界面尺寸
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play a ball hiahiahia")

    background = pygame.image.load(bg_image).convert_alpha()

    # 5 个坑的范围，因为 100% 命中太难，所以只要在范围内即可
    # 每个元素：(x1, x2, y1, y2)
    hole = [(117, 119, 199, 201), (225, 227, 390, 392), \
            (503, 505, 320, 322), (698, 700, 192, 194), \
            (906, 908, 419, 421)]

    # 存放要打印的消息
    msgs = []
    fail = pygame.image.load(fail_image).convert_alpha()
    fail = pygame.transform.scale2x(fail)
    fail_pos = (width - fail.get_width()) // 2, \
                      (height - fail.get_height()) // 2

    # 用来存放小球对象的列表
    balls = []
    group = pygame.sprite.Group()
    controls =[0]

    # 创建 5 个小球
    for i in range(5):
        # 位置随机，速度随机
        position = randint(0, width-100), randint(0, height-100)
        speed = SPEED([randint(-10, 10), randint(-10, 10)])
        while speed[0] == 0 or speed[1]==0:
            speed = SPEED([randint(-10, 10), randint(-10, 10)])
        ball = Ball(grayball_image, greenball_image, position, speed, screen.get_size(), 5 * (i+1))
        # 检测新诞生的球是否会卡住其他球
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0, width-100), randint(0, height-100)
        balls.append(ball)
        group.add(ball)
    balls_active = balls[:]

    # 生成摩擦摩擦的玻璃面板
    glass = Glass(glass_image, mouse_image, bg_size)

    # motion 记录鼠标在玻璃面板产生的事件数量
    motion = 0
    ratio = 1.0
    out = 0

    # 1 秒检查 1 次鼠标摩擦摩擦产生的事件数量
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER, 1000)

    # 设置持续按下键盘的重复响应
    pygame.key.set_repeat(100, 100)

    clock = pygame.time.Clock()

    while running:
        # 坑都补完了，游戏结束
        if not group:
            pygame.mixer.music.stop()
            # 打印“然并卵”
            msg = pygame.image.load(r"C:\Users\ietar1\Desktop\py\img\win.png").convert_alpha()
            msg_pos = (width - msg.get_width()) // 2, \
                      (height - msg.get_height()) // 2
            screen.blit(msg,msg_pos)
            pygame.display.flip()
            pygame.time.delay(2500)
            winner_sound.play()
            running = False
            break
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 游戏失败
            elif event.type == GAMEOVER:
                screen.blit(fail,fail_pos)
                pygame.display.flip()
                loser_sound.play()
                running = False
                out = 1
                break
            

            # 1 秒检查 1 次鼠标摩擦摩擦产生的事件数量
            elif event.type == MYTIMER:
                if motion and controls[0] == 0:
                    for each in group:
                        if each.check(motion):#取得控制权
                            each.speed = SPEED([0, 0])
                            each.control = True
                            controls[0] += 1
                            
                    motion = 0

            elif event.type == MOUSEMOTION and controls[0] == 0:
                motion += 1

            # 当小球的 control 属性为 True 时
            # 可是使用按键 w、s、a、d 分别上、下、左、右移动小球
            # 带加速度的哦^_^
            elif event.type == KEYDOWN:
       
                if event.key == K_z:#test
                    print('controls[0]=',controls[0])

                
                if event.key == K_LEFTBRACKET and ratio <8:
                    ratio *= 2
                    print(ratio)
                    for i in balls:
                        i.speed *= ratio
                if event.key == K_RIGHTBRACKET and ratio > 1/8:
                    ratio /= 2
                    print(ratio)
                    for i in balls:
                        i.speed *= ratio        
                        
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1

                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1

                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1

                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1

                if event.key == K_c and controls[0] == 0:#cheating code
                    balls_active[0].control = True
                    controls[0] += 1
                    print('cheating code,group=',group)

                if event.key == K_SPACE:
                    # 判断小球是否在坑内
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0]-10+diff <= each.rect.left <= i[1]+10-diff and \
                                   i[2]-10+diff <= each.rect.top <= i[3]+10-diff:
                                    # 播放音效
                                    donesound.play()
                                    each.speed = SPEED([0, 0])
                                    #each.control = False
                                    controls[0] -= 1
                                    # 从 group 中移出，这样其他球就会忽视它
                                    group.remove(each)
                                    balls_active.remove(each)
                                    # 放到 balls 列表中的最前，也就是第一个绘制的球
                                    # 这样当球在坑里时，其它球会从它上边过去，而不是下边
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0, temp)
                                    # 一个坑一个球
                                    hole.remove(i)
                                    

        if out == 1:
            break    
        screen.blit(background, (0, 0))
        screen.blit(glass.glass_image, glass.glass_rect)

        # 限制鼠标只能在玻璃内摩擦摩擦
        glass.mouse_rect.left, glass.mouse_rect.top = pygame.mouse.get_pos()
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
        if glass.mouse_rect.left > glass.glass_rect.right - glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right - glass.mouse_rect.width
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height

        screen.blit(glass.mouse_image, glass.mouse_rect)

        for each in balls:#固定的不再移动
            each.move()
            '''
            if each.collide:
                each.speed = [randint(1, 10), randint(1, 10)]
                each.collide = False
                '''
            if each.control:
                screen.blit(each.greenball_image, each.rect)
            else:
                screen.blit(each.grayball_image, each.rect)

        '''for each in group:
            # 先从组中移出当前球
            group.remove(each)
            # 判断当前球与其他球是否相撞
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False
            # 将当前球添加回组中
            group.add(each)'''
        for each in group:
            group.remove(each)
            for b2 in group:
                if Collide_check(each,b2):
                    button_sound.play()
                    each.speed , b2.speed = b2.speed,each.speed
                    each.move()
                    b2.move()
                    if each.control == True:
                        each.control = False
                        controls[0] -= 1
                    if b2.control == True:
                        b2.control = False
                        controls[0] -= 1
            group.add(each)

        pygame.display.flip()
        clock.tick(30)
    print('main over')#test
    tempcount = 0
    while tempcount < 900:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_r:
                main()
        tempcount += 1

        pygame.display.flip()
        clock.tick(30)
    print('sleep over')#test
    pygame.quit()
    sys.exit()
    return    

    
if __name__ == "__main__":
    # 这样做的好处是双击打开时如果出现异常可以报告异常，而不是一闪而过！
    try:
        main()
          
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

'''
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size,RESIZABLE)
                background = pygame.transform.scale(background,event.size)
                glass.glass_rect.left, glass.glass_rect.top = \
                             (event.size[0] - glass.glass_rect.width) // 2, \
                             event.size[1] - glass.glass_rect.height

            #缩放的话还得继续调整洞的坐标 现有手段处理这个太没效率了 放弃'''



