# SteamAutoActivation
Activate multiple steam product keys using a python script.

## Requirements
- Python 3 (Python 2 not tested)
- pyautogui (`pip install pyautogui`)
- Steam client installed

## Notes
- Only tested under Windows 10, Steam client language: Simplified Chinese
- Other languages or OS might work, but corresponding Steam client image should be added in `images` folder. See below for instructions.
- Pull requests for other languages and OS are welcome!

## Usage
1. Copy your keys to `keys.txt`. See `keys.txt` for example.
2. (If using other system or language, change `IMAGE_ROOT` in `activate_keys.py`. See below for instructions.)
3. If your taskbar is not on the bottom of screen, or its height is not 40, change `TASK_BAR_SIZE` in `activate_keys.py`.
4. Make sure Steam client is logged in, and Product Activation dialog is **NOT** opened. Make sure no IME (Input Method Editor) is activated.
5. `python activate_keys.py`
6. Do not move your mouse when the script is running.
7. Check console output and `logs` folder to see if activation is successful.

## Adding images for another language or OS
*Please make a pull request if you successfully added these images!*
- Prepare 6 PNG images:
  - `connecting.png`: When Steam is offline or network unreachable.
  - `empty.png`: Sometimes appears when Steam is offline. You may use the same `connecting.png` and `empty.png` if you don't think you would run into one of the situations.
  - `invalid.png`: When you use an invalid key like `11111-11111-11111`.
  - `owned.png`: When you use an already owned product key.
  - `success.png`: When you successfully added a product.
  - `too_many_times.png`: When you activate more than 6 invalid keys (including already activated) in a short time. This will cause your account temporarily unavaliable to activate products in 30~40 minutes.
  You can take screenshots using Alt-PrtScr to get these images. Make sure they have the same resolution (476x400 for windows client). 
- Crop the images:
  - Copy the 6 images under `images/xxx/xxx` folder
  - Change `IMAGE_ROOT` to `images/xxx/xxx` in both `activate_keys.py` and `crop_image.py`
  - Change `STEAM_BOX_SIZE` and `TARGET_SIZE` if needed. `STEAM_BOX_SIZE` should be equal to your PNG file resolution. The images will be cropped to `TARGET_SIZE` (top-left) and should contain no information about the current activating key. `TARGET_SIZE`=(476, 150) works fine for windows client.
- Maybe wait 30~40 minutes (because you generated `too_many_times.png`) and try `activate_keys.py`

## Variables you might want to change in `activate_keys.py`
- `STEAM_BOX_SIZE`: Steam activation dialog size. (width, height) in pixels.
- `TASK_BAR_SIZE`: Taskbar position and size. (left, top, right, bottom) in pixels. For example, if your taskbar is on the right size of screen and has a width of 80 pixels, set (0, 0, 80, 0).
- `OPERATION_INTERVAL`: Interval between two operations. Increase if your PC is slow.
- `CONNECTION_INTERVAL`: Time to wait for online activation. Increase if your network is slow.
- `TYPE_INTERVAL`: Interval between two virtual key events. Increase as needed.
- `KEY_FILE`: Filename of key file. Change if you want to use another key file.
- `IMAGE_ROOT`: Folder to image patterns for checking activation results.
- `LOG_ROOT`: Folder for logs. Each activation result will be screenshoted and saved here.
