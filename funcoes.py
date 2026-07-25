import pygame
import os
import config
from player import Jogador
import random
import json

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
musica = (os.path.join(config.folderPath,"sons","musicas","Flying_me_softly.ogg"))
tema_boss = (os.path.join(config.folderPath,"sons","musicas","boss_battle_#2.WAV"))
tema_loja = (os.path.join(config.folderPath,"sons","musicas","8bit Bossa.mp3"))
tema_menu = (os.path.join(config.folderPath,"sons","musicas","8bit-spaceshooter.mp3"))
playlist = {
    "waves": musica,
    "boss": tema_boss,
    "store": tema_loja,
    "title": tema_menu
}
balaJogador = pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","laserThing.wav"))
derrota= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","vgdeathsound.wav"))
hitJogador= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","Hit 1.wav"))
moedinha= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","coin1.wav"))
carrergandoCartucho= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","gun_reload.1.ogg"))
bala1Inimigo = pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot1.ogg"))
bala2Inimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot2.ogg"))
balaShotgunInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","alienshoot3.ogg"))
balaLaserInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","laserbeam.wav"))
explosaoInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","explosion.wav"))
hitInimigo= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","Hit 2.wav"))
venceuBoss= pygame.mixer.Sound(os.path.join(config.folderPath,"sons","soundEffects","Win Jingle.wav"))

musicaIsPaused = False

def criarJogador(deltaTime):
    jogadorCriado = Jogador(
        spriteImage=os.path.join(config.folderPath,'images', 'playerSprites', 'spritesheet(3).png'),
        posInicial=(config.bgInitWidth / 2, config.bgInitHeight-300),
        dt=deltaTime,
        tamanhoMapa=(config.bgInitWidth,config.bgInitHeight)
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

def tocarMusica(nome):
    if config.musicaIsPaused:
        pygame.mixer.music.unpause()
        config.musicaIsPaused = False
    if config.musicaAtual != nome:
        pygame.mixer.music.load(playlist[nome])
        pygame.mixer.music.play(-1)
        config.musicaAtual = nome
    pygame.mixer.music.set_volume(config.volume)


def sons(evento):

    if evento == "BossFight":
        tocarMusica("boss")
    elif evento == "jogando":
        tocarMusica("waves")
    elif evento == "lojinha":
        tocarMusica("store")
    elif evento == "menu principal":
        tocarMusica("title")
    elif evento=="pausado" or evento=="Opções" or evento== "menu boss" or evento== "creditos" or evento== "fim do tutorial" or evento== "tela de morte":
        config.musicaIsPaused=True
        pygame.mixer.music.pause()
    if evento=="balaPlayer":
        balaJogador.set_volume(config.volume/2)
        pygame.mixer.Sound.play(balaJogador)
    if evento=="balaInimigo":
        if random.randint(1,2)==1:
            bala1Inimigo.set_volume(config.volume/2)
            pygame.mixer.Sound.play(bala1Inimigo)
        else:
            bala2Inimigo.set_volume(config.volume/2)
            pygame.mixer.Sound.play(bala2Inimigo)
    if evento=="balaShotgunInimigo":
        balaShotgunInimigo.set_volume(config.volume/2)
        pygame.mixer.Sound.play(balaShotgunInimigo)
    if evento=="laser":
        balaLaserInimigo.set_volume(config.volume/2)
        pygame.mixer.Sound.play(balaLaserInimigo)
    if evento=="ExplosaoInimigo":
        explosaoInimigo.set_volume(config.volume/2)
        pygame.mixer.Sound.play(explosaoInimigo)
    if evento== "powInimigo":
        hitInimigo.set_volume(config.volume/2)
        pygame.mixer.Sound.play(hitInimigo)
    if evento== "powJogador":
        hitJogador.set_volume(config.volume/2)
        pygame.mixer.Sound.play(hitJogador)
    if evento== "pegouMoeda":
        moedinha.set_volume(config.volume/2)
        pygame.mixer.Sound.play(moedinha)
    if evento== "reload":
        carrergandoCartucho.set_volume(config.volume)
        pygame.mixer.Sound.play(carrergandoCartucho)
    if evento== "morteJogador":
        derrota.set_volume(config.volume/2)
        pygame.mixer.Sound.play(derrota)
    if evento== "venceu":
        venceuBoss.set_volume(config.volume)
        pygame.mixer.Sound.play(venceuBoss)

def atualizar_ranking(ranking):
    with open(os.path.join(config.folderPath,"ranking.json"), "w", encoding="utf-8") as rank:
        json.dump(ranking, rank, indent=2) #atualiza o json localmente