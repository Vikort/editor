import tkinter as tk
from tkinter import ttk
import line
import second_order_lines
import time
from enum import Enum


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
        self.begin = None
        self.dots = None
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

        self.menu.add_cascade(label='Файл', menu = file_menu)
        self.menu.add_cascade(label='Отрезки', menu = line_menu)
        self.menu.add_cascade(label='Линии второго порядка', menu = second_order_lines_menu)

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

        sep = ttk.Separator(self.toolbar)
        sep.pack(side=tk.LEFT, fill=tk.Y)

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

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.width = 1920
        self.height = 900
        self.canvas = tk.Canvas(self, bg = 'white', width = self.width, height = self.height)

        self.canvas.bind("<Button-1>", self.mouse_pressed)
        self.canvas.bind("<Motion>", self.mouse_motion)

        self.canvas.pack()


        self.statusbar = tk.Frame(self.master, bd=1, relief=tk.RAISED)
        self.debug_button = tk.Checkbutton(self.statusbar, text = "Debug", variable = self.debug, \
                 onvalue = True, offvalue = False, command=self.draw_grid)
        self.debug_button.pack(side=tk.LEFT)
        self.statuslabel = tk.Label(self.statusbar, text='Отрезки будут отрисованы методом ЦДА')
        self.statuslabel.pack(side=tk.RIGHT)
        self.statusbar.pack()

    def mouse_pressed(self, event) -> None:
        x, y = event.x, event.y
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
            self.dots = None    
            self.begin = None
            self.line = None

    def mouse_motion(self, event) -> None:
        if self.begin is not None and not self.debug.get():
            x, y = event.x, event.y
            dots = self.draw_method(self.begin, line.Dot(x = x, y = y))
            self.canvas.delete('line')
            self.draw_lines()
            for dot in dots:
                self.canvas.create_rectangle(dot.x, dot.y, dot.x + 1, dot.y + 1, fill=color_intesity[dot.i], tags='line')

    
    def draw_lines(self):
        for line in self.lines:
            for dot in line:
                self.canvas.create_rectangle(dot.x, dot.y, dot.x + 1, dot.y + 1, fill=color_intesity[dot.i], tags='line')
    
    def exit(self) -> None:
        self.destroy()

    def dda(self):
        self.draw_method = line.digital_differential_analyzer
        self.statuslabel.config(text='Отрезки будут отрисованы методом ЦДА')
    
    def bresenham(self):
        self.draw_method = line.bresenham
        self.statuslabel.config(text='Отрезки будут отрисованы методом Брезенхема')

    def wu(self):
        self.draw_method = line.wu
        self.statuslabel.config(text='Отрезки будут отрисованы алгоритмом Ву')

    def circle(self):
        self.draw_method = second_order_lines.circle
        self.statuslabel.config(text='Будет отрисована окружность')

    def ellipse(self):
        self.draw_method = second_order_lines.ellipse
        self.statuslabel.config(text='Будет отрисован эллипс')

    def hyperbola(self):
        self.draw_method = second_order_lines.hyperbola
        self.statuslabel.config(text='Будет отрисована гипербола')

    def parabola(self):
        self.draw_method = second_order_lines.parabola
        self.statuslabel.config(text='Будет отрисована парабола')

    def draw_grid(self):
        if self.debug.get():
            for line in range(0, self.width + 1, 10):
                self.canvas.create_line([(line, 0), (line, self.height)], fill='#828282', tags='grid_line_w')

            for line in range(0, self.height + 1, 10):
                self.canvas.create_line([(0, line), (self.width, line)], fill='#828282', tags='grid_line_h')
        else:
            self.canvas.delete('grid_line_h', 'grid_line_w', 'dline')

    def clear(self):
        self.canvas.delete('grid_line_h', 'grid_line_w', 'line', 'dline')
        self.lines.clear()
        if self.debug.get():
            self.draw_grid()