#положением мыши можно целиться, удержание левой кнопки увеличивает начальную скорость снарядов. Всего 10 снарядов, если игра закончилась, нажмите пробел



import math
from random import choice, randint as rnd

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        screen - экран
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600). Если мяч врезается в рамку, знак его скорости меняется на противоположный, если мяч падает на пол, его скорость становится равна 0
        Args:
             self - обьект класса Ball
        Returns:
             x - изменение координаты х,
             y - изменение координаты y
        """
        if self.x + self.vx >=0 and self.x + self.vx <= 800 and self.y + self.vy >= 0 and self.y + self.vy <= 600: 
            self.x += self.vx
            self.y -= self.vy
            self.vy = self.vy - 3
        if self.x + self.vx >= 800 or self.x + self.vx <= 0:
            self.vx = -self.vx
        if self.y + self.vy <= 0:
            self.vy = -self.vy
            self.vy = self.vy - 3
        if self.y + self.vy == 600:
            self.vy = 0
            self.vx = 0


        
                    


    def draw(self):
        '''Метод выводит мяч на экран'''
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2) <= obj.r + self.r


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши.(определяет направление выстрела в зависимости от положения мыши)"""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        '''Выводит пушку на экран'''
        pygame.draw.line(screen, self.color, [40, 450],
                         [40 + self.f2_power * math.cos(self.an),
                          450 + self.f2_power * math.sin(self.an)], 10)
    def power_up(self):
        '''Определяет начальную скорость мяча взависимости от времени удержания кнопки выстрела, меняет цвет пушки'''
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
counter = 0

class Target:
     
   
    def __init__(self):
        '''Создает цель и определяет ее параметры
        Args: обьект класса Target'''
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(20, 50)
        self.color = choice(GAME_COLORS)
        self.vx = rnd(-10,10)
        self.vy = rnd(-10,10)
    def new_target(self):
        '''Создает новую цель'''
        self.x = rnd(400, 780)
        self.y = rnd(200, 550)
        self.r = rnd(10, 50)
        self.color = choice(GAME_COLORS)
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):

        '''Выводит изображение цели на экран'''
        pygame.draw.circle(screen, self.color, [self.x,self.y],self.r)
    def move(self):
        '''Определяет параметры движения целей (при столкновении с рамками направление скорости меняется)
        Args:обьект класса Target
        Returns:
        x - координата по оси x
        y - координата по оси y'''
        if self.x + self.vx >= 800 or self.x + self.vx <= 100:
            self.vx = -self.vx
        
        if self.y + self.vy >= 600 or self.y + self.vy <= 100:
            self.vy = -self.vy
        self.x += self.vx
        self.y += self.vy



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    target1.live = 1
    target2.live = 1
    gun.draw()
#проверяем, уничтожены ли цели
    if target1.live == 1:
        target1.draw()
        target1.move()
    if target2.live == 1:
        target2.draw()
        target2.move()
    for b in balls:
        b.draw()
#Проверяем, не закончились ли снаряды. Если закончились, то игра окончена. Выводим счетчик снарядов и счетчик попаданий на экран
    if bullet >= 10:
        text =  pygame.font.Font(None, 100).render('Game over',
                                              True, (180, 0, 0))
        t = pygame.font.Font(None, 50).render('Press SPACE',
                                              True, (180, 0, 0))
        text2 = pygame.font.Font(None, 50).render('Снаряды:'+str(0),
                                              True, (0, 0, 0))
        screen.blit(text, (230, 300))
        screen.blit(t, (280, 370))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = 0
            counter = 0

    

    elif bullet >= 7:
        text2 = pygame.font.Font(None, 50).render('Снаряды:'+str(10 - bullet),
                                              True, (180, 0, 0))
    else:
        text2 = pygame.font.Font(None, 50).render('Снаряды:'+str(10 - bullet),
                                              True, (0, 0, 0))
    text1 = pygame.font.Font(None, 50).render('Попадания:'+str(counter),
                                              True, (0, 0, 0))
    screen.blit(text1, (0, 0))
    screen.blit(text2, (0, 40))
        
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
#проверка на попадание, создание новой цели, подсчет попаданий
    for b in balls:
        b.move()
        if bullet <= 10:
            if b.hittest(target1) and target1.live == 1:
                target1.live = 0
                counter += 1
                target1.hit()
                target1.new_target()
                target1.live = 1
            if b.hittest(target2) and target2.live == 1:
                target2.live = 0
                counter += 1
                target2.hit()
                target2.new_target()
                target2.live = 1
    gun.power_up()
pygame.quit()
