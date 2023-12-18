from .scene import Scene, pygame
from util import Image

class MainScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.main_image = Image("temp.png", (0,0))

    def render(self):
        self.main_image.render(self.screen)
        return super().render()
