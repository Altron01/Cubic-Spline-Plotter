import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import scipy
f_x = []
f_y = []
f_m = []
f_c = []
def m(p1, p2):
    return (p2[1] - p1[1])/(p2[0] - p1[0])
    pass

def linear_f(p1, x2, pendiente):
    return pendiente*(x2 - p1[0]) + p1[1]
    pass

def get_cubic_correction(p, fm, code):
    z2 = (6*(fm[2]*p[1][0] + fm[1]*p[2][0] - fm[2]*p[2][0] + 2*fm[1]*p[3][0] + 2*fm[0]*p[1][0] - 2*fm[0]*p[3][0] - 3*fm[1]*p[1][0]) + 0.0)/(4*(p[0][0]*p[1][0] + p[2][0]*p[3][0] - p[0][0]*p[3][0]) - pow(p[1][0] + p[2][0], 2))  
    z3 = (6*(fm[1]*p[1][0] + fm[0]*p[2][0] - fm[0]*p[1][0] + 2*fm[1]*p[0][0] + 2*fm[2]*p[2][0] - 2*fm[2]*p[0][0] - 3*fm[1]*p[2][0]) + 0.0)/(4*(p[0][0]*p[1][0] + p[2][0]*p[3][0] - p[0][0]*p[3][0]) - pow(p[1][0] + p[2][0], 2))
    a = -1
    b = -1
    if code == 0:
        a = z2/(6*(p[0][0] - p[1][0]))
        b = 2*z2/(6*(p[1][0] - p[0][0]))
    if code == 1:
        a = (2*z2 + z3)/(6*(p[1][0] - p[2][0]))
        b = (2*z3 + z2)/(6*(p[2][0] - p[1][0]))
    if code == 2:
        a = z3/(3*(p[2][0] - p[3][0]))
        b = z3/(6*(p[3][0] - p[2][0]))
    return [a, b]
    pass

def cubic_corrected(a, b, p, x, code):
    return a*pow(x - p[code + 1][0], 2)*(x - p[code][0]) + b*(x - p[code + 1][0])*pow(x - p[code][0], 2)
    pass

def interpolate(p):
    for i in range(0, p.__len__() - 1):
        p1 = p[i]
        p2 = p[i+1]
        pendiente = m(p1, p2)
        f_m.append(pendiente)
        count = p1[0]
        while count < p2[0]:
            f_x.append(count)
            f_y.append(linear_f(p1, count, pendiente))
            count += 0.01
    for i in range(0, p.__len__() - 1):
        p1 = p[i]
        p2 = p[i+1]
        correct = get_cubic_correction(p, f_m, i)
        count = p1[0]
        while count < p2[0]:
            f_c.append((cubic_corrected(correct[0], correct[1], p, count, i)))
            count += 0.01
    for i in range(0, f_y.__len__()):
        f_y[i]  += f_c[i]
    pass

p = [(0, 0), (2, 4), (3, 3), (4, 2)]
interpolate(p)
plt.axis([0, 5, 0, 5])
plt.plot(f_x, f_y)
plt.savefig('spline.png')








