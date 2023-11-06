from modules.display import DisplayModule
from modules.game_runner import GameRunner
from modules.menu import Menu


class Application:
    def __init__(self):
        print("Starting app")
        self.display = DisplayModule()
        self.menu = Menu(self.display)

    def start(self):
        while True:
            # print("On Select Color State")
            # color = self.menu.selectColor()
            color = "WHITE"
            # print("On Select Color State")
            # difficulty = self.menu.selectDifficulty()
            difficulty = 5
            # print("On Select Difficulty State")
            # has_time = self.menu.selectTime()
            has_time = 0
            self.menu.waitStart()

            game = GameRunner(
                color=color,
                difficulty=difficulty,
                has_time=has_time,
                display=self.display,
            )
            game.run()

            self.menu.endGame()

            # joga tudo para cemiterio
            game.finish()


app = Application()
app.start()
