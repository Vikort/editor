import second_order_lines
import ui


def main() -> None:
    # print("x1 = 0, x2 = 8, y1 = 0, y2 = 5;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=8,y=5)
    # for i in line.digital_differential_analyzer(begin, end):
    #     print(i)
    # print("x1 = 0, x2 = -8, y1 = 0, y2 = 5;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=-8,y=5)
    # for i in line.digital_differential_analyzer(begin, end):
    #     print(i)
    # print("x1 = 0, x2 = -8, y1 = 0, y2 = -5;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=-8,y=-5)
    # for i in line.digital_differential_analyzer(begin, end):
    #     print(i)
    # print("x1 = 0, x2 = 8, y1 = 0, y2 = -5;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=8,y=-5)
    # for i in line.digital_differential_analyzer(begin, end):
    #     print(i)
    # print("x1 = 0, x2 = 9, y1 = 0, y2 = 4;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=9,y=4)
    # for i in line.bresenham(begin, end):
    #     # print(i)
    #     pass
    # print("x1 = 0, x2 = -9, y1 = 0, y2 = 4;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=-9,y=4)
    # for i in line.bresenham(begin, end):
    #     # print(i)
    #     pass
    # print("x1 = 0, x2 = 9, y1 = 0, y2 = -4;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=9,y=-4)
    # for i in line.bresenham(begin, end):
    #     # print(i)
    #     pass
    # print("x1 = 0, x2 = -9, y1 = 0, y2 = -4;")
    # begin = line.Dot(x=0,y=0)
    # end = line.Dot(x=-9,y=-4)
    # for i in line.bresenham(begin, end):
    #     print(i)
    #     pass
    print("x = 0, R = 8")
    begin = second_order_lines.Dot(x=0,y=0)
    end = second_order_lines.Dot(x=0,y=8)
    for i in second_order_lines.circle(begin, end):
        print(i)

    app = ui.App()
    app.mainloop()


if __name__ == '__main__':
    main()
