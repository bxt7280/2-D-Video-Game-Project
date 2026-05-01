from pytmx.util_pygame import load_pygame

class Map():
    def __init__(self, path, screen):
        self.screen = screen
        self.tmxData = load_pygame(path)
        

    def draw(self):
        for layer in self.tmxData:
            for tile in layer.tiles():
                x_pixel = tile[0] * 32
                y_pixel = tile[1] * 32
                self.screen.blit(tile[2], (x_pixel, y_pixel))
        