import pygame
import os
import config
from player import Jogador

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
musica = (os.path.join(config.folderPath,"sons","musicas","Flying_me_softly.ogg"))
pygame.mixer.music.load(musica)

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
    grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoCura, grupoMoeda, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser = grupoGrupos
    grupoItem.empty()
    grupoEscudo.empty()
    grupoQuickShot.empty()
    grupoBulletTime.empty()
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
    else:
        pygame.mixer.music.fadeout(200)