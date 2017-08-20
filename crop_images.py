
import os
import sys
from PIL import Image

IMAGE_ROOT = 'images/windows/cn/'
IMAGES = ['empty.png', 'connecting.png', 'invalid.png', 'owned.png', 'success.png', 'too_many_times.png']

STEAM_BOX_SIZE = (476, 400)   # Steam activation dialog size
TARGET_SIZE = (476, 150)      # Cropped size

if __name__ == '__main__':
    for filename in IMAGES:
        image = Image.open(os.path.join(IMAGE_ROOT, filename))
        if image.width == TARGET_SIZE[0] and image.height == TARGET_SIZE[1]:
            print(filename, 'already cropped.')
        elif image.width != STEAM_BOX_SIZE[0] or image.height != STEAM_BOX_SIZE[1]:
            print(filename, 'does not fit steam box size, exiting.')
            sys.exit()
        else:
            image = image.convert('RGB').crop((0, 0, TARGET_SIZE[0], TARGET_SIZE[1]))
            image.save(os.path.join(IMAGE_ROOT, filename))
            print(filename, 'successfully cropped.')
