import os

import pyautogui as pt
from PIL import Image


def get_screen_size():
    return pt.size()


def get_gif_frame_count(gif_path):
    with Image.open(gif_path) as im:
        im.seek(0)
        img_frame_count = 1

        while True:
            try:
                im.seek(im.tell() + 1)  # 尝试获取下一帧
                img_frame_count += 1
            except EOFError:
                break  # 到达文件末尾，退出循环
        return img_frame_count  # 加上第一帧

def get_png_frame_count(pngDir_path):
    files = os.listdir(pngDir_path)

    img_frame_count = 0

    # 遍历文件列表
    for file in files:
        if file.endswith('.png'):
            img_frame_count += 1

    return img_frame_count


def zoom_images(photoImage_dir, zoom_factor):
    zoomed_images = []
    temp_dir = {}
    for action_type, images in photoImage_dir.items():
        zoomed_images = []
        for image in images:
            zoomed_image = image.zoom(zoom_factor, zoom_factor)
            zoomed_images.append(zoomed_image)
        temp_dir[action_type] = zoomed_images

    return temp_dir



if __name__ == "__main__":
    path = './CharacterGifs/momo/RunRight.gif'
    frame_count = get_gif_frame_count(path)
    print(f"gif帧数 {path}: {frame_count}")

