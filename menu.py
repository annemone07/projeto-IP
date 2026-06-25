import pygame
import sys
import os
from config import folderPath, bgWidth, bgHeight

class MenuPrincipal():
    def __init__(self, tela:pygame.surface):
        self.folderPath = folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (bgWidth,bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Iniciar", "Opções", "Sair", "Creditos"]
        self.opcaoSelecionada = 0
        self.dadosGrupo = {"equipe": "Equipe 3", "membros": ("jfag", "rma10", "phcps", "flg", "rtal", "aspr")}
    
    def draw(self, tela):
        tela.blit(self.bg, (0,0))
        cor=(0,0,0)
        for i, text in enumerate(self.opcoes):
            if i == self.opcaoSelecionada:
                cor = (254, 56, 103)
            else:
                cor = (0,0,0)
            renderedText = self.fonte.render(text, True, cor)
            tela.blit(renderedText, (100,100+i*60))
        eq_rend = self.fonte.render(self.dadosGrupo["equipe"], True, (0, 0, 0))
        #membros_rend = self.fonte.render(self.dadosGrupo["membros"], True, (255, 255, 255))
        tela.blit(eq_rend, (bgWidth-250, bgHeight-300))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (bgWidth-300, bgHeight - 220 + 35*n))
            else:
                tela.blit(memb_rend, (bgWidth-150, bgHeight - 220 + 35*(n-1)))

    
    def eventos(self, event):
        #print(event)
            #print(evento)
        print(event)
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_q:
                return "sair"
            elif event.key==pygame.K_w:
                self.opcaoSelecionada = (self.opcaoSelecionada-1)%len(self.opcoes)
            elif event.key==pygame.K_s:
                self.opcaoSelecionada = (self.opcaoSelecionada+1)%len(self.opcoes)
            elif event.key==pygame.K_RETURN:
                return self.opcoes[self.opcaoSelecionada]
        print(self.opcaoSelecionada)
        return None
    

class menuPause():
    def __init__(self, tela:pygame.surface):
        self.fonte = pygame.font.SysFont("Arial", 50, True, False)
        self.opcoes = ("Retomar", "Opções", "Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0

    def draw_tela(self, tela, bg):
        tela.blit(bg, (0, 0))

    def draw_texto(self, tela, tam_tela):
        texto_pause = self.fonte.render("JOGO PAUSADO", True, (255, 255, 255))
        tela.blit(texto_pause, (tam_tela[0]/2 - 200, 100))
        for i in range(len(self.opcoes)):
            if i == self.opcaoAtual:
                cor = (254, 56, 103)
            else:
                cor = (255, 255, 255)
            texto_for = self.fonte.render(self.opcoes[i], True, cor)
            tela.blit(texto_for, ((tam_tela[0]/2 - 100) , 200 + i*80))


    def eventos(self, event):
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.opcaoAtual = (self.opcaoAtual + 1) % 3
            elif event.key == pygame.K_w:
                self.opcaoAtual = (self.opcaoAtual - 1)%3
            elif event.key == pygame.K_RETURN:
                return self.opcoes[self.opcaoAtual]
            return None

class telaMorte(MenuPrincipal):
    def __init__(self, tela:pygame.surface):
        super().__init__(tela)
        self.folderPath = folderPath
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","telaMorteIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Reiniciar", "Menu Principal", "Sair"]
    
    def draw(self, tela):
        tela.blit(self.bg, (0,0))
        cor=(255,255,255)
        for i, text in enumerate(self.opcoes):
            if i == self.opcaoSelecionada:
                cor = (254, 56, 103)
            else:
                cor = (255,255,255)
            renderedText = self.fonte.render(text, True, cor)
            tela.blit(renderedText, (100,100+i*60))

class Creditos():
    def __init__(self, tela:pygame.surface):
        self.folderPath = folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (bgWidth,bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images", "backgrounds","bgCreditos.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Voltar"]
        self.opcaoSelecionada = 0
    
    def draw(self, tela):
        tela.blit(self.bg, (0,0))
        cor=(0,0,0)
        for i, text in enumerate(self.opcoes):
            if i == self.opcaoSelecionada:
                cor = (254, 56, 103)
            else:
                cor = (0,0,0)
            renderedText = self.fonte.render(text, True, cor)
            tela.blit(renderedText, (100,100+i*60))
    
    def eventos(self, event):
        #print(event)
            #print(evento)
        print(event)
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                return self.opcoes[self.opcaoSelecionada]
        print(self.opcaoSelecionada)
        return None