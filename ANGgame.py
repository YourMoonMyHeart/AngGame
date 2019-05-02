import pygame
from pygame.locals import *
from sys import exit
import math
import random

pygame.init()
#窗口大小
SCREEN_SIZE = (800,450)
screen_width, screen_height = SCREEN_SIZE
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
#标题
pygame.display.set_caption("还 没 想 好 名 字 （内测版）")
#字体
font = pygame.font.SysFont('simsunnsimsun',40)
font2 = pygame.font.SysFont('楷体',80)
#帧率控制
clock = pygame.time.Clock()
#背景
background_image_filename = 'pic/background.jpg'#'sushiplate.jpg'
background = pygame.image.load(background_image_filename).convert()
#图片
man_image = [pygame.image.load('pic/man-1.gif'),
             pygame.image.load('pic/man-2.gif')]
wood_image = pygame.image.load('pic/wood.png').convert()
top_image = pygame.image.load('pic/top.png').convert_alpha()
#读入上箭头
UP_img = pygame.image.load('pic/UP.png').convert_alpha()
#读入结束图
over_img = pygame.image.load('pic/gameover.png').convert_alpha()
again_img = [pygame.image.load('pic/playagain1.png').convert_alpha(),\
             pygame.image.load('pic/playagain2.png').convert_alpha()]
#读入音乐
music_backg = ['music/background0.ogg',
              'music/background1.ogg',
              'music/background2.ogg',
              'music/background3.ogg']

music_count = [pygame.mixer.Sound('music/count0.wav'),
                pygame.mixer.Sound('music/count1.wav'),
                pygame.mixer.Sound('music/count2.wav'),
                pygame.mixer.Sound('music/count3.wav'),
                pygame.mixer.Sound('music/count4.wav'),
                pygame.mixer.Sound('music/count5.wav'),
                pygame.mixer.Sound('music/count6.wav')]

music_count_20 = [pygame.mixer.Sound('music/count_20.ogg'),
                  pygame.mixer.Sound('music/count_21.wav'),
                  pygame.mixer.Sound('music/count_22.wav'),
                  pygame.mixer.Sound('music/count_23.wav'),
                  pygame.mixer.Sound('music/count_24.wav')]

music_collision = pygame.mixer.Sound('music/collision.wav')
music_collision.set_volume(0.4)
music_fall = pygame.mixer.Sound('music/fall.wav')
music_fall.set_volume(0.8)
music_end = pygame.mixer.Sound('music/end.ogg')
#重力加速度
g=800.0
class man:
    def __init__(self,Screen,image):
        self.x = 100
        self.y = int(screen_height/2)
        self.vx = 400
        self.vy = -420.0
        self.r = 15
        self.rl = 45
        self.rot = math.atan(self.vy/self.vx)
        self.screen = Screen
        self.image = image
        self.current_img = 1
        self.count = 0
        self.game = True
        #得分音乐数
        self.music_count_num = 0
    def fall_move(self,time):
        #先结束下落时的音乐
        music_fall.fadeout(200)
        self.vy = self.vy+g*time
        self.y += int(self.vy*time)
        self.rl = 45
        self.rot = math.atan(self.vy/self.vx)
    def rope_move(self,time):
        ox = int(self.x+self.y*math.tan(self.rot))
        if self.rl == 45:
            r = self.y/math.cos(self.rot)
            self.rl = int(r)
            #只播放一次
            music_fall.play()
        else:
            r = self.rl
        
        w = self.vx/math.cos(self.rot)/r
        
        dw = g/r*math.sin(self.rot)
        w += dw * time
        self.rot -= w * time

        self.vx = w*r*math.cos(self.rot)
        self.vy = w*r*math.sin(self.rot)
        
        self.y = int(r*math.cos(self.rot))
        #self.y += int(self.vy*time)
        
    def move(self,time):
        if event.type == KEYDOWN:
            if event.key == K_UP or\
                event.key == K_w:
                ball.rope_move(time)
                self.current_img = 1
                
                return
        self.fall_move(time)
        self.current_img = 0


class wood:
    def __init__(self,Screen,image,top_len=190,long=150):
        self.screen = Screen
        self.top_len = top_len-400
        self.long = long
        
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.bottom = top_len + long
        self.x = screen_width*4
    def move(self,time,man):
        self.x -= man.vx * time
            
 
        if self.x <= -self.width:
            self.x = screen_width + random.randint(0.5*screen_width,1.5*screen_width)
            self.top_len = random.randint(-self.height+0.1*screen_height,\
                                          0.9*screen_height-self.height-self.long)
            if self.long>126:#102#逐渐增加难度
                self.long -= 2#4--0.2版本难度，达到20分几乎不可能
                man.vx += 4#11#12
            self.bottom = self.top_len + self.height + self.long
            man.count += 1
            if man.count <20:
                music_count[man.music_count_num].play()
                man.music_count_num += 1
                if man.music_count_num == 7:
                    man.music_count_num = 0
            else:#开启高手模式音效
                music_count_20[random.randint(0,4)].play()
            
        if ball.y > screen_height+400 or not circletoline(man,self):
            #游戏结束前关闭音乐
            music_collision.play()
            pygame.mixer.music.fadeout(500)
            music_end.play()
            man.game = False
        else:
            man.game = True
        
def circletoline(man,wood):
    #调整显示位置左移r后
    man.x -= man.r
    if wood.x - man.x > man.r or\
       man.x - wood.x > man.r + wood.width or\
       (wood.bottom - man.y > man.r and\
       wood.bottom - wood.long < man.y-man.r):
        man.x += man.r
        return True
    else:
        man.x += man.r
        return False

def init():
    ball.__init__(screen,man_image)
    stone.__init__(screen,wood_image)
    x=0
    
    teach_1 = font2.render('Press UP :',True,(255,255,0))
    text_ready = font2.render('3',True,(255,255,0))
    screen.blit(background, (0,0))
    screen.blit(text_ready,(screen_width/2-40,screen_height/2-40))
    screen.blit(teach_1,(screen_width/2-200,screen_height/2+40))
    pygame.display.update()
    clock.tick(2)
    screen.blit(background, (0,0))
    screen.blit(text_ready,(screen_width/2-40,screen_height/2-40))
    screen.blit(teach_1,(screen_width/2-200,screen_height/2+40))
    screen.blit(UP_img,(screen_width/2+80,screen_height/2+20))
    pygame.display.update()
    clock.tick(2)
    
    text_ready = font2.render('2',True,(255,255,0))
    screen.blit(background, (0,0))
    screen.blit(text_ready,(screen_width/2-40,screen_height/2-40))
    screen.blit(teach_1,(screen_width/2-200,screen_height/2+40))
    pygame.display.update()
    clock.tick(2)
    screen.blit(background, (0,0))
    screen.blit(text_ready,(screen_width/2-40,screen_height/2-40))
    screen.blit(teach_1,(screen_width/2-200,screen_height/2+40))
    screen.blit(UP_img,(screen_width/2+80,screen_height/2+20))
    pygame.display.update()
    clock.tick(2)
    
    text_ready = font2.render('1',True,(255,255,0))
    screen.blit(background, (0,0))
    screen.blit(text_ready,(screen_width/2-40,screen_height/2-40))
    screen.blit(teach_1,(screen_width/2-200,screen_height/2+40))
    pygame.display.update()
    clock.tick(2)
    screen.blit(background, (0,0))
    screen.blit(text_ready,(screen_width/2-40,screen_height/2-40))
    screen.blit(teach_1,(screen_width/2-200,screen_height/2+40))
    screen.blit(UP_img,(screen_width/2+80,screen_height/2+20))
    pygame.display.update()
    clock.tick(2)
    #刚开始放平淡的背景音乐
    pygame.mixer.music.load(music_backg[random.randint(0,1)])
    pygame.mixer.music.play()
    

#初始化
ball = man(screen,man_image)
stone = wood(screen,wood_image)
x=0
#开启音乐结束标志----不好，会中断用户操作
#TRACK_END = USEREVENT + 1
#pygame.mixer.music.set_endevent(TRACK_END)
init()
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.music.stop()
            exit()
    if not ball.game:
        #wait for play again
        
        screen.blit(over_img,(screen_width/2-over_img.get_width()/2,\
                              screen_height/2-over_img.get_height()/2))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        again_x = screen_width/2-again_img[0].get_width()/2
        again_y = screen_height/2-again_img[0].get_height()/2+\
                  1.5*over_img.get_height()
        if mouse_x < again_x or\
           mouse_x > again_x+again_img[0].get_width() or\
           mouse_y < again_y or\
           mouse_y > again_y+again_img[0].get_height():
            num = 0
        else:
            num = 1
        screen.blit(again_img[num],(again_x,again_y))
        pygame.display.update()
        pressed_mouse = pygame.mouse.get_pressed()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                init()
                continue
        if pressed_mouse[0] and num:
            init()
        continue
    #播放节奏紧张的几首背景音乐
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(music_backg[random.randint(2,3)])
        pygame.mixer.music.play()
    
    
    time_passed = clock.tick(100)
    time_passed_seconds = time_passed / 1000.0

    x -= ball.vx*time_passed_seconds
    if x <= -screen_width:
        x=0
    if x > 0:
        x = -screen_width+1
    
    ball.move(time_passed_seconds)
    stone.move(time_passed_seconds,ball)
            
    for i in range(2):
        screen.blit(background, (x+i*screen_width,0))
    #画木头
    screen.blit(stone.image,(stone.x,stone.top_len))
    screen.blit(stone.image,(stone.x,stone.bottom))
    #写得分
    text_rl = font.render('得分: '+str(ball.count),True,(255,255,0))
    screen.blit(text_rl,(screen_width/2-80,0))
    #画蛛丝
    top_x = ball.x+ball.rl*math.sin(ball.rot)
    top_y = ball.y-ball.rl*math.cos(ball.rot)
    pygame.draw.line(screen,(255,255,255),\
                     (ball.x,ball.y),(top_x,top_y+top_image.get_height()),3)
    if ball.current_img:
        screen.blit(top_image,(top_x-top_image.get_width()/2,top_y))
    #画人，为了抓到绳子左移r
    screen.blit(pygame.transform.rotate(ball.image[ball.current_img],\
                                        30-ball.rot*180/math.pi)\
                ,(ball.x-2*ball.r,ball.y-ball.r))
    #pygame.draw.circle(screen,(100,0,200),(ball.x,ball.y),ball.r,0)
    
    
    pygame.display.flip()
