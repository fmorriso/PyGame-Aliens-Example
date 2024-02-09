import pyautogui

class Settings:

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings

        # calculate game size as a percentage of device screen size
        device_width, device_height = pyautogui.size()
        self.screenPct: float = float(3.0 / 4.0)

        # round scaled width and height to multiple of 100
        game_width: int = int((device_width * self.screenPct // 100) * 100)
        game_height: int = int((device_height * self.screenPct // 100) * 100)

        self.scaleFactor = device_width / device_height + self.screenPct
        # print(f'scale factor = {self.scaleFactor}')
        self.screen_width = game_width
        self.screen_height = game_height
        self.near_bottom = game_height * 0.90
        self.score_board_y = game_height * 0.95
