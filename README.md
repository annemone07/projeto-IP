# Aerohell

## Projeto Final Disciplina Introdução à Programação

## 👥 Integrantes

Felipe Lopez Guerra (flg)

João Felipe Audet Guerra (jfag)

Pedro Henrique Carício Pereira de Sousa (phcps)

Rafael Tomaz Araujo Leite (rtal)

Rodrigo Machado Araujo (rma10)

Ariel Soares Pereira Rodrigues (aspr)

## 📂 Arquitetura do Projeto

```
projeto-IP/

|
│── images/ # Arquivos de imagem
│   
│── sons/ # Arquivos de som
|
│── config.py # Centraliza as variáveis globais, os parâmetros de redimensionamento da tela e as configurações de áudio
│   
│── enemy.py # Define as classes dos comportamentos dos inimigos
│   
│── funcoes.py # Funções dedicadas ao reinício das variáveis, configuração da música e criação do jogador
│
│── itens.py # Define as classes dos coletáveis (moedas, cura, parte do escudo, charge, imã, quickshot e shotgun)
│
│── loja.py # Define as classe para o ambiente de compra de itens para o jogador
|
│── menu.py # Define as classes dos menus do jogo, incluindo a tela inicial, seleção de modo e de dificuldade, tutorial, créditos e controle de volume e de resolução
│   
│── player.py # Armazena classes do comportamento do jogador
│ 
|── mainCode.py # Loop principal do código
|
├── .gitignore # Configurações do projeto ocultadas para o Git
|
|── prints gameplay/ # Screenshots funcionamento jogo
|
└── README.md # Informações acerca do projeto
```

## 📸 Capturas de tela

Tela Inicial
![tela inicial](https://github.com/annemone07/projeto-IP/blob/main/prints%20gameplay/image7.png)

Gameplay
![jogo normal](https://github.com/annemone07/projeto-IP/blob/main/prints%20gameplay/image8.png)

Boss Fight
![luta com boss](https://github.com/annemone07/projeto-IP/blob/main/prints%20gameplay/image5.png)

Loja de Itens
![loja](https://github.com/annemone07/projeto-IP/blob/main/prints%20gameplay/image0.png)

## 🛠 Ferramentas, bibliotecas e frameworks

**Python**: Linguagem de programação ensinada na disciplina de Introdução à Programação e utilizada pela biblioteca Pygame.

**Pygame-ce**: Biblioteca externa do Python utilizada com a finalidade de facilitar o carregamento de imagens e áudios, sistematização da lógica de colisão e dos sprites, bem como da recepção dos inputs dos usuários.

**Visual Studio Code**: IDE utilizada para programação e testagem do jogo.

**Krita** e **Pixilart**: softwares utilizados para confecção dos sprites do jogo.

**Math**: biblioteca nativa do Python utilizada com o objetivo de gerar maior precisão nas operações matemáticas envolvendo o cálculo dos ângulos associados à trajetória das balas.

**OS**: biblioteca empregada no mapeamento dos diretórios, garantindo o acesso ao som e aos sprites do jogo.

**Random**: biblioteca nativa do Python usada para definir as probabilidades de aparecimento dos coletáveis e dos inimigos, bem como a movimentação destes últimos

**Time**: biblioteca nativa do Python para ter o manejo de tempo de alguns eventos internos de forma mais precisa, por algumas limitações do timer do pygame

**Kenney.nl** e **opengameart.org**: sites utilizados para buscar os assets com os devidos créditos para o jogo.

**GitHub**: plataforma utilizada para hospedagem do repositório do projeto, bem como para versionamento do código-fonte.

## 🤝 Divisão do Trabalho

Felipe Lopez Guerra (flg): criação coletáveis, relatório final e slides

João Felipe Audet Guerra (jfag): mecânicas dos inimigos, modos de jogo, menus e ranking interno

Pedro Henrique Carício Pereira de Sousa (phcps): criação da loja de itens e realização de testes e balanceamento

Rafael Tomaz Araujo Leite (rtal): criação dos upgrades do player e animações do player e dos inimigos 

Rodrigo Machado Araujo (rma10): Sistema para diferentes telas, sistema de som, fundo rolante, centralização das configurações

Ariel Soares Pereira Rodrigues (aspr):

## 📚 Conceitos utilizados

**Operadores Condicionais [if,elif,else]**: foram aplicados com o objetivo de definir as múltiplas respostas do programa em decorrência das ações do jogador e ações automáticas dos inimigos.

**Listas, Tuplas e Dicionários**: aplicadas na lógica de armazenamento dos dados de posição, coleta e tipo dos objetos do jogo. Com cada estrutura sendo usada a depender da necessidade dentro do código.

**Funções e Métodos**: empregados para definir os comportamentos dos objetos dentro das classes.

**Laços de Repetição [for, while]**: utilizados para estabelecer o loop principal de funcionamento do jogo, bem como para definir a mecânica de colisão dos objetos e lógicas cíclicas com ciclo de execução pequeno, como o rolamento da tela de fundo e formação de disparo dos inimigos.

**Programação Orientada a Objetos e Modularização**: Essenciais para a organização do código-fonte. A criação de classes com o objetivo de encapsular os atributos associados aos objetos permitiu maior eficiência no instanciamento dos múltiplos elementos presentes na partida, como inimigos, o player e as balas.

**Versionamento de código**: aplicado no gerenciamento das versões do código-fonte do projeto, possibilitando uma maior organização e transparência a cada modificação nos arquivos do jogo, o que gera a prevenção de erros e a minimização do retrabalho.

## 🧩 Desafios, Erros e Aprendizados

### Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?

O maior erro cometido ao longo do projeto foi a carência de definição de um guia claro de arquitetura do código, o que dificultava a integração entre os módulos gerados pelos diferentes estilos de programação dos integrantes do grupo. Essa divergência de práticas de programação, agravada pela falta de comentários nos trechos do código, potencializou o retrabalho, de modo a retardar o andamento do desenvolvimento do jogo. Diante desse cenário, uma refatoração padronizada e a documentação interna dos scripts foram as ações tomadas pelo grupo para solucionar esse problema.

### Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

O maior desafio com o qual lidamos durante o trabalho foi o aprendizado de Pygame e GitHub simultaneamente à execução do projeto, uma vez que a maior parte dos integrantes do grupo não tinha contato prévio com essas tecnologias. Dessa forma, o aprendizado paralelo ao uso dessas ferramentas gerou erros, tais como conflitos nas fusões das versões do código e retrabalho para a adição das novas mecânicas ao jogo. Levando em conta essa situação, a equipe mostrou-se engajada para buscar conhecimentos acerca dessas ferramentas, por meio de diversas fontes, como os materiais disponibilizados na plataforma Redu e no Discord, bem como através de pesquisas independentes.

### Quais as lições aprendidas durante o projeto?

O projeto foi essencial para reconhecer a importância do alinhamento técnico e da documentação para a colaboração da equipe, o que otimizou a adição de novas funcionalidades e minimizou conflitos de integração, reduzindo o retrabalho. Além disso, os empecilhos iniciais associados ao uso do GitHub possibilitaram à equipe uma importante curva de aprendizado, a qual gerou um amadurecimento coletivo acerca da manutenção de um fluxo de trabalho eficiente e integrado.

## Creditos para assets utilizados
“Void Main Ship”, de Foozle. Disponível em foozlecc.itch.io/void-main-ship, sob licensa CC0,\
“Void Fleet Pack 1”, de Foozle. Disponível em foozlecc.itch.io/void-fleet-pack-1, sob licensa CC0,\
“Pixel Shmup”, de Kenney. Disponível em kenney.nl/assets/pixel-shmup, sob licensa CC0,\
“Gold Coin/Token”, de BizmasterStudios. Disponível em opengameart.org/content/gold-cointoken, sob licensa CC0,\
“Flying me softly”, de Alexandr Zhelanov. Disponível em opengameart.org/content/flying-me-softly, sob licensa CC-BY 3.0,\
“Space Shoot Sounds”, de Robin Lamb. Disponível em opengameart.org/content/space-shoot-sounds, sob licensa CC0,\
“Laser Beam”, de frosty ham. Disponível em opengameart.org/content/laser-beam, sob licensa CC0,\
“Explosion”, de TinyWorlds. Disponível em opengameart.org/content/explosion-0, sob licensa CC0,\
"Bossa Nova", de Joth. Disponível em opengameart.org/content/bossa-nova, sob licença CC0,\
"8-bit Epic Space Shooter Music", de HydroGene. Disponível em opengameart.org/content/8-bit-epic-space-shooter-music, sob licença CC0,\
"NES Shooter Music (5 tracks, 3 jingles)\", de SketchyLogic. Disponível em  opengameart.org/content/nes-shooter-music-5-tracks-3-jingles, sob licença CC0,\
"8bit Death Whirl", de Fupi. Disponível em  opengameart.org/content/8bit-death-whirl, sob licença CC0,\
"10 8bit coin sounds", de Luke.RUSTLTD. Disponível em  opengameart.org/content/10-8bit-coin-sounds, sob licença CC0,\
"8-Bit Sound Effect Pack (Vol. 001)", de Deva. Disponível em opengameart.org/content/8-bit-sound-effect-pack-vol-001, sob licença CC0,\
"Power Up, Level Up #beansjam", de Quitschie. Disponível em  opengameart.org/content/power-up-level-up-beansjam, sob licença CC0,\
"2 Gun Reloads", de StarNinjas. Disponível em  opengameart.org/content/2-gun-reloads, sob licença CC0

## 🎮 Tutorial Instalação Jogo

### 1. Clone o repositório

Escreva o seguinte comando no terminal do Git:

```bash

git clone https://github.com/annemone07/projeto-IP.git
```

### 2. Instale as dependências

```bash

pip install pygame-ce
```

### 3. Execute o arquivo

```bash
python mainCode.py
```
