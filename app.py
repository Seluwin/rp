from tkinter import (
    Tk, Frame, Canvas, BOTH, RIGHT, LEFT, FLAT, PROJECTING,
)

from settings import (
    PROGRAM_TITLE, CANVAS_BACKGROUND_COLOR, CONTROL_PANEL_BACKGROUND_COLOR,
)


class Application(Frame):

    def __init__(self):
        master = Tk()
        Frame.__init__(self, master)
        master.title(PROGRAM_TITLE)

        self.window_geometry()
        self.create_widgets()

        self.point(100, 100)

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
        self.canvas.pack(side=LEFT, fill=BOTH)
        
        self.control_panel = Frame(
            self,
            bg=CONTROL_PANEL_BACKGROUND_COLOR,
            width=self.width/3
        )
        self.control_panel.pack(side=RIGHT, fill=BOTH)

    def window_geometry(self, width=780, height=420):
        self.width = width
        self.height = height
        self.master.minsize(width=width, height=height)
        x = (self.master.winfo_screenwidth() - width) / 2
        y = (self.master.winfo_screenheight() - height) / 2
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.pack(fill=BOTH)

    def run(self):
        self.mainloop()

    def point(self, x, y):
        # default_point_radius = 5
        # self.canvas.create_oval(
        #     x - default_point_radius,
        #     y - default_point_radius,
        #     x + default_point_radius,
        #     y + default_point_radius,
        #     fill='black',
        #     width=0
        # )
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


if __name__ == '__main__':
    app = Application()
    app.run()
