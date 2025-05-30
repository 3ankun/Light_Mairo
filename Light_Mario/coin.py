import pygame as pg

class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((16, 16))
        self.image.fill((255, 215, 0))  # 金色小方块
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def update(self):
        if self.collected:
            self.kill()  # 移除金币