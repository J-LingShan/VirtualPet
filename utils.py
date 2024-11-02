import os

import pyautogui as pt
from PIL import Image, ImageTk


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


def resize_image_png(image_path, new_size):
    with Image.open(image_path) as im:
        if new_size != (0, 0):
            im_resized = im.resize(new_size, resample=Image.BICUBIC)
            # im_resized = im.resize(new_size, resample=Image.BILINEAR)
            # im_resized = im.resize(new_size, resample=Image.LANCZOS)

        else:
            im_resized = im

        return ImageTk.PhotoImage(im_resized)


def resize_image_gif(image_path, new_size):
    im = Image.open(image_path)
    num_frames = im.n_frames
    frames_tk = []

    for i in range(num_frames):
        im.seek(i)

        if new_size != (0, 0):
            # 缩放当前帧
            resized_frame = im.resize(new_size, resample=Image.BICUBIC)
        else:
            # 图像不进行放缩操作
            resized_frame = im

        photo_tk = ImageTk.PhotoImage(resized_frame)
        frames_tk.append(photo_tk)

    return frames_tk


if __name__ == "__main__":
    path = './CharacterGifs/momo/RunRight.gif'
    frame_count = get_gif_frame_count(path)
    print(f"gif帧数 {path}: {frame_count}")

