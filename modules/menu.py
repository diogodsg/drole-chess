import time
from modules.display import DisplayModule
from modules.buttons import ButtonsModule
from modules.display import DisplayModule


class Menu:
    def __init__(self, display):
        self.display = display
        self.buttons = ButtonsModule()

    def endGame(self):
        self.display.display(0, "Jogo Finalizado!")
        self.display.display(1, "ACABO")

        while True:
            if self.buttons.buttonPressed("queen"):
                self.display.display(0, "Arrumando")
                self.display.display(1, "Tabuleiro...")
                time.sleep(2)
                return 0

    def waitStart(self):
        self.display.display(0, "Pressione Q")
        self.display.display(1, "para iniciar")

        while True:
            if self.buttons.buttonPressed("queen"):
                self.display.display(0, "JOGO")
                self.display.display(1, "INICIADO!")
                time.sleep(2)
                return 0

    def selectColor(self):
        self.display.display(0, "Selecione a cor")
        self.display.display(1, "Q-Brancas R-Pretas")

        while True:
            if self.buttons.buttonPressed("queen"):
                self.display.display(0, "Cor Branca")
                self.display.display(1, "Selecionada")
                time.sleep(2)
                return 0
            elif self.buttons.buttonPressed("rook"):
                self.display.display(0, "Cor Preta")
                self.display.display(1, "Selecionada")
                time.sleep(2)
                return 1

    def selectDifficulty(self):
        self.display.display(0, "Selecione a dificuldade")
        self.display.display(1, "Q-5 B-10 N-15 R-20")

        while True:
            if self.buttons.buttonPressed("queen"):
                self.display.display(0, "Dificuldade 5")
                self.display.display(1, "Selecionada")
                time.sleep(2)
                return 5
            elif self.buttons.buttonPressed("bishop"):
                self.display.display(0, "Dificuldade 10")
                self.display.display(1, "Selecionada")
                time.sleep(2)
                return 10
            elif self.buttons.buttonPressed("knight"):
                self.display.display(0, "Dificuldade 15")
                self.display.display(1, "Selecionada")
                time.sleep(2)
                return 15
            elif self.buttons.buttonPressed("rook"):
                self.display.display(0, "Dificuldade 20")
                self.display.display(1, "Selecionada")
                time.sleep(2)
                return 20

    def selectTime(self):
        self.display.display(0, "Selecione a o tempo")
        self.display.display(1, "Q-Sem tempo R-10 min")

        while True:
            if self.buttons.buttonPressed("queen"):
                self.display.display(0, "Sem tempo")
                self.display.display(1, "Selecionado")
                time.sleep(2)
                return 0
            elif self.buttons.buttonPressed("rook"):
                self.display.display(0, "10 min")
                self.display.display(1, "Selecionado")
                time.sleep(2)
                return 1

    def select_promotion(self):
        self.display.display(0, "Selecione a promocao")
        self.display.display(1, "desejada")

        while True:
            if self.buttons.buttonPressed("queen"):
                self.display.display(0, "Peao promovido")
                self.display.display(1, "para rainha")
                time.sleep(2)
                return 0
            elif self.buttons.buttonPressed("bishop"):
                self.display.display(0, "Peao promovido")
                self.display.display(1, "para bispo")
                time.sleep(2)
                return 1
            elif self.buttons.buttonPressed("knight"):
                self.display.display(0, "Peao promovido")
                self.display.display(1, "para cavalo")
                time.sleep(2)
                return 2
            elif self.buttons.buttonPressed("rook"):
                self.display.display(0, "Peao promovido")
                self.display.display(1, "para torre")
                time.sleep(2)
                return 3


#
#    Menu:
#        Welcome to drole chess

#         pergunto se quer jogar com preto ou branco
#         pergunto dificuldade
#         pergunto se quer jogar com tempo

#         pressione para iniciar o jogo

#         mostrar timer

#         Peças pretas ganharam
#         Peças brancas ganharam
#         presisone sus pra continuar

#         promover para:
#         Q K H B


#     ButtonModule:
#         botao resign
