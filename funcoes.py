import pygame
import os
import config
from player import Jogador
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
musica = (os.path.join(config.folderPath,"sons","musicas","Flying_me_softly.ogg"))
pygame.mixer.music.load(musica)
balaJogador = pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","laserThing.wav"))
bala1Inimigo = pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot1.ogg"))
bala2Inimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot2.ogg"))
balaShotgunInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot3.ogg"))
balaLaserInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot2.ogg"))

musicaIsPaused = False

def criarJogador(deltaTime):
    jogadorCriado = Jogador(
        spriteImage=os.path.join(config.folderPath,'images', 'playerSprites', 'spritesheet_player_spaceship_up2.png'),
        posInicial=(config.bgWidth / 2, config.bgHeight-300),
        dt=deltaTime,
        tamanhoMapa=(config.bgWidth,config.bgHeight)
        #grupos=self.all_sprites,
        #game=self
    )
    return jogadorCriado

def resetarVariaveis(grupoGrupos, intermediario):
    grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoShotgun, grupoCura, grupoMoeda, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser = grupoGrupos
    grupoItem.empty()
    grupoEscudo.empty()
    grupoQuickShot.empty()
    grupoBulletTime.empty()
    grupoShotgun.empty()
    grupoCura.empty()
    grupoMoeda.empty()
    grupoRastro.empty()
    grupoBala.empty()
    grupoInimigo.empty()
    grupoBullets.empty()
    grupoLaser.empty()
    if not intermediario:
        grupoJogador.empty()
    
def sons(evento):
    if evento=="jogando":
        if not config.musicaIsPaused:
            pygame.mixer.music.play(-1)
        else:
            config.musicaIsPaused=False
            pygame.mixer.music.unpause()
    elif evento=="pausado":
        config.musicaIsPaused=True
        pygame.mixer.music.pause()
    #else evento=="":
    #    pygame.mixer.music.fadeout(200)
    
    if evento=="balaPlayer":
        pygame.mixer.Sound.play(balaJogador)
    if evento=="balaInimigo":
        if random.randint(1,2)==1:
            pygame.mixer.Sound.play(bala1Inimigo)
        else:
            pygame.mixer.Sound.play(bala2Inimigo)
    if evento=="balaShotgunInimigo":
        pygame.mixer.Sound.play(balaShotgunInimigo)
    if evento=="laser":
        pygame.mixer.Sound.play(balaLaserInimigo)