import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import scipy

from qtpy.QtGui import *
import qtpy.QtWidgets as wid
import sys

a = []

def m(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])
    pass

def linear_f(p1, x2, pendiente):
    return pendiente * (x2 - p1[0]) + p1[1]
    pass

def get_cubic_correction(p, fm, code):
    z2 = (6 * (fm[2] * p[1][0] + fm[1] * p[2][0] - fm[2] * p[2][0] + 2 * fm[1] * p[3][0] + 2 * fm[0] * p[1][0] - 2 * fm[0] *
    p[3][0] - 3 * fm[1] * p[1][0]) + 0.0) / (
             4 * (p[0][0] * p[1][0] + p[2][0] * p[3][0] - p[0][0] * p[3][0]) - pow(p[1][0] + p[2][0], 2))
    z3 = (6 * (
    fm[1] * p[1][0] + fm[0] * p[2][0] - fm[0] * p[1][0] + 2 * fm[1] * p[0][0] + 2 * fm[2] * p[2][0] - 2 * fm[2] *
    p[0][0] - 3 * fm[1] * p[2][0]) + 0.0) / (4 * (p[0][0] * p[1][0] + p[2][0] * p[3][0] - p[0][0] * p[3][0]) - pow(p[1][0] + p[2][0], 2))
    a = -1
    b = -1
    if code == 0:
        a = z2 / (6 * (p[0][0] - p[1][0]))
        b = 2 * z2 / (6 * (p[1][0] - p[0][0]))
    if code == 1:
        a = (2 * z2 + z3) / (6 * (p[1][0] - p[2][0]))
        b = (2 * z3 + z2) / (6 * (p[2][0] - p[1][0]))
    if code == 2:
        a = z3 / (3 * (p[2][0] - p[3][0]))
        b = z3 / (6 * (p[3][0] - p[2][0]))
    return [a, b]
    pass

def cubic_corrected(a, b, p, x, code):
    return a * pow(x - p[code + 1][0], 2) * (x - p[code][0]) + b * (x - p[code + 1][0]) * pow(x - p[code][0], 2)
    pass

def interpolate(p):
    f = []
    f_x = []
    f_y = []
    f_m = []
    f_c = []
    for i in range(0, p.__len__() - 1):
        p1 = p[i]
        p2 = p[i + 1]
        pendiente = m(p1, p2)
        f_m.append(pendiente)
        count = p1[0]
        while count < p2[0]:
            f_x.append(count)
            f_y.append(linear_f(p1, count, pendiente))
            count += 0.01
    for i in range(0, p.__len__() - 1):
        p1 = p[i]
        p2 = p[i + 1]
        correct = get_cubic_correction(p, f_m, i)
        count = p1[0]
        while count < p2[0]:
            f_c.append((cubic_corrected(correct[0], correct[1], p, count, i)))
            count += 0.01
    for i in range(0, f_x.__len__()):
        f.append((f_x[i], f_y[i] + f_c[i]))
    return f
    pass


def add_point(point):
    if a.__len__() % 4 == 0 and a.__len__() > 0:
        new_point = a[a.__len__() - 1]
        pen = m(a[a.__len__() - 2], new_point)
        a.append(new_point)
        if pen < 0:
            a.append(((new_point[0] + 0.5), (new_point[1] - 1)))
        else:
            a.append(((new_point[0] + 0.5), (new_point[1] + 1)))
    a.append(point)
    a.sort(key=lambda x: x[0])
    pass

def draw(p):
    print (p)
    final_data = []
    aux  = p
    if aux.__len__() == 0:
        return
    while aux.__len__() % 4 != 0:
        aux.append((aux[aux.__len__() - 1][0] + 1, aux[aux.__len__() - 1][1]))
    while not (aux.__len__() == 0):
        final_data.extend(interpolate(aux[0:4]))
        aux = aux[4:p.__len__()]
    f_x = []
    f_y = []
    for i in range(0, final_data.__len__()):
       f_x.append(final_data[i][0]) 
       f_y.append(final_data[i][1]) 
    plt.axis([p[0][0], p[p.__len__() - 1][0], min(f_y), max(f_y)])
    plt.plot(f_x, f_y)
    plt.show()
    plt.savefig('spline.png')
    return

def window():
    # Variables
    data = []
    txt = ""
    app = wid.QApplication(sys.argv)
    w = wid.QWidget()
    w.setGeometry(200, 200, 600, 600)
    w.setWindowTitle("Trabajo de Algebra lineal: Splines Cubicos")
    # Labels and text



    # Title
    l = wid.QLabel(w)
    l.setText("Trabajo de Algebra Lineal!")
    l.move(170, 50)
    l.setFont(QFont('SansSerif', 20))

    # information
    l1 = wid.QLabel(w)
    l1.setText("Agrega la cantidad de puntos hasta que desee generar el spline")
    l1.move(30, 100)

    # Textbox
    lx = wid.QLabel(w)
    lx.setText("Inserte valor en X: ")
    lx.move(10, 120)
    tx = wid.QLineEdit(w)
    tx.setGeometry(130, 115, 50, 20)

    ly = wid.QLabel(w)
    ly.setText("Inserte valor en Y: ")
    ly.move(10, 150)
    ty = wid.QLineEdit(w)
    ty.setGeometry(130, 145, 50, 20)

    i1 = wid.QLabel(w)
    i1.setPixmap(QPixmap("data.png"))
    i1.move(200, 200)

    # Functions to add
    def fill():
        temp = (int(tx.text()), int(ty.text()))
        add_point(temp)
        data.append(temp)
        np.sort(a)
        np.sort(data)
        print(data)
        pass
    labels =wid.QLabel(w)
    labels.setGeometry(30, 130, 600, 300)
    def mostrar ():
        temp = ""
        for i in range(0,np.size(data,0)):
           temp = temp + "Valor x: " + str(data[i][0]) + " Valor Y: " + str(data[i][1]) + "\n"
           print(temp)
        labels.setText(temp)
        #a = [(0, 0), (2, 4), (3, 2), (6, 3), (6, 3), (7, 4), (8, 1)]
        draw(a)
        pass
        # Boton 1
    
    bta = []
    bta.append(wid.QPushButton(w))
    bta[0].setText("agregar valor!")
    bta[0].move(200, 140)
    bta[0].clicked.connect(fill)
    
    #btn 2
    bta.append(wid.QPushButton(w))
    bta[1].setText("Generar Spline!")
    bta[1].move(400, 140)
    bta[1].clicked.connect(mostrar)

    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
