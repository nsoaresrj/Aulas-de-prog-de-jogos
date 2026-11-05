from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
import sys
import jogo
import ranking

# 1. Configuração da Janela
janela = Window(800, 600)
janela.set_title("Space Invaders")

mouse = Window.get_mouse()
teclado = Window.get_keyboard()

estado_atual = "MENU"
dificuldade_atual = "FÁCIL"

# ================= FUNÇÃO AUXILIAR =================
def criar_botao_centralizado(caminho_imagem, y):
    botao = Sprite(caminho_imagem)
    botao.x = (janela.width / 2) - (botao.width / 2)
    botao.y = y
    return botao

# ================= CARREGAMENTO DE SPRITES =================
# Sprites do Menu Principal
btn_jogar       = criar_botao_centralizado("spaceinvaders/sprites/play.png", 200)
btn_dificuldade = criar_botao_centralizado("spaceinvaders/sprites/level.png", 280)
btn_ranking     = criar_botao_centralizado("spaceinvaders/sprites/rank.png", 360)
btn_sair        = criar_botao_centralizado("spaceinvaders/sprites/exit.png", 440)

# Sprites da Tela de Dificuldade
btn_facil   = criar_botao_centralizado("spaceinvaders/sprites/easy.png", 200)
btn_medio   = criar_botao_centralizado("spaceinvaders/sprites/normal.png", 280)
btn_dificil = criar_botao_centralizado("spaceinvaders/sprites/hard.png", 360)
btn_voltar  = criar_botao_centralizado("spaceinvaders/sprites/back.png", 480)

# ================= LOOP PRINCIPAL =================
while True:
    janela.set_background_color((0, 0, 0))
    
    # ------------------ ESTADO: MENU ------------------
    if estado_atual == "MENU":
        janela.draw_text("SPACE INVADERS", (janela.width / 2) - 230, 80, size=55, color=(255, 255, 255), bold=True)
        
        btn_jogar.draw()
        btn_dificuldade.draw()
        btn_ranking.draw()
        btn_sair.draw()
        
        if mouse.is_over_object(btn_jogar) and mouse.is_button_pressed(1):
            estado_atual = "JOGAR"
            janela.delay(200)
            
        elif mouse.is_over_object(btn_dificuldade) and mouse.is_button_pressed(1):
            estado_atual = "DIFICULDADE"
            janela.delay(200)
            
        elif mouse.is_over_object(btn_ranking) and mouse.is_button_pressed(1):
            estado_atual = "RANKING"
            janela.delay(200)
            
        elif mouse.is_over_object(btn_sair) and mouse.is_button_pressed(1):
            janela.close()
            sys.exit()

    # ------------------ ESTADO: JOGAR ------------------
    elif estado_atual == "JOGAR":
        jogo.executar(janela, teclado, dificuldade_atual)
        estado_atual = "MENU"
        janela.delay(200)

    # --------------- ESTADO: DIFICULDADE ---------------
    elif estado_atual == "DIFICULDADE":
        janela.draw_text("DIFICULDADE", (janela.width / 2) - 170, 80, size=50, color=(255, 255, 255), bold=True)
        
        btn_facil.draw()
        btn_medio.draw()
        btn_dificil.draw()
        btn_voltar.draw()
        
        if mouse.is_over_object(btn_facil) and mouse.is_button_pressed(1):
            dificuldade_atual = "FÁCIL"
            estado_atual = "JOGAR"
            janela.delay(200)
            
        elif mouse.is_over_object(btn_medio) and mouse.is_button_pressed(1):
            dificuldade_atual = "MÉDIO"
            estado_atual = "JOGAR"
            janela.delay(200)
            
        elif mouse.is_over_object(btn_dificil) and mouse.is_button_pressed(1):
            dificuldade_atual = "DIFÍCIL"
            estado_atual = "JOGAR"
            janela.delay(200)
            
        elif mouse.is_over_object(btn_voltar) and mouse.is_button_pressed(1):
            estado_atual = "MENU"
            janela.delay(200)

    # --------------- ESTADO: RANKING ---------------
    elif estado_atual == "RANKING":
        ranking.executar(janela, mouse, teclado)
        estado_atual = "MENU"
        janela.delay(200)

    janela.update()
