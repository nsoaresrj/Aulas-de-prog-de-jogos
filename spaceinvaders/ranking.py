from PPlay.sprite import *
from datetime import datetime
import os

def salvar(janela, pontos):
    """Exibe aviso na tela, lê o nome no terminal e grava no arquivo ranking.txt."""
    janela.set_background_color((0, 0, 0))
    janela.draw_text("FIM DE JOGO!", (janela.width / 2) - 140, (janela.height / 2) - 40, size=45, color=(255, 0, 0), bold=True)
    janela.draw_text("Digite seu nome no TERMINAL do Python...", (janela.width / 2) - 220, (janela.height / 2) + 20, size=24, color=(255, 255, 255))
    janela.update()
    
    nome = input("\n=== FIM DE JOGO ===\nDigite seu nome para o Ranking: ").strip()
    if not nome:
        nome = "Jogador Anonimo"
        
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    with open("ranking.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome};{pontos};{data_atual}\n")
    print("Pontuação salva com sucesso!\n")


def obter_top5():
    """Lê o arquivo ranking.txt uma única vez e retorna os 5 melhores."""
    if not os.path.exists("ranking.txt"):
        return []
        
    registros = []
    with open("ranking.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 3:
                nome = dados[0]
                try:
                    pontos = int(dados[1])
                except ValueError:
                    pontos = 0
                data = dados[2]
                registros.append((nome, pontos, data))
                
    registros.sort(key=lambda item: item[1], reverse=True)
    return registros[:5]


def executar(janela, mouse, teclado):
    """Loop dedicado da tela de Ranking."""
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
            y_texto = 160
            for posicao, (nome, pontos, data) in enumerate(top5, start=1):
                texto_linha = f"{posicao}º  {nome}  -  {pontos} pts  ({data})"
                janela.draw_text(texto_linha, (janela.width / 2) - 220, y_texto, size=26, color=(255, 255, 255), bold=True)
                y_texto += 50
                
        btn_voltar.draw()
        
        if (mouse.is_over_object(btn_voltar) and mouse.is_button_pressed(1)) or teclado.key_pressed("ESC"):
            return
            
        janela.update()
