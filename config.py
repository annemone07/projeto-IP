import pygame
import os

#se for mover o deltaTime pra ca alterar todos as variaveis do mainCode pra config.variavel

pygame.init()
folderPath = os.path.dirname(os.path.abspath(__file__))
camera = pygame.math.Vector2(0, -6)
bgHeight = pygame.display.Info().current_h
bgWidth = pygame.display.Info().current_w
bgInitWidth = pygame.display.get_desktop_sizes()[0][0] #IMPORTANTE, USAR ESSE PRA POSICIONAR TEXTOS DOS MENUS (não sei direito pq mas precisa ser o inicial)
bgInitHeight = pygame.display.get_desktop_sizes()[0][1]
telaSizePlaceholder = (bgWidth,bgHeight)
os.environ['SDL_VIDEO_CENTERED'] = '1'
tela = pygame.display.set_mode(telaSizePlaceholder, pygame.RESIZABLE, display=0)
tela_virtual = pygame.Surface(telaSizePlaceholder)
tela_escalada = pygame.transform.smoothscale(tela_virtual, (bgWidth,bgHeight))
fonte = pygame.font.SysFont("arial", 40, True, False)
fonte_grande = pygame.font.SysFont("arial", 100, True, False)
fonte_media = pygame.font.SysFont("consolas", 65, True, False)
fonte_titulo = pygame.font.SysFont("comic sans", 180)
fps=60
volume = 1.0
musicaAtual = None
#configs de sons e musicas
musicaIsPaused = False