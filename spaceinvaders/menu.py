from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
import sys
import jogo
import ranking

# =====================================================================
# BLOCO 1: CONFIGURAÇÃO DA JANELA E PERIFÉRICOS
# [COMO ALTERAR]: Para mudar o tamanho da tela, altere 800 (largura) e 600 (altura).
# =====================================================================
janela = Window(800, 600)
janela.set_title("Space Invaders")

mouse = Window.get_mouse()
teclado = Window.get_keyboard()

# Variáveis que controlam em qual tela o jogador está e a dificuldade padrão inicial
estado_atual = "MENU"
dificuldade_atual = "FÁCIL"


# =====================================================================
# BLOCO 2: FUNÇÃO AUXILIAR DE BOTÕES
# Centraliza automaticamente qualquer botão no meio horizontal (eixo X) da tela.
# =====================================================================
def criar_botao_centralizado(caminho_imagem, y):
    botao = Sprite(caminho_imagem)
    botao.x = (janela.width / 2) - (botao.width / 2) # Meio da tela menos metade da largura do botão
    botao.y = y                                      # Altura definida pelo parâmetro 'y'
    return botao


# =====================================================================
# BLOCO 3: CARREGAMENTO DOS SPRITES DOS BOTÕES
# [COMO ALTERAR]: O número no final (ex: 200, 280) é a altura (Y) do botão na tela.
# Aumente o número para descer o botão ou diminua para subir.
# =====================================================================
# Botões do Menu Principal
btn_jogar       = criar_botao_centralizado("spaceinvaders/sprites/play.png", 200)
btn_dificuldade = criar_botao_centralizado("spaceinvaders/sprites/level.png", 280)
btn_ranking     = criar_botao_centralizado("spaceinvaders/sprites/rank.png", 360)
btn_sair        = criar_botao_centralizado("spaceinvaders/sprites/exit.png", 440)

# Botões da Tela de Dificuldade e Ranking
btn_facil   = criar_botao_centralizado("spaceinvaders/sprites/easy.png", 200)
btn_medio   = criar_botao_centralizado("spaceinvaders/sprites/normal.png", 280)
btn_dificil = criar_botao_centralizado("spaceinvaders/sprites/hard.png", 360)
btn_voltar  = criar_botao_centralizado("spaceinvaders/sprites/back.png", 480)


# =====================================================================
# BLOCO 4: LOOP PRINCIPAL E MÁQUINA DE ESTADOS
# Verifica qual é o 'estado_atual' e desenha apenas a tela correspondente.
# O 'janela.delay(200)' evita que um único clique seja lido duas vezes seguidas.
# =====================================================================
while True:
    # Pinta o fundo de preto (R=0, G=0, B=0) a cada frame
    janela.set_background_color((0, 0, 0))
    
    # ------------------ TELA 1: MENU PRINCIPAL ------------------
    if estado_atual == "MENU":
        janela.draw_text("SPACE INVADERS", (janela.width / 2) - 230, 80, size=55, color=(255, 255, 255), bold=True)
        
        btn_jogar.draw()
        btn_dificuldade.draw()
        btn_ranking.draw()
        btn_sair.draw()
        
        # Checa cliques com o botão esquerdo do mouse (1) em cada botão
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

    # ------------------ TELA 2: EXECUTAR O JOGO ------------------
    elif estado_atual == "JOGAR":
        # Chama a função principal do arquivo jogo.py.
        # Quando o jogador perde ou aperta ESC lá dentro, o código volta para a linha abaixo.
        jogo.executar(janela, teclado, dificuldade_atual)
        estado_atual = "MENU"
        janela.delay(200)

    # --------------- TELA 3: SELEÇÃO DE DIFICULDADE ---------------
    elif estado_atual == "DIFICULDADE":
        janela.draw_text("DIFICULDADE", (janela.width / 2) - 170, 80, size=50, color=(255, 255, 255), bold=True)
        
        btn_facil.draw()
        btn_medio.draw()
        btn_dificil.draw()
        btn_voltar.draw()
        
        # [COMO ALTERAR]: Se quiser que clicar na dificuldade apenas mude a configuração
        # e volte para o menu (sem iniciar o jogo direto), troque "JOGAR" por "MENU" abaixo.
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

    # ------------------ TELA 4: TELA DE RANKING ------------------
    elif estado_atual == "RANKING":
        # Chama a tela do arquivo ranking.py e volta ao menu quando o jogador sair dela
        ranking.executar(janela, mouse, teclado)
        estado_atual = "MENU"
        janela.delay(200)

    # Atualiza a tela ao final de cada repetição do loop
    janela.update()
