import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 100), (0, 0, 40, 40)) # Зеленый квадрат
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)

    def update(self):
        # Поворот за мышкой
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-rel_y, rel_x)) - 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Движение WASD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.pos.y -= 5
        if keys[pygame.K_s]: self.pos.y += 5
        if keys[pygame.K_a]: self.pos.x -= 5
        if keys[pygame.K_d]: self.pos.x += 5
        self.rect.center = self.pos
