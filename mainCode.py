import pygame
import math
from player import Jogador, Rastro_Bullet_Time, Bala
from enemy import Inimigo, Bullet
import sys
import os
import random
from itens import itemGeral, ParteEscudo, Quick_Shot, Moedas, Cura, Charge, Ima, Shotgun
from time import perf_counter, sleep
from loja import abrir_loja
from menu import MenuPrincipal, menuPause, telaMorte, Creditos, menuFimTutorial, menuModos, menuDificuldade
from config import folderPath, camera, bgWidth, bgHeight, telaSizePlaceholder, tela, fonte, fonte_grande, fps, fonte_media
from funcoes import criarJogador, resetarVariaveis, sons

#configs permanentes
pygame.init() 
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("nome do jogo") #alterar para o nome do jogo dps
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000

#variáveis do BG scrollante
bg = pygame.image.load(os.path.join(folderPath,"images","backgrounds","bgIP.png")).convert()
bg = pygame.transform.scale(bg, (bgWidth,bgHeight))
bgSize = bg.get_rect()
"""bg_pause = pygame.image.load(os.path.join(folderPath,"images","bgIPpause.png")).convert()
bg_pause = pygame.transform.scale(bg_pause, (bgWidth,bgHeight))"""
scroll=0
tiles = math.ceil(bgHeight/bg.get_height())+2

#criar inimigo(s) inicial, para o futuro tutorial


#Evento de spawn - Moeda Ouro
create_Moeda_Ouro = pygame.USEREVENT + 1
pygame.time.set_timer(create_Moeda_Ouro, 6000)

#Evento de spawn - Moeda Prata
create_Moeda_Prata = pygame.USEREVENT + 11
pygame.time.set_timer(create_Moeda_Prata, 5000)

#Evento de spawn - Cura
create_Cura = pygame.USEREVENT + 2
pygame.time.set_timer(create_Cura, 2000)

#Evento de spawn - Escudo
create_escudo = pygame.USEREVENT + 3
pygame.time.set_timer(create_escudo, 3000)

#Evento de spawn - Quick_shot
create_quickshot = pygame.USEREVENT + 4
pygame.time.set_timer(create_quickshot, 2000)

#Evento de spawn - Cargas
create_charge = pygame.USEREVENT + 5
pygame.time.set_timer(create_charge, 2200)

#Evento de spawn - Shotgun:
create_shotgun = pygame.USEREVENT + 6
pygame.time.set_timer(create_shotgun, 9500)

#eventos de disparo para cada tipo de bala
deltaDisparos = {"follow": 1000, "rajada": 3000, "bigger": 5000, "tracker": 5000, "laser" : 6000}
balas_possiveis = ("follow", "rajada", "bigger", "tracker")
pontos_possiveis = ((bgWidth/2, 200), ((bgWidth/2) + 150, 200), ((bgWidth/2) - 150, 200), ((bgWidth/2) + 500, 200), ((bgWidth/2) -500, 200))
create_bala0, create_bala1, create_bala2, create_bala3, create_bala4 = pygame.USEREVENT + 7,  pygame.USEREVENT + 8, pygame.USEREVENT + 7, pygame.USEREVENT + 10, pygame.USEREVENT + 11
pygame.time.set_timer(create_bala0, deltaDisparos["follow"]), pygame.time.set_timer(create_bala1, deltaDisparos["rajada"]), pygame.time.set_timer(create_bala2, deltaDisparos["bigger"]), pygame.time.set_timer(create_bala3, deltaDisparos["tracker"]), pygame.time.set_timer(create_bala4, deltaDisparos["laser"])

#variáveis do disparo do inimigo 
mudar_direcao, mudar_laser = pygame.USEREVENT + 12,  pygame.USEREVENT + 13
pygame.time.set_timer(mudar_direcao, 1000), pygame.time.set_timer(mudar_laser, 800)
#timers do boss
disparo_boss, criar_laser = pygame.USEREVENT + 14, pygame.USEREVENT + 15
pygame.time.set_timer(disparo_boss, 500), pygame.time.set_timer(criar_laser, 10000)
boss_laser, limpar_laser_boss = 0, 0
#kamikaze
ativar_kamikaze = pygame.USEREVENT + 15
pygame.time.set_timer(ativar_kamikaze, 7000)

#ima
create_ima = pygame.USEREVENT + 16
pygame.time.set_timer(create_ima, 10000)

#variaveis globais entre as cenas
main = True
estadoDoJogo = "menu principal"
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
menu_principal = MenuPrincipal(tela)
menu_pause = menuPause(tela)
tela_de_morte = telaMorte(tela)
creditos = Creditos(tela)
fim_do_tutorial = menuFimTutorial(tela)
escolher_modo = menuModos(tela)
escolher_dificuldade = menuDificuldade(tela)

#temporizadores
t_invencibilidade = 0
t_clicks = 0
tempo_inicio = 0
tempoReiniciar=0.0
tempo_morte=0.0
tempo_de_jogo = perf_counter() - inicio_de_jogo
tempo_no_menu = 0

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

grupoGrupos = (grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoShotgun, grupoCura, grupoMoeda, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser, grupoIma)

#variáveis do bullet time
rect_anterior = jogador.rect.copy() #Salvar a posição do player pra criar o rasto
contador_rastros = 0 #Evitar que crie algum rastro que não seja a partir dos últimos movimentos
wave_counter = 0 #variavel para contar as waves
ja_entrou = 0 #p n entrar na loja infinitas vezes seguidas
acabou_sair = 0 #para a boss fight
filtro_bullet_time = pygame.Surface(telaSizePlaceholder, pygame.SRCALPHA)
filtro_bullet_time.fill((0, 0, 0, 150))
filtro_pause = pygame.Surface(telaSizePlaceholder, pygame.SRCALPHA)
filtro_pause.fill((0, 0, 0, 180))
minimo_inimigos=(3, 3, 4, 5, 6, 7, 10)
tempo_ima_ativo = -999
duracao_ima = 20
boss_fight = 0
while main:
    grupoGrupos = (grupoItem, grupoEscudo, grupoQuickShot, grupoBulletTime, grupoShotgun, grupoCura, grupoMoeda, grupoJogador, grupoRastro, grupoBala, grupoInimigo, grupoBullets, grupoLaser)
    #print(grupoInimigo)
    mudar, laser = 0, 0 #variaveis para as balas com condições especiais
    #todos os eventos
    for event in pygame.event.get():
        #condição de parada
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main=False
        if event.type == pygame.KEYDOWN:
            if event.key == ord("q"):
                pygame.quit()
                sys.exit()
                main=False        
        
        #um if pra cada estado do jogo
        if estadoDoJogo=="menu principal":
            selecao = menu_principal.eventos(event)
            if selecao=="Jogar":
                estadoDoJogo="escolher modo"
                
            elif selecao == "Tutorial":
                estadoDoJogo = "jogando"
                modo = "tutorial"
                grupoJogador.add(jogador)
                enemy01 = Inimigo(i =0, dt=deltaTime, pos=(750, -200), limites_mov=(300, bgWidth - 300), sentido_inicial="L")
                contador_de_teclas_mov, contador_de_teclas_espaco, contador_itens, fim_tutorial = 0, 0, 0, 0
            elif selecao=="Creditos":
                estadoDoJogo="creditos"
                sons(estadoDoJogo)
            elif selecao=="Sair":
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"
        elif estadoDoJogo=="tela de morte":
            sons(estadoDoJogo)
            selecao = tela_de_morte.eventos(event)
            if selecao=="Reiniciar":
                resetarVariaveis(grupoGrupos, 0)
                jogador = criarJogador(deltaTime)
                enemy01 = Inimigo(i =0, dt=deltaTime, pos=(bgWidth/2, -200), limites_mov=(300, bgWidth - 300), sentido_inicial="L")
                wave_counter=0
                inicio_de_jogo=perf_counter()
                tempo_no_menu=0.0
                grupoJogador.add(jogador)
                grupoInimigo.add(enemy01)
                estadoDoJogo="jogando"
                sons(estadoDoJogo)
                wave_counter=0
                inicio_de_jogo=perf_counter()
                tempo_no_menu=0.0
            elif selecao=="Menu Principal":
                resetarVariaveis(grupoGrupos, 0)
                jogador = criarJogador(deltaTime)
                enemy01 = Inimigo(i =0, dt=deltaTime, pos=(bgWidth/2, -200), limites_mov=(300, bgWidth - 300), sentido_inicial="L")
                wave_counter=0
                inicio_de_jogo=perf_counter()
                tempo_no_menu=0.0
                estadoDoJogo="menu principal"
                sons(estadoDoJogo)
            elif selecao=="Sair":
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"
        elif estadoDoJogo == "creditos":
            selecao=creditos.eventos(event)
            if selecao=="Voltar":
                estadoDoJogo="menu principal"
                sons(menu_principal)
        elif estadoDoJogo == "fim do tutorial":
            selecao = fim_do_tutorial.eventos(event)
            if selecao == "Menu principal":
                estadoDoJogo = "menu principal"
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
                sons(estadoDoJogo)
                grupoJogador.add(jogador)
                tempo_no_menu += perf_counter() - inicio_de_jogo
            elif selecao == "Voltar":
                estadoDoJogo = "menu principal"

        elif estadoDoJogo == "escolher dificuldade":
            selecao = escolher_dificuldade.eventos(event)
            if selecao != None:
                modo = "infinito"
                estadoDoJogo = "jogando"
                sons(estadoDoJogo)
                grupoJogador.add(jogador)
                tempo_no_menu += perf_counter() - inicio_de_jogo
                if selecao == "Fácil":
                    wave_counter= 1
                elif selecao == "Médio":
                    wave_counter = 3
                elif selecao == "Difícil":
                    wave_counter = 5
                elif selecao == "Impossível":
                    wave_counter = 6

        elif estadoDoJogo == "jogando":
            #pausar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estadoDoJogo = "pausado"
                    sons(estadoDoJogo)
                    tempo_atual = perf_counter() - tempo_inicio
            #Criar o escudo:
            if event.type == create_escudo and random.randint(1,7)==1 and (modo == "boss" or modo == "infinito") : #chance de spawnar
                if jogador.armadura < 100:
                        x = random.randint(200,bgWidth-200)
                        y = -200
                        escudoSpawnado = ParteEscudo(
                            spriteImage=os.path.join(folderPath,'images', 'Items', 'Escudo.png'),
                            posInicial=(x, y))
                        shield = 1
                        grupoEscudo.add(escudoSpawnado)
            #Criar o powerUP:
            if event.type == create_quickshot and random.randint(1,7)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,bgWidth-200)
                    y = -200
                    powerupSpawnado = Quick_Shot(
                        spriteImage=os.path.join(folderPath,'images', 'Items', 'QS_up.png'),
                        posInicial=(x, y),
                    )
                    qs = 1   
                    grupoQuickShot.add(powerupSpawnado)
            #cria cura
            if event.type == create_Cura and random.randint(1,10)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,bgWidth-200)
                    y = -200
                    cura = Cura(
                        spriteImage=os.path.join(folderPath, 'images','items', 'med_kit.png'),
                        posInicial=(x, y)
                    )
                    heal = 1
                    grupoCura.add(cura)
            #cria moeda ouro 
            if event.type == create_Moeda_Ouro and random.randint(1,9)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,bgWidth-200)
                    y = -200
                    moeda_ouro = Moedas(spriteImage=os.path.join(folderPath,'images','items', 'coin 2.png'),
                        posInicial=(x, y), valor = 3)
                    ouro =1
                    grupoMoeda.add(moeda_ouro)
            #cria moeda prata
            if event.type == create_Moeda_Prata and random.randint(1,5)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                    x = random.randint(200,bgWidth-200)
                    y = -200
                    moeda_prata = Moedas(spriteImage=os.path.join(folderPath,'images','items','Silver.Coin.png'),
                        posInicial=(x, y),valor = 1)
                    prata = 1
                    grupoMoeda.add(moeda_prata)
            #Criar a carga
            if event.type == create_charge and random.randint(1,7)==1 and  (modo == "boss" or modo == "infinito"): #chance de spawnar
                if jogador.charge < 5 and not jogador.bullet_time:
                    x = random.randint(200,bgWidth-200)
                    y = -200
                    charge = Charge(spriteImage=os.path.join(folderPath,'images','items', 'choque_do_trovao.png'),
                        posInicial=(x, y),)
                    bt = 1
                    grupoBulletTime.add(charge)
            #Criar a shotgun
            if event.type == create_shotgun and random.randint(1,2)==1:
                if not jogador.arma == 'shotgun':
                    x = random.randint(200,bgWidth-200)
                    y = -200
                    shotgun = Shotgun(spriteImage=os.path.join(folderPath,'images','items', 'shotgun.png'),
                        posInicial=(x, y),)
                    grupoShotgun.add(shotgun)
            
            #Criar o ima
            if event.type == create_ima and random.randint(1,9)==1 and  (modo == "boss" or modo == "infinito"):
                #print('criando ima')
                #print('tentou ser criado')
                x = random.randint(200,bgWidth-200)
                y = -200
                ima = Ima(spriteImage=os.path.join(folderPath,'images','items', 'icon ima.png'),
                    posInicial=(x, y),)
                grupoIma.add(ima) 

        
            # Abrir loja usando a tecla "L" DESATIVADO!!!
            
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
                    if enemy.tipo_bala == "laser":
                        if not enemy.ja_laser:
                            enemy.disparo = 1
            #mudar estado do laser
            if event.type == mudar_laser:
                laser = 1
            #bala do boss
            if (event.type == disparo_boss) and boss_fight:
                boss.disparo = 1
            if event.type == criar_laser:
                boss_laser = 1
            #inimigo kamikaze começar a seguir
            if event.type == ativar_kamikaze:
                for enemy in grupoInimigo:
                    if enemy.tipo_bala == "self":
                        enemy.disparo = 1
                        #print("PERMITINDO ATIRAR")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    jogador.player_update('kabum')
        elif estadoDoJogo=="pausado":
            selecao = menu_pause.eventos(event)
            #despausar
            if selecao == "Retomar":
                estadoDoJogo = "jogando"
                sons(estadoDoJogo)
                tempo_no_menu += perf_counter() - tempo_atual
                menu_pause.opcaoAtual = 0
            #opções (eventualmente)
            elif selecao == "Opções":
                estadoDoJogo = "jogando" #modificar para criar um menu de opções dps
                sons(estadoDoJogo)
            #sair
            elif selecao == "Sair":
                pygame.quit()
                sys.exit()
                main=False
                estadoDoJogo="fechado"   
    if estadoDoJogo=="menu principal":
        menu_principal.draw(tela)
    elif estadoDoJogo=="tela de morte":
        tela_de_morte.draw(tela, jogador.kills)
    elif estadoDoJogo=="creditos":
        creditos.draw(tela)
    elif estadoDoJogo == "fim do tutorial":
        fim_do_tutorial.draw(tela, telaSizePlaceholder, bg)
    elif estadoDoJogo == "escolher modo":
        escolher_modo.draw(tela)
    elif estadoDoJogo == "escolher dificuldade":
        escolher_dificuldade.draw(tela)
        
    elif estadoDoJogo=="jogando":
        deltaTime = clock.tick(60)/1000
        if deltaTime>1.0:
            deltaTime=1.0
        dt_jogo = deltaTime
        #Salvar tecla apertada
        tecla = pygame.key.get_pressed()

        if jogador.kills % 15 == 0 and jogador.kills !=0 and not ja_entrou and not boss_fight and modo == "boss":
            wave_counter += 1
            mensagem = f"HORDA {wave_counter} FINALIZADA"
            mensagem_form = fonte_grande.render(mensagem, True, (0, 0, 0))
            tela.blit(mensagem_form, ((250), (bgHeight/2) - 55))
            pygame.display.flip() #para colocar a mensagem de final na tela
            sleep(3.0)
            #limpando os elementos da tela
            resetarVariaveis(grupoGrupos, 1)
            
            jogador.quick_shot, tempo_pausado = abrir_loja(tela, clock, jogador, jogador.quick_shot, jogador.bullet_time)
            inicio_de_jogo += tempo_pausado + 3
            ja_entrou = 1
            acabou_sair = 0
            pygame.event.clear() #tirando ""todos os eventos da fila, para não passar comandos p dps do intervalo
        
        if wave_counter % 5 == 0 and wave_counter != 0 and not boss_fight and not acabou_sair and modo == "boss":
            boss = Inimigo("Boss-W1", deltaTime, pos=(bgWidth/2, -100), limites_mov=(0, 0), sentido_inicial="null")
            grupoInimigo.add(boss)
            boss_fight = 1

        if boss_fight:
            if boss.vida >0 and boss.disparo:
                centro_bala = random.choice(pontos_possiveis)
                tipo = random.choice(balas_possiveis)
                print(f"OLHA AQ{centro_bala}")
                if tipo == "rajada":
                    sons("balaShotgunInimigo")
                    for pow in (0, 4, 7):    
                        bullet = Bullet(
                            os.path.join(folderPath, "images", "enemy", "bullet.png"),
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
                        os.path.join(folderPath, "images", "enemy", "bullet.png"),
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
                    bullet = Bullet(
                        os.path.join(folderPath, "images", "enemy", "bullet.png"),
                        (centro_bala),
                        dt=deltaTime,
                        tipo = tipo,
                        boss = 1
                    )
                    grupoLaser.add(bullet)
                    bullet.direcao((jogador.rect.center), centro_bala, pow)


                boss.disparo = 0

            elif boss.vida <= 0:
                tempo_de_jogo = perf_counter() - inicio_de_jogo - tempo_no_menu
                boss_fight = 0
                boss.kill()
                acabou_sair = 1
                mensagem_fim = "LUTA CONCLUIDA"
                mensagem_tempo = f"TEMPO TOTAL {tempo_de_jogo:0.1f}s"
                mensagem_form_fim = fonte_grande.render(mensagem_fim, True, (0, 0, 0))
                mensagem_form_tempo = fonte_media.render(mensagem_tempo, True, (0, 0, 0))
                tela.blit(mensagem_form_fim, ((300), (bgHeight/2) - 55))
                tela.blit(mensagem_form_tempo, ((300), (bgHeight/2) + 55))
                pygame.display.flip() #para colocar a mensagem de final na tela
                sleep(3.0)
                #limpando os elementos da tela
                resetarVariaveis(grupoGrupos, 1)
                jogador.quick_shot, tempo_pausado = abrir_loja(tela, clock, jogador, jogador.quick_shot, jogador.bullet_time)
                inicio_de_jogo += tempo_pausado + 3
                ja_entrou = 1
                pygame.event.clear()

        #calculo temporizador atual
        tempo_de_jogo = perf_counter() - inicio_de_jogo - tempo_no_menu
        
        #spawn novos inimigos
        if (len(grupoInimigo) < minimo_inimigos[wave_counter] and not boss_fight and (modo == "boss" or modo == "infinito")):
            sentido = random.choice(["R", "L"])
            coordenadas = (random.randint(350, bgWidth - 350), -200)
            if not len(grupoLaser):    
                tipo_inimigo = random.randint(0, 5)
            else:
                tipo_inimigo = random.randint(0, 4)
            novoInim = Inimigo(tipo_inimigo, deltaTime, pos=coordenadas, limites_mov=(300, bgWidth - 300), sentido_inicial=sentido)
            grupoInimigo.add(novoInim)

        #HUD da vida
        hp = f"Vida: {jogador.vida}"
        #print(hp)
        hp_form = fonte.render(hp, False, (255, 255, 255))

        #HUD do escudo
        escudos = f"Escudo: {jogador.armadura}"
        escudos_form = fonte.render(escudos, False, (100,180,255))
        
        #HUD das Moedas
        coin = f"Moedas : {jogador.moedas}"
        coin_form = fonte.render(coin, False, (255, 255, 255))

        #HUD do tempo 
        tempo_de_jogo = perf_counter() - inicio_de_jogo - tempo_no_menu
        timer = fonte.render(f"{tempo_de_jogo:.1f}s", False, (255, 255, 255))
        rect_timer = timer.get_rect()
        rect_timer.center = (680, 50)

        #HUD de kills
        kills = f"Kills: {jogador.kills}"
        kills_form = fonte.render(kills, False, (255, 255, 255))

        #HUD da carga:
        cargas = f"cargas:"
        cargas_form = fonte.render(cargas, False, (255, 215, 0))
        carga_icon = pygame.image.load(os.path.join(folderPath,'images','items', 'icon das cargas.png')).convert_alpha()
        carga_icon = pygame.transform.scale(carga_icon, (30, 30))
        
        #colisão player item
        pygame.sprite.spritecollide(jogador, grupoItem, True)    
        
        #moedas coletadas:
        moeda_coletados = []
        for moeda in grupoMoeda:
            if jogador.hitbox.colliderect(moeda.rect):
                moeda_coletados.append(moeda)
                moeda.kill()
            elif moeda.rect.topright[1] > bgHeight + 6: #eliminar o item da memória caso saia da tela
                moeda.kill()

        for moeda in moeda_coletados:
            jogador.moedas += moeda.valor
            
        #Escudo coletado:
        escudo_coletados = []
        for pedacos in grupoEscudo:
            if jogador.hitbox.colliderect(pedacos.rect):
                escudo_coletados.append(pedacos)
                pedacos.kill()
            elif pedacos.rect.topright[1] > bgHeight + 6: #eliminar o item da memória caso saia da tela
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
                cura.kill()
            elif cura.rect.topright[1] > bgHeight + 6: #eliminar o item da memória caso saia da tela
                cura.kill()

        for i in cura_coletados:
            if jogador.vida < 100:
                jogador.vida += 30
    
        #Quick Shot coletado:
        quick_shots_coletados = []
        for powerup in grupoQuickShot:
            if jogador.hitbox.colliderect(powerup.rect):
                quick_shots_coletados.append(powerup)
                powerup.kill()
            elif powerup.rect.topright[1] > bgHeight + 6: #eliminar o item da memória caso saia da tela
                powerup.kill()
        if quick_shots_coletados:
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
                carga.kill()
                if jogador.charge < 5:
                    jogador.charge += 1
            elif carga.rect.topright[1] > bgHeight + 6: #eliminar o item da memória caso saia da tela
                carga.kill()

        #Coletar o Imã
        imas_coletados = []
        for ima in grupoIma:
            if jogador.hitbox.colliderect(ima.rect):
                imas_coletados.append(ima)
                ima.kill()
            elif ima.rect.topright[1] > bgHeight + 6:
                ima.kill()
        #print('ima identificado')
        if imas_coletados:
            #print('ima coletado')
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
        shotgun_coletada = []
        for shotgun in grupoShotgun:
            if jogador.hitbox.colliderect(shotgun.rect):
                shotgun_coletada.append(shotgun)
                shotgun.kill()
            elif shotgun.rect.topright[1] > bgHeight + 6: #eliminar o item da memória caso saia da tela
                shotgun.kill()

            
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
            tela.blit(bg, (0, -bg.get_height()*appender+scroll))
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
            pygame.draw.rect(tela, (100, 180, 255), (x, y, tamanho_quadrado, tamanho_quadrado))
            
        #printar timer na tela
        #Tiro do jogador 
        if tecla[pygame.K_SPACE]:
            if perf_counter() - ultimo_tiro >= intervalo_tiro:
                sons("balaPlayer")
                if jogador.arma == 'shotgun':
                    angulos_shotgun = [-10, 0, 10]
                else:
                    angulos_shotgun = [0]
                for angulo in angulos_shotgun:
                    if not jogador.quick_shot:
                        projetil = Bala(os.path.join(folderPath,"images","playerSprites","bala-player.png"),jogador.rect.center,dt=deltaTime)
                    #quick_shot
                    if jogador.quick_shot:
                        projetil = Bala(os.path.join(folderPath, "images", "Items", "quick_shot.png"),jogador.rect.center,dt=deltaTime)
                    direcao_base = pygame.math.Vector2(0, -projetil.velocidade)
                    projetil.dire = direcao_base.rotate(angulo)
                    grupoBala.add(projetil)
                ultimo_tiro = perf_counter()
                
        #checa os inimigos ativos para disparar
        for enemy in grupoInimigo:
            if (enemy.disparo) and  enemy.rect.bottomleft[1] >15:
                #print("ENTROU AQUI")
                if enemy.tipo_bala == "follow": 
                    sons("balaInimigo") #balaPlayer, balaInimigo, balaShotgunInimigo, laser
                    bullet = Bullet(
                        os.path.join(folderPath, "images", "enemy", "bullet.png"),
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
                            os.path.join(folderPath, "images", "enemy", "bullet.png"),
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
                        os.path.join(folderPath, "images", "enemy", "bullet.png"),
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
                        os.path.join(folderPath, "images", "enemy", "bullet.png"),
                        ((enemy.rect.width/2) + enemy.rect.bottomleft[0],enemy.rect.bottomright[1]),
                        dt=deltaTime,
                        tipo = "laser",
                        boss = 0,
                    )
                    enemy.velocidadex = 0 #para quando atirar o laser
                    enemy.velocidadey = -6
                    grupoLaser.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy.rect.center), pow = 0)
                elif enemy.tipo_bala == "tracker":
                    bullet = Bullet(
                    os.path.join(folderPath, "images", "enemy", "bullet.png"),
                    (enemy.rect.centerx,enemy.rect.centery),
                    dt=deltaTime,
                    tipo = "tracker",
                    boss = 0
                    )
                    grupoBullets.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy.rect.center), pow = 0)

                elif enemy.tipo_bala == "self":
                    enemy.follow((bgWidth/2, bgHeight/2), jogador.rect.center)
                    #print("COMECOU A RASTREAR")


                #ativa o cooldown do disparo do inimigo
                enemy.disparo=0
                
        grupoJogador.update(deltaTime, camera) #Update do player antes por conta da criação do rastro
        
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
            grupoJogador.draw(tela)
        else:
            if perf_counter() - t_clicks < jogador.tempoPiscar:
                grupoJogador.draw(tela)
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
            for laser in grupoLaser:
                if laser.rect.colliderect(jogador.rect):
                    dano = laser.dano
        for bala in grupoBullets:#checando se a bala já saiu da tela
            if bala.rect.topright[1] > bgHeight or bala.rect.topleft[0] < 0 or bala.rect.topleft[0] > bgWidth or bala.rect.topright[1] < 0:
                bala.kill()
                
        #Colisão do inimigo com a hitbox do player
        colisao_i = False
        if pygame.sprite.spritecollide(jogador, grupoInimigo, False, pygame.sprite.collide_mask):
            colisao_i = True
            dano = 10
            for bad in grupoInimigo:
                if bad.rect.colliderect(jogador.rect) and bad.i == 4:
                    bad.kill()
        if (colisao_b or colisao_i) and not jogador.invencibilidade: #as variáveis ficam falsas até detectarem uma colisão, quando recebe um elemento, entra na condicional
            if jogador.armadura == 0:
                jogador.vida -= dano
            else:
                if jogador.armadura < 20:
                    jogador.armadura = 0
                else:
                    jogador.armadura -= dano
            jogador.player_update("D")
            if jogador.vida<=0:
                tempo_morte=perf_counter()
                estadoDoJogo="tela de morte"
            t_invencibilidade = perf_counter()
            t_clicks = perf_counter()
            
        enemyPos = []
        #Colisão tiro dos players com o inimigo e sua morte:
        for enemy in grupoInimigo:
            colisao_inimigo = pygame.sprite.spritecollide(enemy, grupoBala, True, pygame.sprite.collide_mask)
            if colisao_inimigo:
                enemy.vida -= 20
                #print(f"Inimigo: {enemy01.vida}")
            if enemy.vida <= 0:
                #print("morreu")
                enemy.kill()
                jogador.add_kill()
                ja_entrou = 0 #para entrar na loja no proximo 
            if enemy.rect.topright[1] >= bgHeight + 6 or enemy.rect.topright[0] < 0 or enemy.rect.topleft[0] > bgWidth + 6: 
                enemy.kill()

            if enemy.i == 5 or boss_fight:
                enemyPos.append(((enemy.rect.width/2) + enemy.rect.bottomleft[0],enemy.rect.bottomright[1]))

        #update de tudo
        grupoInimigo.update(dt_jogo, camera)
        grupoBullets.update(dt_jogo, camera, jogador.posicao, mudar, laser, enemyPos)
        grupoBala.update(dt_jogo, camera, jogador.posicao)
        grupoRastro.update(deltaTime, camera) #Update do rastro
        grupoQuickShot.update(dt_jogo, camera)
        grupoBulletTime.update(dt_jogo, camera) #Update das cargas
        grupoShotgun.update(dt_jogo, camera)
        grupoEscudo.update(dt_jogo, camera)
        grupoMoeda.update(dt_jogo, camera)
        grupoCura.update(dt_jogo, camera)
        grupoLaser.update(dt_jogo, camera, jogador.posicao, mudar, laser, enemyPos)
        grupoIma.update(dt_jogo, camera)

        #desenha tudo na tela
        
        grupoBullets.draw(tela)
        grupoInimigo.draw(tela)
        grupoQuickShot.draw(tela)
        grupoBulletTime.draw(tela)#Desenhar a carga na tela
        grupoShotgun.draw(tela)
        grupoEscudo.draw(tela) 
        grupoMoeda.draw(tela)
        grupoCura.draw(tela)
        grupoLaser.draw(tela)
        grupoIma.draw(tela)

        #Colocar as novas HUDs na tela:
        tela.blit(hp_form, (18, 18))
        tela.blit(coin_form, (200, 18))
        tela.blit(escudos_form, (20, 68))
        #Filtro Cinza do bullet_time
        if jogador.bullet_time:
            tela.blit(filtro_bullet_time, (0, 0))
        grupoRastro.draw(tela)
        #Pra bala não terem o filtro
        grupoBala.draw(tela)
        tela.blit(timer, (((bgWidth-timer.get_width())/2), 10))
        tela.blit(kills_form, (bgWidth-kills_form.get_width()-20, 10))
        #Representação das cargas
        tela.blit(cargas_form, (18, 108))
        pos_x_inicial_carga = 18 + cargas_form.get_width() + 15
        largura_imagem = 30
        espacamento_carga = 8
        for i in range(jogador.charge):
            x = pos_x_inicial_carga + (i * (largura_imagem + espacamento_carga))
            y = 122 
            tela.blit(carga_icon, (x, y))

        if modo == "tutorial":
            if contador_de_teclas_mov in range(0, 10):
                sug = "use W-A-S-D para se movimentar"
            if contador_de_teclas_mov >= 10 and perf_counter() - inicio_de_jogo > 3 and contador_de_teclas_espaco == 0:
                sug = "aperte espaço para atirar"
            if (contador_de_teclas_mov + contador_de_teclas_espaco) >= 10 and contador_de_teclas_espaco !=0 and len(grupoMoeda) == 0 and jogador.moedas <= 8 and perf_counter() - inicio_de_jogo > 6:
                sug = "moedas compram itens na loja"
                x = random.randint(200,bgWidth-200)
                y = -200
                moeda_ouro = Moedas(spriteImage=os.path.join(folderPath,'images','items', 'coin 2.png'),
                    posInicial=(x, y), valor = 3)
                
                x = random.randint(200,bgWidth-200)
                y = -200
                moeda_prata = Moedas(spriteImage=os.path.join(folderPath,'images','items','Silver.Coin.png'),
                    posInicial=(x, y),valor = 1)
                
                
                grupoMoeda.add(moeda_ouro)
                grupoMoeda.add(moeda_prata)

                if jogador.moedas > 1:
                    x = random.randint(200,bgWidth-200)
                    y = -50
                    ima = Ima(spriteImage=os.path.join(folderPath,'images','items', 'icon ima.png'),
                        posInicial=(x, y),)
                    grupoIma.add(ima)  
                    
                    sug = "use o imã para puxar moedas"

                
            
            if jogador.moedas > 8 and len(grupoEscudo) == 0 and len(grupoCura) == 0 and jogador.escudo == 0:
                sug = "cura e escudo recuperam sua vida"
                x = random.randint(200,bgWidth-200)
                y = -200
                escudoSpawnado = ParteEscudo(
                    spriteImage=os.path.join(folderPath,'images', 'Items', 'Escudo.png'),
                    posInicial=(x, y))
                
                x += 70
                if x > bgWidth - 200: #obrigando o med kit a spawnar perto do escudo so p pegar na mesma hitbox e n dar problema p seguir a lógica
                    x -= 20
                y = -200
                cura = Cura(
                    spriteImage=os.path.join(folderPath, 'images','items', 'med_kit.png'),
                    posInicial=(x, y)
                )
                
                grupoCura.add(cura)
                grupoEscudo.add(escudoSpawnado)

            if len(grupoEscudo) >= 0 and len(grupoCura) >= 0 and intervalo_tiro ==cooldown_normal and jogador.escudo > 0 and len(grupoQuickShot) == 0 and len(grupoInimigo) == 0:
                sug = "quick shot faz atirar mais rápido"
                
                x = random.randint(200,bgWidth-200)
                y = -200
                powerupSpawnado = Quick_Shot(
                    spriteImage=os.path.join(folderPath,'images', 'Items', 'QS_up.png'),
                    posInicial=(x, y),
                )

                grupoQuickShot.add(powerupSpawnado)

            if len(quick_shots_coletados) > 0 and not jogador.bullet_time and len(grupoQuickShot) == 0 and len(grupoInimigo) == 0:
                sug = "aperte shift para o bullet time"
                

                x = random.randint(200,bgWidth-200)
                y = -200
                charge = Charge(spriteImage=os.path.join(folderPath,'images','items', 'choque_do_trovao.png'),
                    posInicial=(x, y),)
                grupoBulletTime.add(charge)

            if tecla[pygame.K_LSHIFT]:
                fim_tutorial =1
            

            if fim_tutorial:
                sug = "mate o inimigo"
                grupoInimigo.add(enemy01)

            if enemy01.vida <= 0:
                sleep(0.5)
                estadoDoJogo = "fim do tutorial"


                
            if tecla[pygame.K_w]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_s]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_a]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_d]:
                contador_de_teclas_mov += 1
            elif tecla[pygame.K_SPACE]:
                contador_de_teclas_espaco += 1
            
            

            sug_form = fonte_media.render(sug, True, (0, 0, 0))
            tela.blit(sug_form, (bgWidth/2-320, 200))

    if estadoDoJogo == "pausado":
        #menu_pause.draw_tela(tela, bg)
        appender=0
        while(appender<tiles):
            tela.blit(bg, (0, -bg.get_height()*appender+scroll))
            appender+=1
        
        #DESENHAR INIMIGOS
        grupoBullets.draw(tela)
        grupoInimigo.draw(tela)
        grupoQuickShot.draw(tela)
        grupoBulletTime.draw(tela)#Desenhar a carga na tela
        grupoEscudo.draw(tela) 
        grupoMoeda.draw(tela)
        grupoCura.draw(tela)
        grupoJogador.draw(tela)
        
        tela.blit(filtro_pause, (0, 0))
        
        
        #NOVAS HUD
        
        tela.blit(hp_form, (18, 18))
        tela.blit(coin_form, (200, 18))
        tela.blit(escudos_form, (20, 68))
        tela.blit(cargas_form, (18, 108))
        for i in range(jogador.charge):
            x = pos_x_inicial_carga + (i * (largura_imagem + espacamento_carga))
            y = 122 
            tela.blit(carga_icon, (x, y))

        tela.blit(timer, (((bgWidth-timer.get_width())/2), 10))
        tela.blit(kills_form, (bgWidth-kills_form.get_width()-20, 10))
        menu_pause.draw_texto(tela, telaSizePlaceholder)

    #flip atualiza a tela
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)        