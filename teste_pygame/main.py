import pygame

from Personagem import Personagem

pygame.init()

window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Jogo teste 1")

personagem = Personagem()

rodar = True
while rodar:
    pygame.time.delay(50)  # delay ao iniciar

    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodar = False

    personagem.mover(window_width, window_height)

    window.fill((0, 0, 0))

    pygame.draw.rect(
        window,
        (255, 0, 0),
        (personagem.x, personagem.y, personagem.width, personagem.height),
    )
    pygame.display.update()  # mostrar as coisas

pygame.quit()
