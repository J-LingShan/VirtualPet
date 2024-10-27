import tkinter as tk
from animation import Animation
import gc


class GUI:
    def __init__(self):
        self.root = tk.Tk()

        self.action = Animation(self.root, taskbar_height=0, characterName="yoyo", characterType="png", zoom_factor=2)
        # self.action = Animation(self.root, taskbar_height=0)
        # self.action = Animation(self.root, taskbar_height=0, characterName="kuku", characterType="png")

        self.root.geometry(f"{int(self.action.img_width)}x{int(self.action.img_height)}+{self.action.start_x}+{self.action.start_y}")
        self.root.overrideredirect(True)
        self.root.config(bg="black")
        self.root.wm_attributes('-transparentcolor', 'black')
        self.root.wm_attributes('-topmost', True)

        self.action.change_status()
        self.action.falling()
        self.action.moving()
        self.action.Action()
        gc.enable()  # 启用垃圾回收
        self.root.mainloop()
