import pygame
from pygame.locals import *
from sys import exit
from time import sleep


class Ying(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.dirt = True  # 默认朝右
        self.jump0 = 0
        self.health = 100
        self.healthflag = False  # 受伤标志。默认不受伤
        self.down = 3  # 跌倒计数
        self.energy = 100
        self.bisha = 0
        self.bishaf = 0
        self.densive = False

    def load(self, filename, width, height, columns, x, y):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(x, y, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=60):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, value):
        self.rect.topleft = value

    positon = property(_getpos, _setpos)


class Button:
    def __init__(self, filename, position):
        self.image = pygame.image.load(filename).convert()
        self.position = position

    def isOver(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.image.get_size()
        if point_x > x - w / 2 and point_x < x + w / 2:
            if point_y > y - h / 2 and point_y < y + h / 2:
                return True


class Bo(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.flag = 0
        self.width = 200
        self.height = 180

    def load(self, filename, position):
        self.image = pygame.image.load(filename).convert_alpha()
        a, b = position
        self.rect = Rect(a, b, 200, 180)
        self.rect = self.image.get_rect()
        self.rect.x = a
        self.rect.y = b


# def menu():    #设置窗口大小、显示背景图片
pygame.init()  # pygame初始化
my_font = pygame.font.SysFont("SimHei", 20)
my_font1 = pygame.font.SysFont("SimHei", 100)
texture1 = my_font.render("血值", True, (255, 253, 253), (0, 0, 0))
texture2 = my_font.render("灵气", True, (255, 253, 253), (0, 0, 0))
texture3 = my_font1.render("END!", True, (255, 253, 253), (0, 0, 0))
pygame.mixer.init()  # 音乐初始化
pygame.mixer.music.load("./source/Escape.mp3")
Screen_width = 1000
Screen_height = 500
screen = pygame.display.set_mode([Screen_width, Screen_height])
background = pygame.image.load("./source/界面.png").convert()
touxiang1 = pygame.image.load("./source/飞影1头像.png").convert()
touxiang2 = pygame.image.load("./source/飞影2头像.png").convert_alpha()
button = Button("./source/开始游戏.png", (127, 422))  # 菜单开始按钮
framerate = pygame.time.Clock()
T = 1
# 菜单界面显示
while T == 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and button.isOver():
            print("hello\n")
            T = 0
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play()
    screen.blit(background, (0, 0))
    screen.blit(button.image, button.position)
    pygame.display.update()
pygame.mixer.music.stop()
# 格斗界面显示
pygame.mixer.music.load("./source/魔强.mp3")
background = pygame.image.load("./source/背景.jpg").convert()
feiying1 = Ying(screen)
feiying2 = Ying(screen)
feiying2.dirt = False
bo = Bo(screen)
bo1 = Bo(screen)
feiying1.load("./source/飞影站立.png", 100, 180, 2, 5, 320)
feiying2.load("./source/飞影2向左站.png", 100, 180, 2, 900, 320)
feiying1.position = 0, 0
feiying2.position = 0, 0
group = pygame.sprite.Group()
group1 = pygame.sprite.Group()
group2 = pygame.sprite.Group()
group.add(feiying1)
group.add(feiying2)
end = 1
musicf = 1
while True:
    framerate.tick(5)
    ticks = pygame.time.get_ticks()
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 按下键盘
        if event.type == pygame.KEYDOWN:
            # 飞影1
            if not feiying1.healthflag:
                if feiying1.jump0 == 0:
                    if event.key == pygame.K_c:  # 飞影1向左站立
                        feiying1.load(
                            "./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y
                        )
                        feiying1.dirt = False
                    if event.key == pygame.K_v:  # 飞影1向右站立
                        feiying1.load(
                            "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                        )
                        feiying1.dirt = True
                    if event.key == pygame.K_z:  # 飞影1黑炎斩
                        if feiying1.energy > 40:
                            if feiying1.dirt:  # 右式
                                feiying1.load(
                                    "./source/飞影黑炎斩.png",
                                    200,
                                    180,
                                    10,
                                    feiying1.X,
                                    feiying1.Y,
                                )
                                if pygame.sprite.collide_rect(
                                    feiying1, feiying2
                                ):  # 飞影1用黑炎斩伤到飞影2
                                    feiying2.health -= 20
                                    feiying2.healthflag = True
                            if not feiying1.dirt:  # 左式
                                feiying1.load(
                                    "./source/飞影黑炎斩左.png",
                                    200,
                                    180,
                                    10,
                                    feiying1.X,
                                    feiying1.Y,
                                )
                                if pygame.sprite.collide_rect(
                                    feiying1, feiying2
                                ):  # 飞影1用黑炎斩伤到飞影2
                                    feiying2.health -= 20
                                    feiying2.healthflag = True
                            feiying1.energy -= 30
                    if event.key == pygame.K_x:
                        if feiying1.energy > 20:
                            if feiying1.dirt:
                                feiying1.load(
                                    "./source/飞影散影拳.png",
                                    200,
                                    180,
                                    5,
                                    feiying1.X,
                                    feiying1.Y,
                                )
                                feiying1.energy -= 20
                                if pygame.sprite.collide_rect(feiying1, feiying2):
                                    feiying2.health -= 20
                                    feiying2.healthflag = True
                    if event.key == pygame.K_f:  # 飞影1跳起
                        feiying1.jump0 = 4
                    if event.key == pygame.K_a:
                        if feiying1.energy > 70:
                            feiying1.bisha = 7
                            feiying1.energy -= 60
                    # feiying1.load('./source/飞影黑龙波.png',200,180,7,feiying1.X,feiying1.Y)

            # 飞影2
            if not feiying2.healthflag:
                if feiying2.jump0 == 0:
                    if event.key == pygame.K_LEFT:  # 飞影2向左站立
                        feiying2.load(
                            "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                        )
                        feiying2.dirt = False
                    if event.key == pygame.K_RIGHT:  # 飞影2向右站立
                        feiying2.load(
                            "./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y
                        )
                        feiying2.dirt = True
                    if event.key == pygame.K_o:  # 飞影2黑炎斩
                        if feiying2.energy > 40:
                            if feiying2.dirt:  # 右式
                                feiying2.load(
                                    "./source/飞影2黑炎斩.png",
                                    200,
                                    180,
                                    10,
                                    feiying2.X,
                                    feiying2.Y,
                                )
                                if pygame.sprite.collide_rect(
                                    feiying2, feiying1
                                ):  # 飞影2用黑炎斩伤到飞影1
                                    feiying1.health -= 20
                                    feiying1.healthflag = True
                            if not feiying2.dirt:  # 左式
                                feiying2.load(
                                    "./source/飞影2黑炎斩左.png",
                                    200,
                                    180,
                                    10,
                                    feiying2.X,
                                    feiying2.Y,
                                )
                                if pygame.sprite.collide_rect(
                                    feiying2, feiying1
                                ):  # 飞影2用黑炎斩伤到飞影1
                                    feiying1.health -= 20
                                    feiying1.healthflag = True
                            feiying2.energy -= 30
                    if event.key == pygame.K_UP:
                        feiying2.jump0 = 4
                    if event.key == pygame.K_k:
                        if feiying2.energy > 70:
                            feiying2.bisha = 7
                            feiying2.energy -= 60

        # 抬起键盘
        # 飞影1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_v:  # 飞影1向右站立
                feiying1.load("./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y)
                feiying1.dirt = True
            if event.key == pygame.K_c:  # 飞影1向左站立
                feiying1.load("./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y)
                feiying1.dirt = False
            if event.key == pygame.K_z:
                if feiying1.dirt:
                    feiying1.load(
                        "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
                if not feiying1.dirt:
                    feiying1.load(
                        "./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
                # feiying.load('./source/飞影黑炎斩.png',200,180,10,feiying.X,feiying.Y)

            # 飞影2
            if event.key == pygame.K_RIGHT:  # 飞影2向右站立
                feiying2.load("./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y)
                feiying2.dirt = True
            if event.key == pygame.K_LEFT:  # 飞影2向左站立
                feiying2.load(
                    "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                )
                feiying2.dirt = False
            if event.key == pygame.K_o:
                if feiying2.dirt:
                    feiying2.load(
                        "./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y
                    )
                if not feiying2.dirt:
                    feiying2.load(
                        "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                    )
            if event.key == pygame.K_d:
                feiying1.densive = False
            if event.key == pygame.K_p:
                feiying2.densive = False
            if event.key == pygame.K_x:
                if feiying1.dirt:
                    feiying1.load(
                        "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
        # 一直按着
    keys = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
        if keys[pygame.K_ESCAPE]:
            exit()
        # 飞影1
        print("value: ", keys[pygame.K_v])
        if keys[pygame.K_v]:  # 飞影1一直右跑
            print("right right\n")
            if not keys[pygame.K_c]:
                feiying1.load("./source/飞影右跑.png", 100, 180, 2, feiying1.X, feiying1.Y)
                if feiying1.X < Screen_width - 100:
                    feiying1.X += 32
        if keys[pygame.K_c]:  # 飞影1一直左跑
            if not keys[pygame.K_v]:
                feiying1.load("./source/飞影左跑.png", 100, 180, 2, feiying1.X, feiying1.Y)
                if feiying1.X > 5:
                    feiying1.X -= 32
        if keys[pygame.K_s]:  # 飞影1充灵气
            if feiying1.energy > 93:
                feiying1.energy = 100
            else:
                feiying1.energy += 5

        # 飞影2
        if keys[pygame.K_RIGHT]:  # 飞影一直右跑
            if not keys[pygame.K_LEFT]:
                feiying2.load("./source/飞影2右跑.png", 100, 180, 2, feiying2.X, feiying2.Y)
                if feiying2.X < Screen_width - 100:
                    feiying2.X += 32
        if keys[pygame.K_LEFT]:  # 飞影一直左跑
            if not keys[pygame.K_RIGHT]:
                feiying2.load("./source/飞影2左跑.png", 100, 180, 2, feiying2.X, feiying2.Y)
                if feiying2.X > 5:
                    feiying2.X -= 32
        if keys[pygame.K_j]:  # 飞影2充灵
            if feiying2.energy > 93:
                feiying2.energy = 100
            else:
                feiying2.energy += 5

        if keys[pygame.K_q]:
            feiying1.densive = True

        if keys[pygame.K_p]:
            feiying2.densive = True
    # 飞影之间碰撞时位置锁定##############################################
    if pygame.sprite.collide_rect(feiying1, feiying2):
        if abs(feiying1.rect.centerx - feiying2.rect.centerx) < 50:
            feiying1.X -= 32
            feiying2.X += 32
    #########################################################################
    # 飞影1炎杀黑龙波处理
    if feiying1.dirt:  # 黑龙波右式
        if feiying1.bisha > 0:
            feiying1.load("./source/飞影黑龙波.png", 200, 180, 7, feiying1.X, feiying1.Y)
            feiying1.bisha -= 1
            if feiying1.bisha == 0:
                feiying1.bishaf = 2
                feiying1.load("./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y)
        if feiying1.bishaf == 2:
            bo.load("./source/飞影黑龙波波.png", (feiying1.X + 80, feiying1.Y))
            group1.add(bo)
            feiying1.bishaf = 3
        if feiying1.bishaf == 3:
            bo.rect.x += 30
            if pygame.sprite.collide_rect(feiying2, bo):
                feiying2.healthflag = True
                if not feiying2.densive:
                    feiying2.health -= 50
                if feiying2.densive:
                    feiying2.health -= 10
                    feiying2.energy -= 30
                feiying1.bishaf = 0
                group1.remove(bo)
            if bo.rect.x > 800:
                feiying1.bishaf = 0
    if feiying1.dirt == False:  # 黑龙波左式
        if feiying1.bisha > 0:
            feiying1.load("./source/飞影左黑龙波新.png", 200, 180, 7, feiying1.X, feiying1.Y)
            feiying1.bisha -= 1
            if feiying1.bisha == 0:
                feiying1.bishaf = 2
                feiying1.load("./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y)
        if feiying1.bishaf == 2:
            bo.load("./source/飞影左黑龙波波.png", (feiying1.X - 200, feiying1.Y))
            group1.add(bo)
            feiying1.bishaf = 3
        if feiying1.bishaf == 3:
            bo.rect.x -= 30
            if pygame.sprite.collide_rect(feiying2, bo):
                feiying1.bishaf = 0
                group1.remove(bo)
                feiying2.healthflag = True
                if not feiying2.densive:
                    feiying2.health -= 50
                else:
                    feiying2.health -= 10
                    feiying2.energy -= 30
            if bo.rect.x < 5:
                feiying1.bishaf = 0

    # 飞影1跳动处理
    if feiying1.jump0 > 2:
        if feiying1.dirt:
            feiying1.load("./source/飞影右跳起.png", 100, 180, 2, feiying1.X, feiying1.Y)
            feiying1.Y -= 200
            feiying1.jump0 -= 1
        else:
            feiying1.load("./source/飞影左跳起.png", 100, 180, 2, feiying1.X, feiying1.Y)
            feiying1.Y -= 200
            feiying1.jump0 -= 1
    if feiying1.jump0 > 0 and feiying1.jump0 < 3:
        if feiying1.dirt:
            feiying1.load("./source/飞影右跳起.png", 100, 180, 2, feiying1.X, feiying1.Y)
            feiying1.Y += 200
            feiying1.jump0 -= 1
            if feiying1.jump0 == 0:
                feiying1.load("./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y)
        else:
            feiying1.load("./source/飞影左跳起.png", 100, 180, 2, feiying1.X, feiying1.Y)
            feiying1.Y += 200
            feiying1.jump0 -= 1
            if feiying1.jump0 == 0:
                feiying1.load("./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y)
    # 飞影2跳动处理
    if feiying2.jump0 > 2:
        if feiying2.dirt:
            feiying2.load("./source/飞影2右跳起.png", 100, 180, 2, feiying2.X, feiying2.Y)
            feiying2.Y -= 200
            feiying2.jump0 -= 1
        else:
            feiying2.load("./source/飞影2左跳起.png", 100, 180, 2, feiying2.X, feiying2.Y)
            feiying2.Y -= 200
            feiying2.jump0 -= 1
    if feiying2.jump0 > 0 and feiying2.jump0 < 3:
        if feiying2.dirt:
            feiying2.load("./source/飞影2右跳起.png", 100, 180, 2, feiying2.X, feiying2.Y)
            feiying2.Y += 200
            feiying2.jump0 -= 1
            if feiying2.jump0 == 0:
                feiying2.load("./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y)
        else:
            feiying2.load("./source/飞影2左跳起.png", 100, 180, 2, feiying2.X, feiying2.Y)
            feiying2.Y += 200
            feiying2.jump0 -= 1
            if feiying2.jump0 == 0:
                feiying2.load(
                    "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                )

    # 飞影2炎杀黑龙波处理
    if feiying2.dirt:  # 右式
        if feiying2.bisha > 0:
            feiying2.load("./source/飞影2黑龙波.png", 200, 180, 7, feiying2.X, feiying2.Y)
            feiying2.bisha -= 1
            if feiying2.bisha == 0:
                feiying2.bishaf = 2
                feiying2.load("./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y)
        if feiying2.bishaf == 2:
            bo1.load("./source/飞影2黑龙波波.png", (feiying2.X + 80, feiying2.Y))
            group2.add(bo1)
            feiying2.bishaf = 3
        if feiying2.bishaf == 3:
            bo1.rect.x += 30
            if pygame.sprite.collide_rect(feiying1, bo1):
                feiying2.bishaf = 0
                group2.remove(bo1)
                feiying1.healthflag = True
                if not feiying1.densive:
                    feiying1.health -= 50
                if feiying1.densive:
                    feiying1.health -= 10
                    feiying1.energy -= 30
            if bo1.rect.x > 800:
                feiying2.bishaf = 0
    if feiying2.dirt == False:  # 左式
        if feiying2.bisha > 0:
            feiying2.load("./source/飞影2左黑龙波新.png", 200, 180, 7, feiying2.X, feiying2.Y)
            feiying2.bisha -= 1
            if feiying2.bisha == 0:
                feiying2.bishaf = 2
                feiying2.load(
                    "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                )
        if feiying2.bishaf == 2:
            bo1.load("./source/飞影2左黑龙波波.png", (feiying2.X - 200, feiying2.Y))
            group2.add(bo1)
            feiying2.bishaf = 3
        if feiying2.bishaf == 3:
            bo1.rect.x -= 30
            if pygame.sprite.collide_rect(feiying1, bo1):
                feiying2.bishaf = 0
                group2.remove(bo1)
                feiying1.healthflag = True
                if not feiying1.densive:
                    feiying1.health -= 90
                else:
                    feiying1.health -= 10
                    feiying1.energy -= 30
            if bo1.rect.x < 5:
                feiying2.bishaf = 0

    # 灵气最低限制###########################################################################
    if feiying1.energy <= 0:
        feiying1.energy = 0
    if feiying2.energy <= 0:
        feiying2.energy = 0
    ############################################################################################
    # 两波相遇处理
    if pygame.sprite.Sprite.alive(bo) and pygame.sprite.Sprite.alive(bo1):
        if pygame.sprite.collide_rect(bo, bo1):
            feiying1.bishaf = 0
            feiying2.bishaf = 0
            group1.remove(bo)
            group2.remove(bo1)
    # 飞影倒下#####################################################################################
    # 飞影1倒下
    if feiying1.healthflag == True and (not feiying1.densive):
        if feiying1.dirt:
            if feiying1.X < feiying2.X:
                feiying1.load(
                    "./source/飞影左倒下.png", 300, 180, 3, feiying1.X - 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
            if feiying1.X > feiying2.X:
                feiying1.load(
                    "./source/飞影右倒下.png", 300, 180, 3, feiying1.X + 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
        if not feiying1.dirt:
            if feiying1.X < feiying2.X:
                feiying1.load(
                    "./source/飞影左倒下.png", 300, 180, 3, feiying1.X - 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
            if feiying1.X > feiying2.X:
                feiying1.load(
                    "./source/飞影右倒下.png", 300, 180, 3, feiying1.X + 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )

    if feiying1.healthflag == True and feiying1.densive:
        if feiying1.dirt:
            if feiying1.X < feiying2.X:
                feiying1.load("./source/飞影朝右防.png", 100, 180, 3, feiying1.X, feiying1.Y)
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
            if feiying1.X > feiying2.X:
                feiying1.load(
                    "./source/飞影右倒下.png", 300, 180, 3, feiying1.X + 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
        if not feiying1.dirt:
            if feiying1.X < feiying2.X:
                feiying1.load(
                    "./source/飞影左倒下.png", 300, 180, 3, feiying1.X - 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影站立.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )
            if feiying1.X > feiying2.X:
                feiying1.load(
                    "./source/飞影右倒下.png", 300, 180, 3, feiying1.X + 20, feiying1.Y
                )
                sleep(0.1)
                feiying1.down -= 1
                if feiying1.down == 0:
                    feiying1.healthflag = False
                    feiying1.down = 3
                    feiying1.load(
                        "./source/飞影向左站.png", 100, 180, 2, feiying1.X, feiying1.Y
                    )

    # 飞影2倒下
    if feiying2.healthflag == True:
        if feiying2.dirt:
            if feiying2.X > feiying1.X:
                feiying2.load(
                    "./source/飞影2右倒下.png", 300, 180, 3, feiying2.X + 20, feiying2.Y
                )
                sleep(0.1)
                feiying2.down -= 1
                if feiying2.down == 0:
                    feiying2.healthflag = False
                    feiying2.down = 3
                    feiying2.load(
                        "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                    )
            if feiying2.X < feiying1.X:
                feiying2.load(
                    "./source/飞影2左倒下.png", 300, 180, 3, feiying2.X - 20, feiying2.Y
                )
                sleep(0.1)
                feiying2.down -= 1
                if feiying2.down == 0:
                    feiying2.healthflag = False
                    feiying2.down = 3
                    feiying2.load(
                        "./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y
                    )

        if not feiying2.dirt:
            if feiying2.X > feiying1.X:
                feiying2.load(
                    "./source/飞影2右倒下.png", 300, 180, 3, feiying2.X + 20, feiying2.Y
                )
                sleep(0.1)
                feiying2.down -= 1
                if feiying2.down == 0:
                    feiying2.healthflag = False
                    feiying2.down = 3
                    feiying2.load(
                        "./source/飞影2向左站.png", 100, 180, 2, feiying2.X, feiying2.Y
                    )
            if feiying2.X < feiying1.X:
                feiying2.load(
                    "./source/飞影2左倒下.png", 300, 180, 3, feiying2.X - 20, feiying2.Y
                )
                sleep(0.1)
                feiying2.down -= 1
                if feiying2.down == 0:
                    feiying2.healthflag = False
                    feiying2.down = 3
                    feiying2.load(
                        "./source/飞影2站立.png", 100, 180, 2, feiying2.X, feiying2.Y
                    )
    ###################################################################################################

    screen.blit(background, (0, 0))
    screen.blit(touxiang1, (0, 0))
    screen.blit(touxiang2, (891, 0))
    screen.blit(texture1, (306, 10))  # 飞影1‘血条’
    screen.blit(texture1, (645, 10))  # 飞影2‘血条’
    screen.blit(texture2, (306, 35))  # 飞影1‘灵气’
    screen.blit(texture2, (645, 35))  # 飞影2‘灵气’
    # screen.blit(pic,(50,50))

    # 飞影的位置限定#####################################################
    if feiying1.X <= 5:
        feiying1.X = 5
    if feiying1.X >= 900:
        feiying1.X = 850
    if feiying2.X <= 5:
        feiying2.X = 5
    if feiying2.X >= 900:
        feiying2.X = 850
    #####################################################################

    # 飞影死###############################################################
    # 飞影1死
    if feiying1.health <= 0:
        feiying1.health = 0
        if feiying1.dirt:
            im = pygame.image.load("./source/飞影左死.png").convert_alpha()
        else:
            im = pygame.image.load("./source/飞影死.png").convert_alpha()
        screen.blit(texture3, (400, 200))
        if feiying1.X <= 200:
            screen.blit(im, (5, feiying1.Y))
        else:
            screen.blit(im, (feiying1.X, feiying1.Y))
        end = 0
    # 飞影2死
    if feiying2.health <= 0:
        feiying2.health = 0
        if feiying2.dirt:
            im = pygame.image.load("./source/飞影2左死.png").convert_alpha()
        else:
            im = pygame.image.load("./source/飞影2死.png").convert_alpha()
        screen.blit(texture3, (400, 200))
        if feiying2.X >= 800:
            screen.blit(im, (800, feiying2.Y))
        else:
            screen.blit(im, (feiying2.X, feiying2.Y))
        end = 0
    ########################################################################
    if end == 1:
        group.update(ticks)
        group1.update(ticks)
        group.draw(screen)
        if feiying1.bishaf == 3:
            group1.draw(screen)
        if feiying2.bishaf == 3:
            group2.draw(screen)
    if end == 0:
        pygame.mixer.music.stop()
        end = 2
    pygame.draw.rect(
        screen, (248, 5, 16), Rect(101, 10, feiying1.health * 2, 20)
    )  # 飞影1的血条
    pygame.draw.rect(
        screen, (113, 227, 248), Rect(101, 35, feiying1.energy * 2, 20)
    )  # 飞影1的灵气
    pygame.draw.rect(
        screen, (248, 5, 16), Rect(690, 10, feiying2.health * 2, 20)
    )  # 飞影2的血条
    pygame.draw.rect(
        screen, (113, 227, 248), Rect(690, 35, feiying2.energy * 2, 20)
    )  # 飞影2的灵气
    pygame.display.update()
