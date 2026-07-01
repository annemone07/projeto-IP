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
balaLaserInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","laserbeam.wav"))
explosaoInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","explosion.wav"))
hitJogador= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","Hit 1.wav"))
hitInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","Hit 2.wav"))
moedinha= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","coin1.wav"))

musicaIsPaused = False

def criarJogador(deltaTime):
    jogadorCriado = Jogador(
        spriteImage=os.path.join(config.folderPath,'images', 'playerSprites', 'spritesheet(3).png'),
        posInicial=(config.bgInitWidth / 2, config.bgInitHeight-300),
        dt=deltaTime,
        tamanhoMapa=(config.bgInitWidth,config.bgInitHeight)

        #grupos=self.all_sprites,
        #game=self
    )
    return jogadorCriado

def resetarVariaveis(grupoGrupos, intermediario):
    grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoShotgun, grupoCura, grupoMoeda, grupoIma, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser, grupoExplosion = grupoGrupos
    grupoItem.empty()
    grupoEscudo.empty()
    grupoQuickShot.empty()
    grupoBulletTime.empty()
    grupoShotgun.empty()
    grupoCura.empty()
    grupoMoeda.empty()
    grupoIma.empty()
    grupoRastro.empty()
    grupoBala.empty()
    grupoInimigo.empty()
    grupoBullets.empty()
    grupoLaser.empty()
    grupoExplosion.empty()
    if not intermediario:
        grupoJogador.empty()
    
def sons(evento):
    if evento=="jogando":
        if not config.musicaIsPaused:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(config.volume)
        else:
            config.musicaIsPaused=False
            pygame.mixer.music.unpause()
    elif evento=="pausado":
        config.musicaIsPaused=True
        pygame.mixer.music.pause()
    #else evento=="":
    #    pygame.mixer.music.fadeout(200)
    if evento in ("menu principal","tela de morte","creditos","fim do tutorial","escolher modo","escolher dificuldade","Opções"):
        pygame.mixer.music.fadeout(200)
    if evento=="balaPlayer":
        balaJogador.set_volume(config.volume)
        pygame.mixer.Sound.play(balaJogador)
    if evento=="balaInimigo":
        if random.randint(1,2)==1:
            bala1Inimigo.set_volume(config.volume)
            pygame.mixer.Sound.play(bala1Inimigo)
        else:
            bala2Inimigo.set_volume(config.volume)
            pygame.mixer.Sound.play(bala2Inimigo)
    if evento=="balaShotgunInimigo":
        balaShotgunInimigo.set_volume(config.volume)
        pygame.mixer.Sound.play(balaShotgunInimigo)
    if evento=="laser":
        balaLaserInimigo.set_volume(config.volume)
        pygame.mixer.Sound.play(balaLaserInimigo)
    if evento=="ExplosaoInimigo":
        explosaoInimigo.set_volume(config.volume)
        pygame.mixer.Sound.play(explosaoInimigo)
    if evento== "powInimigo":
        hitInimigo.set_volume(config.volume)
        pygame.mixer.Sound.play(hitInimigo)
    if evento== "powJogador":
        hitJogador.set_volume(config.volume)
        pygame.mixer.Sound.play(hitJogador)
    if evento== "pegouMoeda":
        moedinha.set_volume(config.volume)
        pygame.mixer.Sound.play(moedinha)