import multiprocessing
import tkinter
import PIL.Image
import PIL.ImageSequence
import PIL.ImageTk
import load
import you_get


class GifPlayer:
    """基于tkinter的轮播类"""

    def __init__(self, frame, gif_path):
        self.frame = frame
        self.gif = PIL.Image.open(gif_path)
        self.gif_list = []
        for image in PIL.ImageSequence.Iterator(self.gif):
            self.gif_list.append(PIL.ImageTk.PhotoImage(image))

        self.label = tkinter.Label(self.frame)
        self.label.pack()
        self.git_index = 0
        self.playerGif()

    def playerGif(self):
        self.label.config(image=self.gif_list[self.git_index])
        self.git_index = (self.git_index + 1) % len(self.gif_list)
        self.frame.after(50, self.playerGif)


def center_window(window, width, height):
    """界面实现屏幕居中"""
    # 获取屏幕尺寸
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算居中坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")
    return True


class App:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("b站视频下载工具(测试版)")
        icon = tkinter.PhotoImage(file="image/doro.ico")
        self.root.iconphoto(True, icon)
        center_window(self.root, 400, 300)
        self.frame = self.frame_main(self._entry_main)
        self.frame.pack(expand=True)
        self.root.mainloop()

    def frame_error(self, _entry_function):
        """错误页面"""
        frame = tkinter.Frame(self.root)
        label = tkinter.Label(frame, text="好像哪里出错了,我们重试一下吧！")
        label.pack()
        GifPlayer(frame, "image/zhidiandror.gif")

        def _entry():
            _entry_function()

        submit_button = tkinter.Button(frame, text="重试", command=_entry)
        submit_button.pack()
        return frame

    def _entry_error(self):
        self._entry_(self.frame, self.frame_main, self._entry_main)

    def frame_main(self, _entry_function):
        """主页面"""
        frame = tkinter.Frame(self.root)
        label = tkinter.Label(frame, text="请输入视频对应的bv编号")
        label.pack()
        entry = tkinter.Entry(frame)
        entry.pack()

        def _entry():
            input_text = entry.get()
            if input_text == "":
                self.frame.pack_forget()
                self.frame = self._frame_noll(self._event_noll)
                self.frame.pack(expand=True)
            else:
                _entry_function(input_text)

        submit_button = tkinter.Button(frame, text="下载", command=_entry)
        submit_button.pack()
        return frame

    @staticmethod
    def _entry_(frame, _frame, _entry_):
        """
        隐藏原页面，显示新页面
        :param frame: 原页面
        :param _frame: 新页面调用函数
        :param _entry_: 新页面控件事件函数
        :return:
        """
        frame.pack_forget()
        frame = _frame(_entry_)
        frame.pack()

    def _event_noll(self):
        self.frame.pack_forget()
        self.frame = self.frame_main(self._entry_main)
        self.frame.pack(expand=True)

    def _frame_noll(self, _entry_function):
        """输入空值"""
        frame = tkinter.Frame(self.root)
        label = tkinter.Label(frame, text="你什么都没有输入哦")
        label.pack()
        GifPlayer(frame, "image/huayadoro.gif")

        def _entry():
            _entry_function()

        button = tkinter.Button(frame, text="我错啦，再也不敢啦", command=_entry)
        button.pack()
        return frame

    def frame_loading(self):
        """下载页面"""
        frame = tkinter.Frame(self.root)
        label = tkinter.Label(frame, text="视频下载中...")
        label.pack()
        GifPlayer(frame, "image/doroturn.gif")
        return frame

    def frame_loaded(self, _entry_function):
        """完成页面"""
        frame = tkinter.Frame(self.root)
        label = tkinter.Label(frame, text="下载完成!请在当前路径从如下的文件夹内找到视频文件")
        label.pack()
        GifPlayer(frame, "image/loading.png")

        def _entry():
            _entry_function()

        submit_button = tkinter.Button(frame, text="返回", command=_entry)
        submit_button.pack()
        return frame

    @staticmethod
    def loadWorkMul(_event, _bv):
        load.load_main(bv=_bv)
        _event.set()

    def _entry_main(self, input_text):
        event = multiprocessing.Event()
        p1 = multiprocessing.Process(target=self.loadWorkMul, args=(event, input_text,))
        p1.start()
        self.frame.pack_forget()
        self.frame = self.frame_loading()
        self.frame.pack(expand=True)

        self.root.after(100, self._chick_event, event, p1)

    def _chick_event(self, event, p1):
        if event.is_set():
            p1.join()
            self.frame.pack_forget()
            self.frame = self.frame_loaded(self._entry_loaded)
            self.frame.pack(expand=True)
        else:
            self.root.after(100, self._chick_event, event, p1)

    def _entry_loaded(self):
        self.frame.pack_forget()
        self.frame = self.frame_main(self._entry_main)
        self.frame.pack(expand=True)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = App()
