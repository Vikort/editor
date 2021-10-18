import tkinter as tk
from tkinter import ttk

import time
from enum import Enum
from tkinter.constants import DISABLED

import line
import second_order_lines
import curve


color_intesity = {
    0 : '#ffffff',
    0.1 : '#e6e6e6',
    0.2 : '#cdcdcd',
    0.3 : '#b4b4b4',
    0.4 : '#9b9b9b',
    0.5 : '#828282',
    0.6 : '#696969',
    0.7 : '#505050',
    0.8 : '#373737',
    0.9 : '#1e1e1e',
    1.0 : '#000000',
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.lines = []
        self.curves = []
        self.dots = []
        self.begin = None
        self.obj = None
        self.is_multiple_dots = False
        self.debug = tk.BooleanVar(False)
        self.draw_method = line.digital_differential_analyzer

        self.title('Editor')

        self.menu = tk.Menu(self)
        self.config(menu = self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label='Очистить', command=self.clear)
        file_menu.add_command(label='Выход', command = self.exit)

        line_menu = tk.Menu(self.menu, tearoff=0)
        line_menu.add_command(label='ЦДА', command=self.dda)
        line_menu.add_command(label='Брезенхем', command=self.bresenham)
        line_menu.add_command(label='Алгоритм Ву', command=self.wu)

        second_order_lines_menu = tk.Menu(self.menu, tearoff=0)
        second_order_lines_menu.add_command(label='Окружность', command=self.circle)
        second_order_lines_menu.add_command(label='Эллипс', command=self.ellipse)
        second_order_lines_menu.add_command(label='Гипербола', command=self.hyperbola)
        second_order_lines_menu.add_command(label='Парабола', command=self.parabola)

        curve_menu = tk.Menu(self.menu, tearoff=0)
        curve_menu.add_command(label='Эрмит', command=self.hermite)
        curve_menu.add_command(label='Безье', command=self.bezier)
        curve_menu.add_command(label='В сплайн', command=self.b_spline)

        self.menu.add_cascade(label='Файл', menu = file_menu)
        self.menu.add_cascade(label='Отрезки', menu = line_menu)
        self.menu.add_cascade(label='Линии второго порядка', menu = second_order_lines_menu)
        self.menu.add_cascade(label='Кривые', menu = curve_menu)

        self.toolbar = tk.Frame(self.master, bd=1, relief=tk.RAISED)
        
        dda_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.dda, text='ЦДА'
        )
        dda_button.pack(side=tk.LEFT)
        
        bresenham_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.bresenham, text='Брезенхем'
        )
        bresenham_button.pack(side=tk.LEFT)

        wu_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.wu, text='Алгоритм Ву'
        )
        wu_button.pack(side=tk.LEFT)

        sep1 = ttk.Separator(self.toolbar)
        sep1.pack(side=tk.LEFT, fill=tk.Y)

        circle_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.circle, text='Окружность'
        )
        circle_button.pack(side=tk.LEFT)

        ellipse_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.ellipse, text='Эллипс'
        )
        ellipse_button.pack(side=tk.LEFT)

        hyperbola_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.hyperbola, text='Гипербола'
        )
        hyperbola_button.pack(side=tk.LEFT)

        parabola_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.parabola, text='Парабола'
        )
        parabola_button.pack(side=tk.LEFT)

        sep2 = ttk.Separator(self.toolbar)
        sep2.pack(side=tk.LEFT, fill=tk.Y)

        hermite_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.hermite, text='Эрмит'
        )
        hermite_button.pack(side=tk.LEFT)

        bezier_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.bezier, text='Безье'
        )
        bezier_button.pack(side=tk.LEFT)

        b_spline_button = tk.Button(
            self.toolbar, relief=tk.FLAT,
            command=self.b_spline, text='B сплайн'
        )
        b_spline_button.pack(side=tk.LEFT)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.width = 1920
        self.height = 900
        self.canvas = tk.Canvas(self, bg = 'white', width = self.width, height = self.height)

        self.canvas.bind("<Button-1>", self.mouse_pressed)
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Button-3>", self.move_object)

        self.canvas.pack()


        self.statusbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.debug_button = tk.Checkbutton(self.statusbar, text = "Debug", variable = self.debug, \
                 onvalue = True, offvalue = False, command=self.draw_grid)
        self.debug_button.pack(side=tk.LEFT)
        self.statuslabel = tk.Label(self.statusbar, text='Отрезки будут отрисованы методом ЦДА')
        self.statuslabel.pack(side=tk.RIGHT)
        self.statusbar.pack()
        
        self.dots_need_bar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.dots_need_label = tk.Label(self.dots_need_bar, text='Количество граничных точек: ')
        self.dots_need_label.pack(side=tk.LEFT)
        self.dots_need = tk.IntVar(value=2)
        self.dots_need_field = tk.Entry(self.dots_need_bar)
        self.dots_need_field['textvariable'] = self.dots_need
        self.dots_need_field.bind('<Key-Return>', self.on_change)
        self.dots_need_field.pack(side=tk.RIGHT)
        self.dots_need_bar.pack()
        self.dots_need_field.config(state='disable')

    def on_change(self, event) -> None:
        if self.dots_need.get() < 4:
            self.dots_need.set(4)

    def move_object(self, event) -> None:
        if self.obj is None:
            self.obj = self.canvas.find_overlapping(event.x-5, event.y-5, event.x + 5, event.y + 5)
            print(self.obj)
        else:
            self.obj = None

    def mouse_pressed(self, event) -> None:
        x, y = event.x, event.y
        if not self.is_multiple_dots:
            if self.begin is None:
                if self.debug.get():
                    self.begin = line.Dot(x = x // 10, y = y // 10)
                else:
                    self.begin = line.Dot(x = x, y = y)
            else:
                if self.debug.get():
                    end = line.Dot(x = x // 10, y = y // 10)
                else:
                    end = line.Dot(x = x, y = y)
                dots = self.draw_method(self.begin, end)
                for dot in dots:
                    if self.debug.get():
                        self.canvas.create_rectangle(dot.x * 10, dot.y * 10, dot.x * 10 + 10, dot.y * 10 + 10, fill=color_intesity[dot.i], tags='dline')
                        print(dot.x, dot.y, dot.i)
                        self.update()
                        time.sleep(0.5)
                    else:
                        self.canvas.create_rectangle(dot.x, dot.y, dot.x + 1, dot.y + 1, fill=color_intesity[dot.i], tags='line')
                if not self.debug.get():
                    self.lines.append(dots)
                self.begin = None
        else:
            if self.debug.get():
                self.dots.append(line.Dot(x = x // 10, y = y // 10))
            else:
                self.dots.append(line.Dot(x = x, y = y))
            self.draw_boudary_points()
            if len(self.dots) == self.dots_need.get():
                dots = self.draw_method(self.dots)
                for i in range(1, len(dots)):
                    if self.debug.get():
                        self.canvas.create_rectangle(dots[i-1].x * 10, dots[i-1].y * 10, dots[i].x * 10, dots[i].y * 10, fill=color_intesity[dots[i-1].i], tags='dcurve')
                        print(dots[i].x, dots[i].y, dots[i].i)
                        self.update()
                        time.sleep(0.5)
                    else:
                        self.canvas.create_line((dots[i-1].x, dots[i-1].y), (dots[i].x, dots[i].y), fill=color_intesity[dots[i].i], tags='curve')
                if not self.debug.get():
                    self.curves.append(dots)
                self.dots.clear()


    def mouse_motion(self, event) -> None:
        if self.begin is not None and not self.debug.get() and not self.is_multiple_dots:
            x, y = event.x, event.y
            dots = self.draw_method(self.begin, line.Dot(x = x, y = y))
            self.canvas.delete('line')
            self.draw_lines()
            for dot in dots:
                self.canvas.create_rectangle(dot.x, dot.y, dot.x + 1, dot.y + 1, fill=color_intesity[dot.i], tags='line')
        elif self.is_multiple_dots and self.obj is not None:
            for obj in self.obj:
                self.canvas.moveto(obj, event.x, event.y)

    
    def draw_lines(self):
        for line in self.lines:
            for dot in line:
                self.canvas.create_rectangle(dot.x, dot.y, dot.x + 1, dot.y + 1, fill=color_intesity[dot.i], tags='line')

    def draw_boudary_points(self):
        i = 0
        for dot in self.dots:
            self.canvas.delete('P' + str(i))
            if self.debug.get():
                self.canvas.create_oval(dot.x*10 - 5, dot.y*10 - 5, dot.x*10 + 5, dot.y*10 + 5, outline='black', tags='P' + str(i))
                self.canvas.create_text(dot.x*10 + 15, dot.y*10,text='P' + str(i), tags = 'P' + str(i))
            else:
                self.canvas.create_oval(dot.x - 5, dot.y - 5, dot.x + 5, dot.y + 5, outline='black', tags='P' + str(i))
                self.canvas.create_text(dot.x + 15, dot.y,text='P' + str(i), tags = 'P' + str(i))
            i += 1
    
    def exit(self) -> None:
        self.destroy()

    def dda(self):
        self.draw_method = line.digital_differential_analyzer
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Отрезки будут отрисованы методом ЦДА')
    
    def bresenham(self):
        self.draw_method = line.bresenham
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Отрезки будут отрисованы методом Брезенхема')

    def wu(self):
        self.draw_method = line.wu
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Отрезки будут отрисованы алгоритмом Ву')

    def circle(self):
        self.draw_method = second_order_lines.circle
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Будет отрисована окружность')

    def ellipse(self):
        self.draw_method = second_order_lines.ellipse
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Будет отрисован эллипс')

    def hyperbola(self):
        self.draw_method = second_order_lines.hyperbola
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Будет отрисована гипербола')

    def parabola(self):
        self.draw_method = second_order_lines.parabola
        self.is_multiple_dots = False
        self.dots_need.set(2)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Будет отрисована парабола')

    def hermite(self):
        self.draw_method = curve.hermite_shape
        self.is_multiple_dots = True
        self.dots_need.set(4)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Будет отрисована кривая формой Эрмита')

    def bezier(self):
        self.draw_method = curve.bezier_shape
        self.is_multiple_dots = True
        self.dots_need.set(4)
        self.dots_need_field.config(state='disable')
        self.statuslabel.config(text='Будет отрисована кривая формой Безье')

    def b_spline(self):
        self.draw_method = curve.b_spline
        self.is_multiple_dots = True
        self.dots_need.set(10)
        self.dots_need_field.config(state='normal')
        self.statuslabel.config(text='Будет отрисована кривая b-сплайн')

    def draw_grid(self):
        if self.debug.get():
            for line in range(0, self.width + 1, 10):
                self.canvas.create_line([(line, 0), (line, self.height)], fill='#828282', tags='grid_line_w')

            for line in range(0, self.height + 1, 10):
                self.canvas.create_line([(0, line), (self.width, line)], fill='#828282', tags='grid_line_h')
        else:
            self.canvas.delete('grid_line_h', 'grid_line_w', 'dline', 'dcurve')

    def clear(self):
        self.canvas.delete('grid_line_h', 'grid_line_w', 'line', 'dline', 'curve', 'dcurve')
        self.lines.clear()
        self.curves.clear()
        if self.debug.get():
            self.draw_grid()
