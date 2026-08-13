from PPlay.window import Window
from PPlay.sprite import Sprite

janela= Window(700,500, "Meu primeiro pong")
janela.set_title("Bolinha no Centro")

bolinha = Sprite("bolinha.png")
bolinha.x = (janela.width / 2) - (bolinha.width / 2)
bolinha.y = (janela.height / 2) - (bolinha.height / 2)


while True:
    janela.set_background_color("Dark Blue")
    bolinha.draw()
    janela.update()