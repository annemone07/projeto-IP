import pygame
import math
from player import Jogador, Rastro_Bullet_Time, Bala
from enemy import Inimigo, Bullet, Explosion
import sys
import os
import random
from itens import itemGeral, ParteEscudo, Quick_Shot, Moedas, Cura, Charge, Ima, Shotgun
from time import perf_counter, sleep
from loja import Loja
from menu import MenuPrincipal, menuPause, telaMorte, Creditos, menuFimTutorial, menuModos, menuDificuldade, menuOpcoes, menuFimBoss, menuAddRanking, exibirRanking, menuTeclas
import config
from funcoes import criarJogador, resetarVariaveis, sons

#configs permanentes
pygame.init() 
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("AeroHell") #alterar para o nome do jogo dps
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000

#variáveis do BG scrollante
bg = pygame.image.load(os.path.join(config.folderPath,"images","backgrounds","bgIP.png")).convert()
bg = pygame.transform.scale(bg, (config.bgWidth,config.bgHeight))
bgSize = bg.get_rect()
scroll=0
tiles = math.ceil(config.bgHeight/bg.get_height())+2

#criar inimigo(s) inicial, para o futuro tutorial


#Evento de spawn - Moeda Ouro
create_Moeda_Ouro = pygame.USEREVENT + 1
pygame.time.set_timer(create_Moeda_Ouro, 700)

#Evento de spawn - Moeda Prata
create_Moeda_Prata = pygame.USEREVENT + 11
pygame.time.set_timer(create_Moeda_Prata, 700)

#Evento de spawn - Cura
create_Cura = pygame.USEREVENT + 2
pygame.time.set_timer(create_Cura, 2000)

#Evento de spawn - Escudo
create_escudo = pygame.USEREVENT + 3
pygame.time.set_timer(create_escudo, 1000)

#Evento de spawn - Quick_shot
create_quickshot = pygame.USEREVENT + 4
pygame.time.set_timer(create_quickshot, 2000)

#Evento de spawn - Cargas
create_charge = pygame.USEREVENT + 5
pygame.time.set_timer(create_charge, 2200)

#Evento de spawn - Shotgun:
create_shotgun = pygame.USEREVENT + 6
pygame.time.set_timer(create_shotgun, 1700)

#eventos de disparo para cada tipo de bala
deltaDisparos = {"follow": 1000, "rajada": 3000, "bigger": 5000, "tracker": 5000, "laser" : 6000}
balas_possiveis = ("follow", "rajada", "bigger", "tracker")
pontos_possiveis = ((config.bgInitWidth/2, 200), ((config.bgInitWidth/2) + 150, 200), ((config.bgInitWidth/2) - 150, 200), ((config.bgInitWidth/2) + 500, 200), ((config.bgInitWidth/2) -500, 200))
create_bala0, create_bala1, create_bala2, create_bala3, create_bala4 = pygame.USEREVENT + 7,  pygame.USEREVENT + 8, pygame.USEREVENT + 7, pygame.USEREVENT + 10, pygame.USEREVENT + 11
pygame.time.set_timer(create_bala0, deltaDisparos["follow"]), pygame.time.set_timer(create_bala1, deltaDisparos["rajada"]), pygame.time.set_timer(create_bala2, deltaDisparos["bigger"]), pygame.time.set_timer(create_bala3, deltaDisparos["tracker"]), pygame.time.set_timer(create_bala4, deltaDisparos["laser"])

#variáveis do disparo do inimigo 
mudar_direcao, mudar_laser = pygame.USEREVENT + 12,  pygame.USEREVENT + 13
pygame.time.set_timer(mudar_direcao, 1000), pygame.time.set_timer(mudar_laser, 1000)
#timers do boss
disparo_boss, criar_laser = pygame.USEREVENT + 14, pygame.USEREVENT + 15
pygame.time.set_timer(disparo_boss, 500), pygame.time.set_timer(criar_laser, 10000)
boss_laser = 0

#ima
create_ima = pygame.USEREVENT + 16
pygame.time.set_timer(create_ima, 10000)

#variaveis globais entre as cenas
main = True
estadoDoJogo = "menu principal"
ultimoEstado = None
inicio_de_jogo = perf_counter ()

#Novas variáveis do tiro:
cooldown_normal = 0.35
cooldown_especial = 0.15
intervalo_tiro = cooldown_normal
ultimo_tiro = 0

#variaveis do power up quickshot
quick_shot_t_inicio = 0
duracao =  5

#telas
menu_principal = MenuPrincipal(config.tela_virtual)
menu_pause = menuPause(config.tela_virtual)
tela_de_morte = telaMorte(config.tela_virtual)
creditos = Creditos(config.tela_virtual)
fim_do_tutorial = menuFimTutorial(config.tela_virtual)
escolher_modo = menuModos(config.tela_virtual)
escolher_dificuldade = menuDificuldade(config.tela_virtual)
menu_opcoes = menuOpcoes(config.tela_virtual)
loja = Loja()
menu_boss = menuFimBoss(config.tela_virtual)
menu_input = menuAddRanking(config.tela_virtual)
menu_ranking = exibirRanking(config.tela_virtual)
menu_teclas = menuTeclas(config.tela_virtual)

#temporizadores
t_invencibilidade = 0
t_clicks = 0
tempo_inicio = 0
tempoReiniciar=0.0
tempo_morte=0.0
tempo_de_jogo = perf_counter() - inicio_de_jogo
tempo_no_menu = 0.0
inicio_menu = 0.0

#configs primeiro load
jogador = criarJogador(deltaTime)

#criar grupos de sprite
grupoItem = pygame.sprite.Group()
grupoEscudo = pygame.sprite.Group()
grupoQuickShot = pygame.sprite.Group()
grupoBulletTime = pygame.sprite.Group()
grupoShotgun =  pygame.sprite.Group()
grupoCura = pygame.sprite.Group()
grupoMoeda = pygame.sprite.Group()
grupoJogador = pygame.sprite.Group()
grupoRastro = pygame.sprite.Group()
grupoBala = pygame.sprite.Group()
grupoInimigo = pygame.sprite.Group()
grupoBullets = pygame.sprite.Group()
grupoLaser = pygame.sprite.Group()
grupoIma = pygame.sprite.Group()
grupoExplosion = pygame.sprite.Group()


grupoGrupos = (grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoShotgun, grupoCura, grupoMoeda, grupoIma, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser, grupoExplosion)

#variáveis do bullet time
rect_anterior = jogador.rect.copy() #Salvar a posição do player pra criar o rasto
contador_rastros = 0 #Evitar que crie algum rastro que não seja a partir dos últimos movimentos
wave_counter = 0 #variavel para contar as waves
venceu = 0
ja_entrou = 0 #p n entrar na loja infinitas vezes seguidas
acabou_sair = 0 #para a boss fight
filtro_bullet_time = pygame.Surface(config.telaSizePlaceholder, pygame.SRCALPHA)
filtro_bullet_time.fill((0, 0, 0, 150))
filtro_pause = pygame.Surface(config.telaSizePlaceholder, pygame.SRCALPHA)
filtro_pause.fill((0, 0, 0, 180))
minimo_inimigos=(3, 3, 4, 5, 6, 7, 10)
tempo_ima_ativo = -999
duracao_ima = 20
boss_fight = 0
pode_spawn_laser = 1
mudar, laser = 0, 0 #variaveis para as balas com condições especiais
ranking_boss = [] #rankings são locais, resetam toda vez que o jogo é iniciado
ranking_infinito = {"Fácil": [], "Médio": [], "Difícil": [], "Impossível": []} #armazena por dificuldade
acabou = 0
tempo_jogo_fim, nao_pode_entrar_mais = 0, 0
while main:
    grupoGrupos = (grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoShotgun, grupoCura, grupoMoeda, grupoIma, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser, grupoExplosion)
    #todos os eventos
    for event in pygame.event.get():
        #condição de parada
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main=False

        if wave_counter != 5 and estadoDoJogo != ultimoEstado:
            sons(estadoDoJogo)
            ultimoEstado = estadoDoJogo
            
        #um if pra cada estado do jogo
        if estadoDoJogo=="menu principal":
            selecao = menu_principal.eventos(event)
        
            if selecao=="Jogar": #Menu principal ---Selecionar---> Tela de Jogar(seleção de modos)
                estadoDoJogo="escolher modo"
                resetarVariaveis(grupoGrupos, 0)#Apagar todo mundo
                jogador = criarJogador(deltaTime)#Cria um jogador novo, esse que tem que ter suas variáveis internas zeradas
                wave_counter = 0#Resetar as Waves
                inicio_de_jogo=perf_counter()#Reiniciar o contador de jogo
                tempo_no_menu=0.0#Tempo passado no menu é zerad
                inicio_menu = perf_counter()
                boss_fight = 0

                
            elif selecao == "Tutorial": #Menu principal ---Selecionar---> Tutorial
                estadoDoJogo = "jogando" #Tutorial rodando
                modo = "tutorial"
                grupoJogador.add(jogador)#Criar o Novo Player
                enemy01 = Inimigo(i =0, dt=deltaTime, pos=(config.bgInitWidth/2, -50), limites_mov=(300, config.bgInitWidth - 300), sentido_inicial="L")
                #Criação do Inimigo do tutorial ↑
                contador_de_teclas_mov, contador_de_teclas_espaco, contador_itens, fim_tutorial, passa_tutorial = 0, 0, 0, 0, 0
    
            elif selecao=="Creditos": #Menu principal ---Selecionar---> Tela de créditos
                estadoDoJogo="creditos"
       
            elif selecao=="Opções": #Menu principal ---Selecionar---> Opções
                estadoAnteriorParaVoltar = estadoDoJogo
                estadoDoJogo="Opções"

            elif selecao == "Teclas":
                estadoDoJogo = "teclas"

            elif selecao=="Sair": #Menu principal ---Selecionar---> fechar o jogo
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"
            elif selecao == "Ranking":
                estadoDoJogo = "ranking"
        elif estadoDoJogo=="tela de morte":
            selecao = tela_de_morte.eventos(event)

            if selecao=="Reiniciar":#Tela de morte ---Selecionar---> Reiniciar o Modo de Jogo
                resetarVariaveis(grupoGrupos, 0)#Apagar todo mundo
                jogador = criarJogador(deltaTime)#Cria um jogador novo, esse que tem que ter suas variáveis internas zeradas
                grupoJogador.add(jogador)
                estadoDoJogo="jogando"

                wave_counter=0
                inicio_de_jogo=perf_counter()
                tempo_no_menu=0.0
                estadoDoJogo="jogando"#Indicar que reiniciou o jogo
 
                menu_input.ja_adicionou = 0
                nao_pode_entrar_mais = 0
                boss_fight = 0
            elif selecao=="Menu Principal":#Tela de morte ---Selecionar---> Menu Principal
                resetarVariaveis(grupoGrupos, 0)#Limpar o Jogo
                inicio_menu = 0.0 
                estadoDoJogo="menu principal"
                menu_input.ja_adicionou = 0
                nao_pode_entrar_mais = 0
            elif selecao == "Ranking" and not menu_input.ja_adicionou:
                estadoAnterior2 = estadoDoJogo
                estadoDoJogo = "add ranking"
                menu_input.ja_adicionou
            elif selecao == "Ranking" and menu_input.ja_adicionou:
                nao_pode_entrar_mais = 1
            elif selecao=="Sair":
                nao_pode_entrar_mais = 0
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"

        elif estadoDoJogo == "creditos": #Menu principal ---Selecionar---> Créditos
            selecao=creditos.eventos(event)
            if selecao=="Voltar":
                estadoDoJogo="menu principal"

        elif estadoDoJogo == "fim do tutorial":#Menu principal --Selecionar--> Tutorial
            selecao = fim_do_tutorial.eventos(event)
            if selecao == "Menu principal":
                resetarVariaveis(grupoGrupos, 0)
                inicio_menu = 0.0
                estadoDoJogo="menu principal"

            elif selecao == "Sair":
                pygame.quit()
                sys.exit()
                main = False
                estadoDoJogo = "fechado"

        elif estadoDoJogo == "escolher modo":
            selecao = escolher_modo.eventos(event)
                
            if selecao == "Infinito":
                modo = "infinito"
                estadoDoJogo = "escolher dificuldade"

            elif selecao == "Boss":
                modo = "boss"
                estadoDoJogo = "jogando"

                grupoJogador.add(jogador)
                tempo_no_menu += perf_counter() - inicio_menu

            elif selecao == "Voltar":
                estadoDoJogo = "menu principal"


        elif estadoDoJogo == "escolher dificuldade":
            selecao = escolher_dificuldade.eventos(event)
            if selecao is not None:
                modo = "infinito"
                if selecao != "Voltar":
                    estadoDoJogo = "jogando"
                    grupoJogador.add(jogador)
                    tempo_no_menu += perf_counter() - inicio_de_jogo
    
                    dificuldade = selecao
                if selecao == "Fácil":
                    wave_counter= 1
                elif selecao == "Médio":
                    wave_counter = 3
                elif selecao == "Difícil":
                    wave_counter = 5
                elif selecao == "Impossível":
                    wave_counter = 6
                elif selecao == "Voltar":
                    estadoDoJogo = "escolher modo"
    
        elif estadoDoJogo=="Opções":
            selecao = menu_opcoes.eventos(event)
            if selecao[1] is not None:
                config.volume=float(selecao[1])/100.0
            if selecao[0] == "Tela Cheia":
                config.bgWidth, config.bgHeight = pygame.display.get_desktop_sizes()[0]
                config.tela = pygame.display.set_mode((config.bgWidth,config.bgHeight), pygame.RESIZABLE, display=0)
            if selecao[0] in ["1920x1080","960x540"]:
                tamanho = selecao[0].split("x")
                config.bgWidth=int(tamanho[0])
                config.bgHeight=int(tamanho[1])
                config.tela = pygame.display.set_mode((config.bgWidth,config.bgHeight), pygame.RESIZABLE, display=0)
            if selecao[2] == 1:
                estadoDoJogo=estadoAnteriorParaVoltar


        elif estadoDoJogo == "menu boss":
            selecao = menu_boss.eventos(event)
            if venceu == 0:
                sons("venceu")
                venceu += 1

            if selecao == "Reiniciar":
                resetarVariaveis(grupoGrupos, 0)
                jogador = criarJogador(deltaTime)
                inicio_de_jogo=perf_counter()
                tempo_no_menu=0.0
                grupoJogador.add(jogador)
                estadoDoJogo="jogando"
                menu_input.ja_adicionou = 0
                nao_pode_entrar_mais = 0
                boss_fight = 0
                

            elif selecao == "Opções":
                estadoAnteriorParaVoltar = estadoDoJogo
                estadoDoJogo = "Opções"
                nao_pode_entrar_mais = 0

            elif selecao == "Menu Principal":
                estadoDoJogo = "menu principal"
                menu_input.ja_adicionou = 0
                nao_pode_entrar_mais = 0
            elif selecao == "Ranking" and not menu_input.ja_adicionou:
                estadoAnterior2 = estadoDoJogo
                estadoDoJogo = "add ranking"
                menu_input.ja_adicionou = 1
            elif selecao == "Ranking" and menu_input.ja_adicionou:
                nao_pode_entrar_mais = 1
            elif selecao == "Sair":
                nao_pode_entrar_mais = 0
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"

        elif estadoDoJogo == "add ranking":
            selecao = menu_input.eventos(event)
            if selecao is not None:
                menu_input.ja_adicionou = 1
                if modo == "boss":
                    ranking_boss.append({"user": selecao, "tempo": tempo_jogo_fim})
                    ranking_boss.sort(key=lambda x: x["tempo"], reverse=False) #ordenar os tempos de forma decrescente
                    estadoDoJogo = estadoAnterior2
                elif modo == "infinito":
                    ranking_infinito[dificuldade].append({"user": selecao, "tempo": tempo_jogo_fim})
                    ranking_infinito[dificuldade].sort(key=lambda x: x["tempo"], reverse=True) #ordenar os tempos de forma decrescente
                    estadoDoJogo = estadoAnterior2
        elif estadoDoJogo == "ranking":
            selecao = menu_ranking.eventos(event)
            if selecao == "Voltar":
                estadoDoJogo = "menu principal"

        elif estadoDoJogo == "teclas":
            selecao = menu_teclas.eventos(event)
            if selecao == "Voltar":
                estadoDoJogo = "menu principal"

        elif estadoDoJogo == "jogando":
            #pausar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estadoDoJogo = "pausado"
    
                    tempo_atual = perf_counter()
                if event.key == pygame.K_l and modo == "infinito":
                    ja_entrou = 0
                    sons("lojinha")
                    jogador.quick_shot, tempo_pausado = loja.abrir(clock, jogador, jogador.quick_shot, jogador.bullet_time)
                    sons("jogando")
                    inicio_de_jogo += tempo_pausado
            #Criar o escudo:
            if event.type == create_escudo and random.randint(1,5)==1 and (modo == "boss" or modo == "infinito") : #chance de spawnar
                if jogador.armadura < 100:
                        x = random.randint(200,config.bgInitWidth-200)
                        y = -200
                        escudoSpawnado = ParteEscudo(
                            spriteImage=os.path.join(config.folderPath,'images', 'Items', 'Escudo.png'),
                            posInicial=(x, y))
                        shield = 1
                        grupoEscudo.add(escudoSpawnado)
            #Criar o powerUP:
            if event.type == create_quickshot and random.randint(1,7)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -200
                    powerupSpawnado = Quick_Shot(
                        spriteImage=os.path.join(config.folderPath,'images', 'Items', 'QS_up.png'),
                        posInicial=(x, y),
                    )
                    qs = 1   
                    grupoQuickShot.add(powerupSpawnado)
            #cria cura
            if event.type == create_Cura and random.randint(1,10)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -200
                    cura = Cura(
                        spriteImage=os.path.join(config.folderPath, 'images','items', 'med_kit.png'),
                        posInicial=(x, y)
                    )
                    heal = 1
                    grupoCura.add(cura)
            #cria moeda ouro 
            if event.type == create_Moeda_Ouro and random.randint(1,9)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -200
                    moeda_ouro = Moedas(spriteImage=os.path.join(config.folderPath,'images','items', 'coin 2.png'),
                        posInicial=(x, y), valor = 3)
                    ouro =1
                    grupoMoeda.add(moeda_ouro)
            #cria moeda prata
            if event.type == create_Moeda_Prata and (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -200
                    moeda_prata = Moedas(spriteImage=os.path.join(config.folderPath,'images','items','Silver.Coin.png'),
                        posInicial=(x, y),valor = 1)
                    prata = 1
                    grupoMoeda.add(moeda_prata)
            #Criar a carga
            if event.type == create_charge and random.randint(1,7)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                if jogador.charge < 5 and not jogador.bullet_time:
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -200
                    charge = Charge(spriteImage=os.path.join(config.folderPath,'images','items', 'choque_do_trovao.png'),
                        posInicial=(x, y),)
                    bt = 1
                    grupoBulletTime.add(charge)
            #Criar a shotgun
            if event.type == create_shotgun and random.randint(1,9)==1 and (modo == "boss" or modo == "infinito"):
                if not jogador.arma == 'shotgun':
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -200
                    cartucho = Shotgun(spriteImage=os.path.join(config.folderPath,'images','items', 'bala_shotgun.png'),
                        posInicial=(x, y),)
                    grupoShotgun.add(cartucho)
            
            #Criar o ima
            if event.type == create_ima and random.randint(1,9)==1 and  (modo == "boss" or modo == "infinito"):
                x = random.randint(200,config.bgInitWidth-200)
                y = -200
                ima = Ima(spriteImage=os.path.join(config.folderPath,'images','items', 'icon ima.png'),
                    posInicial=(x, y),)
                grupoIma.add(ima) 
            
            
            #criar bala padrão
            if event.type == create_bala0:
                for enemy in grupoInimigo:
                    if enemy.tipo_bala == "follow" :
                        enemy.disparo=1
            #criar bala shotgun
            if event.type == create_bala1:
                for enemy in grupoInimigo:
                    if enemy.tipo_bala == "rajada":
                        enemy.disparo=1
            #criar bala que aumenta
            if event.type == create_bala2:
                for enemy in grupoInimigo:
                    if enemy.tipo_bala == "bigger":
                        enemy.disparo=1
            #criar bala que segue
            if event.type == create_bala3:
                for enemy in grupoInimigo:
                    if enemy.tipo_bala == "tracker":
                        enemy.disparo=1
            #mudança direção da bala que segue
            if event.type == mudar_direcao:
                mudar = 1
            #criar laser
            if event.type == create_bala4:
                for enemy in grupoInimigo:
                    if enemy.tipo_bala == "laser" and enemy.rect.centery > 100: #só inicia o laser após estar na tela
                        if not enemy.ja_laser:
                            enemy.disparo = 1
            #mudar estado do laser
            if event.type == mudar_laser and len(grupoLaser) == 1:
                laser = 1
            #bala do boss
            if (event.type == disparo_boss) and boss_fight:
                boss.disparo = 1
            if event.type == criar_laser and boss_fight:
                boss_laser = 1
            #inimigo kamikaze começar a seguir
            for enemy in grupoInimigo:
                if enemy.tipo_bala == "self" and enemy.rect.centery > 150 and not enemy.ja_rastro:
                    enemy.disparo = 1
                    enemy.ja_rastro = 1

#--------------------------------------------------------------------------------------------
#Apertar Tab pra poder trocar de arma:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                        jogador.player_update('kabum')
#--------------------------------------------a      ------------------------------------------------
        elif estadoDoJogo=="pausado":
            selecao = menu_pause.eventos(event)

            #despausar
            if selecao == "Retomar":
                estadoDoJogo = "jogando"

                tempo_no_menu += perf_counter() - tempo_atual
                menu_pause.opcaoAtual = 0
            #opções (eventualmente)
            elif selecao == "Opções":
                estadoAnteriorParaVoltar = estadoDoJogo
                estadoDoJogo = "Opções" #modificar para criar um menu de opções dps

            elif selecao == "Menu Principal":
                resetarVariaveis(grupoGrupos, 0)
                jogador = criarJogador(deltaTime)
                inicio_de_jogo=perf_counter()
                tempo_no_menu=0.0
                estadoDoJogo="menu principal"

            #sair
            elif selecao == "Sair":
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"   
    if estadoDoJogo=="menu principal":
        menu_principal.draw(config.tela_virtual)
    elif estadoDoJogo=="tela de morte":
        tela_de_morte.draw(config.tela_virtual, jogador.kills, modo)
        if nao_pode_entrar_mais:
            msg_form = config.fonte_media.render("SEU TEMPO JÁ FOI REGISTRADO", True, (255, 0, 0))
            config.tela_virtual.blit(msg_form, (config.bgWidth/2 - msg_form.width/2, config.bgHeight - 100))
    elif estadoDoJogo=="creditos":
        creditos.draw(config.tela_virtual)
    elif estadoDoJogo == "fim do tutorial":
        fim_do_tutorial.draw(config.tela_virtual, config.telaSizePlaceholder, bg)
    elif estadoDoJogo == "escolher modo":
        escolher_modo.draw(config.tela_virtual)
    elif estadoDoJogo == "escolher dificuldade":
        escolher_dificuldade.draw(config.tela_virtual)
    elif estadoDoJogo == "Opções":
        menu_opcoes.draw(config.tela_virtual)
    elif estadoDoJogo == "menu boss":
        menu_boss.draw_texto(config.tela_virtual, config.telaSizePlaceholder, tempo_jogo_fim)
        if nao_pode_entrar_mais:
            msg_form = config.fonte_media.render("SEU TEMPO JÁ FOI REGISTRADO", True, (255, 0, 0))
            config.tela_virtual.blit(msg_form, (config.bgWidth/2 - msg_form.width/2, config.bgHeight - 100))
    elif estadoDoJogo == "add ranking":
        menu_input.draw_texto(config.tela_virtual, config.telaSizePlaceholder, tempo_jogo_fim)
    elif estadoDoJogo == "ranking":
        menu_ranking.draw_texto(config.tela_virtual, config.telaSizePlaceholder, (ranking_boss, ranking_infinito))
    elif estadoDoJogo == "teclas":
        menu_teclas.draw_texto(config.tela_virtual, config.telaSizePlaceholder)
        


        
    elif estadoDoJogo=="jogando":
        deltaTime = clock.tick(60)/1000
        if deltaTime>1.0:
            deltaTime=1.0
        dt_jogo = deltaTime
        #Salvar tecla apertada
        tecla = pygame.key.get_pressed()

        if acabou and len(grupoExplosion) == 0 and not ja_entrou and not boss_fight and modo == "boss" and jogador.vida >0:
            wave_counter += 1
            mensagem = f"HORDA {wave_counter} FINALIZADA"
            mensagem_form = config.fonte_grande.render(mensagem, True, (0, 0, 0))
            config.tela_virtual.blit(mensagem_form, (config.bgInitWidth/2-mensagem_form.get_width()/2, config.bgInitHeight/2-mensagem_form.get_height()/2))
            config.tela_escalada = pygame.transform.smoothscale(config.tela_virtual, (config.bgWidth,config.bgHeight)) ##################
            config.tela.blit(config.tela_escalada,(0,0))
            acabou = 0
            pygame.display.flip() #para colocar a mensagem de final na tela
            sleep(3.0)
            #limpando os elementos da tela
            resetarVariaveis(grupoGrupos, 1)
            sons("lojinha")
            jogador.quick_shot, tempo_pausado = loja.abrir(clock, jogador, jogador.quick_shot, jogador.bullet_time)
            sons("jogando")
            inicio_de_jogo += tempo_pausado + 3
            ja_entrou = 1
            acabou_sair = 0
            pygame.event.clear() #tirando ""todos os eventos da fila, para não passar comandos p dps do intervalo
        
        if wave_counter ==5 and wave_counter != 0 and not boss_fight and not acabou_sair and modo == "boss":
            boss = Inimigo("Boss-W1", deltaTime, pos=(config.bgInitWidth/2, 180), limites_mov=(0, 0), sentido_inicial="null")
            grupoInimigo.add(boss)
            sons("BossFight")
            boss_fight = 1

        if boss_fight:
            if boss.vida >0 and boss.disparo:
                centro_bala = random.choice(pontos_possiveis)
                tipo = random.choice(balas_possiveis)
                if tipo == "rajada":
                    sons("balaShotgunInimigo")
                    for pow in (0, 4, 7):    
                        bullet = Bullet(
                            os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                            (centro_bala),
                            dt=deltaTime,
                            tipo = "rajada",
                            boss = 1
                        )
                        grupoBullets.add(bullet)
                        bullet.direcao((jogador.rect.center), centro_bala, pow)
                else:
                    sons("balaInimigo")
                    bullet = Bullet(
                        os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                        (centro_bala),
                        dt=deltaTime,
                        tipo = tipo,
                        boss = 1
                    )
                    grupoBullets.add(bullet)
                    bullet.direcao((jogador.rect.center), centro_bala, pow)
                if boss_laser:
                    sons("laser")
                    tipo = "laser"
                    boss_laser = 0
                    piu = Bullet(
                        os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                        (centro_bala),
                        dt=deltaTime,
                        tipo = tipo,
                        boss = 1
                    )
                    grupoLaser.add(piu)
                    piu.direcao((jogador.rect.center), centro_bala, pow)


                boss.disparo = 0

            elif boss.vida <= 0 and len(grupoExplosion) == 0:
                tempo_de_jogo = perf_counter() - inicio_de_jogo - tempo_no_menu
                tempo_jogo_fim = tempo_de_jogo
                boss_fight = 0
                boss.kill()
                acabou_sair = 1
                mensagem_fim = "LUTA CONCLUIDA"
                mensagem_tempo = f"TEMPO TOTAL {tempo_de_jogo:0.1f}s"
                mensagem_form_fim = config.fonte_grande.render(mensagem_fim, True, (0, 0, 0))
                mensagem_form_tempo = config.fonte_media.render(mensagem_tempo, True, (0, 0, 0))
                sleep(0.5)
                estadoDoJogo = "menu boss"
                wave_counter = 0
                #limpando os elementos da tela
                resetarVariaveis(grupoGrupos, 0)
                pygame.event.clear()

        #calculo temporizador atual
        tempo_de_jogo = perf_counter() - inicio_de_jogo - tempo_no_menu
        
        #spawn novos inimigos
        if (len(grupoInimigo) < minimo_inimigos[wave_counter] and not boss_fight and (modo == "boss" or modo == "infinito")):
            sentido = random.choice(["R", "L"])
            coordenadas = (random.randint(350, config.bgInitWidth - 350), -200)
            if pode_spawn_laser:      
                tipo_inimigo = random.randint(0,5)
            else:
                tipo_inimigo = random.randint(0,4)
            if tipo_inimigo == 5:
                pode_spawn_laser = 0
            novoInim = Inimigo(tipo_inimigo, deltaTime, pos=coordenadas, limites_mov=(300, config.bgInitWidth - 300), sentido_inicial=sentido)
            grupoInimigo.add(novoInim)

        #HUD da vida
        hp = f"Vida: {jogador.vida}"
        hp_form = config.fonte.render(hp, False, (255, 255, 255))

        #HUD do escudo
        escudos = f"Escudo: {jogador.armadura}"
        escudos_form = config.fonte.render(escudos, False, (100,180,255))
        
        #HUD das Moedas
        coin = f"Moedas : {jogador.moedas}"
        coin_form = config.fonte.render(coin, False, (255, 255, 255))

        #HUD do tempo 
        tempo_de_jogo = perf_counter() - inicio_de_jogo - tempo_no_menu
        if modo == "tutorial":
            tempo_de_jogo = 0
        timer = config.fonte.render(f"{tempo_de_jogo:.1f}s", False, (255, 255, 255))
        rect_timer = timer.get_rect()
        rect_timer.center = (680, 50)

        #HUD de kills
        kills = f"Kills: {jogador.kills}"
        kills_form = config.fonte.render(kills, False, (255, 255, 255))

        #HUD da carga:
        cargas = "Cargas:"
        cargas_form = config.fonte.render(cargas, False, (255, 215, 0))
        carga_icon = pygame.image.load(os.path.join(config.folderPath,'images','items', 'icon das cargas.png')).convert_alpha()
        carga_icon = pygame.transform.scale(carga_icon, (30, 30))

        #Hud de Balas - Shotgun:
        cartuchos = f"Cartuchos:    {jogador.cartuchos} "
        cartuchos_form = config.fonte.render(cartuchos, False, (255, 215, 0))
        cartuchos_icon = pygame.image.load(os.path.join(config.folderPath,'images','items', 'bala_shotgun.png')).convert_alpha()
        cartuchos_icon = pygame.transform.scale(cartuchos_icon, (64, 64))

        #colisão player item
        pygame.sprite.spritecollide(jogador, grupoItem, True)    
        
        #moedas coletadas:
        moeda_coletados = []
        for moeda in grupoMoeda:
            if jogador.hitbox.colliderect(moeda.rect):
                moeda_coletados.append(moeda)
                sons("pegouMoeda")
                moeda.kill()
            elif moeda.rect.topright[1] > config.bgInitHeight + 6: #eliminar o item da memória caso saia da tela
                moeda.kill()

        for moeda in moeda_coletados:
            jogador.moedas += moeda.valor
            
        #Escudo coletado:
        escudo_coletados = []
        for pedacos in grupoEscudo:
            if jogador.hitbox.colliderect(pedacos.rect):
                escudo_coletados.append(pedacos)
                sons("coletado")
                pedacos.kill()
            elif pedacos.rect.topright[1] > config.bgInitHeight + 6: #eliminar o item da memória caso saia da tela
                pedacos.kill()
        for i in escudo_coletados:
            jogador.escudo += 1
            if jogador.escudo >= 4:
                if jogador.armadura < 100:
                    jogador.armadura += 25
                jogador.escudo = 0
                
        #curas coletado:
        cura_coletados = []
        for cura in grupoCura:
            if jogador.hitbox.colliderect(cura.rect):
                cura_coletados.append(cura)
                sons("coletado")
                cura.kill()
            elif cura.rect.topright[1] > config.bgInitHeight + 6: #eliminar o item da memória caso saia da tela
                cura.kill()

        for i in cura_coletados:
            if jogador.vida < 100:
                jogador.vida += 30
                if jogador.vida>100:
                    jogador.vida=100
    
        #Quick Shot coletado:
        quick_shots_coletados = []
        for powerup in grupoQuickShot:
            if jogador.hitbox.colliderect(powerup.rect):
                quick_shots_coletados.append(powerup)
                sons("coletado")
                powerup.kill()
            elif powerup.rect.topright[1] > config.bgInitHeight + 6: #eliminar o item da memória caso saia da tela
                powerup.kill()
        if quick_shots_coletados:
            if not jogador.quick_shot:
                jogador.player_update("PU")
            quick_shot_t_inicio = perf_counter()
            intervalo_tiro = cooldown_especial

        if jogador.quick_shot:
            tempo_passado = perf_counter() - quick_shot_t_inicio
            if tempo_passado >= 5: #dura 5 segundos
                jogador.player_update("PU")
                intervalo_tiro = cooldown_normal
                jogador.quick_shot = False
                
        #Pegar a Carga
        charges_coletados = []
        for carga in grupoBulletTime:
            if jogador.hitbox.colliderect(carga.rect):
                charges_coletados.append(carga)
                sons("coletado")
                carga.kill()
                if jogador.charge < 5:
                    jogador.charge += 1
            elif carga.rect.topright[1] > config.bgInitHeight + 6: #eliminar o item da memória caso saia da tela
                carga.kill()

        #Coletar o Imã
        imas_coletados = []
        for ima in grupoIma:
            if jogador.hitbox.colliderect(ima.rect):
                imas_coletados.append(ima)
                sons("coletado")
                ima.kill()
            elif ima.rect.topright[1] > config.bgInitHeight + 6:
                ima.kill()
        if imas_coletados:
            tempo_ima_ativo = perf_counter()

        # Atrair moedas se imã estiver ativo
        if perf_counter() - tempo_ima_ativo < duracao_ima:
            for moeda in grupoMoeda:
                nova_x, nova_y = Ima.atracao(
                    None,
                    moeda.posicao.x, moeda.posicao.y,
                    jogador.rect.centerx, jogador.rect.centery
                )
                moeda.posicao.x = nova_x
                moeda.posicao.y = nova_y
                moeda.rect.centerx = nova_x
                moeda.rect.centery = nova_y


#Pegar a shotgun: -------------------------------------------------------------------------------------------------------------------------------------
        cartuchos_coletados = []
        for cartuchos in grupoShotgun:
            if jogador.hitbox.colliderect(cartuchos.rect):
                if jogador.cartuchos < 50:
                    jogador.cartuchos += 1
                cartuchos_coletados.append(cartuchos)
                sons("reload")
                cartuchos.kill()
            elif cartuchos.rect.topright[1] > config.bgInitHeight + 6: #eliminar o item da memória caso saia da tela
                cartuchos.kill()
#Pegar a shotgun: -------------------------------------------------------------------------------------------------------------------------------------


        #Ativando o bullet time:
        if tecla[pygame.K_LSHIFT]:
            if jogador.charge > 0:
                jogador.bullet_time = True
                tempo_inicio = perf_counter()
                duracao = jogador.charge
                jogador.charge = 0
        #duracao bullet time
        if jogador.bullet_time:
            if perf_counter() - tempo_inicio >= duracao:
                jogador.bullet_time = False
                dt_jogo = dt_jogo
            else:
                dt_jogo = deltaTime * 0.3
                
        #background scrolling
        appender=0
        while(appender<tiles):
            config.tela_virtual.blit(bg, (0, -bg.get_height()*appender+scroll))
            appender+=1
        scroll+=12
        #reset scrolling
        if abs(scroll)>bg.get_height():
            scroll=0
            
        
        pos_x_inicial = 18 + escudos_form.get_width() + 15#Ele tem que ficar 15 pixels dps da quantidade de escudo
        tamanho_quadrado = 30 #Lado do quadrado 
        espacamento = 8       
        for i in range(jogador.escudo):
            x = pos_x_inicial + (i * (tamanho_quadrado + espacamento))
            y = 75
            pygame.draw.rect(config.tela_virtual, (100, 180, 255), (x, y, tamanho_quadrado, tamanho_quadrado))
            
        #Tiro do jogador 
        if tecla[pygame.K_SPACE]:
            if perf_counter() - ultimo_tiro >= intervalo_tiro:
                sons("balaPlayer")
                if jogador.arma == "normal" or (jogador.arma == "shotgun" and jogador.cartuchos > 0):
                    if jogador.arma == 'shotgun':
                        angulos_shotgun = [-10, 0, 10]
                        jogador.cartuchos -= 1
                    else:
                        angulos_shotgun = [0]
                    for angulo in angulos_shotgun:
                        if not jogador.quick_shot:
                            projetil = Bala(os.path.join(config.folderPath,"images","playerSprites","bala-player.png"),jogador.rect.center,dt=deltaTime)
                        #quick_shot
                        if jogador.quick_shot:
                            projetil = Bala(os.path.join(config.folderPath, "images", "Items", "quick_shot.png"),jogador.rect.center,dt=deltaTime)
                        direcao_base = pygame.math.Vector2(0, -projetil.velocidade)
                        projetil.dire = direcao_base.rotate(angulo)
                        grupoBala.add(projetil)
                ultimo_tiro = perf_counter()
        if jogador.arma == "shotgun" and jogador.cartuchos == 0 and perf_counter()-ultimo_tiro >= 1:
            jogador.player_update('kabum')
                
        #checa os inimigos ativos para disparar
        for enemy in grupoInimigo:
            if (enemy.disparo) and  enemy.rect.topleft[1] >5:
                if enemy.tipo_bala == "follow": 
                    sons("balaInimigo") #balaPlayer, balaInimigo, balaShotgunInimigo, laser
                    bullet = Bullet(
                        os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                        (enemy.rect.centerx,enemy.rect.centery),
                        dt=deltaTime,
                        tipo = "follow",
                        boss = 0
                    )
                    grupoBullets.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy.rect.center), pow = 0)
                elif enemy.tipo_bala == "rajada":
                    sons("balaShotgunInimigo")
                    for pow in range(7):    
                        bullet = Bullet(
                            os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                            (enemy.rect.centerx,enemy.rect.centery),
                            dt=deltaTime,
                            tipo = "rajada",
                            boss = 0
                        )
                        grupoBullets.add(bullet)
                        bullet.direcao((jogador.rect.center), (enemy.rect.center), pow)
                elif enemy.tipo_bala == "bigger":
                    sons("balaInimigo")
                    bullet = Bullet(
                        os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                        (enemy.rect.centerx,enemy.rect.centery),
                        dt=deltaTime,
                        tipo = "bigger",
                        boss = 0
                    )
                    grupoBullets.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy.rect.center), pow = 0)
                elif enemy.tipo_bala == "laser":
                    sons("laser")
                    enemy.ja_laser = 1
                    bullet = Bullet(
                        os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                        ((enemy.rect.width/2) + enemy.rect.bottomleft[0],enemy.rect.bottomright[1]),
                        dt=deltaTime,
                        tipo = "laser",
                        boss = 0,
                    )
                    #bullet.ord = len(grupoLaser)
                    enemy.velocidadex = 0 #para quando atirar o laser
                    enemy.velocidadey = -6
                    grupoLaser.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy.rect.center), pow = 0)
                elif enemy.tipo_bala == "tracker":
                    bullet = Bullet(
                    os.path.join(config.folderPath, "images", "enemy", "bullet.png"),
                    (enemy.rect.centerx,enemy.rect.centery),
                    dt=deltaTime,
                    tipo = "tracker",
                    boss = 0
                    )
                    grupoBullets.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy.rect.center), pow = 0)

                elif enemy.tipo_bala == "self":
                    enemy.follow(enemy.rect.center, jogador.rect.center)


                #ativa o cooldown do disparo do inimigo
                enemy.disparo=0
                
        grupoJogador.update(deltaTime, config.camera) #Update do player antes por conta da criação do rastro
        
        #Criação do rastro
        if jogador.bullet_time: #Só cria o rastro na hora do bulletime
            distancia_x = abs(rect_anterior.x - jogador.rect.x)
            distancia_y = abs(rect_anterior.y - jogador.rect.y)
            if distancia_x > 10 or distancia_y > 10:
                novo_rastro = Rastro_Bullet_Time(jogador.image, rect_anterior)
                rect_anterior = jogador.rect.copy() #Salvar a posição do player pra criar o rasto
                contador_rastros += 1
                if contador_rastros > 1:
                    grupoRastro.add(novo_rastro)
                    
        
        
        if not jogador.invencibilidade:
            grupoJogador.draw(config.tela_virtual)
        else:
            if perf_counter() - t_clicks < jogador.tempoPiscar:
                grupoJogador.draw(config.tela_virtual)
            else:
                t_clicks = perf_counter()

        if jogador.invencibilidade and (perf_counter() - t_invencibilidade) >= 3:
            jogador.player_update("D")
            
        #Colisão do disparo do inimigo com a hitbox do player
        colisao_b = False
        if pygame.sprite.spritecollide(jogador, grupoBullets, True, pygame.sprite.collide_mask):
            colisao_b = True
            dano = 20
        if pygame.sprite.spritecollide(jogador, grupoLaser, False, pygame.sprite.collide_mask):
            colisao_b = True
            for go in grupoLaser:
                if go.rect.colliderect(jogador.rect):
                    dano = go.dano
                
                

                
        #Colisão do inimigo com a hitbox do player
        colisao_i = False
        if pygame.sprite.spritecollide(jogador, grupoInimigo, False, pygame.sprite.collide_mask):
            colisao_i = True
            dano = 10
            for bad in grupoInimigo:
                if bad.rect.colliderect(jogador.rect) and bad.i == 4:
                    bad.kill()
                    dano = 50
        if (colisao_b or colisao_i) and not jogador.invencibilidade: #as variáveis ficam falsas até detectarem uma colisão, quando recebe um elemento, entra na condicional
            if jogador.armadura == 0:
                jogador.vida -= dano
            else:
                if jogador.armadura < 20:
                    jogador.armadura = 0
                else:
                    jogador.armadura -= dano
            sons("powJogador")
            jogador.player_update("D")
            if jogador.vida<=0:
                tempo_morte=perf_counter()
                sons("morteJogador")
                estadoDoJogo="tela de morte"
                tempo_jogo_fim = perf_counter() - inicio_de_jogo - tempo_no_menu
            t_invencibilidade = perf_counter()
            t_clicks = perf_counter()
            
        enemyPos = []
        #Colisão tiro dos players com o inimigo e sua morte:
        for enemy in grupoInimigo:
            inimigo_morto=0
            colisao_inimigo = pygame.sprite.spritecollide(enemy, grupoBala, True, pygame.sprite.collide_mask)
            if colisao_inimigo:
                enemy.levou_dano()
                sons("powInimigo")
                #print(f"Inimigo: {enemy01.vida}")
                enemy.vida -= 20
            if enemy.vida <= 0:
                explosao = Explosion(pos=enemy.rect.center, id=enemy.i)
                grupoExplosion.add(explosao)
                sons("ExplosaoInimigo")
                jogador.add_kill()
                if jogador.kills in(15, 30, 45, 60, 75):
                    acabou = 1
                ja_entrou = 0 #para entrar na loja no proximo 
                enemy.kill()
            if enemy.rect.topright[1] >= config.bgInitHeight + 6 or enemy.rect.topright[0] < 0 or enemy.rect.topleft[0] > config.bgInitWidth + 6: 
                enemy.kill()


            if enemy.i == 5 or boss_fight:
                enemyPos.append((enemy.rect.width/2 + enemy.rect.bottomleft[0],enemy.rect.bottomright[1]))

        #update de tudo
        grupoInimigo.update(dt_jogo, config.camera)
        grupoBullets.update(dt_jogo, config.camera, jogador.posicao, mudar, laser, enemyPos)
        grupoBala.update(dt_jogo, config.camera, jogador.posicao)
        grupoRastro.update(deltaTime, config.camera) #Update do rastro
        grupoQuickShot.update(dt_jogo, config.camera)
        grupoBulletTime.update(dt_jogo, config.camera) #Update das cargas
        grupoShotgun.update(dt_jogo, config.camera)
        grupoEscudo.update(dt_jogo, config.camera)
        grupoMoeda.update(dt_jogo, config.camera)
        grupoCura.update(dt_jogo, config.camera)
        grupoLaser.update(dt_jogo, config.camera, jogador.posicao, mudar, laser, enemyPos)
        grupoIma.update(dt_jogo, config.camera)
        if laser:
            laser = 0
        if mudar:
            mudar = 0

        grupoExplosion.update(dt_jogo)

        #desenha tudo na tela
        
        grupoBullets.draw(config.tela_virtual)
        grupoInimigo.draw(config.tela_virtual)

        grupoExplosion.draw(config.tela_virtual)

        grupoQuickShot.draw(config.tela_virtual)
        grupoBulletTime.draw(config.tela_virtual)#Desenhar a carga na tela
        grupoShotgun.draw(config.tela_virtual)
        grupoEscudo.draw(config.tela_virtual) 
        grupoMoeda.draw(config.tela_virtual)
        grupoCura.draw(config.tela_virtual)
        grupoLaser.draw(config.tela_virtual)
        grupoIma.draw(config.tela_virtual)

        #Colocar as novas HUDs na tela:
        config.tela_virtual.blit(hp_form, (18, 18))
        config.tela_virtual.blit(coin_form, (200, 18))
        config.tela_virtual.blit(escudos_form, (20, 68))
        #Filtro Cinza do bullet_time
        if jogador.bullet_time:
            config.tela_virtual.blit(filtro_bullet_time, (0, 0))
        grupoRastro.draw(config.tela_virtual)
        #Pra bala não terem o filtro
        grupoBala.draw(config.tela_virtual)
        config.tela_virtual.blit(timer, (((config.bgInitWidth-timer.get_width())/2), 10))
        config.tela_virtual.blit(kills_form, (config.bgInitWidth-kills_form.get_width()-20, 10))
        #Representação das cargas
        config.tela_virtual.blit(cargas_form, (18, 108))
        pos_x_inicial_carga = 18 + cargas_form.get_width() + 15
        largura_imagem = 30
        espacamento_carga = 8
        for i in range(jogador.charge):
            x = pos_x_inicial_carga + (i * (largura_imagem + espacamento_carga))
            y = 122 
            config.tela_virtual.blit(carga_icon, (x, y))
        #Representação da Shotgun
        config.tela_virtual.blit(cartuchos_form, (18, 148))
        config.tela_virtual.blit(cartuchos_icon, (216, 140))
        if boss_fight:
            pygame.draw.rect(config.tela_virtual, (0, 0, 0), (config.bgInitWidth/2 - 300, 55, 600, 40), 3)
            barra_vida = int(boss.vida*6/10) #regra de 3 com o retangulo tendo 600 de tamanho e vida do boss 1000
            pygame.draw.rect(config.tela_virtual, (255, 0, 0), (config.bgInitWidth/2 - 300, 55, barra_vida, 40))

        if modo == "infinito" and perf_counter() - inicio_de_jogo - tempo_no_menu < 3:
            mensagem_loja = "APERTE L PARA ENTRAR NA LOJA"
            mensagem_loja_rend = config.fonte_media.render(mensagem_loja, True, (0, 0, 0))
            config.tela_virtual.blit(mensagem_loja_rend, (config.bgInitWidth/2 - mensagem_loja_rend.width/2, config.bgHeight - 100))
            


        if modo == "tutorial": #sequencia lógica do tutorial
            if contador_de_teclas_mov in range(0, 10):
                sug = "  Use W-A-S-D para se movimentar"
            if contador_de_teclas_mov >= 10 and perf_counter() - inicio_de_jogo - tempo_no_menu > 3 and contador_de_teclas_espaco == 0:
                sug = "Aperte espaço para atirar"
            if (contador_de_teclas_mov + contador_de_teclas_espaco) >= 10 and contador_de_teclas_espaco !=0 and len(grupoMoeda) == 0 and jogador.moedas <= 8 and perf_counter() - inicio_de_jogo - tempo_no_menu > 6:
                sug = "Moedas compram itens na loja"
                x = random.randint(200,config.bgInitWidth-200)
                y = -200
                moeda_ouro = Moedas(spriteImage=os.path.join(config.folderPath,'images','items', 'coin 2.png'),
                    posInicial=(x, y), valor = 3)
                
                x = random.randint(200,config.bgInitWidth-200)
                y = -200
                moeda_prata = Moedas(spriteImage=os.path.join(config.folderPath,'images','items','Silver.Coin.png'),
                    posInicial=(x, y),valor = 1)
                
                grupoMoeda.add(moeda_ouro)
                grupoMoeda.add(moeda_prata)

                if jogador.moedas > 1:
                    x = random.randint(200,config.bgInitWidth-200)
                    y = -50
                    ima = Ima(spriteImage=os.path.join(config.folderPath,'images','items', 'icon ima.png'),
                        posInicial=(x, y),)
                    grupoIma.add(ima)  
                    
                    sug = "Use o imã para atrair moedas"
            
            if jogador.moedas > 8 and len(grupoEscudo) == 0 and len(grupoCura) == 0 and jogador.escudo == 0:
                sug = "   Cura recupera sua vida e\n    4 escudos dão proteção extra"
                x = random.randint(200,config.bgInitWidth-200)
                y = -200
                escudoSpawnado = ParteEscudo(
                    spriteImage=os.path.join(config.folderPath,'images', 'Items', 'Escudo.png'),
                    posInicial=(x, y))
                
                x += 70
                if x > config.bgInitWidth - 200: #obrigando o med kit a spawnar perto do escudo so p pegar na mesma hitbox e n dar problema p seguir a lógica
                    x -= 20
                y = -200
                cura = Cura(
                    spriteImage=os.path.join(config.folderPath, 'images','items', 'med_kit.png'),
                    posInicial=(x, y)
                )
                
                grupoCura.add(cura)
                grupoEscudo.add(escudoSpawnado)

            if len(grupoEscudo) >= 0 and len(grupoCura) >= 0 and intervalo_tiro ==cooldown_normal and jogador.escudo > 0 and len(grupoQuickShot) == 0 and len(grupoInimigo) == 0 and not passa_tutorial:
                sug = "  Quick shot aumenta\n  a velocidade de disparo"
                
                x = random.randint(200,config.bgInitWidth-200)
                y = -200
                powerupSpawnado = Quick_Shot(
                    spriteImage=os.path.join(config.folderPath,'images', 'Items', 'QS_up.png'),
                    posInicial=(x, y),
                )

                grupoQuickShot.add(powerupSpawnado)

            if len(quick_shots_coletados) > 0 and not jogador.bullet_time and len(grupoQuickShot) == 0 and len(grupoInimigo) == 0 and not passa_tutorial:
                sug = "  Pegue a carga e aperte shift\n   para usar o bullet time"
                x = random.randint(200,config.bgInitWidth-200)
                y = -200
                charge = Charge(spriteImage=os.path.join(config.folderPath,'images','items', 'choque_do_trovao.png'),
                    posInicial=(x, y),)
                grupoBulletTime.add(charge)

            if tecla[pygame.K_LSHIFT] and len(grupoBulletTime) >= 0 and len(grupoInimigo) == 0 and sug == "  Pegue a carga e aperte shift\n   para usar o bullet time":
                passa_tutorial =1
            

            if passa_tutorial and len(grupoShotgun) ==0 and len(grupoInimigo) == 0 and len(grupoQuickShot) >= 0 and not fim_tutorial:
                sug = "   Pegue o cartucho e aperte tab\n   para trocar para shotgun"
                x = random.randint(200,config.bgInitWidth-200)
                y = -50
                cartucho = Shotgun(spriteImage=os.path.join(config.folderPath,'images','items', 'bala_shotgun.png'),
                    posInicial=(x, y),)
                grupoShotgun.add(cartucho)

                x = x + 20
                y = -50
                cartucho = Shotgun(spriteImage=os.path.join(config.folderPath,'images','items', 'bala_shotgun.png'),
                    posInicial=(x, y),)
                grupoShotgun.add(cartucho)

                x = x - 40
                y = -50
                cartucho = Shotgun(spriteImage=os.path.join(config.folderPath,'images','items', 'bala_shotgun.png'),
                    posInicial=(x, y),)
                grupoShotgun.add(cartucho)
                
                 
            if tecla[pygame.K_TAB] and passa_tutorial and len(grupoShotgun) > 0 and len(grupoInimigo) == 0 and jogador.kills == 0:
                sug = "Mate o inimigo!"
                grupoInimigo.add(enemy01)
                fim_tutorial = 1

            if fim_tutorial and len(grupoInimigo) == 0 and jogador.kills == 0:
                enemy01 = Inimigo(i =0, dt=deltaTime, pos=(config.bgInitWidth/2, -50), limites_mov=(300, config.bgInitWidth - 300), sentido_inicial="L")
                grupoInimigo.add(enemy01)
                

            if enemy01.vida <= 0 and len(grupoExplosion) == 0 and jogador.kills > 0:
                estadoDoJogo = "fim do tutorial"

                
            if tecla[pygame.K_w]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_s]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_a]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_d]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_SPACE] and contador_de_teclas_mov > 5:
                contador_de_teclas_espaco += 1
            
            

            sug_form = config.fonte_media.render(sug, True, (0, 0, 0))
            config.tela_virtual.blit(sug_form, ((config.bgInitWidth/2)-(sug_form.width/2) + 45, 100))

    if estadoDoJogo == "pausado":
        appender=0
        while(appender<tiles):
            config.tela_virtual.blit(bg, (0, -bg.get_height()*appender+scroll))
            appender+=1
        
        #DESENHAR INIMIGOS
        grupoBullets.draw(config.tela_virtual)
        grupoInimigo.draw(config.tela_virtual)
        grupoQuickShot.draw(config.tela_virtual)
        grupoBulletTime.draw(config.tela_virtual)#Desenhar a carga na tela
        grupoEscudo.draw(config.tela_virtual) 
        grupoMoeda.draw(config.tela_virtual)
        grupoCura.draw(config.tela_virtual)
        grupoJogador.draw(config.tela_virtual)
        grupoLaser.draw(config.tela_virtual)
        
        config.tela_virtual.blit(filtro_pause, (0, 0))
        
        
        #NOVAS HUD
        
        config.tela_virtual.blit(hp_form, (18, 18))
        config.tela_virtual.blit(coin_form, (200, 18))
        config.tela_virtual.blit(escudos_form, (20, 68))
        config.tela_virtual.blit(cargas_form, (18, 108))
        for i in range(jogador.charge):
            x = pos_x_inicial_carga + (i * (largura_imagem + espacamento_carga))
            y = 122 
            config.tela_virtual.blit(carga_icon, (x, y))

        config.tela_virtual.blit(timer, (((config.bgInitWidth-timer.get_width())/2), 10))
        config.tela_virtual.blit(kills_form, (config.bgInitWidth-kills_form.get_width()-20, 10))
        menu_pause.draw_texto(config.tela_virtual, config.telaSizePlaceholder)

                
    config.tela_escalada = pygame.transform.smoothscale(config.tela_virtual, (config.bgWidth,config.bgHeight)) ##################
    config.tela.blit(config.tela_escalada,(0,0))


    #flip atualiza a tela
    pygame.display.update()
    pygame.display.flip()
    clock.tick(config.fps)        