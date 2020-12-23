from PIL import Image
import typing
import random
from math import sqrt

class Canvas:
    def __init__(self, open_image: str=None, size: tuple=(64, 64), color: tuple=(255, 255, 255)):
        # open_image is used to open a present image, size and tuple are used to generate one
        if open_image != None:
            self.canvas = Image.open("image.jpg")
            self.canvas = self.canvas.convert("RGBA")
        else:
            self.canvas = Image.new(mode="RGBA", size=size, color=color)
        self.size = self.canvas.size
        self.pixel_count = size[0] * size[1]

    def show(self) -> None:
        """QOL shortcut to Object.canvas.show"""
        self.canvas.show()

    def save(self, name: str) -> None:
        """QOL shortcut to Object.canvas.save"""
        self.canvas.save("output/" + name, format="png")

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

    def distance_from(self, start: tuple, end: tuple) -> float:
        """Returns the distance from a coordinate in pixels"""
        dy = abs(end[1] - start[1])
        dx = abs(end[0] - start[0])
        hypothenuse = round(sqrt(dy ** 2 + dx ** 2))
        return hypothenuse

    def max_distance(self, start: tuple) -> tuple:
        """Returns greatest difference between any pixel and the given pixel."""
        max_x = self.size[0] - 1
        max_y = self.size[1] - 1
        corners = [(0, 0), (0, max_y), (max_x, 0), (max_x, max_y)]
        distance_from_corners = []
        for coord in corners:
            distance_from_corners.append(self.distance_from(start, coord))
        distance_from_corners.sort(reverse=True)
        return distance_from_corners[0]

    def to_max_multiple(self, distance: int, max_distance:int) -> float:
        """Determines a multiple for image manipulation based on distance between two points."""
        return(round(distance/max_distance, 5))

    def randomize_pixels_abs(self) -> None:
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

    def randomize_pixels(self, start: tuple=(0, 0)) -> None:
        """Randomizes the color and alpha of each pixel based on distance between each pixel and a given pixel."""
        max_dist = self.max_distance(start)
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pixel = list(self.canvas.getpixel((x, y)))
                dist_from_start = self.distance_from(start, (x, y))
                mult = self.to_max_multiple(dist_from_start, max_dist)
                for i in range(4):
                    max_add = int((255-pixel[i])*mult)
                    max_sub = int((-pixel[i])*mult)
                    change = random.choice([max_sub, max_add])
                    pixel[i] += change
                self.canvas.putpixel((x, y), tuple(pixel))

texture = Canvas(open_image="image.jpg")
texture.randomize_pixels()
texture.save("static_overlay_around_point.png")