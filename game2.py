import pygame
import sys
import random
from pygame.locals import *

pygame.init()

# Função para inicializar o jogo e configurar a tela
def init_game():
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Meu Jogo")
    return screen

# Função para desenhar texto na tela
def draw_text(surface, text, font_size, color, position):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Função para o menu inicial
def main_menu(screen):
    menu_active = True
    while menu_active:
        screen.fill((0, 0, 0))
        draw_text(screen, "Pressione ESPAÇO para começar", 36, (255, 255, 255), (200, 400))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    menu_active = False

# Classe Player para o avatar do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 740)
    
    def slide(self):
        pressed_button = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_button[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < 800:
            if pressed_button[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe Enemy para os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 760), 0)
        self.speed = speed
    
    def fall(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > 800:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe Collectible para itens colecionáveis
class Collectible(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 760), 0)
        self.speed = speed
    
    def fall(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > 800:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Função para atualizar a posição dos inimigos e verificar colisões
def update_enemies(enemies, player_rect):
    for enemy in enemies:
        enemy.fall()
        if player_rect.colliderect(enemy.rect):
            return True
    return False

# Função para criar novos inimigos
def spawn_enemy():
    enemy_type = random.choice(["enemy1.png", "enemy2.png"])
    if enemy_type == "enemy1.png":
        return Enemy("enemy1.png", 5)
    else:
        return Enemy("enemy2.png", 8)

# Função para criar novos itens colecionáveis
def spawn_collectible():
    collectible_type = "collectible.png"  # Use uma imagem apropriada para o item
    return Collectible(collectible_type, 3)

# Função para atualizar os itens colecionáveis e verificar a coleta
def update_collectibles(collectibles, player_rect):
    collected_items = 0
    for item in collectibles:
        item.fall()
        if player_rect.colliderect(item.rect):
            item.kill()
            collected_items += 1
    return collected_items

# Função principal do jogo
def main():
    screen = init_game()
    player = Player()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    clock = pygame.time.Clock()
    last_spawn_time = 0
    spawn_delay = 1000
    score = 0
    
    main_menu(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_delay:
            last_spawn_time = current_time
            enemies.add(spawn_enemy())
            if random.randint(0, 1) == 0:  # 50% chance de spawnar um item colecionável
                collectibles.add(spawn_collectible())
        
        player.slide()
        if update_enemies(enemies, player.rect):
            print("Game Over")
            break
        
        # Atualizar e verificar a coleta de itens
        score += update_collectibles(collectibles, player.rect)
        
        screen.fill((255, 255, 255))
        player.draw(screen)
        enemies.draw(screen)
        collectibles.draw(screen)

        # Desenhar a pontuação na tela
        draw_text(screen, f"Pontos: {score}", 24, (0, 0, 0), (10, 10))
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
