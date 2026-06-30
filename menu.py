import pygame
import sys
import os
import config

class MenuPrincipal():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (config.bgWidth,config.bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Jogar", "Tutorial", "Opções", "Sair", "Creditos"]
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
        tela.blit(eq_rend, (config.bgInitWidth-250, config.bgInitHeight-300))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (config.bgInitWidth-300, config.bgInitHeight - 220 + 35*n))
            else:
                tela.blit(memb_rend, (config.bgInitWidth-150, config.bgInitHeight - 220 + 35*(n-1)))

    
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
        self.folderPath = config.folderPath
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","telaMorteIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, (config.bgWidth,config.bgHeight))
        self.opcoes = ["Reiniciar", "Menu Principal", "Sair"]
    
    def draw(self, tela, n_kills):
        tela.blit(self.bg, (0,0))
        cor=(255,255,255)
        for i, text in enumerate(self.opcoes):
            if i == self.opcaoSelecionada:
                cor = (254, 56, 103)
            else:
                cor = (255,255,255)
            renderedText = self.fonte.render(text, True, cor)
            tela.blit(renderedText, (100,100+i*60))

        if n_kills == 1:
            kills_tex = f"{n_kills} ABATE"
        else:
            kills_tex = f"{n_kills} ABATES"
        kills_rend = self.fonte.render(kills_tex, True, (255, 255, 255))
        tela.blit(kills_rend, (100, 500))

class Creditos():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (config.bgWidth,config.bgHeight)
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
    



class menuFimTutorial():
    def __init__(self, tela:pygame.surface):
        self.fonte = pygame.font.SysFont("Arial", 50, True, False)
        self.opcoes = ("Menu principal", "Opções", "Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0

    #def draw_tela(self, tela, bg):
        

    def draw(self, tela, tam_tela, bg):
        tela.blit(bg, (0, 0))
        texto_pause = self.fonte.render("FIM DO TUTORIAL", True, (255, 255, 255))
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



class menuModos():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (config.bgWidth,config.bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Infinito", "Boss", "Voltar"]
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
        tela.blit(eq_rend, (config.bgInitWidth-250, config.bgInitHeight-300))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (config.bgInitWidth-300, config.bgInitHeight - 220 + 35*n))
            else:
                tela.blit(memb_rend, (config.bgInitWidth-150, config.bgInitHeight - 220 + 35*(n-1)))

    
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
    



class menuDificuldade():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (config.bgWidth,config.bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Fácil", "Médio", "Difícil", "Impossível", "Voltar"]
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
        tela.blit(eq_rend, (config.bgInitWidth-250, config.bgInitHeight-300))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (config.bgInitWidth-300, config.bgInitHeight - 220 + 35*n))
            else:
                tela.blit(memb_rend, (config.bgInitWidth-150, config.bgInitHeight - 220 + 35*(n-1)))

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
    
class menuOpcoes():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.tamanho = (config.bgWidth,config.bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgCreditos.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = {"Volume":(0, 20, 40, 60, 80, 100), "Resolução":("Tela Cheia","1920x1080","960x540"),"Voltar": ()}
        self.opcaoSelecionada = 0
        self.valoresOpcoes = {0: "Volume", 1: "Resolução", 2: "Voltar"}
        self.subopcao = 5
        #self.num_barras = 5
        self.ultimos_valores = [5, 0]
        """""100","80","60","40","20","0"""""
        
        
        

    def draw(self, tela):
        tela.blit(self.bg, (0,0))
        cor=(255,255,255)
        pygame.draw.rect(tela, (255, 255, 255), (config.bgInitWidth/2 - 150, 200, 390, 50))
        #tela.blit(self.fonte.render("Volume", True, (255, 255, 255)), (config.bgWidth/2 - 300, 200))
        #tela.blit(self.fonte.render("Resolução", True, (255, 255, 255)), (100, 100))
        #print(f"olha aq {self.opcoes.keys()}")
        for i, text in enumerate(self.opcoes.keys()):
            if i == self.opcaoSelecionada:
                cor = (254, 56, 103)
            else:
                cor = (255,255,255)
            renderedText = self.fonte.render(text, True, cor)
            
            tela.blit(renderedText, (config.bgWidth/2 - 300, 200 + i*100))
        if self.valoresOpcoes[self.opcaoSelecionada] == "Volume":
            self.ultimos_valores[0] = self.ultimos_valores[self.opcaoSelecionada]
            for k in range(self.ultimos_valores[self.opcaoSelecionada]):
                pygame.draw.rect(tela, (0, 0, 255), (config.bgInitWidth/2 - 150 + 80*k, 200, 50, 50))
            
        else:
            for k in range(self.ultimos_valores[0]):
                pygame.draw.rect(tela, (0, 0, 255), (config.bgInitWidth/2 - 150 + 80*k, 200, 50, 50))

        #if self.valoresOpcoes[self.opcaoSelecionada] == "Resolução":
        self.ultimos_valores[1] == self.ultimos_valores[1]
        tela.blit(self.fonte.render(self.opcoes["Resolução"][self.ultimos_valores[1]], True, (0, 0, 255)), (config.bgWidth/2 - 50, 300))
        
        


    
    def eventos(self, event):
        #print(event)
            #print(evento)
        print(event)
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            print(f"VALOR DO OPÇÃO {self.opcaoSelecionada}")
            if event.key==pygame.K_q:
                return "sair"
            elif event.key==pygame.K_w:
                self.opcaoSelecionada -=1 
                if self.opcaoSelecionada < 0:
                    self.opcaoSelecionada = 0
                    
            elif event.key==pygame.K_a and self.valoresOpcoes[self.opcaoSelecionada] != "Voltar":
                self.ultimos_valores[self.opcaoSelecionada] -=1
                if self.ultimos_valores[self.opcaoSelecionada] < 0:
                    self.ultimos_valores[self.opcaoSelecionada] = 0
            elif event.key==pygame.K_s:
                self.opcaoSelecionada +=1
                if self.opcaoSelecionada ==len(self.opcoes):
                    self.opcaoSelecionada = len(self.opcoes) - 1
            elif event.key==pygame.K_d and self.valoresOpcoes[self.opcaoSelecionada] != "Voltar":
                self.ultimos_valores[self.opcaoSelecionada] += 1
                if self.ultimos_valores[self.opcaoSelecionada] == len(self.opcoes[self.valoresOpcoes[self.opcaoSelecionada]]):
                    self.ultimos_valores[self.opcaoSelecionada] = len(self.opcoes[self.valoresOpcoes[self.opcaoSelecionada]]) - 1
            
            elif event.key==pygame.K_RETURN and self.opcaoSelecionada != 2:
                return self.opcoes["Resolução"][self.ultimos_valores[1]], self.ultimos_valores[0] * 20, 0
            elif event.key==pygame.K_RETURN and self.opcaoSelecionada ==2:
                return self.opcoes["Resolução"][self.ultimos_valores[1]], self.ultimos_valores[0] * 20, 1

        
        return None, None, None