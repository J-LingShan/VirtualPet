import tkinter as tk
from PIL import Image, ImageTk
import utils
import random


class Animation:
    def __init__(self, root, taskbar_height, characterName="momo", characterType="gif", new_size=(0, 0)):
        self.root = root
        self.taskbar_height = taskbar_height
        self.characterName = characterName
        self.characterType = characterType
        self.new_size = new_size

        self.img_width = 0
        self.img_height = 0

        self.screen_width, self.screen_height = utils.get_screen_size()

        self.status_num = 1
        self.current_frame = 0
        self.edge = 100

        self.rate = 150

        self.images = {}
        self.action_name = ['Rightward', 'Leftward', 'RunRight', 'RunLeft', 'Fall']

        self.action_frames = {}

        self.get_action_frame()

        self.frame_counts = [
            self.action_frames["Rightward"],
            self.action_frames["Leftward"],
            self.action_frames["RunRight"],
            self.action_frames["RunLeft"],
            self.action_frames["Fall"],
        ]  # 对应每个文件的帧数

        # 设置状态字典
        self.status = {
            0: ('Fall', 0),
            1: ('Rightward', 0),
            2: ('Leftward', 0),
            3: ('RunRight', 0),
            4: ('RunLeft', 0)
        }

        self.load_img()
        self.label = None
        self.label_show()
        self.start_x, self.start_y = int(self.screen_width / 2 - self.img_width / 2), 0

    def get_action_frame(self):
        
        if self.characterType == "gif":
            self.action_frames = {
                'Rightward': utils.get_gif_frame_count(f'./Character/{self.characterName}/Rightward.gif'),
                'Leftward': utils.get_gif_frame_count(f'./Character/{self.characterName}/Leftward.gif'),
                'RunRight': utils.get_gif_frame_count(f'./Character/{self.characterName}/RunRight.gif'),
                'RunLeft': utils.get_gif_frame_count(f'./Character/{self.characterName}/RunLeft.gif'),
                'Fall': utils.get_gif_frame_count(f'./Character/{self.characterName}/Fall.gif')

            }
            
        elif self.characterType == "png":
            self.action_frames = {
                'Rightward': utils.get_png_frame_count(f'./Character/{self.characterName}/Rightward'),
                'Leftward': utils.get_png_frame_count(f'./Character/{self.characterName}/Leftward'),
                'RunRight': utils.get_png_frame_count(f'./Character/{self.characterName}/RunRight'),
                'RunLeft': utils.get_png_frame_count(f'./Character/{self.characterName}/RunLeft'),
                'Fall': utils.get_png_frame_count(f'./Character/{self.characterName}/Fall')

            }
            

    def load_img(self):
        if self.characterType == "gif":
            self.load_animation_gif()

        elif self.characterType == "png":
            self.load_animation_png()

    def load_animation_gif(self):
        for file, count in zip(self.action_name, self.frame_counts):
            self.images[file] = []

            img_path = f'./Character/{self.characterName}/{file}.gif'
            image = utils.resize_image_gif(img_path, self.new_size)

            for i in range(len(image)):
                # print(type(image[i]))
                self.images[file].append(image[i])
                if self.img_width < image[i].width():
                    self.img_width = image[i].width()

                if self.img_height < image[i].height():
                    self.img_height = image[i].height()

    def load_animation_png(self):

        for action_type, count in zip(self.action_name, self.frame_counts):
            self.images[action_type] = []
            img_path = ''

            for i in range(count):
                img_path = f'./Character/{self.characterName}/{action_type}/{i}.png'
                try:
                    # print(img_path)
                    photo = utils.resize_image_png(img_path, self.new_size)
                    # print(type(photo))
                    # 添加到 images 字典中
                    self.images[action_type].append(photo)

                    if self.img_width < photo.width():
                        self.img_width = photo.width()

                    if self.img_height < photo.height():
                        self.img_height = photo.height()

                except Exception as e:
                    print(f"加载异常：{e}")

    def change_status(self):
        self.status_num = random.choice([1, 2, 3, 4])  # 随机选择一个新的状态
        self.root.after(random.randint(1000, 5000), self.change_status)

    def falling(self):
        if self.root.winfo_y() + self.img_height < self.screen_height - self.taskbar_height:
            self.status_num = 0
            self.start_y += 1
            self.root.geometry(f"{int(self.img_width)}x{int(self.img_height)}+{self.start_x}+{self.start_y}")
            self.root.after(1, self.falling)

        elif self.root.winfo_y() + self.img_height >= self.screen_height - self.taskbar_height and self.status_num == 0:
            self.status_num = 1

    def moving(self):
        if self.status_num == 3 and self.root.winfo_x() + self.img_width < self.screen_width - self.edge:
            self.start_x += 1  # 向右移动
            self.root.geometry(f"{int(self.img_width)}x{int(self.img_height)}+{self.start_x}+{self.start_y}")

        elif self.status_num == 3 and self.root.winfo_x() + self.img_width >= self.screen_width - self.edge:
            self.status_num = 1  # 达到屏幕边缘后设定状态为向右站立

        if self.status_num == 4 and self.root.winfo_x() > self.edge:
            self.start_x -= 1  # 向左移t动
            self.root.geometry(f"{int(self.img_width)}x{int(self.img_height)}+{self.start_x}+{self.start_y}")

        elif self.status_num == 4 and self.root.winfo_x() <= self.edge:
            self.status_num = 2  # 达到屏幕边缘后设定状态为向左站立
        self.root.after(3, self.moving)  # 每隔3毫秒重复执行

    def Action(self):  # 让动画生效
        frame_list, start_index = self.status[self.status_num]

        if self.current_frame < len(self.images[frame_list]):
            self.current_frame += 1  # 切换到下一个动画帧
        else:
            self.current_frame = start_index  # 重置到指定的起始帧

        action_type = self.images[frame_list]

        img_len = len(self.images[frame_list])  # 该动画一共帧数大小

        now_frames = self.current_frame % img_len  # 现在要使用的是第n帧的图片

        image_label = action_type[now_frames % img_len]

        # 更新现有的 Label 组件的图像
        self.label.config(image=image_label)
        self.root.after(self.rate, self.Action)  # 每隔指定毫秒重复执行

    def label_show(self):

        action_type = self.status[self.status_num][0]  # 动作类型
        initial_frame = self.status[self.status_num][1]  # 动作的初始帧(从该帧开始播放动作)

        self.label = tk.Label(self.root, image=self.images[action_type][initial_frame], bg='black', bd=0)
        self.label.pack()
