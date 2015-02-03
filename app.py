from tkinter import Tk, Frame, Canvas, BOTH, RIGHT, LEFT, FLAT

from settings import PROGRAM_TITLE, CANVAS_BACKGROUND_COLOR


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
        self.canvas.pack(side=LEFT, fill=BOTH)
        
        self.control_panel = Frame(self, bg='black', width=self.width/3)
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


if __name__ == '__main__':
    app = Application()
    app.run()
