import os.path
import sys

from yangke.common.win.win_x64 import (get_all_window, find_window, capture_pic_undecorated, post_key, do_click,
                                       get_size_of_window)
from yangke.objDetect.ocr import ocr
from yangke.base import show_pic
from yangke.common.config import logger


class Step:
    def __init__(self, op, target, judge, condition):
        self.op = op
        self.target: Position | str = target  # 按键操作则为键名，鼠标时间则为鼠标点击位置
        self.judge = judge
        self.condition: "Exist" = condition

    def _action(self, win_frame: "Frame"):
        if self.op == "press":
            if "+" not in self.target:  # 单独按键
                post_key(win_frame.window, self.target)
            else:
                pass
        elif self.op == "left-click":
            if isinstance(self.target, Position):
                x, y = self.target.get_point(win_frame)
                do_click(x, y, win_frame.window)

    def do(self, win_frame: "Frame"):
        logger.debug(f"执行步骤")
        self._action(win_frame)
        satisfied = self.condition.satisfied(win_frame)
        while not satisfied:  # 如果结束条件不满足，则继续执行本步骤定义的操作
            self._action(win_frame)
        return True

    def __str__(self):
        return f"{self.op} {self.target} {self.judge} {self.condition}"


class Steps:
    def __init__(self, steps):
        """
        定义游戏内操作的步骤
        """
        self.steps = steps

    def run(self, win_frame):
        """
        逐步执行Steps对象中记录的步骤
        """
        last_step: Step | None = None
        for step in self.steps:
            step: Step = step
            success = step.do(win_frame)  # 执行步骤，可能执行失败，如点击某个按钮但画面上找不到就会失败
            if not success and last_step is not None:  # 如果执行失败，就尝试再次执行上一个步骤
                last_step.do(win_frame)
                success = step.do(win_frame)

            if success:  # 如果当前步骤执行结束，就记录当前步骤
                last_step = step


class Frame:
    def __init__(self, title, game_path=None):
        """
        游戏图像识别框架

        :@param title: 游戏窗口标题，为标题的子字符串，但需要唯一确定的窗口
        :@param game_path: 游戏文件路径，如果不存在游戏窗口，则启动该可执行文件
        """
        self.set_window_size_steps = None  # 设置窗口尺寸的步骤
        self.title = title
        self.snapshot = None
        self.window = find_window(title, exact=False)
        if isinstance(self.window, dict) and len(self.window) == 1:
            _ = list(self.window.keys())[0]
            self.window_title = self.window[_]
            self.window = _
        else:
            logger.error(f"未找到或找到多个包含{title}的窗口，目前不支持这种情况！")
            sys.exit()
        self.window_size = get_size_of_window(self.window, True)  # 不包括标题栏的大小

    def define_set_window_size(self, steps: Steps):
        self.set_window_size_steps = steps

    def capture_window(self, x1=0, y1=0, x2=0, y2=0):
        self.snapshot = capture_pic_undecorated(self.window)
        return self.snapshot

    def set_window_size(self, width=None, height=None):
        """
        将游戏窗口设置为指定大小
        @return:
        """
        # show_pic(self.capture_window())
        self.run_steps(self.set_window_size_steps)

    def run_steps(self, steps: Steps):
        steps.run(self)

    def get_text(self, region=None):
        if region is None:
            self.capture_window()
        else:
            self.capture_window(*region)
        return ocr(self.snapshot, paragraph=True)

    def get_text_position(self, text, region=None):
        """
        获取给定文字在画面上的位置
        """
        if region is not None:
            pic = self.capture_window(*region)
        else:
            pic = self.capture_window()

    def get_window_size(self, refresh=False):
        if refresh:
            self.window_size = get_size_of_window(self.window)
        return self.window_size


class Exist:
    def __init__(self, type_="text", value: str | list = "查找的文字或列表", op="or", region: tuple | None = None):
        """
        判断画面中是否存在某个元素的类
        @param type_: 元素的类型
        @param value: 元素的值的列表
        @param op: 元素值列表存在于画面中的条件是 与还是或
        @param region: 可以通过该参数指定画面区域
        """
        self.type_ = type_
        self.value = value if isinstance(value, list) else [value]
        self.op = op
        self.region = region

    def satisfied(self, win_frame: "Frame"):
        """
        画面中存在某个元素的条件满足

        @param win_frame:
        @return:
        """
        if self.type_ == "text":
            text = win_frame.get_text(self.region)
            if self.op == "or":
                for v in self.value:
                    if v in text:
                        return True
                return False
            else:
                for v in self.value:
                    if v not in text:
                        return False
                return True


class Align:
    def __init__(self, x_offset, y_offset=0):
        self.dx = x_offset
        self.dy = y_offset


class Position:
    def __init__(self, value, align: str | Align = 'center', region=None):
        """
        定义画面上的位置对象

        @param value:
        @param align:
        """
        self.value = value
        self.region = region

    def get_point(self, win_frame: "Frame"):
        """
        获取位置在画面上的相对坐标
        @param win_frame:
        @return:
        """
        if isinstance(self.value, str):
            pos = win_frame.get_text_position(self.value)
            return pos
        else:
            return None


class Region:
    def __init__(self, win_frame: "Frame"):
        """
        定义窗口中的某个区域，通过该类可以获取(x,y,w,h)这种类型的相对区域坐标
        """
        self.frame = win_frame
        self.width_window, self.height_window = win_frame.get_window_size()

    def get_region(self, align="center", width_child=0, height_child=0):
        """
        根据传入的区域定义，获取区域的数字范围，例如：
        region.get_region("center", 100, 100)  # 表示窗口中间100*100范围的(x,y,w,h)定义
        """
        if width_child == 0:  # 如果不指定区域的宽和高，则默认宽和高等于窗口的宽和高
            width_child = self.width_window
        if height_child == 0:
            height_child = self.height_window
        if align == "center":
            left_pad = int((self.width_window - width_child) / 2)
            top_pad = int((self.height_window - height_child) / 2)
        elif align == "left":
            left_pad = 0
            top_pad = int((self.height_window - height_child) / 2)
        elif align == "right":
            left_pad = self.width_window - width_child
            top_pad = int((self.height_window - height_child) / 2)
        elif align == "top":
            left_pad = int((self.width_window - width_child) / 2)
            top_pad = 0
        elif align == "bottom":
            left_pad = int((self.width_window - width_child) / 2)
            top_pad = self.height_window - height_child
        else:
            left_pad = 0
            top_pad = 0
        return left_pad, top_pad, width_child, height_child


if __name__ == "__main__":
    # logger.debug(ocr("temp.png", paragraph=False))
    # frame = Frame('天谕-无束缚3D')
    # frame = Frame('炎火前哨, 狄澜')
    frame = Frame('炎火前哨, 卖萌的萝莉酱')
    r = Region(frame)
    steps_1 = Steps(
        steps=[
            # 按Esc键，直到窗口中心区域(317, 532)大小范围内出现文字"游戏设置"
            Step("press", "escape", "until", Exist(value="游戏设置", region=r.get_region("center", 317, 532))),

            # 单击中心区域的【游戏设置】，直到中心区域(874, 609)出现【分辨率】
            Step("left-click", Position("游戏设置", region=r.get_region("center", 874, 609)), "until",
                 Exist(value="分辨率", region=r.get_region("center", 874, 609))),

            # 单机
            Step("left-click", Position("分辨率", align=Align(20)), "until", Exist())
        ])
    frame.define_set_window_size(steps=steps_1)
    frame.set_window_size()
    # frame.capture_window()
    # logger.debug(frame.get_text())
