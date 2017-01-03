from requests import request
from PIL import Image, ImageFilter
import numpy
import operator
import logging

RESULT_COLOR = (0, 255, 0)
ERROR_COLOR = (255, 0, 0)
logging.basicConfig()
logger = logging.getLogger(__name__)


def draw_line(position, original_image, new_image, direction):

    if direction is None:
        return

    new_image[position] = RESULT_COLOR
    new_position = tuple(map(operator.add, position, direction))
    try:
        new_direction_vector = get_direction(
            rgb=original_image[new_position],
            old_direction=direction
        )
    except IndexError:
        # end of image border
        # logger.warning(f"IndexError, line might continue over frame, pos: {position}")
        logger.warning("IndexError, line might continue over frame, pos: {position}".format(position=position))
        new_image[position] = ERROR_COLOR
        return
    if new_direction_vector is None:
        new_direction_vector = direction

    if new_direction_vector != (0, 0):
        return draw_line(
            position=new_position,
            original_image=original_image,
            new_image=new_image,
            direction=new_direction_vector
        )
    else:
        new_image[new_position] = RESULT_COLOR
        return


def get_direction(rgb, old_direction):
    """ Create new direction vector.

    Instructions:
        Ala piirtää ylöspäin, kun pikselin väri on 7, 84, 19.
        Ala piirtää vasemmalle, kun pikselin väri on 139, 57, 137.
        Lopeta viivan piirtäminen, kun pikselin väri on 51, 69, 169.
        Käänny oikealle, kun pikselin väri on 182, 149, 72.
        Käänny vasemmalle, kun pikselin väri on 123, 131, 154.

        source: Instructions: http://wunder.dog/secret-message-1

    :param rgb: tuple(123, 20, 254)
    :param old_direction: old direction vector, None if drawing starts
    :return: (direction string("up"), direction vector(0, -1)

    NOTE! direction vector is in y-x format, since PIL -> numpy array 'rotates' image.
    """

    directions = {
        (7, 84, 19): "north",
        (139, 57, 137): "east",
        (51, 69, 169): "stop",
        (182, 149, 72): "right",
        (123, 131, 154): "left"
    }

    rgb = tuple(rgb)
    if not old_direction:
        # Start drawing
        if directions.get(rgb, None) == "north":
            return -1, 0
        elif directions.get(rgb, None) == "east":
            return 0, -1
    else:
        # Continue drawing
        if directions.get(rgb, None) == "stop":
            return 0, 0
        elif directions.get(rgb, None) == "right":
            return old_direction[1], old_direction[0] * -1
        elif directions.get(rgb, None) == "left":
            return old_direction[1] * -1, old_direction[0]
    return None


def main():
    rgb_image = Image.open("wunder_image.png").convert("RGB")
    encrypted_array = numpy.asarray(rgb_image)
    secret_array = numpy.asarray(rgb_image.filter(ImageFilter.BLUR)).copy()  # Blur for aesthetics

    method = 4

    if method == 1:
        coordinates = numpy.ndindex(encrypted_array.shape[:2])
        list(map(lambda x: draw_line(
                position=x,
                original_image=encrypted_array,
                new_image=secret_array,
                direction=get_direction(encrypted_array[x], old_direction=None)
                ),
            coordinates
            ))

    if method == 2:
        coordinates = numpy.ndindex(encrypted_array.shape[:2])
        for coordinate in coordinates:
            color = encrypted_array[coordinate]
            direction_vector = get_direction(color, old_direction=None)
            if direction_vector:
                draw_line(
                    position=coordinate,
                    original_image=encrypted_array,
                    new_image=secret_array,
                    direction=direction_vector
                )

    if method == 3:

        def my_func(x): draw_line(
                position=x,
                original_image=encrypted_array,
                new_image=secret_array,
                direction=get_direction(encrypted_array[x], old_direction=None)
                )

        coordinates = numpy.ndindex(encrypted_array.shape[:2])
        [my_func(coordinate) for coordinate in coordinates]

    if method == 4:

        coordinates = numpy.ndindex(encrypted_array.shape[:2])
        [
            draw_line(
                position=coordinate,
                original_image=encrypted_array,
                new_image=secret_array,
                direction=get_direction(encrypted_array[coordinate], old_direction=None)
                )
            for coordinate in coordinates]

    Image.fromarray(secret_array).show()

if __name__ == "__main__":
    main()



