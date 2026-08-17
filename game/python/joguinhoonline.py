import pygame
from pathlib import Path


TAMANHO_JANELA = (1280, 720)
FPS = 60

PASTA_FONTES = Path(__file__).resolve().parent / "fonts"
FONTE_REGULAR = PASTA_FONTES / "PixelifySans-Regular.ttf"
FONTE_BOLD = PASTA_FONTES / "PixelifySans-Bold.ttf"

CORES = {
    "fundo": (8, 8, 9),
    "painel": (17, 17, 19),
    "painel_claro": (25, 25, 28),
    "linha": (42, 42, 46),
    "texto": (240, 240, 240),
    "texto_fraco": (128, 128, 134),
    "destaque": (240, 240, 240),
}

tela_cheia = False
tela = None
relogio = None
usuario_atual = None
fonte_logo = None
fonte_titulo = None
fonte_botao = None
fonte_texto = None
fonte_pequena = None


def carregar_fonte(tamanho, negrito=False):
    caminho = FONTE_BOLD if negrito else FONTE_REGULAR
    return pygame.font.Font(str(caminho), tamanho)


class Botao:
    def __init__(self, texto, rect, acao, selecionado=False):
        self.texto = texto
        self.rect = pygame.Rect(rect)
        self.acao = acao
        self.selecionado = selecionado

    def desenhar(self, superficie):
        mouse_em_cima = self.rect.collidepoint(pygame.mouse.get_pos())

        cor_fundo = CORES["painel_claro"] if mouse_em_cima else CORES["painel"]
        espessura_linha = 2 if self.selecionado else 1
        cor_linha = CORES["destaque"] if (self.selecionado or mouse_em_cima) else CORES["linha"]

        pygame.draw.rect(superficie, cor_fundo, self.rect, border_radius=2)
        pygame.draw.rect(superficie, cor_linha, self.rect, espessura_linha, border_radius=2)

        texto = fonte_botao.render(self.texto, True, CORES["texto"])
        texto_rect = texto.get_rect(midleft=(self.rect.x + 18, self.rect.centery))
        superficie.blit(texto, texto_rect)

    def clicou(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


def tamanho_tela():
    return tela.get_size()


def alternar_tela_cheia():
    global tela, tela_cheia

    tela_cheia = not tela_cheia
    if tela_cheia:
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        tela = pygame.display.set_mode(TAMANHO_JANELA)


def desenhar_fundo():
    largura, altura = tamanho_tela()
    tela.fill(CORES["fundo"])

    pygame.draw.line(tela, CORES["linha"], (0, altura - 76), (largura, altura - 76), 1)
    pygame.draw.rect(tela, CORES["fundo"], (0, altura - 75, largura, 75))


def desenhar_texto(texto, fonte, cor, posicao):
    renderizado = fonte.render(texto, True, cor)
    tela.blit(renderizado, posicao)


def desenhar_topo(titulo):
    largura, _ = tamanho_tela()
    pygame.draw.line(tela, CORES["linha"], (48, 98), (largura - 48, 98), 1)
    desenhar_texto("RLF", fonte_logo, CORES["texto"], (48, 30))
    desenhar_texto(titulo, fonte_titulo, CORES["texto_fraco"], (154, 49))

    if usuario_atual:
        texto_usuario = fonte_pequena.render(f"Logado: {usuario_atual['nome']}", True, CORES["texto_fraco"])
        tela.blit(texto_usuario, (largura - texto_usuario.get_width() - 48, 53))


def desenhar_rodape():
    _, altura = tamanho_tela()
    desenhar_texto("ESC volta ao menu   |   F11 alterna tela cheia", fonte_pequena, CORES["texto_fraco"], (48, altura - 45))


def criar_botoes_menu():
    x = 56
    y = 185
    largura = 240
    altura = 46
    espaco = 12

    return [
        Botao("Abrir", (x, y, largura, altura), "abrir"),
        Botao("Historia", (x, y + (altura + espaco), largura, altura), "historia"),
        Botao("Opcoes", (x, y + (altura + espaco) * 2, largura, altura), "opcoes"),
        Botao("Apoiar", (x, y + (altura + espaco) * 3, largura, altura), "apoiar"),
    ]


def criar_botoes_opcoes():
    largura, _ = tamanho_tela()
    x = largura - 360
    return [
        Botao("Tela cheia: Sim" if tela_cheia else "Tela cheia: Nao", (x, 210, 260, 44), "tela_cheia", tela_cheia),
        Botao("Som: Ligado" if som_ligado else "Som: Desligado", (x, 266, 260, 44), "som", som_ligado),
        Botao("Voltar", (x, 342, 260, 44), "menu"),
    ]


def desenhar_menu():
    desenhar_topo("Menu principal")

    desenhar_texto("Selecione uma opcao", fonte_titulo, CORES["texto"], (56, 135))
    desenhar_texto(
        "meinha 123 | teste 456 | teste 789 | teste 000",
        fonte_texto,
        CORES["texto_fraco"],
        (56, 430),
    )

    for botao in criar_botoes_menu():
        botao.desenhar(tela)


def desenhar_pagina(titulo, linhas):
    desenhar_topo(titulo)
    x = 56
    y = 150

    for linha in linhas:
        desenhar_texto(linha, fonte_texto, CORES["texto_fraco"], (x, y))
        y += 34

    Botao("Voltar", (56, 330, 180, 42), "menu").desenhar(tela)


def desenhar_opcoes():
    desenhar_topo("Opcoes")

    desenhar_texto("Video e interface", fonte_titulo, CORES["texto"], (56, 150))
    desenhar_texto("Use F11 ou o botao para alternar tela cheia.", fonte_texto, CORES["texto_fraco"], (56, 194))
    desenhar_texto("As opcoes ficam separadas do jogo para manter o projeto organizado.", fonte_texto, CORES["texto_fraco"], (56, 228))

    for botao in criar_botoes_opcoes():
        botao.desenhar(tela)


def preparar_janela():
    global tela, relogio, fonte_logo, fonte_titulo, fonte_botao, fonte_texto, fonte_pequena

    pygame.init()
    tela = pygame.display.set_mode(TAMANHO_JANELA)
    pygame.display.set_caption("RLF")
    relogio = pygame.time.Clock()

    fonte_logo = carregar_fonte(54, True)
    fonte_titulo = carregar_fonte(28, True)
    fonte_botao = carregar_fonte(19, True)
    fonte_texto = carregar_fonte(18)
    fonte_pequena = carregar_fonte(14)


def executar_jogo(usuario=None):
    global estado, rodando, som_ligado, usuario_atual, tela_cheia

    usuario_atual = usuario
    estado = "menu"
    rodando = True
    som_ligado = True
    tela_cheia = False

    preparar_janela()

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = "menu"
                elif evento.key == pygame.K_F11 or (
                    evento.key == pygame.K_RETURN and evento.mod & pygame.KMOD_ALT
                ):
                    alternar_tela_cheia()

            if estado == "menu":
                for botao in criar_botoes_menu():
                    if botao.clicou(evento):
                        estado = botao.acao

            elif estado == "opcoes":
                for botao in criar_botoes_opcoes():
                    if botao.clicou(evento):
                        if botao.acao == "tela_cheia":
                            alternar_tela_cheia()
                        elif botao.acao == "som":
                            som_ligado = not som_ligado
                        else:
                            estado = botao.acao

            else:
                voltar = Botao("Voltar", (56, 330, 180, 42), "menu")
                if voltar.clicou(evento):
                    estado = "menu"

        desenhar_fundo()

        if estado == "menu":
            desenhar_menu()
        elif estado == "abrir":
            desenhar_pagina(
                "Abrir",
                [
                    "So tem a tela de abrir kkkk",
                    "Por enquanto eu deixei apenas a tela pronta, sem gameplay improvisado.",
                ],
            )
        elif estado == "historia":
            desenhar_pagina(
                "Historia",
                [
                    "Aqui entra a introducao do mundo, personagens e objetivo principal.",
                    "nao tem historia ainda pq ninguem pensou kkkkkkkkkkkkk",
                ],
            )
        elif estado == "opcoes":
            desenhar_opcoes()
        elif estado == "apoiar":
            desenhar_pagina(
                "Apoiar",
                [
                    "sla acho q vou colocar os pix para rapaziada apoiar se bombar .",
                    "e insta tambem.",
                ],
            )

        desenhar_rodape()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    executar_jogo()
