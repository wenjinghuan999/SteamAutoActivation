
import pyautogui
import os
import sys
import time
from PIL import Image, ImageChops
from find_keys import find_keys

STEAM_BOX_SIZE = (476, 400)    # Steam activation dialog size
TASK_BAR_SIZE = (0, 0, 0, 40)  # Task bar size and position (left, top, right, bottom)

OPERATION_INTERVAL = 0.5
CONNECTION_INTERVAL = 1
TYPE_INTERVAL = 0.01

KEY_FILE = 'keys.txt'
IMAGE_ROOT = 'images/windows/cn/'
LOG_ROOT = 'logs/'


def get_result_image():
    image = pyautogui.screenshot()
    box = (TASK_BAR_SIZE[0], TASK_BAR_SIZE[1], image.width - TASK_BAR_SIZE[0] - TASK_BAR_SIZE[2],
           image.height - TASK_BAR_SIZE[1] - TASK_BAR_SIZE[3])
    image = image.crop(box)
    box = ((image.width - STEAM_BOX_SIZE[0]) / 2, (image.height - STEAM_BOX_SIZE[1]) / 2,
           (image.width + STEAM_BOX_SIZE[0]) / 2, (image.height + STEAM_BOX_SIZE[1]) / 2)
    image = image.crop(box)
    return image


def activate_key(key):
    os.startfile('steam://open/activateproduct')
    time.sleep(OPERATION_INTERVAL)
    pyautogui.press('enter')
    time.sleep(OPERATION_INTERVAL)
    pyautogui.press('enter')
    time.sleep(OPERATION_INTERVAL)
    pyautogui.typewrite(key, interval=TYPE_INTERVAL)
    pyautogui.press('enter')
    time.sleep(CONNECTION_INTERVAL)
    image = get_result_image()
    image.save(os.path.join(LOG_ROOT, key + ' ' + time.strftime("%Y-%m-%d %H%M%S", time.gmtime()) + '.png'))
    pyautogui.press('enter')
    time.sleep(OPERATION_INTERVAL)
    pyautogui.press('esc')
    return image


def image_equal(im1, im2):
    if im1 is None or im2 is None:
        return False
    return ImageChops.difference(im1, im2).getbbox() is None


def image_contain(image, sub_image):
    if image is None or sub_image is None:
        return False
    return image_equal(image.crop((0, 0, sub_image.width, sub_image.height)), sub_image)


def get_game_name(image):
    pass


def activate_keys(keys):
    too_many_times_image = Image.open(os.path.join(IMAGE_ROOT, 'too_many_times.png'))
    empty_image = Image.open(os.path.join(IMAGE_ROOT, 'empty.png'))
    connecting_image = Image.open(os.path.join(IMAGE_ROOT, 'connecting.png'))
    invalid_image = Image.open(os.path.join(IMAGE_ROOT, 'invalid.png'))
    owned_image = Image.open(os.path.join(IMAGE_ROOT, 'owned.png'))
    success_image = Image.open(os.path.join(IMAGE_ROOT, 'success.png'))
    counts = {'activated': 0, 'owned': 0, 'invalid': 0, 'unknown': 0}
    for key in keys:
        image = activate_key(key)
        if image_equal(image, too_many_times_image):
            print('Too many activation attempts, stop activating. Please retry 30~40 minutes later.')
            sys.exit()
        elif image_equal(image, empty_image) or image_equal(image, connecting_image):
            print('It seems your network is not connected or is too slow. Consider increasing CONNECTION_INTERVAL.')
            sys.exit()
        elif image_equal(image, invalid_image):
            print(key, 'is invalid')
            counts['invalid'] += 1
        elif image_equal(image, owned_image):
            print(key, 'is already owned')
            counts['owned'] += 1
        elif image_equal(image, success_image):
            print(key, 'is successfully activated')
            counts['activated'] += 1
        else:
            print(key, 'state unknown. Please check log to verify.')
            counts['unknown'] += 1
    return counts


def main():
    if not os.path.exists(IMAGE_ROOT):
        print('Path does not exist:', IMAGE_ROOT)
    if not os.path.exists(LOG_ROOT):
        os.makedirs(LOG_ROOT, exist_ok=True)
    pyautogui.moveTo(0, 1)
    keys = find_keys(KEY_FILE)
    print(len(keys), 'keys in total.')
    if 'AAAAA-AAAAA-AAAAA' in keys:
        print('Please change keys.txt first.\n'
              'Note that Steam will temporary lock your activation after 6 invalid tries.\n'
              'If you want to try out this script, use one or two keys a time and rest 30~40 minutes before next try.')
        sys.exit()
    counts = activate_keys(keys)
    print(counts)

if __name__ == '__main__':
    main()
