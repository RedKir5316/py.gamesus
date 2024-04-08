from pygame import *
from sys import exit


class Sprite(sprite.Sprite):
    def __init__(self, filename, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw (self):
        window.blit(self.image, (self.rect.x, self.rect.y))


""" sus """
class Player(Sprite):
    def __init__(self, filename, width, height, x, y, ):
        super().__init__(filename, width, height, x, y)
        self.speedx = 0
        self.speedy = 0
        self.touch_jump = False
        
    def update(self):
        keys_pressed = key.get_pressed()
        self.speedx = 0
        if self.speedy < 10:
            self.speedy += 1
        if keys_pressed[K_d]:
            self.speedx = 5
        if keys_pressed[K_a]:
            self.speedx = -5
        if keys_pressed[K_w] and self.touch_jump:
            self.speedy = -25
            self.touch_jump = False
        if keys_pressed[K_s]:
            self.speedy = 5
        self.rect.y += self.speedy
        platforms_touched = sprite.spritecollide(self, platforms, False)
        for platform in platforms_touched:
            if self.speedy > 0:
                self.rect.bottom = min(self.rect.bottom, platform.rect.top)
                self.touch_jump = True
            if self.speedy < 0:
                self.rect.top = max(self.rect.top, platform.rect.bottom)
        self.rect.x += self.speedx
        platforms_touched = sprite.spritecollide(self, platforms, False)
        for platform in platforms_touched:
            if self.speedx > 0:
                self.rect.right = min(self.rect.right, platform.rect.left)
            if self.speedx < 0:
                self.rect.left = max(self.rect.left, platform.rect.right)


class Enemy(Sprite):
    def __init__(self, filename, width, height, x, y, speed):
        super().__init__(filename, width, height, x, y)
        self.speed = speed
        
    def update(self):
        if toast.rect.x > self.rect.x:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if toast.rect.y > self.rect.y:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed


window = display.set_mode((1280, 720))
display.set_caption("СУС")#Название окна
display.set_icon(image.load("CYC.jpg"))#Иконка
toast = Player("toast.png", 50, 50, 850, 600)
background = image.load("SUS.jpg")#Фон
background = transform.scale(background,(1280, 720))
clock = time.Clock()
toast_earth = Sprite("toast.png", 2500, 10, 70, 600)
toast_earth1 = Sprite("toast.png", 2500, 10, 500, 300)
toast_earth2 = Sprite("toast.png", 250, 10, 270, 295)
target = Sprite("finish.png", 100, 100, 1000, 200)
platforms = sprite.Group(toast_earth,
                         toast_earth1,
                         Sprite("stena.png", 25, 250, 200, 300),
                         Sprite("stena.png", 15, 230, 305, 300),
                         toast_earth2,
                         Sprite("stena.png", 25, 250, 500, 140),
                         Sprite("stena.png", 25, 250, 700, 0),
                         Sprite("stena.png", 15, 230, 800, 200),
                         Sprite("stena.png", 15, 230, 800, 500))
toast_gohts = Enemy("toast.png", 50, 50, 200, 200, 1)
gohts = sprite.Group(
     toast_gohts
)
boom = image.load("Cabooom.jpg")
boom = transform.scale(boom,(1280, 720))
finish = False


while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
    if not finish:
        window.blit(background, (0,0))
        toast.draw()
        toast.update()
        platforms.draw(window)
        gohts.draw(window)
        gohts.update()
        target.draw()
    if sprite.spritecollide(toast, gohts, False):
        window.blit(boom, (0,0))
        finish = True
    if toast.rect.colliderect(target.rect):
        window.blit(boom, (0,0))
        finish = True
    display.update()
    clock.tick(60)
