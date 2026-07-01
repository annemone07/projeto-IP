import pygame
import sys
import os
import config

class MenuPrincipal():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("consolas", 50)
        self.fonte_titulo = pygame.font.SysFont("comic sans", 180)
        self.tamanho = (config.bgWidth,config.bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = ["Jogar", "Tutorial", "Opções","Ranking", "Sair", "Creditos"]
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
            tela.blit(renderedText, (100,170+i*60))
        eq_rend = self.fonte.render(self.dadosGrupo["equipe"], True, (0, 0, 0))
        titulo_rend = self.fonte_titulo.render("AeroHell", True, (0, 0, 0))
        config.tela_virtual.blit(titulo_rend, (600, 40))
        #membros_rend = self.fonte.render(self.dadosGrupo["membros"], True, (255, 255, 255))
        tela.blit(eq_rend, (config.bgInitWidth-620, config.bgInitHeight-370))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (config.bgInitWidth-650, config.bgInitHeight - 270 + 35*n))
            else:
                tela.blit(memb_rend, (config.bgInitWidth-500, config.bgInitHeight - 270 + 35*(n-1)))

    
    def eventos(self, event):
        #print(event)
            #print(evento)
        #print(event)
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
        #print(self.opcaoSelecionada)
        return None
    

class menuPause():
    def __init__(self, tela:pygame.surface):
        self.fonte = pygame.font.SysFont("consolas", 50, True, False)
        self.opcoes = ("Retomar", "Opções", "Menu Principal", "Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0

    def draw_tela(self, tela, bg):
        tela.blit(bg, (0, 0))

    def draw_texto(self, tela, tam_tela):
        texto_pause = self.fonte.render("JOGO PAUSADO", True, (255, 255, 255))
        tela.blit(texto_pause, (tam_tela[0]/2 - 160, 100))
        for i in range(len(self.opcoes)):
            delta = 0
            if i == self.opcaoAtual:
                cor = (254, 56, 103)
            else:
                cor = (255, 255, 255)
            if i == 2:
                delta = 30
            texto_for = self.fonte.render(self.opcoes[i], True, cor)
            tela.blit(texto_for, ((tam_tela[0]/2 - texto_for.width/2 + delta) , 200 + i*80))


    def eventos(self, event):
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.opcaoAtual = (self.opcaoAtual + 1) % 4
            elif event.key == pygame.K_w:
                self.opcaoAtual = (self.opcaoAtual - 1)%4
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
    
    def draw(self, tela, n_kills, mod):
        if mod == "infinito":
            self.opcoes = ["Reiniciar", "Menu Principal","Ranking", "Sair"]
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
        #print(event)
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                return self.opcoes[self.opcaoSelecionada]
        #print(self.opcaoSelecionada)
        return None
    



class menuFimTutorial():
    def __init__(self, tela:pygame.surface):
        self.fonte = pygame.font.SysFont("consolas", 50, True, False)
        self.opcoes = ("Menu principal", "Opções", "Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0

    #def draw_tela(self, tela, bg):
        

    def draw(self, tela, tam_tela, bg):
        tela.blit(bg, (0, 0))
        texto_pause = self.fonte.render("PARABÉNS!\nFIM DO TUTORIAL", True, (255, 255, 255))
        tela.blit(texto_pause, (tam_tela[0]/2 - 180, 100))
        for i in range(len(self.opcoes)):
            delta = 0
            if i == self.opcaoAtual:
                cor = (254, 56, 103)
            else:
                cor = (255, 255, 255)
            if i == 0:
                delta = 30
            texto_for = self.fonte.render(self.opcoes[i], True, cor)
            tela.blit(texto_for, ((tam_tela[0]/2 - texto_for.width/2 + delta) , 200 + i*80))


            

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
        self.fonte = pygame.font.SysFont("consolas", 50)
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
            tela.blit(renderedText, (100,170+i*60))
        eq_rend = self.fonte.render(self.dadosGrupo["equipe"], True, (0, 0, 0))
        titulo_rend = config.fonte_titulo.render("AeroHell", True, (0, 0, 0))
        config.tela_virtual.blit(titulo_rend, (600, 40))
        #membros_rend = self.fonte.render(self.dadosGrupo["membros"], True, (255, 255, 255))
        tela.blit(eq_rend, (config.bgInitWidth-620, config.bgInitHeight-370))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (config.bgInitWidth-650, config.bgInitHeight - 270 + 35*n))
            else:
                tela.blit(memb_rend, (config.bgInitWidth-500, config.bgInitHeight - 270 + 35*(n-1)))

    
    def eventos(self, event):
        #print(event)
            #print(evento)
        #print(event)
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
        #print(self.opcaoSelecionada)
        return None
    



class menuDificuldade():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("consolas", 50)
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
            tela.blit(renderedText, (100,170+i*60))
        eq_rend = self.fonte.render(self.dadosGrupo["equipe"], True, (0, 0, 0))
        titulo_rend = config.fonte_titulo.render("AeroHell", True, (0, 0, 0))
        config.tela_virtual.blit(titulo_rend, (600, 40))
        #membros_rend = self.fonte.render(self.dadosGrupo["membros"], True, (255, 255, 255))
        tela.blit(eq_rend, (config.bgInitWidth-620, config.bgInitHeight-370))
        for n in range(len(self.dadosGrupo["membros"])):
            memb_rend = self.fonte.render(self.dadosGrupo["membros"][n], True, (0, 0, 0))
            if n % 2 == 0:
                tela.blit(memb_rend, (config.bgInitWidth-650, config.bgInitHeight - 270 + 35*n))
            else:
                tela.blit(memb_rend, (config.bgInitWidth-500, config.bgInitHeight - 270 + 35*(n-1)))

    def eventos(self, event):
        #print(event)
            #print(evento)
        #print(event)
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
        #print(self.opcaoSelecionada)
        return None
    
class menuOpcoes():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("consolas", 50)
        self.tamanho = (config.bgWidth,config.bgHeight)
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgCreditos.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.opcoes = {"Volume":(0, 20, 40, 60, 80, 100), 
                       "Resolução":("Tela Cheia >","< 1920x1080 >","< 960x540"),  
                       "Voltar": ()}
        self.opcaoSelecionada = 0
        self.valoresOpcoes = {0: "Volume", 1: "Resolução",2: "Voltar"}
        self.imgs = ("soundbar- mute.png", "soundbar-20%.png", "soundbar-40%.png", "soundbar-60%.png", "soundbar - 80%.png", "soundbar - 100%.png")
        self.subopcao = 5
        self.ultimos_valores = [5, 0, 5]
        self.vol = pygame.image.load(os.path.join(self.folderPath,"images","SoundSprite",self.imgs[self.ultimos_valores[0]])).convert_alpha()
        self.vol = pygame.transform.scale(self.vol, (1000, 50))
        
        
        

    def draw(self, tela):
        config.tela_virtual.blit(self.bg, (0,0))
        cor=(255,255,255)
        #pygame.draw.rect(tela, (255, 255, 255), (config.bgInitWidth/2 - 150, 200, 390, 50), 3)
        #tela.blit(self.fonte.render("Volume", True, (255, 255, 255)), (config.bgWidth/2 - 300, 200))
        #tela.blit(self.fonte.render("Resolução", True, (255, 255, 255)), (100, 100))
        #print(f"olha aq {self.opcoes.keys()}")
        for i, text in enumerate(self.opcoes.keys()):
            if i == self.opcaoSelecionada:
                cor = (254, 56, 103)
            else:
                cor = (255,255,255)
            renderedText = self.fonte.render(text, True, cor)
            
            config.tela_virtual.blit(renderedText, (config.bgWidth/2 - 300, 200 + i*100))
        
        
        #pegando o sprite do volume
        self.vol = pygame.image.load(os.path.join(self.folderPath,"images","SoundSprite",self.imgs[self.ultimos_valores[0]])).convert_alpha()
        self.vol = pygame.transform.scale(self.vol, (360, 250))
        
        #colocando os textos/imagens na tela
        config.tela_virtual.blit(self.vol, (config.bgWidth/2 - 120,90))
        config.tela_virtual.blit(self.fonte.render(self.opcoes["Resolução"][self.ultimos_valores[1]], True, (0, 0, 255)), (config.bgWidth/2 - 50, 300))
        """"pygame.draw.rect(config.tela_virtual, (230, 230, 230), (600, 400, 360, 60), 3)
        tx_volume = 36*self.ultimos_valores[2]
        pygame.draw.rect(config.tela_virtual, (0, 0, 230), (605, 405, tx_volume - 10, 50))"""
        
        
        
        #lógica antiga da barra --> caso seja necessário retornar
        """for k in range(self.ultimos_valores[self.opcaoSelecionada]):
            pygame.draw.rect(tela, (0, 0, 255), (config.bgInitWidth/2 - 150 + 80*k, 200, 50, 50))"""
            
        """else:
            config.tela_virtual.blit(self.vol, (config.bgInitWidth/2 - 140,90))"""
        """for k in range(self.ultimos_valores[0]):
            pygame.draw.rect(tela, (0, 0, 255), (config.bgInitWidth/2 - 150 + 80*k, 200, 50, 50))"""
        

        


    
    def eventos(self, event):
        #print(event)
            #print(evento)
        #print(event)
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            #print(f"VALOR DO OPÇÃO {self.opcaoSelecionada}")
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
                res_adaptada = self.opcoes["Resolução"][self.ultimos_valores[1]].removeprefix("< ").removesuffix(" >")
                #print(f"OLHA AQ{res_adaptada}")
                return res_adaptada, self.ultimos_valores[0] * 20, 0#, self.opcoes["Brilho"][self.ultimos_valores[2]]
            elif event.key==pygame.K_RETURN and self.opcaoSelecionada ==2:
                res_adaptada = self.opcoes["Resolução"][self.ultimos_valores[1]].removeprefix("< ").removesuffix(" >")
                #print(f"OLHA AQ{res_adaptada}")
                return res_adaptada, self.ultimos_valores[0] * 20, 1#, self.opcoes["Brilho"][self.ultimos_valores[2]]

        
        return None, None, None, None
    


class menuFimBoss():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("consolas", 50, True, False)
        self.opcoes = ("Reiniciar", "Opções", "Adicionar Ranking" ,"Menu Principal","Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)

    def draw_tela(self, tela, bg):
        tela.blit(bg, (0, 0))

    def draw_texto(self, tela, tam_tela, tempo_de_jogo):
        config.tela_virtual.blit(self.bg, (0,0))
        mensagem_fim = "LUTA CONCLUIDA"
        mensagem_tempo = f"TEMPO TOTAL: {tempo_de_jogo:0.1f}s"
        mensagem_form_fim = config.fonte_grande.render(mensagem_fim, True, (0, 0, 0))
        mensagem_form_tempo = config.fonte_media.render(mensagem_tempo, True, (0, 0, 0))
        config.tela_virtual.blit(mensagem_form_fim, (350, 30))
        config.tela_virtual.blit(mensagem_form_tempo, (450, 130))
        pygame.display.flip() #para colocar a mensagem de final na tela
        
        for i in range(len(self.opcoes)):
            if i == self.opcaoAtual:
                cor = (254, 56, 103)
            else:
                cor = (255, 255, 255)
            texto_for = self.fonte.render(self.opcoes[i], True, cor)
            tela.blit(texto_for, ((tam_tela[0]/2 - texto_for.width/2) , 300 + i*80))


    def eventos(self, event):
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.opcaoAtual = (self.opcaoAtual + 1) % 5
            elif event.key == pygame.K_w:
                self.opcaoAtual = (self.opcaoAtual - 1)%5
            elif event.key == pygame.K_RETURN:
                return self.opcoes[self.opcaoAtual]
        return None
    




class menuAddRanking():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("consolas", 70, True, False)
        #self.opcoes = ("Reiniciar", "Opções", "Menu Principal","Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.nome = ""


    def draw_texto(self, tela, tam_tela, tempo_de_jogo):
        config.tela_virtual.blit(self.bg, (0,0))
        mensagem_fim = "DIGITE SEU NOME"
        mensagem_tempo = f"TEMPO TOTAL: {tempo_de_jogo:0.1f}s"
        mensagem_form_fim = config.fonte_grande.render(mensagem_fim, True, (0, 0, 0))
        mensagem_form_tempo = config.fonte_media.render(mensagem_tempo, True, (0, 0, 0))
        config.tela_virtual.blit(mensagem_form_fim, (300, 30))
        config.tela_virtual.blit(mensagem_form_tempo, (300, 130))
        #pygame.display.flip() #para colocar a mensagem de final na tela
        #pygame.draw.rect(config.tela_virtual, (0, 0, 0), (300 + 30*i, 250, 20, 5))
        
        for i in range(6):
            if i == self.opcaoAtual:
                cor = (254, 56, 103)
            else:
                cor = (255, 255, 255)
            pygame.draw.rect(config.tela_virtual, cor, (550 + 70*i, 500, 60,15))

        for letra in range(len(self.nome)):
            x_form = config.fonte_media.render(self.nome[letra], True, (0, 0, 0))
            config.tela_virtual.blit(x_form,(550 + 70*letra, 420))



    def eventos(self, event):
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.TEXTINPUT:
            self.nome += (event.text).upper()
            self.opcaoAtual += 1
            if self.opcaoAtual == 6:
                self.opcaoAtual = 5
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.nome = self.nome[:-1]
                self.opcaoAtual -= 1
                if self.opcaoAtual < 0:
                    self.opcaoAtual = 0
            if event.key == pygame.K_RETURN:
                self.opcaoAtual = 0
                user = self.nome
                self.nome = ""
                return user

            
        return None
    




class exibirRanking():
    def __init__(self, tela:pygame.surface):
        self.folderPath = config.folderPath
        self.fonte = pygame.font.SysFont("consolas", 30, True, False)
        #self.opcoes = ("Reiniciar", "Opções", "Menu Principal","Sair")
        self.tamanho = tela.get_size()
        self.opcaoAtual = 0
        self.bg = pygame.image.load(os.path.join(self.folderPath,"images","backgrounds","bgIP.png")).convert()
        self.bg = pygame.transform.scale(self.bg, self.tamanho)
        self.dificuldades = ("Fácil", "Médio", "Difícil", "Impossível")


    def draw_texto(self, tela, tam_tela, rankings):
        config.tela_virtual.blit(self.bg, (0,0))
        ranking_boss = "BOSS"
        ranking_infinito = "INFINITO"
        #mensagem_tempo = f"TEMPO TOTAL {tempo_de_jogo:0.1f}s"
        mensagem_form_1 = config.fonte_media.render(ranking_boss, True, (0, 0, 0))
        mensagem_form_2 = config.fonte_media.render(ranking_infinito, True, (0, 0, 0))
        dif = self.fonte.render(self.dificuldades[self.opcaoAtual], True, (0, 0, 0))

        config.tela_virtual.blit(mensagem_form_1, (150, 30))
        config.tela_virtual.blit(mensagem_form_2, (config.bgInitWidth - 500, 27))
        config.tela_virtual.blit(dif, (config.bgInitWidth - 350 - dif.width/2, 120))
        
        
        
        for i in range(len(rankings[0])):
            if 150 + 40*i < config.bgHeight:
                dado_atual = self.fonte.render(f"{rankings[0][i]["user"]}:  {rankings[0][i]["tempo"]:.1f}s" , True, (0, 0, 0))
                config.tela_virtual.blit(dado_atual,(150, 150 + 40 * i) )
        for j in range(len(rankings[1][self.dificuldades[self.opcaoAtual]])):
            if 200 + 40*j < config.bgHeight:   
                dado_atual = self.fonte.render(f"{rankings[1][self.dificuldades[self.opcaoAtual]][j]["user"]}:  {rankings[1][self.dificuldades[self.opcaoAtual]][j]["tempo"]:.1f}s" , True, (0, 0, 0))
                config.tela_virtual.blit(dado_atual,(config.bgInitWidth - 500, 200 + 40 * j) )



    def eventos(self, event):
        if event.type == pygame.QUIT:
            return "sair"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.opcaoAtual -= 1
                if self.opcaoAtual < 0:
                    self.opcaoAtual = 3
            if event.key == pygame.K_d:
                self.opcaoAtual += 1
                if self.opcaoAtual > 3:
                    self.opcaoAtual = 0
            if event.key == pygame.K_ESCAPE:
                return "Voltar"

            
        return None