from time import sleep

from tkinter import (
    Tk, Frame, Canvas, BOTH, X, Y, RIGHT, LEFT, FLAT, PROJECTING, Button,
    Entry, Label, W, E, ALL,
)

from settings import (
    PROGRAM_TITLE, CANVAS_BACKGROUND_COLOR, CONTROL_PANEL_BACKGROUND_COLOR,
    PNTS_ON_X, PNTS_ON_Y
)

from matica import Matica


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
        if new_value in ('', '-'):
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

    def get_matrix(self):
        res, tmp = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], []
        for i in range(len(self.e)):
            res[i % 3][i // 3] = self.e[i].get
        return Matica(res)

    def create_elements(self):
        # inputs, button
        self.e = []
        self.point_entry = []
        for i in range(2):
            self.point_entry.append(FloatEntry(self,width=4))

        for i in range(9):
            if i in (0,4,8):
                self.e.append( FloatEntry(self, width=4, value=1.0))
            else:
                self.e.append( FloatEntry(self, width=4))

        for elem in range(len(self.e)):
            self.e[elem].grid(row=elem // 3 + 1, column=elem % 3)

        for i,elem in enumerate(self.point_entry):
            print(i,elem)
            elem.grid(row=5, column=i)

        self.update()
        self.button_add_point_frame = Frame(
            self, 
            width=self.winfo_width()/3,
            height=20
            )
        self.button_add_point_frame.pack_propagate(0)
        self.button_add_point = Button(
            self.button_add_point_frame,
            text='+',
            command=lambda: self.master.master.add_point(
                self.point_entry[0].get,
                self.point_entry[1].get
            )
        )
        self.label = Label(self, text='Tr.matica')
        self.label.grid(row=0, columnspan=3, sticky=W+E)
 
        self.button_frame = Frame(self, width=self.winfo_width(), height=25)
        self.button_frame.pack_propagate(0) #tell frame children not control its size!
        self.button = Button(
            self.button_frame,
            text='Transformuj',
            command=  self.master.master.make_transform)

        self.button_add_point_frame.grid(row=5, column=2)
        self.button_add_point.pack(fill=BOTH, expand=1)
        self.button_frame.grid(row=4, columnspan=3)
        self.button.pack(fill=BOTH, expand=1)


def virtual_to_real_xy(vx ,vy, canvas, N=12):
    x , y = (canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    real_width, real_height = x*2, y*2
    offset = min(x / N, y / N)
    real_x = (real_width / 2) + vx * offset
    real_y = (real_height / 2) - (vy * offset)
    return (real_x, real_y)


class Point(Matica):

    def __init__(self, vx, vy, canv, visible=True):
        Matica.__init__(self,[[vx], [vy], [1]])
        self.x, self.y = vx, vy
        self.visible = visible
        self.canvas = canv

    def __mul__(self, matrix):
        m = Matica.__mul__(self,matrix)
        self.x = m[0][0]
        self.y = m[0][1]
        self.matrix = m.matrix

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

class Points():
    def __init__(self):
        pass

class Application(Frame):

    def __init__(self):
        master = Tk()
        Frame.__init__(self, master)
        master.title(PROGRAM_TITLE)
        self.nuber_of_points = 12
        self.points = []
        self.window_geometry()
        self.create_widgets()
        self.redraw()

    def create_points(self, num_x, num_y):
        if num_x % 2 == 0:
            pass
        for i in range( -num_x//2, num_x//2 ):
            for j in range( -num_y//2, num_y//2):
                self.points.append(Point(i, j, self.canvas))

    def add_point(self, x, y):
        self.points.append(
            Point(x, y, self.canvas)
        )
        self.redraw()

    def make_transform(self):
        tr_matrix = self.trans.get_matrix()
        for pnt in self.points:
            p = tr_matrix * pnt
            pnt.matrix = p.matrix
            pnt.x = p.matrix[0][0]
            pnt.y = p.matrix[1][0]
        self.redraw()
        #print("sucess")

    def create_widgets(self):
        self.canvas = Canvas(
            self,
            bg=CANVAS_BACKGROUND_COLOR,
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

        self.cp_wrap = Frame(
            self.control_panel,
            bg=CONTROL_PANEL_BACKGROUND_COLOR,
            width=150,
            #width=self.width/9
        )
        self.cp_wrap.pack(fill=X, expand=0)

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

    def reset(self):
        self.canvas.delete(ALL)
        if self.points == []:
            self.create_points(PNTS_ON_X, PNTS_ON_Y)
        else:
            self.points = []
        self.redraw()

    def redraw(self):
        self.canvas.delete(ALL)
        self.draw_edge_axes()
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

    def draw_edge_axes(self, col='black', points=8):
        mx , my = (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2)
        x, y = mx, my
        bot_y = my * 2 - 20
        length = max(x, y)
        len_x, len_y = 2*x, 2*y
        OFFSET = 25
        #draw x
        self.canvas.create_line(
            x - length,
            len_y - OFFSET,
            x + length,
            len_y - OFFSET,
            fill=col,
            width=1,
            capstyle=PROJECTING,
        )
        #draw y
        self.canvas.create_line(
            OFFSET,
            y - length,
            OFFSET,
            y + length,
            fill=col,
            width=1,
            capstyle=PROJECTING,
        )
        # markings on axes
        N = points
        spacing = min(x,y) / N
        for i in range(-N, N + 1):
            print(i)
            #mark x line
            self.canvas.create_line(
                x + spacing*i,
                len_y - OFFSET - 2,
                x + spacing*i,
                len_y - OFFSET + 2,
                fill=col
            )
            #mark y line
            self.canvas.create_line(
                OFFSET - 2,
                y + spacing*i,
                OFFSET + 2,
                y + spacing*i,
                fill=col
            )
            #write numbers on axes
            self.canvas.create_text(x + spacing*i, len_y - OFFSET + 8, text='%d'% (i))
            self.canvas.create_text(OFFSET - 7, y + spacing*i, text='%d'% (-i))
        self.canvas.create_text(OFFSET + 7, 25, text='y')
        self.canvas.create_text(x*2 - 25, y*2 - OFFSET + 7, text='x')

    def draw_mid_axes(self, col='black', points=8):
        mx , my = (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2)
        #mid = x,y
        x, y = mx, my
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


if __name__ == '__main__':
    app = Application()
    app.run()
