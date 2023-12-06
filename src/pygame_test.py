import pygame

pygame.init()

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

img = pygame.image.load("wii.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            quit()

    screen.blit(img, (0,0))

    pygame.display.update()
