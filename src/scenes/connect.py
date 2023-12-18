from .scene import Scene, pygame
from util import Image


class ConnectScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.screenImage = Image("scenes/connect/screen.png", (0,0))

    def render(self):
        self.screenImage.render(self.screen)
        return super().render()
