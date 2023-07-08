import tkinter as tk

ROOT = tk.Tk()
ROOT.geometry('250x250')


def calculator_main():
    from main import get_func
    from gui.gui_functions import pack_elements1

    main_frame = tk.Frame(ROOT)

    display_frame = tk.Frame(main_frame)
    display = tk.Label(display_frame)

    func = get_func(ROOT, display)

    func_main_frame = tk.Frame(main_frame)
    main_button = tk.Button(func_main_frame, text='main')
    func_button = tk.Button(func_main_frame, text='func',
                            command=lambda: [main_frame.destroy(), calculator_main_frame.destroy(), func_widget()])

    calculator_main_frame = tk.Frame(ROOT)

    calculator_frame1 = tk.Frame(calculator_main_frame)

    sub_frame1 = tk.Frame(calculator_frame1)
    closing_brackets = tk.Button(sub_frame1, text=']', command=lambda x='}': func.send(x))
    a_power_b = tk.Button(sub_frame1, text='^', command=lambda x='^': func.send(x))
    ln = tk.Button(sub_frame1, text='ln', command=lambda x='ln': func.send(x))

    sub_frame2 = tk.Frame(calculator_frame1)
    open_brackets = tk.Button(sub_frame2, text='[', command=lambda x='{': func.send(x))
    exp = tk.Button(sub_frame2, text='exp', command=lambda x='exp': func.send(x))
    pi = tk.Button(sub_frame2, text='π')

    sub_frame3 = tk.Frame(calculator_frame1)
    cos = tk.Button(sub_frame3, text='cos', command=lambda x='cos': func.send(x))
    sin = tk.Button(sub_frame3, text='sin', command=lambda x='sin': func.send(x))
    tan = tk.Button(sub_frame3, text='tan', command=lambda x='tan': func.send(x))

    sub_frame4 = tk.Frame(calculator_frame1)
    open_parenthesis = tk.Button(sub_frame4, text='(', command=lambda x='(': func.send(x))
    close_parenthesis = tk.Button(sub_frame4, text=')', command=lambda x=')': func.send(x))
    comma = tk.Button(sub_frame4, text=',')

    calculator_frame2 = tk.Frame(calculator_main_frame)

    sub_frame5 = tk.Frame(calculator_frame2)
    seven = tk.Button(sub_frame5, text='7', command=lambda x=7: func.send(x))
    eight = tk.Button(sub_frame5, text='8', command=lambda x=8: func.send(x))
    nine = tk.Button(sub_frame5, text='9', command=lambda x=9: func.send(x))
    divide = tk.Button(sub_frame5, text='/', command=lambda x='/': func.send(x))

    sub_frame6 = tk.Frame(calculator_frame2)
    four = tk.Button(sub_frame6, text='4', command=lambda x=4: func.send(x))
    five = tk.Button(sub_frame6, text='5', command=lambda x=5: func.send(x))
    six = tk.Button(sub_frame6, text='6', command=lambda x=6: func.send(x))
    multiply = tk.Button(sub_frame6, text='*', command=lambda x='*': func.send(x))

    sub_frame7 = tk.Frame(calculator_frame2)
    one = tk.Button(sub_frame7, text='1', command=lambda x=1: func.send(x))
    two = tk.Button(sub_frame7, text='2', command=lambda x=2: func.send(x))
    three = tk.Button(sub_frame7, text='3', command=lambda x=3: func.send(x))
    minus = tk.Button(sub_frame7, text='-', command=lambda x='-': func.send(x))

    sub_frame8 = tk.Frame(calculator_frame2)
    zero = tk.Button(sub_frame8, text='0', command=lambda x=0: func.send(x))
    dot = tk.Button(sub_frame8, text='.')
    ans = tk.Button(sub_frame8, text='ans')
    add = tk.Button(sub_frame8, text='+', command=lambda x='+': func.send(x))

    calculator_frame3 = tk.Frame(calculator_main_frame)

    delete = tk.Button(calculator_frame3, text='x')
    c = tk.Button(calculator_frame3, text='C', command=lambda x='c': func.send(x))
    result = tk.Button(calculator_frame3, text='↵', command=lambda x='res': func.send(x))
    percentage = tk.Button(calculator_frame3, text='%')

    main_frame.pack(fill='both', expand=True)
    display_frame.pack(side='top', fill='both', expand=True)
    calculator_main_frame.pack(side='top', fill='both', expand=True)
    func_main_frame.pack(side='top', fill='both', expand=True)

    display.pack(fill='both', expand=True)
    func_button.pack(side='left', fill='both', expand=True)
    main_button.pack(side='left', fill='both', expand=True)

    calculator_frame1.pack(side='left', fill='both', expand=True)
    pack_elements1(sub_frame1, closing_brackets, a_power_b, ln)
    pack_elements1(sub_frame2, open_brackets, exp, pi)
    pack_elements1(sub_frame3, sin, cos, tan)
    pack_elements1(sub_frame4, open_parenthesis, close_parenthesis, comma)

    calculator_frame2.pack(side='left', fill='both', expand=True)
    pack_elements1(sub_frame5, seven, eight, nine, divide)
    pack_elements1(sub_frame6, four, five, six, multiply)
    pack_elements1(sub_frame7, one, two, three, minus)
    pack_elements1(sub_frame8, zero, dot, ans, add)

    calculator_frame3.pack(side='left', fill='both')
    delete.pack(side='top', fill='both', expand=True)
    c.pack(side='top', fill='both', expand=True)
    result.pack(side='top', fill='both', expand=True)
    percentage.pack()


def func_widget():
    from math_calcul2.function_study import Function
    main_frame = tk.Frame(ROOT)

    y = tk.StringVar()

    back = tk.Button(main_frame, text='◀️', command=lambda: [main_frame.destroy(), calculator_main()])

    frame1 = tk.Frame(main_frame)
    label = tk.Label(frame1, text='f(x) = ')
    entry = tk.Entry(frame1, textvariable=y)
    button = tk.Button(frame1, text='▶️', command=lambda: Function([element for element in y.get() if element != ' ']))

    frame2 = tk.Frame(main_frame)
    label2 = tk.Label(frame2)

    main_frame.pack(fill='both', expand=True)
    back.pack(side='left')

    frame1.pack(side='top', fill='x', expand=True)
    label.pack(side='left', fill='x', expand=True)
    entry.pack(side='left', fill='x', expand=True)
    button.pack(side='left', fill='x', expand=True)

    frame2.pack(side='top', fill='both', expand=True)
    label2.pack(side='top', fill='both', expand=True)



