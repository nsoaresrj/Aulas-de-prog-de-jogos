from PPlay.window import Window
from PPlay.sprite import Sprite

# --- CONFIGURAÇÃO DA JANELA ---
janela = Window(700, 500)
janela.set_title("Pong - IA na Direita")
teclado = janela.get_keyboard()

# --- VARIÁVEIS DE PLACAR E ESTADO ---
placar_jogador = 0 # Jogador agora fica na esquerda
placar_ia = 0      # IA agora fica na direita
esperando_espaco = True 

# --- CONFIGURAÇÃO DA BOLINHA ---
bolinha = Sprite("bolinha.png")
bolinha.x = (janela.width / 2) - (bolinha.width / 2)
bolinha.y = (janela.height / 2) - (bolinha.height / 2)

vel_bola_x = 350 
vel_bola_y = 350

# --- CONFIGURAÇÃO DAS BARRINHAS ---
vel_barras = 400
vel_ia = 220 

# Jogador (AGORA NA ESQUERDA)
barra_jogador = Sprite("pad.png")
barra_jogador.x = 10
barra_jogador.y = (janela.height / 2) - (barra_jogador.height / 2)

# IA (AGORA NA DIREITA)
barra_ia = Sprite("pad.png")
barra_ia.x = janela.width - barra_ia.width - 10
barra_ia.y = (janela.height / 2) - (barra_ia.height / 2)

# --- GAME LOOP ---
while True:
    janela.set_background_color((0, 0, 139))
    
    # === DESENHA O PLACAR ===
    # Coloquei o placar_jogador primeiro para refletir o lado esquerdo
    texto_placar = str(placar_jogador) + " - " + str(placar_ia)
    janela.draw_text(texto_placar, (janela.width / 2) - 30, 20, size=40, color=(255, 255, 255))

    # === VERIFICA SE ESTÁ ESPERANDO O ESPAÇO ===
    if esperando_espaco:
        janela.draw_text("Pressione ESPAÇO para iniciar", (janela.width / 2) - 150, (janela.height / 2) + 50, size=20, color=(255, 255, 0))
        
        if teclado.key_pressed("SPACE"):
            esperando_espaco = False
    
    # === SE NÃO ESTIVER ESPERANDO, O JOGO RODA NORMALMENTE ===
    else:
        # 1. Movimentação da Bolinha
        bolinha.x += vel_bola_x * janela.delta_time()
        bolinha.y += vel_bola_y * janela.delta_time()

        # 2. Movimentação do Jogador (Setas)
        if teclado.key_pressed("UP") and barra_jogador.y > 0:
            barra_jogador.y -= vel_barras * janela.delta_time()
        if teclado.key_pressed("DOWN") and barra_jogador.y + barra_jogador.height < janela.height:
            barra_jogador.y += vel_barras * janela.delta_time()

        # 3. Movimentação da IA (PREDITIVA PARA A DIREITA)
        alvo_y = barra_ia.y 

        # Mudamos a condição: a IA prevê quando a bola vai para a DIREITA (> 0)
        if vel_bola_x > 0: 
            # A distância agora é a posição da barra menos a posição da frente da bola
            distancia_x = barra_ia.x - (bolinha.x + bolinha.width)
            tempo_impacto = distancia_x / vel_bola_x
            
            # Cálculo de Y continua o mesmo
            destino_y = bolinha.y + (vel_bola_y * tempo_impacto)
            
            limite_y = janela.height - bolinha.height
            while destino_y < 0 or destino_y > limite_y:
                if destino_y < 0:
                    destino_y = abs(destino_y) 
                elif destino_y > limite_y:
                    destino_y = (2 * limite_y) - destino_y 
            
            alvo_y = destino_y - (barra_ia.height / 2)
        else:
            # Se a bola está indo para o jogador, a IA volta pro meio
            alvo_y = (janela.height / 2) - (barra_ia.height / 2)

        if barra_ia.y < alvo_y - 5 and barra_ia.y + barra_ia.height < janela.height:
            barra_ia.y += vel_ia * janela.delta_time()
        elif barra_ia.y > alvo_y + 5 and barra_ia.y > 0:
            barra_ia.y -= vel_ia * janela.delta_time()

        # 4. Colisão com Teto e Chão
        if bolinha.y < 0:
            bolinha.y = 0
            vel_bola_y = -vel_bola_y
        elif bolinha.y + bolinha.height > janela.height:
            bolinha.y = janela.height - bolinha.height
            vel_bola_y = -vel_bola_y

        # 5. Colisão com as Barras (INVERTIDAS)
        if bolinha.collided(barra_jogador):
            bolinha.x = barra_jogador.x + barra_jogador.width # Jogador expulsa pra direita
            vel_bola_x = -vel_bola_x
        elif bolinha.collided(barra_ia):
            bolinha.x = barra_ia.x - bolinha.width # IA expulsa pra esquerda
            vel_bola_x = -vel_bola_x

        # 6. GOLS E PONTUAÇÃO (INVERTIDOS)
        if bolinha.x < 0: # Saiu pelo lado esquerdo -> IA fez gol
            placar_ia += 1
            esperando_espaco = True
        elif bolinha.x + bolinha.width > janela.width: # Saiu pelo lado direito -> Jogador fez gol
            placar_jogador += 1
            esperando_espaco = True
            
        # Reseta o jogo
        if esperando_espaco:
            bolinha.x = (janela.width / 2) - (bolinha.width / 2)
            bolinha.y = (janela.height / 2) - (bolinha.height / 2)
            vel_bola_x = 350 if vel_bola_x > 0 else -350
            vel_bola_y = 350 if vel_bola_y > 0 else -350

    # === DESENHANDO OS ELEMENTOS ===
    barra_ia.draw()
    barra_jogador.draw()
    bolinha.draw()

    janela.update()


