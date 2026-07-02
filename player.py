import pygame
import os
import math


clock = pygame.time.Clock()

# =============================================================================
class Jogador(pygame.sprite.Sprite):
    
    folderPath = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, spriteImage, posInicial, dt, tamanhoMapa):
        
        super().__init__()

        self.tamanhoMapa = tamanhoMapa
        self.deltaTime = dt
        self.images = []
        self.sheet = pygame.image.load(spriteImage).convert_alpha()
        self.direction=pygame.math.Vector2()
        self.animacoes = self.fatiar_spritesheet(self.sheet)
        self.estadoAnimacao = "run"
        self.frameAtual = 0
        self.velocidade = 1000
        self.image = self.animacoes["run"][0] #pygame.image.load(os.path.join(folderPath, "images", "playerSprites", "climb-0.png")).convert_alpha()
        self.rect = self.image.get_rect()
        #Criando a hitbox:
        self.hitbox = pygame.Rect(0, 0, 100, 100)
        self.rect.center = posInicial
        self.hitbox.center = posInicial
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.vida = 100
        self.invencibilidade = False
        self.tempoPiscar = 0.5
        self.escudo = 0
        self.armadura = 0
        self.kills = 0
        self.quick_shot = False
        self.charge = 0
        self.bullet_time = False
        self.moedas = 0
        self.arma = 'normal'#Tipo da arma do player
        self.cartuchos = 0 #Balas da shotgun
        self.mask = pygame.mask.from_surface(self.image)

    def fatiar_spritesheet(self,sheet):
        larguraSprite=48
        alturaSprite=48
        animacoes = {"run":[]}
        for linha in range(4):
            for coluna in range(8):
                x = larguraSprite*coluna
                y = alturaSprite*linha
                sprite = sheet.subsurface(pygame.Rect(x,y, larguraSprite, alturaSprite))
                sprite = pygame.transform.scale(sprite, (200, 200))
                animacoes["run"].append(sprite)

        return animacoes
            
    def getDirection(self):
        moveKeys = pygame.key.get_pressed()
        self.direction.x = int(moveKeys[pygame.K_d]) - int(moveKeys[pygame.K_a])
        self.direction.y = int(moveKeys[pygame.K_s]) - int(moveKeys[pygame.K_w])
        #pelo jeito da erro se tentar normalizar um vetor (0,0)
        if self.direction != (0,0):
            self.direction = self.direction.normalize()
    
    def movimentacao(self, camera):
        nextPosX = self.posicao.x + self.direction.x * self.velocidade * self.deltaTime
        nextPosY = (self.posicao.y + self.direction.y * self.velocidade * self.deltaTime)# - 6 colocar movimentação padrão do player    
        if nextPosX >= self.rect[2]/4 and nextPosX <= (self.tamanhoMapa[0])-self.rect[2]/4:
            self.posicao.x = nextPosX
            self.rect.centerx = self.posicao.x
        if nextPosY <= (self.tamanhoMapa[1])-self.rect[3]/4 and nextPosY >= self.rect[3]/4: #nextPosY >= self.rect[3]/4 and
            self.posicao.y = nextPosY+2
            self.rect.centery = self.posicao.y
        
        #Hitbox 2:
        self.hitbox.center = self.rect.center
    
    def player_update(self, tipo): #Atualizar quando o player sofrer algum evento
        if tipo == "D":
            self.invencibilidade = not self.invencibilidade
        elif tipo == "PU":
            self.quick_shot = not self.quick_shot
        elif tipo == "kabum":
            if self.arma == "normal":
                self.arma = "shotgun"
            else:
                self.arma = "normal"
        self.image_update()

    def image_update(self):
        if self.vida <= 25:
            indice = 3
        elif self.vida <= 50:
            indice = 2
        elif self.vida <= 75:
            indice = 1
        else:
            indice = 0
        # Shotgun 
        if self.arma == "shotgun":
            indice += 16
        # Quick_Shot
        if self.quick_shot:
            indice += 8
        # dano
        if self.invencibilidade:
            indice += 4

        self.image = self.animacoes["run"][indice]

    
    def add_kill(self):
        self.kills += 1

    def update(self,dt,camera):
        self.deltaTime = dt
        self.getDirection()
        self.movimentacao(camera)
        self.image_update()#Atualiza o sprite sempre, sem depender de acontecer algum evento

# =============================================================================
#Rastro do player que vai ser usado no Bullet Time
class Rastro_Bullet_Time(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        #criar uma cópia da imagem pra não mexer no jogador
        self.image = image.copy()
        self.rect = rect.copy()
        self.image.fill((50, 150, 255), special_flags=pygame.BLEND_RGB_ADD)
        self.alpha = 80 
        self.image.set_alpha(self.alpha)

    def update(self, dt, camera):
        self.alpha -= 250 * dt 
        if self.alpha <= 0:
            self.kill() # Destrói o fantasma quando ficar invisível
        else:
            self.image.set_alpha(self.alpha)
# =============================================================================

#Bala do player:
class Bala(pygame.sprite.Sprite):
    folderPath = os.path.dirname(os.path.abspath(__file__))
    def __init__(self, image, posicao, dt):
        super().__init__()
        self.dt = dt
        self.image = pygame.image.load(os.path.join(image)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posicao[0]
        self.rect.centery = posicao[1]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.velocidade = 600
        self.dire = pygame.math.Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        
        
    def direcao(self, posA, posB, inclinação=0):
        dx = (posA[0] - posB[0])
        dy = (posA[1] - posB[1])

        ang_base = (math.atan2(dy/dx))
        ang_final = ang_base + math.radians(inclinação)
        cos = math.cos(ang_final)
        sin = math.sin(ang_final)

        self.dire = pygame.math.Vector2(math.ceil(cos*self.velocidade), math.ceil(sin*self.velocidade))


    def mov(self, camera):
        self.posicao.x += (self.dire.x + camera.x) * self.dt
        self.posicao.y += (self.dire.y + camera.y) * self.dt
        #atualiza o centro
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y

        
        
    def update(self, dt, camera, playerPos):
        self.mov(camera)
        self.dt = dt
        if abs(playerPos.x-self.posicao.x) >= 3000 or abs(playerPos.y-self.posicao.y) >= 3000:
            self.kill()
# =============================================================================
