from PPlay.sprite import *

# Transformamos o jogo em uma função que recebe as variáveis do Menu
def executar(janela, teclado, dificuldade_atual):
    
    # Baseado na dificuldade que VEIO DO MENU, definimos os atributos
    if dificuldade_atual == "FÁCIL":
        velocidade_jogador = 500
        tempo_recarga_tiro = 0.2
    elif dificuldade_atual == "MÉDIO":
        velocidade_jogador = 350
        tempo_recarga_tiro = 0.4
    elif dificuldade_atual == "DIFÍCIL":
        velocidade_jogador = 200
        tempo_recarga_tiro = 0.7

    jogador = Sprite("assets/jogador.png")
    jogador.x = (janela.width / 2) - (jogador.width / 2)
    jogador.y = janela.height - jogador.height - 20

    tiros = []
    velocidade_tiro = 600
    cronometro_tiro = 0

    # O loop do jogo roda aqui dentro
    while True:
        janela.set_background_color((0, 0, 0))
        dt = janela.delta_time()
        
        # Movimento e Limites
        if teclado.key_pressed("LEFT"):
            jogador.x -= velocidade_jogador * dt
        if teclado.key_pressed("RIGHT"):
            jogador.x += velocidade_jogador * dt
            
        if jogador.x < 0:
            jogador.x = 0
        elif jogador.x > janela.width - jogador.width:
            jogador.x = janela.width - jogador.width
            
        # Tiros
        cronometro_tiro += dt 
        if teclado.key_pressed("SPACE") and cronometro_tiro >= tempo_recarga_tiro:
            novo_tiro = Sprite("assets/tiro.png")
            novo_tiro.x = jogador.x + (jogador.width / 2) - (novo_tiro.width / 2)
            novo_tiro.y = jogador.y - novo_tiro.height
            tiros.append(novo_tiro)
            cronometro_tiro = 0

        for tiro in tiros[:]:
            tiro.y -= velocidade_tiro * dt
            if tiro.y < -tiro.height:
                tiros.remove(tiro)
            else:
                tiro.draw()

        jogador.draw()
        
        # HUD de Debug
        janela.draw_text(f"Dificuldade: {dificuldade_atual}", 10, 10, size=18, color=(255, 255, 255))
        janela.draw_text(f"Tiros na cena: {len(tiros)}", 10, 35, size=18, color=(255, 255, 0))

        # Se apertar ESC, o 'return' encerra essa função e devolve o controle pro Menu!
        if teclado.key_pressed("ESC"):
            return 

        janela.update()
