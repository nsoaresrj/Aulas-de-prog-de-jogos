from PPlay.sprite import *
import random
import ranking

def criar_matriz(L, C, largura_janela):
    """Cria e retorna uma nova matriz de monstros centralizada."""
    matriz = []
    temp_sprite = Sprite("spaceinvaders/sprites/monstro.png")
    largura_m = temp_sprite.width
    altura_m = temp_sprite.height
    
    espaco_x = largura_m / 2
    espaco_y = altura_m / 2
    
    largura_total = (C * largura_m) + ((C - 1) * espaco_x)
    offset_x = (largura_janela / 2) - (largura_total / 2)
    offset_y = 60
    
    for linha in range(L):
        linha_monstros = []
        for coluna in range(C):
            monstro = Sprite("spaceinvaders/sprites/monstro.png")
            monstro.x = offset_x + (coluna * (largura_m + espaco_x))
            monstro.y = offset_y + (linha * (altura_m + espaco_y))
            linha_monstros.append(monstro)
        matriz.append(linha_monstros)
        
    return matriz, largura_m, altura_m


def configurar_dificuldade(indice_tier, sub_nivel):
    """
    Retorna os atributos do jogo com base na categoria (Fácil, Médio, Difícil, Extremo)
    e no subnível atual (1, 2 ou 3).
    """
    nomes_tiers = ["FÁCIL", "MÉDIO", "DIFÍCIL", "EXTREMO"]
    nome_tier = nomes_tiers[min(indice_tier, 3)]
    nome_completo = f"{nome_tier} {sub_nivel}"
    
    # Fator de progressão interna do subnível (0 para nível 1, 1 para nível 2, 2 para nível 3)
    passo = sub_nivel - 1

    if indice_tier == 0:  # FÁCIL 1, 2, 3
        velocidade_jogador = 500
        tempo_recarga_tiro = 0.22
        vel_monstros_x = 130 + (passo * 30)          # 130 -> 160 -> 190
        base_recarga_monstros = 1.6 - (passo * 0.2)  # 1.6s -> 1.4s -> 1.2s
        multiplicador_pontos = 10
        
    elif indice_tier == 1:  # MÉDIO 1, 2, 3
        velocidade_jogador = 380
        tempo_recarga_tiro = 0.38
        vel_monstros_x = 220 + (passo * 35)          # 220 -> 255 -> 290
        base_recarga_monstros = 1.0 - (passo * 0.12) # 1.0s -> 0.88s -> 0.76s
        multiplicador_pontos = 20
        
    elif indice_tier == 2:  # DIFÍCIL 1, 2, 3
        velocidade_jogador = 260
        tempo_recarga_tiro = 0.55
        vel_monstros_x = 330 + (passo * 40)          # 330 -> 370 -> 410
        base_recarga_monstros = 0.65 - (passo * 0.1) # 0.65s -> 0.55s -> 0.45s
        multiplicador_pontos = 30
        
    else:  # EXTREMO 1, 2, 3... (Caso o jogador passe do Difícil 3)
        velocidade_jogador = 250
        tempo_recarga_tiro = 0.55
        vel_monstros_x = 450 + (passo * 45)
        base_recarga_monstros = max(0.2, 0.35 - (passo * 0.03))
        multiplicador_pontos = 50

    return (nome_completo, velocidade_jogador, tempo_recarga_tiro, 
            vel_monstros_x, base_recarga_monstros, multiplicador_pontos)


def executar(janela, teclado, dificuldade_inicial):
    
    # Define o índice inicial a partir da escolha no menu
    mapa_inicial = {"FÁCIL": 0, "MÉDIO": 1, "DIFÍCIL": 2}
    indice_tier = mapa_inicial.get(dificuldade_inicial, 0)
    sub_nivel = 1

    (nome_dificuldade, velocidade_jogador, tempo_recarga_tiro, 
     vel_monstros_x, base_recarga_monstros, multiplicador_pontos) = configurar_dificuldade(indice_tier, sub_nivel)

    # ================= JOGADOR, VIDA, PONTOS E TEMPO =================
    jogador = Sprite("spaceinvaders/sprites/jogador.png")
    jogador.x = (janela.width / 2) - (jogador.width / 2)
    jogador.y = janela.height - jogador.height - 20

    vidas = 3
    pontos = 0
    invencivel = False
    tempo_invencibilidade = 0

    # Variáveis do Bônus de Tempo
    tempo_fase = 0.0
    ultimo_bonus = 0
    timer_aviso_bonus = 0.0

    relogio_fps = 0.0
    contador_frames = 0
    fps_atual = 0

    # ================= TIROS =================
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
    matriz_monstros, largura_monstro, altura_monstro = criar_matriz(L, C, janela.width)
    sentido_monstros = 1 

    # ================= LOOP PRINCIPAL DO JOGO =================
    while True:
        janela.set_background_color((0, 0, 0))
        dt = janela.delta_time()
        
        # Contabiliza o tempo gasto na fase atual
        tempo_fase += dt
        if timer_aviso_bonus > 0:
            timer_aviso_bonus -= dt
        
        relogio_fps += dt
        contador_frames += 1
        if relogio_fps >= 1.0:
            fps_atual = contador_frames
            contador_frames = 0
            relogio_fps = 0.0
        
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

        # ------------------ LÓGICA DOS MONSTROS E MUDANÇA DE FASE ------------------
        inverter_movimento = False
        monstros_vivos = []

        for linha in matriz_monstros:
            for monstro in linha:
                monstros_vivos.append(monstro)
                if (monstro.x <= 0 and sentido_monstros == -1) or \
                   (monstro.x + monstro.width >= janela.width and sentido_monstros == 1):
                    inverter_movimento = True

        # MUDANÇA DE FASE: Todos os monstros foram destruídos
        if len(monstros_vivos) == 0:
            # 1. Cálculo do Bônus de Tempo (meta base de 45 segundos; mínimo garantido de 50 pts)
            fator_dificuldade = indice_tier + 1
            tempo_economizado = max(0.0, 45.0 - tempo_fase)
            ultimo_bonus = max(50, int(tempo_economizado * 20 * fator_dificuldade))
            pontos += ultimo_bonus
            timer_aviso_bonus = 2.5  # Exibe o bônus na tela por 2.5 segundos
            tempo_fase = 0.0         # Zera o cronômetro para a nova fase

            # 2. Progressão de Dificuldade (1 -> 2 -> 3 -> Próxima Dificuldade 1)
            sub_nivel += 1
            if sub_nivel > 3 and indice_tier < 3:
                indice_tier += 1
                sub_nivel = 1

            (nome_dificuldade, velocidade_jogador, tempo_recarga_tiro, 
             vel_monstros_x, base_recarga_monstros, multiplicador_pontos) = configurar_dificuldade(indice_tier, sub_nivel)
            
            # 3. Reinicia a horda e limpa projéteis antigos da tela
            tiros.clear()
            tiros_monstros.clear()
            matriz_monstros, largura_monstro, altura_monstro = criar_matriz(L, C, janela.width)
            sentido_monstros = 1
            continue

        if inverter_movimento:
            sentido_monstros *= -1 
            for linha in matriz_monstros:
                for monstro in linha:
                    monstro.y += altura_monstro 

        min_x = janela.width
        max_x = 0
        min_y = janela.height
        max_y = 0

        for linha in matriz_monstros:
            for monstro in linha:
                monstro.x += (vel_monstros_x * sentido_monstros) * dt
                
                if monstro.y + monstro.height >= jogador.y:
                    ranking.salvar(janela, pontos)
                    return
                    
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
                    ranking.salvar(janela, pontos)
                    return
                else:
                    jogador.x = (janela.width / 2) - (jogador.width / 2)
                    invencivel = True
                    tempo_invencibilidade = 0

        # ------------------ COLISÃO OTIMIZADA: TIROS JOGADOR x MONSTROS ------------------
        for tiro in tiros[:]:
            if (tiro.y > max_y or 
                tiro.y + tiro.height < min_y or 
                tiro.x + tiro.width < min_x or 
                tiro.x > max_x):
                continue

            tiro_colidiu = False
            for linha in matriz_monstros:
                for monstro in linha[:]: 
                    if tiro.collided(monstro):
                        linha.remove(monstro) 
                        pontos += multiplicador_pontos
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
        janela.draw_text(f"Pontos: {pontos}", 10, 10, size=20, color=(255, 255, 0), bold=True)
        janela.draw_text(f"Vidas: {vidas}", 10, 35, size=20, color=(255, 50, 50), bold=True)
        janela.draw_text(f"Nivel: {nome_dificuldade}", 10, 60, size=16, color=(0, 255, 255), bold=True)
        janela.draw_text(f"Tempo: {tempo_fase:.1f}s", 10, 82, size=16, color=(200, 200, 200))
        janela.draw_text(f"FPS: {fps_atual}", janela.width - 90, 10, size=18, color=(0, 255, 0), bold=True)

        # Exibe mensagem de bônus no topo central quando o jogador passa de fase
        if timer_aviso_bonus > 0:
            janela.draw_text(f"FASE CONCLUIDA! Bonus de Tempo: +{ultimo_bonus} pts", 
                             (janela.width / 2) - 210, 20, size=20, color=(50, 255, 50), bold=True)

        if teclado.key_pressed("ESC"):
            return 

        janela.update()
