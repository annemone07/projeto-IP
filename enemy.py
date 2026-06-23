import pygame
import os
import math #para deixar o código mais claro durante as operações matemáticas
#from time import perf_counter
clock = pygame.time.Clock()
folderPath = os.path.dirname(os.path.abspath(__file__))
inimigos_data = {
            0: {"imagem" : "follow.png", "velocidade" :(700, 250), "vida" : 100, "bala" : "follow"}, 
            1: {"imagem" : "rajada.png", "velocidade" : (300, 250), "vida": 150, "bala": "rajada"},
            2: {"imagem" : "bigger.png", "velocidade": (800, 200), "vida": 75, "bala": "bigger"},
            3 :{"imagem" : "tracker.png", "velocidade": (500, 200), "vida": 125, "bala": "tracker"},
            4 :{"imagem" : "retangulo_verde.png", "velocidade": (400, 250), "vida": 100, "bala": "laser"},
            "boss": {"imagem" : "boss.png", "velocidade": (0, 0), "vida": 1000, "bala": ("follow", "rajada", "bigger", "tracker", "laser")}
               }

class Inimigo(pygame.sprite.Sprite):
    
    def __init__(self, i, dt, pos, limites_mov, sentido_inicial):
        
        super().__init__()
        folderPath = os.path.dirname(os.path.abspath(__file__))
        self.i = i
        self.dt = dt
        
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", inimigos_data[i]["imagem"])).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        if self.i == "boss":
            self.image = pygame.transform.scale(self.image, (pygame.display.Info().current_w - 100, 200))
        #print(self.imagens[i])
        self.rect = self.image.get_rect()
        #print(self.rect)

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
        #self.dDisparo = dDisparo #intervalo entre os disparos
        #self.t_disparo = 0

    """def timer_disparo(self):
        self.t_disparo = perf_counter()
        if self.disparo == 0:
            self.disparo = 1
        else:
            self.disparo = 0"""
    

    def _mudar_sentido(self):
        if self.sentido_inicial == "R":
            self.sentido_inicial = "L"
        elif self.sentido_inicial == "L":
            self.sentido_inicial = "R"
        

    def dir(self):
        
        ##print(self.posicao) #trocar isso aqui por um timer fixo (subir por x segundos, direita por y segundos, etc)
        #if self.velocidadex != 0 and self.velocidadey!=0:
        if self.posicao.x >= self.limites_mov[1]:
            self._mudar_sentido()
        elif self.posicao.x <= self.limites_mov[0]:
            self._mudar_sentido()

        if self.sentido_inicial == "R":
            self.posicao.x += self.velocidadex * self.dt
        elif self.sentido_inicial == "L":
            self.posicao.x -= self.velocidadex * self.dt
        
        self.posicao.y -= self.velocidadey * self.dt

        """elif self.velocidadex != 0:
            if self.posicao.x >= self.limites_mov[1]:
                self._mudar_sentido()
            elif self.posicao.x <= self.limites_mov[0]:
                self._mudar_sentido()
            
            if self.sentido_inicial == "R":
                self.posicao.x += self.velocidadex * self.dt
            elif self.sentido_inicial == "L":
                self.posicao.x -= self.velocidadex * self.dt"""

        """elif self.velocidadey != 0:
            if self.posicao.y >= self.limites_mov[3]:
                self._mudar_sentido()
            elif self.posicao.y <= self.limites_mov[2]:
                self._mudar_sentido()

            if self.sentido_inicial == "R":
                self.posicao.y += self.velocidadey * self.dt
            elif self.sentido_inicial == "L":
                self.posicao.y -= self.velocidadey * self.dt"""
                #print("DESCE CARALHO PORRA")

            #print(f"POSICAO DESSE CORNO {self.posicao}")



    def update(self, dt, camera):
        self.dt = dt
        if self.i != "boss" or (self.i == "boss" and self.rect.bottomleft[1]< 200):  
            if self.i != "boss":    
                self.dir()  
            self.posicao.y -= camera.y
            self.rect.centerx = self.posicao.x - camera.x
            self.rect.centery = self.posicao.y
        #print("OLHA AQUI"), print(self.rect.centery)
        """self.direcao.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direcao.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direcao != (0, 0):
            self.direcao = self.direcao.normalize()"""
        

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, image, posicao, dt, tipo, boss):
        "folderPath = os.path.dirname(os.path.abspath(__file__))"
        self.dados_balas = {"follow": {"velocidade" :600, "imagem": "bala-vermelha-retang..png"}, 
                       "rajada": {"velocidade" : 500, "imagem" :"bala-amarela-hexa.png"}, 
                       "bigger": {"velocidade" :400, "imagem" : "bala-roxo-retang..png" }, 
                       "tracker": {"velocidade" :450, "imagem" : "bala-''cinza''-retang..png"},
                       "laser" : {"velocidade" : 12, "imagem" : "balaLaser3.png", "danos": (5, 10, 20, 40, 80, 100)}
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
        else:
            self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", "estadosLaser", self.imagem)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 1000))
            self.rect = self.image.get_rect()
            self.rect.centerx = posicao[0]
            self.rect.centery = posicao[1] + (self.rect.height/2)
        
            self.primeira_pos = (posicao[0], posicao[1] + (self.rect.height/2))
        
        
        
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.estado_laser = 0
        self.contador_mover = 0
        


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
                print("rect bullet bigger", self.rect)
        
        #print(self.dire)
        self.posicao.x += (self.dire.x) * self.dt
        self.posicao.y += (self.dire.y) *self.dt
        #atualiza a posicao atual
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y

        print("AQUI TB"), print(self.rect.topright[1])


    def mudar_disparo(self):
        if self.disparo == 0:
            self.disparo =1
        else:
            self.disparo =0

            

    def update(self, dt, camera, playerPos, mudar, laser, enemyPos):
        k = 0
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
                    estados_laser = (10, 15, 20, 25, 40)
                    if self.estado_laser != 4:
                        self.estado_laser += 1
                if self.boss:
                    estados_laser = (10, 20, 40, 80, 100, 200)
                    if self.estado_laser !=5:
                        self.estado_laser += 1
                        continuar = 1

                if not continuar:
                    self.kill()
                else:
                    self.image = pygame.transform.scale(self.image, (estados_laser[self.estado_laser], 1000))
                    diff_x = (estados_laser[self.estado_laser] - estados_laser[self.estado_laser -1])/estados_laser[self.estado_laser - 1]
                    

                    
            if k == len(enemyPos) - 1 and continuar:
                self.rect.centerx = enemyPos[k][0]
                self.rect.centery = enemyPos[k][1] + (self.rect.height/2)
                self.rect = self.rect.scale_by(diff_x, 1)
            
                self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        
        


        
        

