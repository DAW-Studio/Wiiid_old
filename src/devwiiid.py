import sys
import time
import pygame
from util import Image
from scenes.connect import ConnectScene
from scenes.main import MainScene


class DevWiiid:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((720,720))
        pygame.display.set_caption("Wiiid")

        self.scenes = [ConnectScene(self.screen), MainScene(self.screen)]
        self.current_scene = 1


    def run(self):
        while True:
            scene = self.scenes[self.current_scene]
            self.screen.fill((0,0,0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYDOWN:
                #     scene.main_image.surface = scene.main_image.surface.convert()
                #     print("convert")


            scene.render()

            pygame.display.update()


DevWiiid().run()
