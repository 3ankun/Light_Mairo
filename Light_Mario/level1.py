import copy
import mario
import constants as c
import pygame as pg
import collider


class FlipSwitch(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((1, 1))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=(x, y))


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = c.GFX['coin']
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def update(self, *args, **kwargs):
        if self.collected:
            self.kill()


class Level1:
    def __init__(self):
        self.camera_adjust = 0
        self.win = False
        self.score = 0
        self.world_flipped = False
        self.alt_world_flipped = False
        self.font = pg.font.Font(None, 36)
        self.castle_rect = pg.Rect(8700, c.GROUND_HEIGHT - 90, 60, 90)
        self.vision_mask = pg.Surface(c.SCREEN_SIZE).convert_alpha()
        self.startup()

    def startup(self):
        self.mario = mario.Mario()
        self.setup_mario_location()
        self.all_sprites = pg.sprite.Group(self.mario)

        self.background = c.GFX['level_1']
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(
            self.background,
            (int(self.back_rect.width * c.BACK_SIZE_MULTIPLER),
             int(self.back_rect.height * c.BACK_SIZE_MULTIPLER))
        )

        self.setup_ground()
        self.setup_pipes()
        self.setup_steps()
        self.setup_coins()
        self.setup_flip_switch()

        self.collide_group = pg.sprite.Group(
            self.ground_group,
            self.step_group,
            self.pipe_group
        )

    def setup_mario_location(self):
        self.mario.rect.x = 80
        self.mario.rect.bottom = c.GROUND_HEIGHT

    def setup_ground(self):
        self.ground_rect1 = collider.Collider(0, c.GROUND_HEIGHT, 2953, 60)
        self.ground_rect2 = collider.Collider(3048, c.GROUND_HEIGHT, 635, 60)
        self.ground_rect3 = collider.Collider(3819, c.GROUND_HEIGHT, 2735, 60)
        self.ground_rect4 = collider.Collider(6647, c.GROUND_HEIGHT, 2300, 60)

        self.ground_group = pg.sprite.Group(self.ground_rect1,
                                            self.ground_rect2,
                                            self.ground_rect3,
                                            self.ground_rect4)

    def setup_pipes(self):
        self.pipe1 = collider.Collider(1202, 452, 83, 82)
        self.pipe2 = collider.Collider(1631, 409, 83, 140)
        self.pipe3 = collider.Collider(1973, 409, 83, 140)
        self.pipe4 = collider.Collider(2445, 409, 83, 140)
        self.pipe5 = collider.Collider(6989, 452, 83, 82)
        self.pipe6 = collider.Collider(7675, 452, 83, 82)

        self.pipe_group = pg.sprite.Group(self.pipe1, self.pipe2,
                                          self.pipe3, self.pipe4,
                                          self.pipe5, self.pipe6)

    def setup_steps(self):
        self.step_group = pg.sprite.Group()
        positions = [
            (5745, 495), (5788, 452), (5831, 409), (5874, 366),
            (6001, 366), (6044, 408), (6087, 452), (6130, 495),
            (6345, 495), (6388, 452), (6431, 409), (6474, 366),
            (6517, 366), (6644, 366), (6687, 408), (6728, 452),
            (6771, 495), (7760, 495), (7803, 452), (7845, 409),
            (7888, 366), (7931, 323), (7974, 280), (8017, 237),
            (8060, 194), (8103, 194), (8488, 495)
        ]
        for pos in positions:
            width = 40
            height = 44 if pos[1] != 366 and pos[1] != 194 else 176 if pos[0] in (5874, 6001, 6517, 6644) else 360 if pos[0] == 8103 else 40
            self.step_group.add(collider.Collider(pos[0], pos[1], width, height))

    def setup_coins(self):
        self.coins = [
            Coin(320, c.GROUND_HEIGHT - 100),
            Coin(420, c.GROUND_HEIGHT - 140),
            Coin(820, c.GROUND_HEIGHT - 140),
            Coin(920, c.GROUND_HEIGHT - 160),
            Coin(1230, c.GROUND_HEIGHT - 200),
            Coin(2200, c.GROUND_HEIGHT - 100),
            Coin(3620, c.GROUND_HEIGHT - 100),
            Coin(3665, c.GROUND_HEIGHT - 140),
            Coin(4200, c.GROUND_HEIGHT - 100),
            Coin(4620, c.GROUND_HEIGHT - 100),
            Coin(5265, c.GROUND_HEIGHT - 140),
            Coin(5500, c.GROUND_HEIGHT - 100),
            Coin(5600, c.GROUND_HEIGHT - 100),
            Coin(6200, c.GROUND_HEIGHT - 100),
            Coin(7200, c.GROUND_HEIGHT - 140),
            Coin(7500, c.GROUND_HEIGHT - 140),
        ]
        self.coin_group = pg.sprite.Group(self.coins)
        self.all_sprites.add(self.coins)

    def setup_flip_switch(self):
        self.switch1 = FlipSwitch(1500, c.GROUND_HEIGHT - 32)
        self.switch2 = FlipSwitch(4800, c.GROUND_HEIGHT - 32)
        self.flip_switch_group = pg.sprite.Group(self.switch1, self.switch2)

    def camera(self):
        if self.mario.rect.right > c.SCREEN_WIDTH / 3:
            self.camera_adjust = self.mario.rect.right - c.SCREEN_WIDTH / 3
        else:
            self.camera_adjust = 0

    def update_mario_position(self):
        self.mario.rect.y += self.mario.y_vel
        collider = pg.sprite.spritecollideany(self.mario, self.collide_group)
        if collider:
            if self.mario.y_vel > 0:
                self.mario.y_vel = 0
                self.mario.jump_count = 0
                self.mario.state = c.WALK
                self.mario.rect.bottom = collider.rect.top
        else:
            self.mario.rect.y += 1
            if not pg.sprite.spritecollideany(self.mario, self.collide_group):
                if self.mario.state != c.JUMP:
                    self.mario.state = c.FALL
            self.mario.rect.y -= 1

        self.mario.rect.x += self.mario.x_vel
        collider = pg.sprite.spritecollideany(self.mario, self.collide_group)
        if collider:
            if self.mario.x_vel > 0:
                self.mario.rect.right = collider.rect.left
            else:
                self.mario.rect.left = collider.rect.right
            self.mario.x_vel = 0

        if self.mario.rect.y > c.SCREEN_HEIGHT:
            self.startup()

        if self.mario.rect.x < 5:
            self.mario.rect.x = 5

    def update(self, surface, keys, current_time):
        surface.blit(self.background, (0, 0),
                     area=pg.Rect(self.camera_adjust, 0, c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

        if not self.win:
            self.update_mario_position()
            self.all_sprites.update(keys, current_time)
            self.camera()

            for sprite in self.all_sprites:
                surface.blit(sprite.image, sprite.rect.move(-self.camera_adjust, 0))

            hit_coins = pg.sprite.spritecollide(self.mario, self.coin_group, False)
            for coin in hit_coins:
                if not coin.collected:
                    self.score += 100
                    coin.collected = True
                    if 'coin' in c.SOUNDS:
                        c.SOUNDS['coin'].play()

            if self.mario.rect.colliderect(self.switch1.rect):
                self.world_flipped = not self.world_flipped
                if 'switch' in c.SOUNDS:
                    c.SOUNDS['switch'].play()
            if self.mario.rect.colliderect(self.switch2.rect):
                self.alt_world_flipped = not self.alt_world_flipped
                if 'switch' in c.SOUNDS:
                    c.SOUNDS['switch'].play()

            if self.mario.rect.colliderect(self.castle_rect):
                self.win = True
                if 'win' in c.SOUNDS:
                    c.SOUNDS['win'].play()
                pg.mixer.music.pause()

        final_surface = surface.copy()

        self.vision_mask.fill((0, 0, 0, 200))
        mario_pos = self.mario.rect.centerx - self.camera_adjust, self.mario.rect.centery
        pg.draw.circle(self.vision_mask, (0, 0, 0, 0), mario_pos, 120)
        final_surface.blit(self.vision_mask, (0, 0))

        if self.world_flipped:
            final_surface = pg.transform.flip(final_surface, False, True)
        if self.alt_world_flipped:
            final_surface = pg.transform.flip(final_surface, False, True)

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        final_surface.blit(score_text, (20, 20))

        if self.win:
            win_text = self.font.render("You Win!", True, (255, 0, 0))
            final_surface.blit(win_text, (c.SCREEN_WIDTH // 2 - 60, c.SCREEN_HEIGHT // 2 - 20))
            restart_text = self.font.render("Press R to Restart", True, (255, 0, 0))
            final_surface.blit(restart_text, (c.SCREEN_WIDTH // 2 - 100, c.SCREEN_HEIGHT // 2 + 20))
            keys = pg.key.get_pressed()
            if keys[pg.K_r]:
                self.__init__()
                pg.mixer.music.unpause()

        pg.display.get_surface().blit(final_surface, (0, 0))
