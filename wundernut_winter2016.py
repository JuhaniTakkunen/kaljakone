from requests import request
from PIL import Image, ImageFilter
import numpy
from itertools import product
import operator
#Read image

directions = dict()

rgb_image = Image.open("wunder_image.png").convert("RGB")

array = numpy.array(rgb_image)


def draw_line(position, original_image, new_image, direction):
    pixel_color = array[original_image]

    new_direction = directions.get(pixel_color, default=direction)
    new_position = tuple(map(operator.add, position, new_direction))
    new_image[position] = (0, 0, 0)

    if new_position:
        return draw_line(
            position=new_position,
            original_image=original_image,
            new_image=new_image,
            direction=new_direction
        )
    else:
        return new_image


h, w, dum = array.shape
new_image2 = array.copy()

for pos in product(range(h), range(w)):
    pixel_color = array[pos]
    print(pos)
    print(pixel_color)

    if pixel_color == "start":
        draw_line(
            position=pos,
            original_image=array,
            new_image=new_image2,
            direction=directions.get(pixel_color)
        )

