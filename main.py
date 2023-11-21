from modules.display import DisplayModule
from modules.game_runner import GameRunner
from modules.menu import Menu
from modules.camera import CameraModule


class Application:
    def __init__(self):
        print("Starting app")
        self.display = DisplayModule()
        self.menu = Menu(self.display)
        self.camera_module = CameraModule()

    def start(self):
        while True:
            print("On Select Color State")
            color = self.menu.selectColor()
            #color = "BLACK"
            print("On Select Color State")
            difficulty = self.menu.selectDifficulty()
            #difficulty = 5
            print("On Select Difficulty State")
            has_time = self.menu.selectTime()
            #has_time = 0
            
            self.camera_module.player_color = color

            game = GameRunner(
                color=color,
                difficulty=difficulty,
                has_time=has_time,
                display=self.display,
                menu=self.menu,
                camera_module=self.camera_module
            )
            game.run()

            self.menu.endGame()


app = Application()
app.start()
