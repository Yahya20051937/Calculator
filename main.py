from gui.gui2 import display_async, display
from gui.gui1 import calculator_main, ROOT
from math_calcul.math1 import calcul_async, calcul


def get_func(root, label):
    func = display_async(display(root, label))
    func.send(None)

    return func


def get_func2(root, label):
    func = calcul_async(calcul(root, label))
    func.send(None)

    return func


if __name__ == '__main__':
    calculator_main()
    ROOT.mainloop()
