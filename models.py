import random
from typing import List

import pygame as pg

from settings import Settings


class Alien(pg.sprite.Sprite):
    """An alien space ship. That slowly moves down the screen."""

    speed = 13
    animcycle = 12
    images: List[pg.Surface] = []

    def __init__(self, *groups):

        self.settings = Settings()
        self.SCREENRECT = self.settings.SCREENRECT

        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = self.SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not self.SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(self.SCREENRECT)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]


class Bomb(pg.sprite.Sprite):
    """A bomb the aliens drop."""

    speed = 9
    images: List[pg.Surface] = []

    def __init__(self, alien, explosion_group, *groups):
        self.settings = Settings()
        self.SCREENRECT = self.settings.SCREENRECT

        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0, 5).midbottom)
        self.explosion_group = explosion_group

    def update(self):
        """called every time around the game loop.

        Every frame we move the sprite 'rect' down.
        When it reaches the bottom we:

        - make an explosion.
        - remove the Bomb.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= self.settings.near_bottom:
            Explosion(self, self.explosion_group)
            self.kill()


class Shot(pg.sprite.Sprite):
    """a bullet the Player sprite fires."""

    speed = -11
    images: List[pg.Surface] = []

    def __init__(self, pos, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        """called every time around the game loop.

        Every tick we move the shot upwards.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    """An explosion. Hopefully the Alien and not the player!"""

    defaultlife = 12
    animcycle = 3
    images: List[pg.Surface] = []

    def __init__(self, actor, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        """called every time around the game loop.

        Show the explosion surface for 'defaultlife'.
        Every game tick(update), we decrease the 'life'.

        Also we animate the explosion.
        """
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()


class Score(pg.sprite.Sprite):
    """to keep track of the score."""

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.settings = Settings()
        self.font = pg.font.Font(None, self.settings.score_font_size)
        self.font.set_italic(1)
        self.color = "white"
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, self.settings.score_board_y)

    def update(self):
        """We only update the score in update() when it has changed."""

        if Settings.SCORE != self.lastscore:
            self.lastscore = Settings.SCORE
            msg = f"Score: {Settings.SCORE}"
            self.image = self.font.render(msg, 0, self.color)
