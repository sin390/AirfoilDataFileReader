import airfoilreader as ar
import os
import matplotlib.pyplot as plt

file = os.getcwd() + '/hs1606.dat'

reader = ar.airfoilReader(file)
reader.read()

reader.output(format='merged')

resultdict = reader.getresults()

plt.plot(resultdict['upper_x'],resultdict['upper_y'],'r')
plt.plot(resultdict['lower_x'],resultdict['lower_y'],'b')
plt.axis('equal')
plt.show()