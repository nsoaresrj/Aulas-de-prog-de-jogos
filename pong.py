from PPlay.window import Window
from PPlay.sprite import Sprite

# --- CONFIGURAÇÃO DA JANELA ---
janela = Window(700, 500)
janela.set_title("Pong - Versão Final")
teclado = janela.get_keyboard() # Prepara a leitura do teclado

# --- VARIÁVEIS DE PLACAR E ESTADO ---
placar_ia = 0
placar_jogador = 0
esperando_espaco = True # Controla se o jogo está pausado aguardando o ESPAÇO

# --- CONFIGURAÇÃO DA BOLINHA ---
bolinha = Sprite("bolinha.png")
bolinha.x = (janela.width / 2) - (bolinha.width / 2)
bolinha.y = (janela.height / 2) - (bolinha.height / 2)

vel_bola_x = 350 # Velocidade com delta_time
vel_bola_y = 350

# --- CONFIGURAÇÃO DAS BARRINHAS ---
vel_barras = 400
vel_ia = 320 # IA um pouco mais lenta que a bolinha para não ser invencível

# IA (Esquerda)
barra_ia = Sprite("pad.png")
barra_ia.x = 10
barra_ia.y = (janela.height / 2) - (barra_ia.height / 2)

# Jogador (Direita)
barra_jogador = Sprite("pad.png")
barra_jogador.x = janela.width - barra_jogador.width - 10
barra_jogador.y = (janela.height / 2) - (barra_jogador.height / 2)

# --- GAME LOOP ---
while True:
    janela.set_background_color((0, 0, 139))
    
    # === DESENHA O PLACAR ===
    # Parâmetros: Texto, X, Y, Tamanho, Cor(RGB)
    texto_placar = str(placar_ia) + " - " + str(placar_jogador)
    janela.draw_text(texto_placar, (janela.width / 2) - 30, 20, size=40, color=(255, 255, 255))

    # === VERIFICA SE ESTÁ ESPERANDO O ESPAÇO ===
    if esperando_espaco:
        janela.draw_text("Pressione ESPAÇO para iniciar", (janela.width / 2) - 150, (janela.height / 2) + 50, size=20, color=(255, 255, 0))
        
        # Se apertar espaço, o jogo começa
        if teclado.key_pressed("SPACE"):
            esperando_espaco = False
    
    # === SE NÃO ESTIVER ESPERANDO, O JOGO RODA NORMALMENTE ===
    else:
        # 1. Movimentação da Bolinha (com delta_time)
        bolinha.x += vel_bola_x * janela.delta_time()
        bolinha.y += vel_bola_y * janela.delta_time()

        # 2. Movimentação do Jogador (Setas)
        if teclado.key_pressed("UP") and barra_jogador.y > 0:
            barra_jogador.y -= vel_barras * janela.delta_time()
        if teclado.key_pressed("DOWN") and barra_jogador.y + barra_jogador.height < janela.height:
            barra_jogador.y += vel_barras * janela.delta_time()

        # 3. Movimentação da IA "Inteligente" (Segue o eixo Y da bola)
        meio_bolinha = bolinha.y + (bolinha.height / 2)
        meio_ia = barra_ia.y + (barra_ia.height / 2)
        
        if meio_bolinha < meio_ia and barra_ia.y > 0:
            barra_ia.y -= vel_ia * janela.delta_time()
        elif meio_bolinha > meio_ia and barra_ia.y + barra_ia.height < janela.height:
            barra_ia.y += vel_ia * janela.delta_time()

        # 4. Colisão com Teto e Chão (Proteção contra Glitch)
        if bolinha.y < 0:
            bolinha.y = 0
            vel_bola_y = -vel_bola_y
        elif bolinha.y + bolinha.height > janela.height:
            bolinha.y = janela.height - bolinha.height
            vel_bola_y = -vel_bola_y

        # 5. Colisão com as Barras (Pads)
        if bolinha.collided(barra_ia):
            bolinha.x = barra_ia.x + barra_ia.width # Expulsa a bolinha pra direita
            vel_bola_x = -vel_bola_x
        elif bolinha.collided(barra_jogador):
            bolinha.x = barra_jogador.x - bolinha.width # Expulsa a bolinha pra esquerda
            vel_bola_x = -vel_bola_x

        # 6. GOLS E PONTUAÇÃO (Saiu pela esquerda ou direita)
        if bolinha.x < 0: # Jogador fez gol
            placar_jogador += 1
            esperando_espaco = True # Pausa o jogo
        elif bolinha.x + bolinha.width > janela.width: # IA fez gol
            placar_ia += 1
            esperando_espaco = True # Pausa o jogo
            
        # Se houve gol, centraliza a bola imediatamente e reseta a velocidade
        if esperando_espaco:
            bolinha.x = (janela.width / 2) - (bolinha.width / 2)
            bolinha.y = (janela.height / 2) - (bolinha.height / 2)
            # Para evitar que a bola fique impossível, podemos resetar a velocidade original aqui
            vel_bola_x = 350 if vel_bola_x > 0 else -350
            vel_bola_y = 350 if vel_bola_y > 0 else -350

    # === DESENHANDO OS ELEMENTOS ===
    # Isso fica fora do "else", pois queremos desenhar as barras e a bola mesmo pausados
    barra_ia.draw()
    barra_jogador.draw()
    bolinha.draw()

    janela.update()

