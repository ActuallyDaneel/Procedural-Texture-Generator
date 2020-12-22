from PIL import Image
import typing
import random


class Canvas:
    def __init__(self, size: tuple=(64, 64), color: tuple=(200, 0, 0)):
        self.canvas = Image.new(mode="RGBA", size=size, color=color)
        self.size = size
        self.pixel_count = size[0] * size[1]

    def show(self) -> None:
        """QOL shortcut to Object.canvas.show"""
        self.canvas.show()

    def save(self, name: str) -> None:
        """QOL shortcut to Object.canvas.save"""
        self.canvas.save(name, format="png")

    def pixel_list(self) -> list:
        """Returns list of pixels in horizontal lines from the bottom up."""
        pixels = []
        y_line = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                y_line.append(self.canvas.getpixel((x, y)))
            pixels.append(y_line.copy())
            y_line.clear()
        return pixels
    
    def randomize_pixels(self) -> None:
        """Randomizes the color and alpha of each pixel."""
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pixel = list(self.canvas.getpixel((x, y)))
                for i in range(4):
                    max_add = 255-pixel[i]
                    max_sub = -pixel[i]
                    change = random.randrange(max_sub, max_add)
                    pixel[i] += change
                self.canvas.putpixel((x, y), tuple(pixel))

texture = Canvas((1000, 1000))
texture.randomize_pixels()
texture.save("static.png")
texture.show()
