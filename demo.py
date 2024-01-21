import airfoilreader as ar
import os
import matplotlib.pyplot as plt

file = os.getcwd() + '/sd7037.dat'

reader = ar.airfoilReader(file)
reader.read()

reader.output(format='seperate')

plt.plot(reader.results['upper_x'],reader.results['upper_y'],'r')
plt.plot(reader.results['lower_x'],reader.results['lower_y'],'b')
plt.axis('equal')
plt.show()