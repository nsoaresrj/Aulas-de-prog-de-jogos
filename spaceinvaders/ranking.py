from PPlay.sprite import *
from datetime import datetime
import os

# =====================================================================
# BLOCO 1: LOCALIZAÇÃO DO ARQUIVO DE TEXTO
# Descobre automaticamente a pasta onde o 'ranking.py' está salvo e fixa
# o arquivo 'ranking.txt' dentro dela (pasta spaceinvaders).
# =====================================================================
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_RANKING = os.path.join(DIRETORIO_ATUAL, "ranking.txt")


# =====================================================================
# BLOCO 2: GRAVAÇÃO DE NOVO RECORDE (QUANDO O JOGADOR PERDE)
# =====================================================================
def salvar(janela, pontos):
    """Exibe aviso na tela gráfica, lê o nome no terminal e salva no ranking.txt."""
    # Desenha aviso na janela do jogo para o jogador saber que precisa digitar no terminal
    janela.set_background_color((0, 0, 0))
    janela.draw_text("FIM DE JOGO!", (janela.width / 2) - 140, (janela.height / 2) - 40, size=45, color=(255, 0, 0), bold=True)
    janela.draw_text("Digite seu nome no TERMINAL do Python...", (janela.width / 2) - 220, (janela.height / 2) + 20, size=24, color=(255, 255, 255))
    janela.update()
    
    # Pede o nome no terminal do VS Code
    nome = input("\n=== FIM DE JOGO ===\nDigite seu nome para o Ranking: ").strip()
    if not nome:
        nome = "Jogador Anonimo"
        
    # Pega a data atual do computador no formato Dia/Mês/Ano
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Abre o arquivo no modo "a" (append = adicionar no final sem apagar os antigos)
    with open(CAMINHO_RANKING, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome};{pontos};{data_atual}\n")
    print("Pontuação salva com sucesso!\n")


# =====================================================================
# BLOCO 3: LEITURA E ORDENAÇÃO DO TOP 5
# [COMO ALTERAR]: Se quiser mostrar o Top 10 em vez de Top 5, mude 'registros[:5]'
# no final desta função para 'registros[:10]'.
# =====================================================================
def obter_top5():
    """Lê o arquivo ranking.txt, coloca em ordem do maior para o menor e retorna os 5 primeiros."""
    if not os.path.exists(CAMINHO_RANKING):
        return []
        
    registros = []
    with open(CAMINHO_RANKING, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            # Divide a linha "Nome;Pontos;Data" em 3 partes usando o ';' como separador
            dados = linha.strip().split(";")
            if len(dados) == 3:
                nome = dados[0]
                try:
                    pontos = int(dados[1]) # Converte os pontos de texto para número inteiro
                except ValueError:
                    pontos = 0
                data = dados[2]
                registros.append((nome, pontos, data))
                
    # Ordena a lista baseando-se nos pontos (item[1]) em ordem decrescente (reverse=True)
    registros.sort(key=lambda item: item[1], reverse=True)
    return registros[:5]


# =====================================================================
# BLOCO 4: TELA GRÁFICA DO RANKING
# =====================================================================
def executar(janela, mouse, teclado):
    """Loop dedicado da tela de Ranking (lê o arquivo do disco apenas 1 vez ao abrir)."""
    top5 = obter_top5()
    
    btn_voltar = Sprite("spaceinvaders/sprites/back.png")
    btn_voltar.x = (janela.width / 2) - (btn_voltar.width / 2)
    btn_voltar.y = 480

    while True:
        janela.set_background_color((0, 0, 0))
        janela.draw_text("RANKING - TOP 5", (janela.width / 2) - 190, 60, size=45, color=(255, 255, 0), bold=True)
        
        if len(top5) == 0:
            janela.draw_text("Nenhuma pontuacao registrada ainda.", (janela.width / 2) - 210, 250, size=24, color=(200, 200, 200))
        else:
            # Desenha cada um dos 5 jogadores dando um espaço vertical de 50 pixels entre eles
            y_texto = 160
            for posicao, (nome, pontos, data) in enumerate(top5, start=1):
                texto_linha = f"{posicao}º  {nome}  -  {pontos} pts  ({data})"
                janela.draw_text(texto_linha, (janela.width / 2) - 220, y_texto, size=26, color=(255, 255, 255), bold=True)
                y_texto += 50
                
        btn_voltar.draw()
        
        # Sai da tela de ranking se clicar no botão Voltar ou apertar ESC
        if (mouse.is_over_object(btn_voltar) and mouse.is_button_pressed(1)) or teclado.key_pressed("ESC"):
            return
            
        janela.update()
