from PPlay.sprite import *
import random
import ranking

# =====================================================================
# BLOCO 1: CRIAÇÃO DA MATRIZ DE MONSTROS
# Gera uma grade de monstros (L linhas por C colunas) centralizada na tela.
# [COMO ALTERAR]: Para mudar a distância entre os monstros, altere 'espaco_x' e 'espaco_y'.
# Para os monstros começarem mais para baixo ou mais para cima, altere 'offset_y = 60'.
# =====================================================================
def criar_matriz(L, C, largura_janela):
    """Cria e retorna uma nova matriz de monstros centralizada."""
    matriz = []
    
    # Carrega um sprite temporário apenas para medir a largura e altura da imagem do monstro
    temp_sprite = Sprite("spaceinvaders/sprites/monstro.png")
    largura_m = temp_sprite.width
    altura_m = temp_sprite.height
    
    # Define o espaço vazio entre um monstro e outro (metade do tamanho do monstro)
    espaco_x = largura_m / 2
    espaco_y = altura_m / 2
    
    # Calcula a largura total que o bloco inteiro de monstros vai ocupar para centralizá-lo
    largura_total = (C * largura_m) + ((C - 1) * espaco_x)
    offset_x = (largura_janela / 2) - (largura_total / 2)
    offset_y = 60 # Distância do topo da janela até a primeira fileira de monstros
    
    # Preenche as linhas e colunas posicionando cada monstro na sua coordenada X e Y
    for linha in range(L):
        linha_monstros = []
        for coluna in range(C):
            monstro = Sprite("spaceinvaders/sprites/monstro.png")
            monstro.x = offset_x + (coluna * (largura_m + espaco_x))
            monstro.y = offset_y + (linha * (altura_m + espaco_y))
            linha_monstros.append(monstro)
        matriz.append(linha_monstros)
        
    return matriz, largura_m, altura_m


# =====================================================================
# BLOCO 2: BALANCEAMENTO E PROGRESSÃO DE DIFICULDADE
# Controla os status de cada Tier (0=Fácil, 1=Médio, 2=Difícil, 3=Extremo)
# e de cada subnível (1, 2 ou 3).
# [COMO ALTERAR]: Ajuste os números abaixo para deixar a nave mais rápida, 
# o tiro mais rápido (diminuindo 'tempo_recarga_tiro') ou dar mais pontos por abate.
# =====================================================================
def configurar_dificuldade(indice_tier, sub_nivel):
    nomes_tiers = ["FÁCIL", "MÉDIO", "DIFÍCIL", "EXTREMO"]
    nome_tier = nomes_tiers[min(indice_tier, 3)]
    nome_completo = f"{nome_tier} {sub_nivel}"
    
    # 'passo' vale 0 no subnível 1, 1 no subnível 2, e 2 no subnível 3.
    # Ele serve para aumentar a velocidade dos monstros gradualmente dentro do mesmo Tier.
    passo = sub_nivel - 1

    if indice_tier == 0:  # FÁCIL 1, 2, 3
        velocidade_jogador = 500                     # Velocidade da nave (pixels por segundo)
        tempo_recarga_tiro = 0.22                    # Cooldown do tiro do jogador (em segundos)
        vel_monstros_x = 130 + (passo * 30)          # Velocidade lateral dos monstros: 130 -> 160 -> 190
        base_recarga_monstros = 1.6 - (passo * 0.2)  # Cooldown de tiro inimigo: 1.6s -> 1.4s -> 1.2s
        multiplicador_pontos = 10                    # Pontos ganhos por cada monstro destruído
        
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


# =====================================================================
# BLOCO 3: PREPARAÇÃO DA PARTIDA (VARIÁVEIS INICIAIS)aa
# =====================================================================
def executar(janela, teclado, dificuldade_inicial):
    
    # Converte o texto vindo do menu ("FÁCIL", "MÉDIO", "DIFÍCIL") para número (0, 1 ou 2)
    mapa_inicial = {"FÁCIL": 0, "MÉDIO": 1, "DIFÍCIL": 2}
    indice_tier = mapa_inicial.get(dificuldade_inicial, 0)
    sub_nivel = 1

    # Carrega os atributos iniciais da dificuldade escolhida
    (nome_dificuldade, velocidade_jogador, tempo_recarga_tiro, 
     vel_monstros_x, base_recarga_monstros, multiplicador_pontos) = configurar_dificuldade(indice_tier, sub_nivel)

    # --- Posicionamento Inicial do Jogador ---
    jogador = Sprite("spaceinvaders/sprites/jogador.png")
    jogador.x = (janela.width / 2) - (jogador.width / 2)
    jogador.y = janela.height - jogador.height - 20 # Fica a 20 pixels de distância da borda inferior

    # --- Atributos do Jogador ---
    # [COMO ALTERAR]: Mude 'vidas = 3' para alterar com quantas vidas o jogador começa.
    vidas = 3
    pontos = 0
    invencivel = False
    tempo_invencibilidade = 0.0

    # --- Cronômetros de Fase e FPS ---
    tempo_fase = 0.0
    ultimo_bonus = 0
    timer_aviso_bonus = 0.0

    relogio_fps = 0.0
    contador_frames = 0
    fps_atual = 0

    # --- Configuração dos Tiros (Jogador e Monstros) ---
    # [COMO ALTERAR]: Mude 'velocidade_tiro' ou 'velocidade_tiro_monstro' para acelerar os projéteis.
    tiros = []
    velocidade_tiro = 600
    cronometro_tiro = 0.0

    tiros_monstros = []
    velocidade_tiro_monstro = 400
    cronometro_tiros_monstros = 0.0
    tempo_recarga_atual_monstros = base_recarga_monstros 

    # --- Tamanho da Matriz de Monstros ---
    # [COMO ALTERAR]: Mude L (Linhas) e C (Colunas) para ter mais ou menos monstros por fase.
    L = 4  
    C = 6  
    matriz_monstros, largura_monstro, altura_monstro = criar_matriz(L, C, janela.width)
    sentido_monstros = 1 # 1 = movendo para a direita | -1 = movendo para a esquerda

    # [NOVO] Variaveis do Monstro Especial
    monstro_especial = None
    tempo_piscar_especial = 0.0


    # =====================================================================
    # BLOCO 4: LOOP PRINCIPAL DA PARTIDA (RODA A CADA FRAME)
    # =====================================================================
    while True:
        janela.set_background_color((0, 0, 0))
        dt = janela.delta_time() # Tempo exato (em segundos) que demorou entre o último frame e este
        
        # --- 4.1: Atualização de Relógios (Tempo da Fase e FPS) ---
        tempo_fase += dt
        if timer_aviso_bonus > 0:
            timer_aviso_bonus -= dt
        
        relogio_fps += dt
        contador_frames += 1
        if relogio_fps >= 1.0: # Atualiza o número do FPS na tela a cada 1 segundo completo
            fps_atual = contador_frames
            contador_frames = 0
            relogio_fps = 0.0

            tempo_fase += dt
            tempo_piscar_especial += dt # Atualiza o tempo do monstro especial 
        
        # --- 4.2: Controle de Invencibilidade (Quando o jogador toma dano) ---
        # [COMO ALTERAR]: Mude '2.0' se quiser que o jogador fique invencível por mais ou menos segundos.
        if invencivel:
            tempo_invencibilidade += dt
            if tempo_invencibilidade >= 2.0:
                invencivel = False
                tempo_invencibilidade = 0.0

        # --- 4.3: Movimento do Jogador e Limites da Tela ---
        if teclado.key_pressed("LEFT"):
            jogador.x -= velocidade_jogador * dt
        if teclado.key_pressed("RIGHT"):
            jogador.x += velocidade_jogador * dt
            
        # Impede que a nave saia pelas laterais da janela
        if jogador.x < 0:
            jogador.x = 0
        elif jogador.x > janela.width - jogador.width:
            jogador.x = janela.width - jogador.width
            
        # --- 4.4: Disparo e Movimento dos Tiros do Jogador ---
        cronometro_tiro += dt 
        if teclado.key_pressed("SPACE") and cronometro_tiro >= tempo_recarga_tiro:
            novo_tiro = Sprite("spaceinvaders/sprites/tiro.png")
            # Posiciona o tiro saindo exatamente do meio superior da nave
            novo_tiro.x = jogador.x + (jogador.width / 2) - (novo_tiro.width / 2)
            novo_tiro.y = jogador.y - novo_tiro.height
            tiros.append(novo_tiro)
            cronometro_tiro = 0.0

        # Move todos os tiros para cima e apaga os que já saíram pelo topo da tela
        for tiro in tiros[:]:
            tiro.y -= velocidade_tiro * dt
            if tiro.y < -tiro.height:
                tiros.remove(tiro)

        # --- 4.5: Verificação dos Monstros Vivos e Mudança de Fase ---
        inverter_movimento = False
        monstros_vivos = []

        # Passa por toda a matriz guardando quem está vivo e checando se alguém bateu na parede lateral
        for linha in matriz_monstros:
            for monstro in linha:
                monstros_vivos.append(monstro)
                if (monstro.x <= 0 and sentido_monstros == -1) or \
                   (monstro.x + monstro.width >= janela.width and sentido_monstros == 1):
                    inverter_movimento = True

        # [NOVO] Se ainda não há um monstro especial (início do jogo, nova fase ou o anterior morreu), sorteia outro!
        if (monstro_especial is None or monstro_especial not in monstros_vivos) and len(monstros_vivos) > 0:
            monstro_especial = random.choice(monstros_vivos)
            
            # Pinta a imagem desse monstro de Vermelho/Laranja automaticamente (sem precisar de outro PNG)
            monstro_especial.image = monstro_especial.image.copy()
            monstro_especial.image.fill((255, 80, 80), special_flags=3) # 3 = BLEND_RGB_MULT (tinge a cor)

        # Se não há mais nenhum monstro vivo, a fase terminou!
        if len(monstros_vivos) == 0:
            # A) Cálculo do Bônus de Tempo (Quanto menor que 45s for o tempo gasto, maior o bônus)
            fator_dificuldade = indice_tier + 1
            tempo_economizado = max(0.0, 45.0 - tempo_fase)
            ultimo_bonus = max(50, int(tempo_economizado * 20 * fator_dificuldade))
            pontos += ultimo_bonus
            timer_aviso_bonus = 2.5  # Mostra mensagem de bônus por 2.5 segundos
            tempo_fase = 0.0         # Zera o relógio para a nova fase
            monstro_especial = None        # Remove o monstro especial da fase anterior
            # B) Progressão de Nível (Ex: Fácil 1 -> Fácil 2 -> Fácil 3 -> Médio 1)
            tier_antigo = indice_tier
            sub_nivel += 1
            if sub_nivel > 3 and indice_tier < 3:
                indice_tier += 1
                sub_nivel = 1
            
            # C) Recompensa de Vida ao mudar de Tier (Ex: saiu do Fácil 3 para o Médio 1)
            if indice_tier > tier_antigo:
                vidas += 1
                # [COMO ALTERAR]: Descomente a linha abaixo se quiser limitar o máximo de vidas (ex: 5)
                # vidas = min(vidas, 5)

            # D) Atualiza velocidades e recria a matriz de monstros para a nova fase
            (nome_dificuldade, velocidade_jogador, tempo_recarga_tiro, 
             vel_monstros_x, base_recarga_monstros, multiplicador_pontos) = configurar_dificuldade(indice_tier, sub_nivel)
            
            tiros.clear()
            tiros_monstros.clear()
            matriz_monstros, largura_monstro, altura_monstro = criar_matriz(L, C, janela.width)
            sentido_monstros = 1
            continue

        # --- 4.6: Movimento da Matriz e Cálculo da Bounding Box (Área de Colisão) ---
        # Se algum monstro tocou na borda da tela, inverte a direção e desce uma linha
        if inverter_movimento:
            sentido_monstros *= -1 
            for linha in matriz_monstros:
                for monstro in linha:
                    monstro.y += altura_monstro # [COMO ALTERAR]: Mude aqui para descer mais ou menos pixels

        # Variáveis para encontrar o retângulo (Bounding Box) que envolve todos os monstros vivos
        min_x = janela.width
        max_x = 0
        min_y = janela.height
        max_y = 0

        for linha in matriz_monstros:
            for monstro in linha:
                # Move o monstro horizontalmente
                monstro.x += (vel_monstros_x * sentido_monstros) * dt
                
                # DERROTA POR INVASÃO: Se algum monstro encostar na altura da nave do jogador, fim de jogo!
                if monstro.y + monstro.height >= jogador.y:
                    ranking.salvar(janela, pontos)
                    return
                
                # Atualiza as bordas esquerda (min_x), direita (max_x), topo (min_y) e base (max_y) do grupo
                if monstro.x < min_x:
                    min_x = monstro.x
                if monstro.x + monstro.width > max_x:
                    max_x = monstro.x + monstro.width
                if monstro.y < min_y:
                    min_y = monstro.y
                if monstro.y + monstro.height > max_y:
                    max_y = monstro.y + monstro.height

        # --- 4.7: Disparo Aleatório dos Monstros ---
        cronometro_tiros_monstros += dt
        if monstros_vivos and cronometro_tiros_monstros >= tempo_recarga_atual_monstros:
            # Sorteia um monstro qualquer dentre os que estão vivos para atirar
            atirador = random.choice(monstros_vivos)
            tiro_m = Sprite("spaceinvaders/sprites/tiro_monstro.png")
            tiro_m.x = atirador.x + (atirador.width / 2) - (tiro_m.width / 2)
            tiro_m.y = atirador.y + atirador.height
            tiros_monstros.append(tiro_m)
            
            cronometro_tiros_monstros = 0.0
            # Escalona o tempo do próximo tiro aleatoriamente entre 50% (0.5) e 150% (1.5) do tempo base
            tempo_recarga_atual_monstros = base_recarga_monstros * random.uniform(0.5, 1.5)

        # --- 4.8: Colisão dos Tiros dos Monstros contra o Jogador ---
        for tiro_m in tiros_monstros[:]:
            tiro_m.y += velocidade_tiro_monstro * dt 
            
            # Remove o tiro se ele passar do fundo da tela
            if tiro_m.y > janela.height:
                tiros_monstros.remove(tiro_m)
                
            # Verifica se acertou o jogador (apenas se o jogador NÃO estiver piscando/invencível)
            elif tiro_m.collided(jogador) and not invencivel:
                tiros_monstros.remove(tiro_m)
                vidas -= 1
                
                # DERROTA POR VIDAS ZERADAS: Salva no ranking e volta ao menu
                if vidas <= 0:
                    ranking.salvar(janela, pontos)
                    return
                else:
                    # Se ainda tem vidas, volta para o meio da tela e fica invencível por 2 segundos
                    jogador.x = (janela.width / 2) - (jogador.width / 2)
                    invencivel = True
                    tempo_invencibilidade = 0.0

  # --- 4.9: Colisão Otimizada (Tiros do Jogador contra os Monstros) ---
        for tiro in tiros[:]:
            # OTIMIZAÇÃO (Bounding Box)
            if (tiro.y > max_y or 
                tiro.y + tiro.height < min_y or 
                tiro.x + tiro.width < min_x or 
                tiro.x > max_x):
                continue

            tiro_colidiu = False
            for linha in matriz_monstros:
                for monstro in linha[:]: 
                    if tiro.collided(monstro):
                        
                        # Verifica se acertou o Monstro Especial
                        if monstro == monstro_especial:
                            qtd_na_linha = len(linha)
                            pontos += qtd_na_linha * multiplicador_pontos
                            linha.clear()
                            monstro_especial = None
                        else:
                            linha.remove(monstro) 
                            pontos += multiplicador_pontos
                            
                        tiro_colidiu = True
                        break 
                
                if tiro_colidiu:
                    tiros.remove(tiro) 
                    break
        # =====================================================================
        # BLOCO 5: DESENHO NA TELA (RENDERIZAÇÃO E INTERFACE HUD)
        # =====================================================================
        # Efeito de piscar: quando invencível, alterna entre desenhar e não desenhar a cada 0.1s
        if not invencivel or (int(tempo_invencibilidade * 10) % 2 == 0):
            jogador.draw()
        
        for tiro in tiros:
            tiro.draw()

        for tiro_m in tiros_monstros:
            tiro_m.draw()
            
        # Substitua o for de desenho dos monstros por este:
        for linha in matriz_monstros:
            for monstro in linha:
                # [NOVO] Se for o monstro especial, ele pisca rápidamente (alterna a cada 0.1s)
                if monstro == monstro_especial:
                    if int(tempo_piscar_especial * 10) % 2 == 0:
                        monstro.draw()
                else:
                    monstro.draw() # Monstros normais são desenhados sempre
        
        # --- Textos da Interface (HUD) ---
        # [COMO ALTERAR]: Os parâmetros são (Texto, Posição X, Posição Y, size=Tamanho, color=(R,G,B))
        janela.draw_text(f"Pontos: {pontos}", 10, 10, size=20, color=(255, 255, 0), bold=True)
        janela.draw_text(f"Vidas: {vidas}", 10, 35, size=20, color=(255, 50, 50), bold=True)
        janela.draw_text(f"Nivel: {nome_dificuldade}", 10, 60, size=16, color=(0, 255, 255), bold=True)
        janela.draw_text(f"Tempo: {tempo_fase:.1f}s", 10, 82, size=16, color=(200, 200, 200))
        janela.draw_text(f"FPS: {fps_atual}", janela.width - 90, 10, size=18, color=(0, 255, 0), bold=True)

        # Aviso temporário de bônus ao limpar uma fase
        if timer_aviso_bonus > 0:
            janela.draw_text(f"FASE CONCLUIDA! Bonus de Tempo: +{ultimo_bonus} pts", 
                             (janela.width / 2) - 210, 20, size=20, color=(50, 255, 50), bold=True)

        # Tecla de saída rápida (volta ao menu sem salvar pontuação)
        if teclado.key_pressed("ESC"):
            return 

        janela.update()
