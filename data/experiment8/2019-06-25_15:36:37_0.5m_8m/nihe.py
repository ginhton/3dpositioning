import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
# 用指数形式来拟合
# x = np.arange(1, 17, 1)
# y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])

x = [-44.511,-54.1275,-46.4818,-53.7157,-52.7459,-52.7065,-59.4051,-56.4223,-57.7944,-55.8226,-60.5681,-59.7432,-63.1536,-60.673,-62.2467,-61.899]
y = np.arange(0.5, 8.5, 0.5)
x = list(map(lambda x:x+70, x))
def func(x,a,b):
    # return a*np.exp(b/x)
	return a*np.log(x) + b
popt, pcov = curve_fit(func, x, y)
a=popt[0] # popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
yvals=func(x,a,b)
plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, '*', label='curve_fit values')
# plot2=plt.plot(x, yvals, 'r',label='curve_fit values')
# print(*yvals)
print(a)
print(b)
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4) # 指定legend的位置,读者可以自己help它的用法
plt.title('curve_fit')
plt.show()
# plt.savefig('p2.png')
