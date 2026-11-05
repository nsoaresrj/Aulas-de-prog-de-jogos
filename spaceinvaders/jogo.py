from PPlay.sprite import *
import random

def executar(janela, teclado, dificuldade_atual):
    
    # ================= CONFIGURAÇÕES DE DIFICULDADE =================
    if dificuldade_atual == "FÁCIL":
        velocidade_jogador = 500
        tempo_recarga_tiro = 0.2
        vel_monstros_x = 150
        base_recarga_monstros = 1.5
        multiplicador_pontos = 10
    elif dificuldade_atual == "MÉDIO":
        velocidade_jogador = 350
        tempo_recarga_tiro = 0.4
        vel_monstros_x = 250
        base_recarga_monstros = 1.0
        multiplicador_pontos = 20
    elif dificuldade_atual == "DIFÍCIL":
        velocidade_jogador = 200
        tempo_recarga_tiro = 0.7
        vel_monstros_x = 350
        base_recarga_monstros = 0.5
        multiplicador_pontos = 30

    # ================= JOGADOR, VIDA E PONTOS =================
    jogador = Sprite("spaceinvaders/sprites/jogador.png")
    jogador.x = (janela.width / 2) - (jogador.width / 2)
    jogador.y = janela.height - jogador.height - 20

    vidas = 3
    pontos = 0
    invencivel = False
    tempo_invencibilidade = 0

    # Controle de FPS (acumulador de 1 segundo para leitura estável na tela)
    relogio_fps = 0.0
    contador_frames = 0
    fps_atual = 0

    # ================= TIROS (JOGADOR E MONSTROS) =================
    tiros = []
    velocidade_tiro = 600
    cronometro_tiro = 0

    tiros_monstros = []
    velocidade_tiro_monstro = 400
    cronometro_tiros_monstros = 0
    tempo_recarga_atual_monstros = base_recarga_monstros 

    # ================= MATRIZ DE MONSTROS =================
    L = 4  
    C = 6  
    matriz_monstros = []
    
    temp_sprite = Sprite("spaceinvaders/sprites/monstro.png")
    largura_monstro = temp_sprite.width
    altura_monstro = temp_sprite.height
    
    espaco_x = largura_monstro / 2
    espaco_y = altura_monstro / 2
    
    largura_total_matriz = (C * largura_monstro) + ((C - 1) * espaco_x)
    offset_x_inicial = (janela.width / 2) - (largura_total_matriz / 2)
    offset_y_inicial = 60 
    
    for linha in range(L):
        linha_monstros = []
        for coluna in range(C):
            monstro = Sprite("spaceinvaders/sprites/monstro.png")
            monstro.x = offset_x_inicial + (coluna * (largura_monstro + espaco_x))
            monstro.y = offset_y_inicial + (linha * (altura_monstro + espaco_y))
            linha_monstros.append(monstro)
        matriz_monstros.append(linha_monstros)

    sentido_monstros = 1 
    game_over = False

    # ================= LOOP PRINCIPAL DO JOGO =================
    while True:
        janela.set_background_color((0, 0, 0))
        dt = janela.delta_time()
        
        # Cálculo estável do FPS
        relogio_fps += dt
        contador_frames += 1
        if relogio_fps >= 1.0:
            fps_atual = contador_frames
            contador_frames = 0
            relogio_fps = 0.0
        
        if not game_over:
            # ------------------ ESTADO DE INVENCIBILIDADE ------------------
            if invencivel:
                tempo_invencibilidade += dt
                if tempo_invencibilidade >= 2.0:
                    invencivel = False
                    tempo_invencibilidade = 0

            # ------------------ MOVIMENTO DO JOGADOR ------------------
            if teclado.key_pressed("LEFT"):
                jogador.x -= velocidade_jogador * dt
            if teclado.key_pressed("RIGHT"):
                jogador.x += velocidade_jogador * dt
                
            if jogador.x < 0:
                jogador.x = 0
            elif jogador.x > janela.width - jogador.width:
                jogador.x = janela.width - jogador.width
                
            # ------------------ LÓGICA DE TIROS (JOGADOR) ------------------
            cronometro_tiro += dt 
            if teclado.key_pressed("SPACE") and cronometro_tiro >= tempo_recarga_tiro:
                novo_tiro = Sprite("spaceinvaders/sprites/tiro.png")
                novo_tiro.x = jogador.x + (jogador.width / 2) - (novo_tiro.width / 2)
                novo_tiro.y = jogador.y - novo_tiro.height
                tiros.append(novo_tiro)
                cronometro_tiro = 0

            for tiro in tiros[:]:
                tiro.y -= velocidade_tiro * dt
                if tiro.y < -tiro.height:
                    tiros.remove(tiro)

            # ------------------ LÓGICA DOS MONSTROS E LIMITES DA ÁREA ------------------
            inverter_movimento = False
            monstros_vivos = []

            for linha in matriz_monstros:
                for monstro in linha:
                    monstros_vivos.append(monstro)
                    if (monstro.x <= 0 and sentido_monstros == -1) or \
                       (monstro.x + monstro.width >= janela.width and sentido_monstros == 1):
                        inverter_movimento = True
                        
            if inverter_movimento:
                sentido_monstros *= -1 
                for linha in matriz_monstros:
                    for monstro in linha:
                        monstro.y += altura_monstro 

            # Variáveis para guardar a caixa delimitadora (Bounding Box) do grupo de monstros
            min_x = janela.width
            max_x = 0
            min_y = janela.height
            max_y = 0

            for linha in matriz_monstros:
                for monstro in linha:
                    monstro.x += (vel_monstros_x * sentido_monstros) * dt
                    if monstro.y + monstro.height >= jogador.y:
                        game_over = True
                        
                    # Atualiza os limites extremos onde existem monstros vivos
                    if monstro.x < min_x:
                        min_x = monstro.x
                    if monstro.x + monstro.width > max_x:
                        max_x = monstro.x + monstro.width
                    if monstro.y < min_y:
                        min_y = monstro.y
                    if monstro.y + monstro.height > max_y:
                        max_y = monstro.y + monstro.height

            # ------------------ TIROS DOS MONSTROS ------------------
            cronometro_tiros_monstros += dt
            if monstros_vivos and cronometro_tiros_monstros >= tempo_recarga_atual_monstros:
                atirador = random.choice(monstros_vivos)
                tiro_m = Sprite("spaceinvaders/sprites/tiro.png")
                tiro_m.x = atirador.x + (atirador.width / 2) - (tiro_m.width / 2)
                tiro_m.y = atirador.y + atirador.height
                tiros_monstros.append(tiro_m)
                
                cronometro_tiros_monstros = 0
                tempo_recarga_atual_monstros = base_recarga_monstros * random.uniform(0.5, 1.5)

            # ------------------ COLISÃO: TIROS MONSTROS x JOGADOR ------------------
            for tiro_m in tiros_monstros[:]:
                tiro_m.y += velocidade_tiro_monstro * dt 
                
                if tiro_m.y > janela.height:
                    tiros_monstros.remove(tiro_m)
                elif tiro_m.collided(jogador) and not invencivel:
                    tiros_monstros.remove(tiro_m)
                    vidas -= 1
                    
                    if vidas <= 0:
                        return # Vidas zeradas: encerra a partida e retorna ao menu principal
                    else:
                        jogador.x = (janela.width / 2) - (jogador.width / 2)
                        invencivel = True
                        tempo_invencibilidade = 0

            # ------------------ COLISÃO OTIMIZADA: TIROS JOGADOR x MONSTROS ------------------
            for tiro in tiros[:]:
                # OTIMIZAÇÃO: Verifica se o tiro está FORA da área ocupada pelos monstros
                # 1. Abaixo do monstro mais baixo (tiro.y > max_y)
                # 2. Acima do monstro mais alto (tiro.y + tiro.height < min_y)
                # 3. À esquerda do monstro mais à esquerda (tiro.x + tiro.width < min_x)
                # 4. À direita do monstro mais à direita (tiro.x > max_x)
                if (tiro.y > max_y or 
                    tiro.y + tiro.height < min_y or 
                    tiro.x + tiro.width < min_x or 
                    tiro.x > max_x):
                    continue # Pula imediatamente todos os testes exaustivos para este tiro!

                # Teste exaustivo: só executa se o tiro já estiver infiltrado na área da matriz
                tiro_colidiu = False
                for linha in matriz_monstros:
                    for monstro in linha[:]: 
                        if tiro.collided(monstro):
                            linha.remove(monstro) 
                            pontos += multiplicador_pontos # Incrementa a pontuação
                            tiro_colidiu = True
                            break 
                    
                    if tiro_colidiu:
                        tiros.remove(tiro) 
                        break 

        # ------------------ DESENHO DOS ELEMENTOS ------------------
        if not invencivel or (int(tempo_invencibilidade * 10) % 2 == 0):
            jogador.draw()
        
        for tiro in tiros:
            tiro.draw()

        for tiro_m in tiros_monstros:
            tiro_m.draw()
            
        for linha in matriz_monstros:
            for monstro in linha:
                monstro.draw()
        
        # ------------------ HUD E INTERFACE ------------------
        # Canto superior esquerdo: Pontos, Vidas e Dificuldade
        janela.draw_text(f"Pontos: {pontos}", 10, 10, size=20, color=(255, 255, 0), bold=True)
        janela.draw_text(f"Vidas: {vidas}", 10, 35, size=20, color=(255, 50, 50), bold=True)
        janela.draw_text(f"Dificuldade: {dificuldade_atual}", 10, 60, size=16, color=(200, 200, 200))
        
        # Canto superior direito: FPS
        janela.draw_text(f"FPS: {fps_atual}", janela.width - 90, 10, size=18, color=(0, 255, 0), bold=True)
        
        if game_over:
            janela.draw_text("GAME OVER!", (janela.width / 2) - 150, janela.height / 2, size=50, color=(255, 0, 0), bold=True)
            janela.draw_text("Pressione ESC para voltar ao Menu", (janela.width / 2) - 180, (janela.height / 2) + 60, size=24, color=(255, 255, 255))

        if teclado.key_pressed("ESC"):
            return 

        janela.update()