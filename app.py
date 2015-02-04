from time import sleep

from tkinter import (
    Tk, Frame, Canvas, BOTH, RIGHT, LEFT, FLAT, PROJECTING, Button, Entry, Label,
)

from settings import (
    PROGRAM_TITLE, CANVAS_BACKGROUND_COLOR, CONTROL_PANEL_BACKGROUND_COLOR,
)


def args_for_f(func, *args, **kwargs):
    def wrap():
        func(*args, **kwargs)
    return wrap


class TransformationInputs(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        # self.create_elements()

    def create_elements(self):
        # inputs, button
        self.e = [Entry(self, width=4) for i in range(9) ]
        for elem in range(len(self.e)):
            self.e[elem].grid(row=elem // 3 + 1, column=elem % 3)
        self.update()
        self.label = Label(self, text='Tr.matica')
        self.label.grid(row=0, columnspan=3)
        self.button_frame = Frame(self, width=self.winfo_width(), height=25)
        self.button_frame.pack_propagate(0) #tell frame children not control its size!
        self.button = Button(self.button_frame, text='Tr')
        self.button_frame.grid(row=4, columnspan=3)
        self.button.pack(fill=BOTH, expand=1)


class Application(Frame):

    def __init__(self):
        master = Tk()
        Frame.__init__(self, master)
        master.title(PROGRAM_TITLE)

        self.window_geometry()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self,
            bg=CANVAS_BACKGROUND_COLOR,
            width=2*self.width/3,
            height=self.height,
            bd=0,
            highlightthickness=0,
            relief=FLAT
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.control_panel = Frame(
            self,
            bg=CONTROL_PANEL_BACKGROUND_COLOR,
            width=self.width/9
        )
        self.control_panel.pack(side=RIGHT, fill=BOTH, expand=1)

        self.button1 = Button(
            self.control_panel,
            text='prd',
            command=args_for_f(self.matrix_draw, 5)
        )
        self.button2 = Button(
            self.control_panel,
            text='ja som dlhy dext', 
            command=args_for_f(self.matrix_draw, 50)
        )
        self.button1.pack()
        self.button2.pack()

        self.trans = TransformationInputs(self.control_panel, bg='red')
        self.trans.pack()
        self.trans.create_elements()

    def window_geometry(self, width=780, height=420):
        self.width = width
        self.height = height
        self.master.minsize(width=width, height=height)
        x = (self.master.winfo_screenwidth() - width) / 2
        y = (self.master.winfo_screenheight() - height) / 2
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.pack(fill=BOTH, expand=1)

    def run(self):
        self.mainloop()

    def point(self, x, y):
        point_radius = 2
        self.canvas.create_line(
            x-point_radius,
            y,
            x+point_radius,
            y,
            fill='black',
            width=1,
            capstyle=PROJECTING,
        )
        self.canvas.create_line(
            x,
            y-point_radius,
            x,
            y+point_radius,
            fill='black',
            width=1,
            capstyle=PROJECTING,
        )

    def matrix_draw(self, N):
        pass
        # print(self.canvas['height'])
        # print(self.canvas['width'])
        # sleep(1)
        # self.config(width=900)
        # self.canvas.config(width=620)
        # print(self.canvas['height'])
        # print(self.canvas['width'])

        # startx = int(self.canvas['width']) / N
        # starty = int(self.canvas['height']) / N
        # for i in range(N):
        #     self.point(startx/2 + startx*i, starty)


if __name__ == '__main__':
    app = Application()
    app.run()
