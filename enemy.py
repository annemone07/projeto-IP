import pygame
import os
import math #para deixar o código mais claro durante as operações matemáticas
#from time import perf_counter
clock = pygame.time.Clock()
folderPath = os.path.dirname(os.path.abspath(__file__))
inimigos_data = {
            0: {"imagem" : "Follow-W1.png", "velocidade" :(550, 250), "vida" : 100, "bala" : "follow"}, 
            1: {"imagem" : "Rajada-W1.png", "velocidade" : (300, 250), "vida": 150, "bala": "rajada"},
            2: {"imagem" : "Bigger-W1.png", "velocidade": (800, 200), "vida": 75, "bala": "bigger"},
            3 :{"imagem" : "Tracker-W1.png", "velocidade": (500, 200), "vida": 125, "bala": "tracker"},
            4: {"imagem" : "Kamikaze-W1.png", "velocidade": (900, 200), "vida": 50, "bala": "self"},
            5 :{"imagem" : "Laser-W1.png", "velocidade": (400, 250), "vida": 100, "bala": "laser"},
            "Boss-W1": {"imagem" : "boss-W1.png", "velocidade": (0, 0), "vida": 1000, "bala": ("follow", "rajada", "bigger", "tracker", "laser")}
               }

class Inimigo(pygame.sprite.Sprite):
    
    def __init__(self, i, dt, pos, limites_mov, sentido_inicial):
        
        super().__init__()
        folderPath = os.path.dirname(os.path.abspath(__file__))
        self.i = i
        self.dt = dt
        
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", inimigos_data[i]["imagem"])).convert_alpha()
        self.image = pygame.transform.scale(self.image, (256, 256))
        if self.i == "Boss-W1":
            self.image = pygame.transform.scale(self.image, (1.5*pygame.display.Info().current_w, (pygame.display.Info().current_w)*0.8))
        #print(self.imagens[i])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.velocidadex = inimigos_data[i]["velocidade"][0]
        self.velocidadey = inimigos_data[i]["velocidade"][1]
        self.direcao = pygame.Vector2()
        self.posicao = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.vida = inimigos_data[i]["vida"]
        self.limites_mov = limites_mov #padrão --> (x_min, x_max)
        self.sentido_inicial = sentido_inicial
        self.tipo_bala = inimigos_data[i]["bala"]
        self.disparo = 1
        if self.i == 5:
            self.disparo = 0
        #self.dDisparo = dDisparo #intervalo entre os disparos
        #self.t_disparo = 0
        if self.i == 4: #para deixar o laser alinhado
            self.rect = self.rect.inflate(0, -45)
        self.stop = 0 #para o kamikaze
        

            
    def dir(self):
        
        ##print(self.posicao) #trocar isso aqui por um timer fixo (subir por x segundos, direita por y segundos, etc)
        #if self.velocidadex != 0 and self.velocidadey!=0:
        if self.posicao.x > self.limites_mov[1] and self.sentido_inicial == "R":
            self.sentido_inicial = "L"
        elif self.posicao.x <= self.limites_mov[0] and self.sentido_inicial == "L":
            self.sentido_inicial = "R"

        if self.sentido_inicial == "R":
            self.posicao.x += self.velocidadex * self.dt
        elif self.sentido_inicial == "L":
            self.posicao.x -= self.velocidadex * self.dt
        
        self.posicao.y -= self.velocidadey * self.dt

    def follow(self, posSelf, posJog):
        dx = (posJog[0] - posSelf[0])
        dy = (posJog[1] - posSelf[1])
        if dx !=0: #para evitar divisao por zero    
            ang = (math.atan(dy/dx))
        else:
            ang = (math.pi)/2
        angG = math.degrees(ang)
        cos = math.cos(ang)
        sin = math.sin(ang)
        if (dx <=0 and dy <= 0) or (dy >= 0 and dx<=0): #caso precise inverter alguma coordenada
            cos = -cos
            sin = -sin
        
        self.tracking = pygame.Vector2(cos*self.velocidadex, sin*self.velocidadex)
        self.stop = 1
        #rotacionando
        self.image = pygame.transform.rotate(self.image, angG)
        self.rect = self.image.get_rect()
        print(angG)

    def update(self, dt, camera):
        self.dt = dt
        if (self.i in (0, 1, 2, 3 ,4) or (self.i == "Boss-W1" and self.rect.bottomleft[1]< 200)) or (self.i ==5 and self.stop == 0):  
            if self.i != "Boss-W1":    
                self.dir()  
            self.posicao.y -= camera.y
            self.rect.centerx = self.posicao.x - camera.x
            self.rect.centery = self.posicao.y
        
        elif (self.i == 5 and self.stop == 1):
            self.posicao.x += self.tracking[0] * dt
            self.posicao.y += (self.tracking[1] * dt)

            self.rect.centerx = self.posicao.x
            self.rect.centery = self.posicao.y

            #self.hitbox.center = self.rect.center
        #print("OLHA AQUI"), print(self.rect.centery)

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, image, posicao, dt, tipo, boss):
        "folderPath = os.path.dirname(os.path.abspath(__file__))"
        self.dados_balas = {"follow": {"velocidade" :600, "imagem": "bala-vermelha-retang..png"}, 
                       "rajada": {"velocidade" : 500, "imagem" :"bala-amarela-hexa.png"}, 
                       "bigger": {"velocidade" :400, "imagem" : "bala-roxo-retang..png" }, 
                       "tracker": {"velocidade" :450, "imagem" : "bala-''cinza''-retang..png"},
                       "laser" : {"velocidade" : 12, "imagem" : "laser-bonito.png", "danos": (10, 20, 40, 80, 100)}
                       }
        #print("teste 1")
        super().__init__()
        self.boss = boss
        self.dt = dt
        self.velocidade = self.dados_balas[tipo]["velocidade"]
        self.disparo = 1
        self.tipo = tipo
        self.imagem = self.dados_balas[tipo]["imagem"]
        if tipo != "laser":
            self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", self.imagem)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()
            self.rect.centerx = posicao[0]
            self.rect.centery = posicao[1]
            self.rect = self.image.get_rect(center=posicao)
            self.dano = 20
            print(f"POSICAO FINAL{self.rect.center}")
        else:
            self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", "estadosLaser", self.imagem)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 1000))
            self.rect = self.image.get_rect()
            self.rect.centerx = posicao[0]
            self.rect.centery = posicao[1] + (self.rect.height/2)
        
            self.primeira_pos = (posicao[0], posicao[1] + (self.rect.height/2))
            self.dano = 10
            self.ja_laser = 0
        
        
        
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.estado_laser = 0
        self.contador_mover = 0
        self.mask = pygame.mask.from_surface(self.image)

        


    def direcao(self, posA, posB, pow):
        dx = (posA[0] - posB[0])
        dy = (posA[1] - posB[1])
        
        if self.tipo == "follow" or self.tipo == "bigger" or self.tipo == "tracker":
            if dx !=0: #para evitar divisao por zero    
                ang = (math.atan(dy/dx))
            else:
                ang = (math.pi)/2
            cos = math.cos(ang)
            sin = math.sin(ang)
            if (dx <=0 and dy <= 0) or (dy >= 0 and dx<=0): #caso precise inverter alguma coordenada
                cos = -cos
                sin = -sin
            self.dire = pygame.math.Vector2((cos*self.velocidade), (sin*self.velocidade))
    
        if self.tipo == "rajada":
            if dy <0:
                dy = -dy
            #print(pow)
            indicies = {"b0" : (0, -posB[0]), "b1" : (posB[0], 0), "b2" : (-posB[0], 0), "b3":(0, posB[0]), "b4" :(118, 96), "b5": (118, -96), "b6": (-118, 96), "b7" :(-118, -96)}
            if pow not in (0, 3):
                ang = math.atan(indicies[f"b{pow}"][1]/indicies[f"b{pow}"][0])
            else:
              ang = (math.pi)/2
            cos = math.cos(ang)
            sin = math.sin(ang)
            if pow in (0, 2, 5, 7): #correcao para os valores do cosseno negativo
                cos = -cos
            """if sin<0:  #correcao para o seno, para ele sempre atirar p baixo 
                sin = -sin"""
            self.dire = pygame.math.Vector2((cos*self.velocidade), (sin*self.velocidade))
            #print("AQUI porra"),print(self.dire)

        if self.tipo == "laser":
            self.dire = pygame.math.Vector2(0, self.velocidade)


    def mov(self, camera):
        #if self.tipo == "follow":    
            
            #caso especial do bigger
            
        if self.tipo == "bigger":
            deltax = int(self.rect.bottomright[0] - self.rect.bottomleft[0])
            deltay = int(abs(self.rect.bottomleft[1] - self.rect.topleft[1]))
            if deltax < 300 and deltay < 300:    
                self.image = pygame.transform.scale(self.image, (int(deltax*1.02), int(deltay*1.02)))
                self.rect = self.rect.scale_by(1.02, 1.02)
                #print("rect bullet bigger", self.rect)
        
        #print(self.dire)
        self.posicao.x += (self.dire.x) * self.dt
        self.posicao.y += (self.dire.y) *self.dt
        #atualiza a posicao atual
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y

        #print("AQUI TB"), print(self.rect.topright[1])


    def mudar_disparo(self):
        if self.disparo == 0:
            self.disparo =1
        else:
            self.disparo =0

            

    def update(self, dt, camera, playerPos, mudar, laser, enemyPos):
        self.mov(camera)
        self.dt = dt
        if abs(playerPos.x-self.posicao.x) >= 3000 or abs(playerPos.y-self.posicao.y) >= 3000:
            self.kill()
            #print("Dead")
        if self.tipo == "tracker" and mudar and self.contador_mover < 3:
            self.direcao(playerPos, self.posicao, pow="null")
            self.contador_mover += 1

        if self.tipo == "laser":
            continuar = 0
            if laser: 
                if not self.boss:
                    continuar = 1
                    estados_laser = (10, 20, 30, 50, 60)
                    if self.estado_laser != 4:
                        self.estado_laser += 1
                if self.boss:
                    estados_laser = (20, 40, 80, 100, 200)
                    if self.estado_laser !=4:
                        self.estado_laser += 1
                        continuar = 1

                if not continuar:
                    self.kill()
                else:
                    self.image = pygame.transform.scale(self.image, (estados_laser[self.estado_laser], 1000))
                    self.rect = self.image.get_rect()
                    self.dano = self.dados_balas["laser"]["danos"][self.estado_laser]
                      
            if len(enemyPos) == 0:
                self.kill()
            else: #atualiza o laser p ficar sempre embaixo do inimigo, só tenta atualizar se tiver passado pelo menos 1 inimigo com laser   
                self.rect.centerx = enemyPos[0][0] 
                self.rect.centery = enemyPos[0][1] + (self.rect.height/2)
                self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
            
        
        


        
        

