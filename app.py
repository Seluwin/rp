from time import sleep

from tkinter import (
    Tk, Frame, Canvas, BOTH, X, Y, RIGHT, LEFT, FLAT, PROJECTING, Button,
    Entry, Label, W, E, ALL,
)

from settings import (
    PROGRAM_TITLE, CANVAS_BACKGROUND_COLOR, CONTROL_PANEL_BACKGROUND_COLOR,
)


def args_for_f(func, *args, **kwargs):
    def wrap():
        func(*args, **kwargs)
    return wrap


class FloatEntry(Entry):
    def __init__(self, master, value=0.0, **kwargs):
        Entry.__init__(self, master, **kwargs)
        self.insert(0, str(value))
        vcmd = (self.register(self._is_valid), '%s', '%P')
        self.configure(vcmd=vcmd, validate='all')
        self._value = float(value)

    @property
    def get(self):
        val = Entry.get(self)
        if val == '':
            return self._value
        return float(val)

    @property
    def value(self):
        return float(self.get)

    def _is_valid(self, old_value, new_value):
        if new_value == '':
            return True
        try:
            self._value = float(new_value)
            return True
        except:
            return False


class TransformationInputs(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        # self.create_elements()

    def create_elements(self):
        # inputs, button
        self.e = []
        for i in range(9):
            if i in (0,4,8):
                self.e.append( FloatEntry(self, width=4, value=1.0))
            else:
                self.e.append( FloatEntry(self, width=4))

        for elem in range(len(self.e)):
            self.e[elem].grid(row=elem // 3 + 1, column=elem % 3)
        self.update()
        self.label = Label(self, text='Tr.matica')
        self.label.grid(row=0, columnspan=3, sticky=W+E)
        self.button_frame = Frame(self, width=self.winfo_width(), height=25)
        self.button_frame.pack_propagate(0) #tell frame children not control its size!
        self.button = Button(self.button_frame, text='Transformuj')
        self.button_frame.grid(row=4, columnspan=3)
        self.button.pack(fill=BOTH, expand=1)


def virtual_to_real_xy(vx ,vy, canvas, N=12):
    x , y = (canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    real_width, real_height = x*2, y*2
    offset = min(x / N, y / N)
    real_x = (real_width / 2) + vx * offset
    real_y = (real_height / 2) - (vy * offset)
    return (real_x, real_y)


class Point():

    def __init__(self, vx, vy, canv, visible=True):
        self.x, self.y = vx, vy
        self.visible = visible
        self.canvas = canv

    def draw(self):
        if not self.visible:
            return
        x, y = virtual_to_real_xy(self.x, self.y, self.canvas, 8)
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


class Application(Frame):

    def __init__(self):
        master = Tk()
        Frame.__init__(self, master)
        master.title(PROGRAM_TITLE)
        self.nuber_of_points = 12
        self.window_geometry()
        self.create_widgets()

    def create_points(self, num_x, num_y):
        self.points = []
        for i in range(1, num_x + 1):
            for j in range(1, num_y + 1):
                self.points.append(Point(i, j, self.canvas))

    def create_widgets(self):
        self.canvas = Canvas(
            self,
            bg=CANVAS_BACKGROUND_COLOR,
            # width=2*self.width/3,
            # height=self.height,
            bd=0,
            highlightthickness=0,
            relief=FLAT
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.control_panel = Frame(
            self,
            bg=CONTROL_PANEL_BACKGROUND_COLOR,
            width=500,
            #width=self.width/9
        )
        self.control_panel.pack(side=LEFT, fill=Y, expand=0)

        self.ac = Frame(
            self.control_panel,
            bg=CONTROL_PANEL_BACKGROUND_COLOR,
            width=150,
            #width=self.width/9
        )
        self.ac.pack(fill=X, expand=0)

        self.button1 = Button(
            self.control_panel,
            text='Reset',
            command=self.reset
        )
        self.button1.pack()

        self.trans = TransformationInputs(
                self.control_panel, 
                bg=CONTROL_PANEL_BACKGROUND_COLOR
                )
        self.trans.pack()
        self.trans.create_elements()
        self.create_points(8,5)

    def reset(self):
        self.canvas.delete(ALL)
        self.draw_axes()
                #self.point(x,y)
        for pnt in self.points:
            pnt.draw()

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

    def draw_axes(self, col='black', points=8):
        x , y = (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2)
        #mid = x,y
        length = max(x, y)
        #draw x
        self.canvas.create_line(
            x - length,
            y,
            x + length,
            y,
            fill=col,
            width=1,
            capstyle=PROJECTING,
        )
        #draw y
        self.canvas.create_line(
            x,
            y - length,
            x,
            y + length,
            fill=col,
            width=1,
            capstyle=PROJECTING,
        )
        # markings on axes
        N = points
        spacing = min(x,y) / N
        for i in range(1,N):
            self.canvas.create_line(
                x + spacing*i,
                y - 2,
                x + spacing*i,
                y + 2,
                fill=col
            )
            self.canvas.create_line(
                x - spacing*i,
                y - 2,
                x - spacing*i,
                y + 2,
                fill=col
            )
            self.canvas.create_line(
                x - 2,
                y + spacing*i,
                x + 2,
                y + spacing*i,
                fill=col
            )
            self.canvas.create_line(
                x - 2,
                y - spacing*i,
                x + 2,
                y - spacing*i,
                fill=col
            )
            self.canvas.create_text(x + spacing*i, y + 7, text='%d'% (i))
            self.canvas.create_text(x - spacing*i, y + 7, text='%d'% (-i))
            self.canvas.create_text(x - 6, y + spacing*i, text='%d'% (-i))
            self.canvas.create_text(x - 6, y - spacing*i, text='%d'% (i))
        self.canvas.create_text(x + 7, 25, text='y')
        self.canvas.create_text(x*2 - 25, y + 7, text='x')

    def draw_matrix(self, N):
        pass

if __name__ == '__main__':
    app = Application()
    app.run()
