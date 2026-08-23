import pygame


class Personagem:
    def __init__(self):
        self.x = 50
        self.y = 425
        self.width = 40
        self.height = 60
        self.velocity = 10
        self.isJumping = False
        self.jumpCount = 10

    def mover(self, width_janela, height_janela):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] and self.x > self.velocity:
            self.x -= self.velocity
        if (
            teclas[pygame.K_RIGHT]
            and self.x < width_janela - self.width - self.velocity
        ):
            self.x += self.velocity
        if not(self.isJumping):
            if teclas[pygame.K_UP] and self.y > self.velocity:
                self.y -= self.velocity

            if (
                teclas[pygame.K_DOWN]
                and self.y < height_janela - self.height - self.velocity
            ):
                self.y += self.velocity
            if teclas[pygame.K_SPACE]:
                self.isJumping = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 10
