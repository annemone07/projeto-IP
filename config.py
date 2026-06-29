import pygame
import os

#se for mover o deltaTime pra ca alterar todos as variaveis do mainCode pra config.variavel

pygame.init()
folderPath = os.path.dirname(os.path.abspath(__file__))
camera = pygame.math.Vector2(0, -6)
bgHeight = pygame.display.Info().current_h
bgWidth = pygame.display.Info().current_w
#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]
telaSizePlaceholder = (bgWidth,bgHeight)
os.environ['SDL_VIDEO_CENTERED'] = '1'
tela = pygame.display.set_mode(telaSizePlaceholder, pygame.RESIZABLE, display=0)
fonte = pygame.font.SysFont("arial", 40, True, False)
fonte_grande = pygame.font.SysFont("arial", 100, True, False)
fonte_media = pygame.font.SysFont("arial", 65, True, False)
fps=60
volume = 1.0

#configs de sons e musicas
musicaIsPaused = False