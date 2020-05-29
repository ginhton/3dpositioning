import numpy as np
import matplotlib.pyplot as plt


x = np.arange(-65, -40, 1)
x = list(map(lambda x:x+70, x))

a = -5.540181629441472
b = 18.32217145287159

def func(x,a,b):
    return a*np.log(x) + b
yval = func(x, a, b)
print(*yval)
plt.plot(x, yval, '*')

plt.show()

