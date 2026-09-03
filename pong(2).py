from PPlay.window import Window
from PPlay.sprite import Sprite

# --- CONFIGURAÇÃO DA JANELA ---
janela = Window(700, 500)
janela.set_title("Pong - IA Mais Justa")
teclado = janela.get_keyboard()

# --- VARIÁVEIS DE PLACAR E ESTADO ---
placar_jogador = 0 
placar_ia = 0      
esperando_espaco = True 

# --- CONFIGURAÇÃO DA BOLINHA ---
bolinha = Sprite("bolinha.png")
bolinha.x = (janela.width / 2) - (bolinha.width / 2)
bolinha.y = (janela.height / 2) - (bolinha.height / 2)

vel_bola_x = 350 
vel_bola_y = 350

# --- CONFIGURAÇÃO DAS BARRINHAS ---
vel_barras = 400

# 1º NERF NA IA: Velocidade reduzida para dar chance em bolas anguladas
vel_ia = 160 

# Jogador (ESQUERDA)
barra_jogador = Sprite("pad(1).png")
barra_jogador.x = 10
barra_jogador.y = (janela.height / 2) - (barra_jogador.height / 2)

# IA (DIREITA)
barra_ia = Sprite("pad(1).png")
barra_ia.x = janela.width - barra_ia.width - 10
barra_ia.y = (janela.height / 2) - (barra_ia.height / 2)

# --- GAME LOOP ---
while True:
    janela.set_background_color((0, 0, 139))
    
    # === DESENHA O PLACAR ===
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

        # 2º NERF NA IA: Ela só "enxerga" a bola se ela já passou do MEIO DA TELA!
        # Se a bola acabou de sair do seu pad, a IA fica parada esperando.
        if vel_bola_x > 0 and bolinha.x > janela.width / 2: 
            distancia_x = barra_ia.x - (bolinha.x + bolinha.width)
            tempo_impacto = distancia_x / vel_bola_x
            
            destino_y = bolinha.y + (vel_bola_y * tempo_impacto)
            
            limite_y = janela.height - bolinha.height
            while destino_y < 0 or destino_y > limite_y:
                if destino_y < 0:
                    destino_y = abs(destino_y) 
                elif destino_y > limite_y:
                    destino_y = (2 * limite_y) - destino_y 
            
            alvo_y = destino_y - (barra_ia.height / 2)
        else:
            # Se a bola está longe ou indo pra você, a IA volta pro meio de campo
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

        # 5. Colisão com as Barras
        if bolinha.collided(barra_jogador):
            bolinha.x = barra_jogador.x + barra_jogador.width 
            vel_bola_x = -vel_bola_x
        elif bolinha.collided(barra_ia):
            bolinha.x = barra_ia.x - bolinha.width 
            vel_bola_x = -vel_bola_x

        # 6. GOLS E PONTUAÇÃO 
        if bolinha.x < 0: 
            placar_ia += 1
            esperando_espaco = True
        elif bolinha.x + bolinha.width > janela.width: 
            placar_jogador += 1
            esperando_espaco = True
            
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


# ==============================================================================================
# 🎯 POSSÍVEIS PEDIDOS DO PROFESSOR NA PROVA (NÍVEL BÁSICO E INTERMEDIÁRIO)
# ==============================================================================================
#
# 1. BOLA ACELERANDO:
# Como fazer: Em "bolinha.collided", faça `vel_bola_x = -(vel_bola_x * 1.10)` para aumentar 10% a velocidade.
#
# 2. MODO 2 JOGADORES (PVP):
# Como fazer: Apague a IA e coloque: `if teclado.key_pressed("W"): barra_ia.y -= ...`
#
# 3. OBSTÁCULO NO MEIO DA TELA:
# Como fazer: Crie um `Sprite` no centro da tela. Use `if bolinha.collided(obstaculo): vel_bola_x *= -1`.
#
# ==============================================================================================
# 🔥 POSSÍVEIS PEDIDOS DO PROFESSOR NA PROVA (NÍVEL AVANÇADO - "CHEFÕES")
# ==============================================================================================
#
# 4. VÁRIAS BOLINHAS NA TELA (MULTIBALL)
# O professor pode pedir: "Crie um jogo com 3 bolinhas rebatendo ao mesmo tempo."
# Como fazer (Lógica de Listas): 
# - Em vez de uma bolinha só, crie listas vazias: `bolinhas = []`, `vels_x = []`, `vels_y = []`.
# - Use um `for i in range(3):` para criar 3 sprites e colocá-los na lista.
# - No Game Loop, tudo que envolve a bolinha deve ir para dentro de um `for i in range(len(bolinhas)):`
#
# 5. PONG DE 4 LADOS (BARRAS NO TETO E NO CHÃO)
# O professor pode pedir: "Adicione uma barra no teto e uma no chão controladas por A e D."
# Como fazer:
# - Você precisará de uma imagem de pad "deitada" (horizontal). (ex: Sprite("pad_deitado.png"))
# - Na colisão com o teto/chão, ao invés de rebater sozinho, cheque se bateu na barra nova.
#
# 6. MAIS DE UMA BARRA POR JOGADOR (ZAGUEIRO E ATACANTE)
# O professor pode pedir: "O jogador controla 2 barras ao mesmo tempo com as setinhas."
# Como fazer: Crie duas barras para o jogador e use o mesmo `if teclado.key_pressed("UP")` para mover o Y de ambas.
#
# 7. ITENS ESPECIAIS (POWER-UPS)
# O professor pode pedir: "Faça aparecer um item na tela que deixa a barra gigante."
# Como fazer: Crie um sprite novo e um contador de tempo. Se bater no sprite, mude as propriedades do jogador.
#
# 8. BARRA FANTASMA ALEATÓRIA (PISCA-PISCA E POSIÇÃO LIMITADA)
# O professor pode pedir: "Faça uma barra aparecer e desaparecer a cada 3 segundos em posições aleatórias,
# na região de 1/3 de distancia de cada borda."
# Como fazer:
# - No início do arquivo, coloque: `import random`
# - Crie as variáveis: `barra_fantasma = Sprite("pad(1).png")`, `tempo_fantasma = 0`, `fantasma_visivel = False`
# - Calcule a "área de 1/3": 
#     limite_esq = janela.width / 3
#     limite_dir = (janela.width / 3) * 2
#     limite_cima = janela.height / 3
#     limite_baixo = (janela.height / 3) * 2
# - Dentro do `while True` (no bloco `else`, onde o jogo roda):
#     tempo_fantasma += janela.delta_time()
#     if tempo_fantasma >= 3.0:  # Passou 3 segundos
#         tempo_fantasma = 0     # Zera o cronômetro
#         fantasma_visivel = not fantasma_visivel # Inverte: se estava sumida aparece, se estava visível some.
#         
#         if fantasma_visivel: # Se for aparecer agora, sorteia a posição nas regras dos 1/3
#             barra_fantasma.x = random.randint(int(limite_esq), int(limite_dir - barra_fantasma.width))
#             barra_fantasma.y = random.randint(int(limite_cima), int(limite_baixo - barra_fantasma.height))
#
# - Na lógica de COLISÃO:
#     if fantasma_visivel and bolinha.collided(barra_fantasma):
#         vel_bola_x = -vel_bola_x  # Rebate a bola
#
# - No final do `while`, na hora de desenhar:
#     if fantasma_visivel:
#         barra_fantasma.draw()
# ==============================================================================================
