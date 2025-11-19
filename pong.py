import pygame
import sys

# Inicialização
pygame.init()

# --- CONFIGURAÇÕES DA JANELA ---
LARGURA = 800
ALTURA = 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Super Pong")

FPS = 60
clock = pygame.time.Clock()

# --- CORES ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# --- OBJETOS DO JOGO ---

# Barras usando Rect (x, y, largura, altura)
largura_barra = 15
altura_barra = 100

barra_esq = pygame.Rect(20, ALTURA//2 - altura_barra//2, largura_barra, altura_barra)
barra_dir = pygame.Rect(LARGURA - 40, ALTURA//2 - altura_barra//2, largura_barra, altura_barra)

# Bola
bola = pygame.Rect(LARGURA//2 - 10, ALTURA//2 - 10, 20, 20)

# Velocidades
vel_bola_x = 4
vel_bola_y = 4
vel_barra = 6

# Pontuação
pontos_esq = 0
pontos_dir = 0
fonte = pygame.font.SysFont(None, 40)

def resetar_bola():
    global vel_bola_x, vel_bola_y
    bola.center = (LARGURA//2, ALTURA//2)
    vel_bola_x *= -1  # Muda lado do saque


while True:
    # --- 1. EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- 2. MOVIMENTO DO JOGADOR (barra esquerda) ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and barra_esq.top > 0:
        barra_esq.y -= vel_barra
    if teclas[pygame.K_s] and barra_esq.bottom < ALTURA:
        barra_esq.y += vel_barra

    # --- 3. MOVIMENTO CPU SIMPLES (barra direita) ---
    # Acompanha a bola lentamente
    if bola.centery > barra_dir.centery:
        barra_dir.y += vel_barra * 0.9
    else:
        barra_dir.y -= vel_barra * 0.9

    # Não deixa passar da tela
    barra_dir.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

    # --- 4. MOVIMENTO DA BOLA ---
    bola.x += vel_bola_x
    bola.y += vel_bola_y

    # Colisão com bordas superior/inferior
    if bola.top <= 0 or bola.bottom >= ALTURA:
        vel_bola_y *= -1

    # --- 5. COLISÕES COM AS BARRAS ---
    if bola.colliderect(barra_esq) or bola.colliderect(barra_dir):
        vel_bola_x *= -1

    # --- 6. MARCAR PONTO ---
    if bola.left <= 0:
        pontos_dir += 1
        resetar_bola()

    if bola.right >= LARGURA:
        pontos_esq += 1
        resetar_bola()

    # --- 7. DESENHO NA TELA ---
    TELA.fill(PRETO)

    # Desenha barras e bola
    pygame.draw.rect(TELA, BRANCO, barra_esq)
    pygame.draw.rect(TELA, BRANCO, barra_dir)
    pygame.draw.ellipse(TELA, BRANCO, bola)

    # Linha central
    pygame.draw.aaline(TELA, BRANCO, (LARGURA//2, 0), (LARGURA//2, ALTURA))

    # Pontuação
    pont_texto = fonte.render(f"{pontos_esq}  x  {pontos_dir}", True, BRANCO)
    TELA.blit(pont_texto, (LARGURA//2 - pont_texto.get_width()//2, 20))

    pygame.display.update()
    clock.tick(FPS)
