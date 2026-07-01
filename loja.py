import pygame
import sys
import os
import config
from time import perf_counter
# ==========================================
# LOJA EM FORMATO DE CLASSE
# ==========================================


class Loja:
    def __init__(self):
        # Cores (RGB)
        self.BRANCO    = (255, 255, 255)
        self.PRETO     = (0, 0, 0)
        self.VERDE     = (46, 204, 113)
        self.VERMELHO  = (231, 76, 60)
        self.AMARELO   = (255, 215, 0)
        self.LARANJA   = (255, 165, 0)
        self.AZUL      = (91, 124, 153)
        self.ROSA      = (252, 15, 192)
        self.CINZA     = (240, 240, 240)
        self.BORDA_CD  = (189, 195, 199)

        # Fontes
        self.fonte_texto  = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_preco  = pygame.font.SysFont("Arial", 22, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Arial", 45, bold=True)
        self.fonte_status = pygame.font.SysFont("Arial", 20)
        self.fonte_feedback = pygame.font.SysFont("Arial", 28, bold=True)

        # ==========================================
        # CARREGAMENTO E AJUSTE DAS IMAGENS (uma única vez)
        # ==========================================
        DIRETORIO_LOJA = os.path.dirname(os.path.abspath(__file__))

        caminho_moeda   = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "coin 2.png")
        caminho_cura    = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "med_kit.png")
        caminho_escudo  = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "Escudo.png")
        caminho_powerup = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "QS_up.png")
        caminho_carga   = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "choque_do_trovao.png")
        caminho_cartucho = os.path.join(DIRETORIO_LOJA, 'images', 'Items', 'bala_shotgun.png')

        self.img_moeda   = pygame.image.load(caminho_moeda).convert_alpha()
        self.img_cura    = pygame.image.load(caminho_cura).convert_alpha()
        self.img_escudo  = pygame.image.load(caminho_escudo).convert_alpha()
        self.img_powerup = pygame.image.load(caminho_powerup).convert_alpha()
        self.img_carga   = pygame.image.load(caminho_carga).convert_alpha()
        self.img_cartucho = pygame.image.load(caminho_cartucho).convert_alpha()

        self.img_moeda    = pygame.transform.scale(self.img_moeda,  (25, 25))
        self.img_cura     = pygame.transform.scale(self.img_cura,   (90, 90))
        self.img_escudo   = pygame.transform.scale(self.img_escudo, (90, 90))
        self.img_powerup  = pygame.transform.scale(self.img_powerup, (90, 90))
        self.img_carga    = pygame.transform.scale(self.img_carga, (90, 90))
        self.img_cartucho = pygame.transform.scale(self.img_cartucho, (90, 90))

        # ==========================================
        # ESTRUTURA DOS ITENS DA LOJA
        # ==========================================
        self._montar_itens()

    def _montar_itens(self):
        """Monta (ou remonta) o layout dos cards, baseado no tamanho atual da tela."""
        LARGURA, ALTURA = config.bgInitWidth, config.bgInitHeight
        CARD_W, CARD_H = 140, 200
        CARD_Y = ALTURA // 2 - CARD_H // 2
        ESPACO = 60
        total = 5 * CARD_W + 4 * ESPACO
        x0 = LARGURA // 2 - total // 2

        self.loja_itens = {
            "cura": {
                "nome": "Cura", "preco": 10,
                "img": self.img_cura,
                "rect": pygame.Rect(x0, CARD_Y, CARD_W, CARD_H)
            },
            "escudo": {
                "nome": "Escudo", "preco": 5,
                "img": self.img_escudo,
                "rect": pygame.Rect(x0 + CARD_W + ESPACO, CARD_Y, CARD_W, CARD_H)
            },
            "powerup": {
                "nome": "Quick Shot", "preco": 15,
                "img": self.img_powerup,
                "rect": pygame.Rect(x0 + 2 * (CARD_W + ESPACO), CARD_Y, CARD_W, CARD_H)
            },
            "charge": {
                "nome": "Carga", "preco": 12,
                "img": self.img_carga,
                "rect": pygame.Rect(x0 + 3 * (CARD_W + ESPACO), CARD_Y, CARD_W, CARD_H)
            },
            "shotgun": {
                "nome": "Cartuchos", "preco": 2,
                "img": self.img_cartucho,
                "rect": pygame.Rect(x0 + 4 * (CARD_W + ESPACO), CARD_Y, CARD_W, CARD_H)
            }
        }

    def _processar_compra(self, id_item, dados, jogador, powerup_ativo, bullet_time_ativo):
        """Retorna (powerup_ativo, bullet_time_ativo, mensagem_feedback) após tentar comprar."""
        mensagem_feedback = None

        if jogador.moedas < dados["preco"]:
            return powerup_ativo, bullet_time_ativo, "Moedas insuficientes para comprar este item!"

        if id_item == "cura":
            if jogador.vida >= 100:
                mensagem_feedback = "Vida já está cheia!"
            else:
                jogador.moedas -= dados["preco"]
                jogador.vida = min(100, jogador.vida + 10)  # Cura 10, limite de 100
                mensagem_feedback = "Você comprou Cura! +10 de Vida."

        elif id_item == "escudo":
            if jogador.armadura >= 100 and jogador.escudo == 3:
                mensagem_feedback = "Não é possivel completar os escudos com a armadura cheia!"
            else:
                jogador.moedas -= dados["preco"]
                jogador.escudo += 1
                if jogador.escudo >= 4:
                    jogador.armadura += 25
                    jogador.escudo = 0
                if jogador.armadura > 100:
                    jogador.armadura = 100
                mensagem_feedback = "Você comprou Escudo!"

        elif id_item == "powerup":
            if powerup_ativo:
                mensagem_feedback = "Quick Shot já está ativo!"
            else:
                jogador.moedas -= dados["preco"]
                powerup_ativo = True
                mensagem_feedback = "Quick Shot ativado!"

        elif id_item == "charge":
            if bullet_time_ativo:
                mensagem_feedback = "Bullet Time já está ativo!"
            elif jogador.charge == 5:
                mensagem_feedback = "Você já tem o máximo de cargas para o Bullet Time!"
            else:
                jogador.moedas -= dados["preco"]
                jogador.charge += 1
                mensagem_feedback = "Você comprou uma carga para o Bullet Time"

        elif id_item == "shotgun":
            if jogador.cartuchos == 50:
                mensagem_feedback = "Você já tem o limite de cartuchos de Shotgun!"
            else:
                jogador.moedas -= dados["preco"]
                jogador.cartuchos += 2
                mensagem_feedback = "Você comprou cartuchos de Shotgun!"

        return powerup_ativo, bullet_time_ativo, mensagem_feedback

    def _desenhar(self, jogador, powerup_ativo, mensagem_feedback):
        LARGURA, ALTURA = config.bgInitWidth, config.bgInitHeight

        # Título Principal
        txt_titulo = self.fonte_titulo.render("LOJA DE ITENS", True, self.PRETO)
        config.tela_virtual.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 40))

        # Caixa de Feedback (Mensagens sobre a compra)
        palavras_negativas = ("insuficientes", "já está", "Não é possivel", "máximo", "limite")
        if any(p in mensagem_feedback for p in palavras_negativas):
            cor_feedback = self.VERMELHO
        elif "Bem-vindo" in mensagem_feedback:
            cor_feedback = self.PRETO
        else:
            cor_feedback = self.VERDE

        txt_feed = self.fonte_feedback.render(mensagem_feedback, True, cor_feedback)
        feed_x = LARGURA // 2 - txt_feed.get_width() // 2
        feed_y = 105

        caixa_feed = pygame.Rect(0, 0, txt_feed.get_width() + 40, txt_feed.get_height() + 20)
        caixa_feed.center = (LARGURA // 2, feed_y + txt_feed.get_height() // 2)
        pygame.draw.rect(config.tela_virtual, self.CINZA, caixa_feed, border_radius=12)
        pygame.draw.rect(config.tela_virtual, cor_feedback, caixa_feed, width=2, border_radius=12)

        config.tela_virtual.blit(txt_feed, (feed_x, feed_y))

        # --- Painel de Status do Jogador (Canto Superior Direito) ---
        config.tela_virtual.blit(self.img_moeda, (LARGURA - 170, 30))
        txt_moedas = self.fonte_texto.render(f"Moedas: {jogador.moedas}", True, self.PRETO)
        config.tela_virtual.blit(txt_moedas, (LARGURA - 135, 32))

        txt_vida  = self.fonte_status.render(f"Vida Atual: {jogador.vida}/100", True, self.VERMELHO)
        txt_esc   = self.fonte_status.render(f"Escudo: {jogador.escudo}/4 pedaços", True, self.AZUL)
        txt_arm   = self.fonte_status.render(f"Armadura: {jogador.armadura}/100", True, self.AZUL)
        txt_dano  = self.fonte_status.render(f"Quick Shot ativo: {powerup_ativo}", True, self.ROSA)
        txt_carga = self.fonte_status.render(f"Charges: {jogador.charge}/5", True, self.AMARELO)
        txt_carts = self.fonte_status.render(f"Cartuchos: {jogador.cartuchos}", True, self.VERMELHO)

        config.tela_virtual.blit(txt_vida,  (30, 30))
        config.tela_virtual.blit(txt_esc,   (30, 55))
        config.tela_virtual.blit(txt_arm,   (30, 80))
        config.tela_virtual.blit(txt_dano,  (30, 105))
        config.tela_virtual.blit(txt_carga, (30, 125))
        config.tela_virtual.blit(txt_carts, (30, 145))

        # Instrução para fechar
        txt_fechar = self.fonte_status.render("Pressione ESC para fechar a loja", True, self.PRETO)
        config.tela_virtual.blit(txt_fechar, (LARGURA // 2 - txt_fechar.get_width() // 2, ALTURA - 40))

        # --- Desenho dos Cards dos Itens ---
        for id_item, dados in self.loja_itens.items():
            rect = dados["rect"]

            pygame.draw.rect(config.tela_virtual, self.CINZA, rect, border_radius=12)
            pygame.draw.rect(config.tela_virtual, self.BORDA_CD, rect, width=2, border_radius=12)

            img_x = rect.x + (rect.width - dados["img"].get_width()) // 2
            config.tela_virtual.blit(dados["img"], (img_x, rect.y + 20))

            txt_nome = self.fonte_texto.render(dados["nome"], True, self.PRETO)
            nome_x = rect.x + (rect.width - txt_nome.get_width()) // 2
            config.tela_virtual.blit(txt_nome, (nome_x, rect.y + 125))

            txt_preco = self.fonte_preco.render(f"${dados['preco']}", True, self.VERDE)
            preco_x = rect.x + (rect.width - txt_preco.get_width()) // 2
            config.tela_virtual.blit(txt_preco, (preco_x, rect.y + 155))

    def _mouse_para_virtual(self, pos_mouse):
        """Converte a posição do mouse (em coordenadas da janela real, que muda
        quando a resolução é alterada)"""
        escala_x = config.bgInitWidth / config.bgWidth
        escala_y = config.bgInitHeight / config.bgHeight
        return (pos_mouse[0] * escala_x, pos_mouse[1] * escala_y)

    def abrir(self, relogio, jogador, powerup_ativo, bullet_time_ativo):
        """Abre o loop da loja. Mantém a mesma assinatura/retorno da função original."""
        tempo_de_entrada = perf_counter()

        # Recalcula o layout dos cards (caso a resolução tenha mudado desde o __init__)
        self._montar_itens()

        mensagem_feedback = "Bem-vindo à loja! Clique em um item para comprar."

        rodando = True
        while rodando:
            config.tela_virtual.fill(self.LARANJA)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key in (pygame.K_l, pygame.K_ESCAPE):
                        rodando = False

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    pos_mouse = self._mouse_para_virtual(pos_mouse)

                    for id_item, dados in self.loja_itens.items():
                        if dados["rect"].collidepoint(pos_mouse):
                            powerup_ativo, bullet_time_ativo, msg = self._processar_compra(
                                id_item, dados, jogador, powerup_ativo, bullet_time_ativo
                            )
                            if msg is not None:
                                mensagem_feedback = msg

            self._desenhar(jogador, powerup_ativo, mensagem_feedback)

            config.tela_escalada = pygame.transform.smoothscale(config.tela_virtual, (config.bgWidth, config.bgHeight))
            config.tela.blit(config.tela_escalada, (0, 0))
            pygame.display.flip()
            relogio.tick(60)

        tempo_saida = perf_counter()
        tempo_pausado = tempo_saida - tempo_de_entrada

        return powerup_ativo, tempo_pausado