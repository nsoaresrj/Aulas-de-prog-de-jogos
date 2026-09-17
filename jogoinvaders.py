from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *

# 1. Configuração da Janela
janela = Window(800, 600)
janela.set_title("Space Invaders - Game Loop")
teclado = Window.get_keyboard()

# ================= VARIÁVEIS DE DIFICULDADE =================
# Vamos simular que essa variável veio do seu menu
dificuldade_atual = "MÉDIO" 

# Baseado na dificuldade, definimos os atributos do jogo
if dificuldade_atual == "FÁCIL":
    velocidade_jogador = 500
    tempo_recarga_tiro = 0.2  # Pode atirar a cada 0.2 segundos
elif dificuldade_atual == "MÉDIO":
    velocidade_jogador = 350
    tempo_recarga_tiro = 0.4
elif dificuldade_atual == "DIFÍCIL":
    velocidade_jogador = 200
    tempo_recarga_tiro = 0.7  # Demora quase 1 segundo pra atirar de novo

# ================= CONFIGURAÇÃO DO JOGADOR =================
jogador = Sprite("assets/jogador.png")
# Posiciona o jogador no meio da tela, na parte inferior
jogador.x = (janela.width / 2) - (jogador.width / 2)
jogador.y = janela.height - jogador.height - 20

# ================= CONFIGURAÇÃO DOS TIROS =================
tiros = [] # Lista vazia que vai guardar todos os tiros ativos na cena
velocidade_tiro = 600
cronometro_tiro = 0 # Variável para controlar o tempo de recarga

# ================= LOOP PRINCIPAL DO JOGO =================
while True:
    janela.set_background_color((0, 0, 0))
    
    # Pegamos o Delta Time (tempo que passou desde o último frame, em segundos)
    dt = janela.delta_time()
    
    # ------------------ MOVIMENTO DO JOGADOR ------------------
    if teclado.key_pressed("LEFT"):
        jogador.x -= velocidade_jogador * dt
    if teclado.key_pressed("RIGHT"):
        jogador.x += velocidade_jogador * dt
        
    # Colisão com as paredes (Limites da tela)
    if jogador.x < 0:
        jogador.x = 0 # Bateu na esquerda, não passa de zero
    elif jogador.x > janela.width - jogador.width:
        jogador.x = janela.width - jogador.width # Bateu na direita, crava no limite
        
    # ------------------ LÓGICA DE TIROS (COOLDOWN) ------------------
    # O cronômetro sempre aumenta baseado no tempo que se passou (dt)
    cronometro_tiro += dt 
    
    # Se apertou ESPAÇO e o cronômetro passou do tempo limite (recarga):
    if teclado.key_pressed("SPACE") and cronometro_tiro >= tempo_recarga_tiro:
        # Cria um novo sprite de tiro
        novo_tiro = Sprite("assets/tiro.png")
        
        # Centraliza o tiro no bico da nave do jogador
        novo_tiro.x = jogador.x + (jogador.width / 2) - (novo_tiro.width / 2)
        novo_tiro.y = jogador.y - novo_tiro.height
        
        # Adiciona na lista
        tiros.append(novo_tiro)
        
        # Zera o cronômetro para ter que esperar a recarga de novo!
        cronometro_tiro = 0

    # ------------------ ATUALIZAÇÃO E DESENHO DOS TIROS ------------------
    # Usamos uma cópia da lista [:] para conseguir remover itens com segurança durante o loop
    for tiro in tiros[:]: 
        # Move o tiro para cima usando o delta time
        tiro.y -= velocidade_tiro * dt
        
        # Se o tiro saiu completamente da tela (passou do Y = 0)...
        if tiro.y < -tiro.height:
            tiros.remove(tiro) # ...Ele é destruído e retirado da lista
        else:
            # Se ainda está na tela, desenha!
            tiro.draw()

    # ------------------ DESENHO DO JOGADOR E HUD ------------------
    jogador.draw()
    
    # Textos de debug para você ver a mecânica funcionando
    janela.draw_text(f"Dificuldade: {dificuldade_atual}", 10, 10, size=18, color=(255, 255, 255))
    janela.draw_text(f"Tiros ativos na cena: {len(tiros)}", 10, 35, size=18, color=(255, 255, 0))
    janela.draw_text(f"Recarga: {cronometro_tiro:.1f} / {tempo_recarga_tiro}", 10, 60, size=18, color=(0, 255, 255))

    # Condição de saída para fechar essa janela de teste
    if teclado.key_pressed("ESC"):
        break

    janela.update()
