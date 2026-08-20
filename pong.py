from PPlay.window import Window
from PPlay.sprite import Sprite

#configurações da janela
janela= Window(800,600,)
janela.set_title("Meu primeiro pong")

#configurações da bolinha
bolinha = Sprite("bolinha.png") #s
bolinha.x = (janela.width / 2) - (bolinha.width / 2) #posição vertical da bola
bolinha.y = (janela.height / 2) - (bolinha.height / 2) #posição horizontal da bola

#variaveis da velocidade da bola
vel_x = 4
vel_y = 4

#configurações dos pads
pad_esq = Sprite("pad(1).png")
pad_esq.x = 5 # 5 pixels de distancia da borda esquerda
pad_esq.y = (janela.height / 2) - (pad_esq.height / 2) #deixa o pad centralizado na altura

pad_dir = Sprite("pad(1).png")
pad_dir.x = janela.width - pad_dir.width - 5 # 5 pixels de distancia da borda esquerda
pad_dir.y = (janela.height / 2) - (pad_dir.height / 2) #deixa o pad centralizado na altura

#game loop
while True:
    janela.set_background_color("Dark Blue")
#movimento da bola
    bolinha.x += vel_x
    bolinha.y += vel_y
#colisão com as paredes Horizontais (teto e chão)
    if bolinha.y <= 0 or bolinha.y >= janela.height - bolinha.height:
        vel_y *= -1 #inverte a direção

#colisão com as paredes Verticais (paredes da esquerda e direita)
    if bolinha.x <= 0 or bolinha.x >= janela.width - bolinha.width:
        vel_x *= -1.03 #aumenta a velocidade da bola sempre que colide nas paredes 
        vel_y *= 1.03 #aumenta a velocidade verticalmente para que a bola não va super rapido para 
                     #os lados e lento para cima
    #desenha os elementos na tela
    pad_esq.draw()
    pad_dir.draw()
    bolinha.draw()

    janela.update()
