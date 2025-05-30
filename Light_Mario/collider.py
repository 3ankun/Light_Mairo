import pygame as pg
import constants as c

class Collider(pg.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width,height)).convert()
        self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class FlipSwitch(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.image.fill((255, 0, 255))  #可识别方块
        self.rect = self.image.get_rect(topleft=(x, y))
        self.activated = False