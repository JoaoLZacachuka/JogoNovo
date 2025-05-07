import pygame
import random
import math

# Inicializar o pygame
pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Space Invaders")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Jogador
jogador_img = pygame.Surface((50, 30))
jogador_img.fill((0, 255, 0))
jogador_x = LARGURA // 2 - 25
jogador_y = ALTURA - 60
jogador_vel = 5

# Tiro
tiro_img = pygame.Surface((5, 20))
tiro_img.fill((255, 255, 0))
tiro_x = 0
tiro_y = jogador_y
tiro_vel = 7
tiro_ativo = False

# Inimigos
inimigo_img = pygame.Surface((40, 30))
inimigo_img.fill((255, 0, 0))
inimigos = []
vel_inimigo = 2

for _ in range(6):
    x = random.randint(0, LARGURA - 40)
    y = random.randint(50, 150)
    dx = vel_inimigo
    inimigos.append([x, y, dx])

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 36)

def mostrar_pontuacao():
    texto = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto, (10, 10))

# Colisão
def colisao(x1, y1, x2, y2, dist=27):
    return math.hypot(x2 - x1, y2 - y1) < dist

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    tela.fill(PRETO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Controles
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador_x > 0:
        jogador_x -= jogador_vel
    if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - 50:
        jogador_x += jogador_vel
    if teclas[pygame.K_SPACE] and not tiro_ativo:
        tiro_x = jogador_x + 22
        tiro_y = jogador_y
        tiro_ativo = True

    # Movimento do tiro
    if tiro_ativo:
        tela.blit(tiro_img, (tiro_x, tiro_y))
        tiro_y -= tiro_vel
        if tiro_y < 0:
            tiro_ativo = False

    # Desenhar jogador
    tela.blit(jogador_img, (jogador_x, jogador_y))

    # Movimento inimigos
    for inimigo in inimigos:
        inimigo[0] += inimigo[2]
        if inimigo[0] <= 0 or inimigo[0] >= LARGURA - 40:
            inimigo[2] *= -1
            inimigo[1] += 30  # desce uma linha

        # Colisão
        if tiro_ativo and colisao(tiro_x, tiro_y, inimigo[0] + 20, inimigo[1] + 15):
            pontuacao += 1
            tiro_ativo = False
            inimigo[0] = random.randint(0, LARGURA - 40)
            inimigo[1] = random.randint(50, 150)

        tela.blit(inimigo_img, (inimigo[0], inimigo[1]))

    mostrar_pontuacao()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
