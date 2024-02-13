from typing import ClassVar

import pyautogui
import pygame as pg


class Settings:
    SCORE: ClassVar[int] = 0
    # game constants:
    MAX_SHOTS: ClassVar[int] = 2  # most player bullets onscreen
    ALIEN_ODDS: ClassVar[int] = 22  # chances a new alien appears
    BOMB_ODDS: ClassVar[float] = 60.0  # chances a new bomb will drop
    ALIEN_RELOAD: ClassVar[int]  = 12  # frames between new aliens
    ONE_TIME_COUNT: ClassVar[int] = 0 # for one-time print() calls 

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings

        # calculate game size as a percentage of device screen size
        device_width, device_height = pyautogui.size()
        self.screenPct: float = float(0.85)

        # ratio to original hard-coded values of 640 (w) x 480 (h) in the PyGame.examples.aliens GitHub repo
        ratio_height:float = device_height / 480.0
        ratio_width:float = device_width / 640.0
        if(Settings.ONE_TIME_COUNT == 0):
            print(f'ratios: height: {ratio_height:.2f}, width: {ratio_width:.2f}')            

        # round scaled width and height to multiple of 100
        game_width: int = int((device_width * self.screenPct // 100) * 100)
        game_height: int = int((device_height * self.screenPct // 100) * 100)
        if(Settings.ONE_TIME_COUNT == 0):
            print(f'game width: {game_width}, height: {game_height}')

        self.screen_width = game_width
        self.screen_height = game_height
        self.near_bottom = game_height * 0.90
        self.score_board_y = game_height * 0.95
        self.score_font_size = int(device_height * 0.03)
        self.SCREENRECT = pg.Rect(0, 0, self.screen_width, self.screen_height)

        Settings.ONE_TIME_COUNT += 1