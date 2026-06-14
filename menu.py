import pygame
import sys
import os

class MenuPrincipal():
    def __init__(self, tela:pygame.surface):
        self.folderPath = os.path.dirname(os.path.abspath(__file__))
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = tela.get_size()
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Iniciar", "Opções", "Sair"]
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
        
        