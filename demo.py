'''
=========================
= Author:   Han Zexu    =
= Version:  1.0         =
= Date:     2024/01/22  =
=========================
'''
import airfoilreader as ar
import os
import matplotlib.pyplot as plt

file = f'{os.path.dirname(__file__)}/refAirfoils/hs1606.dat'
reader = ar.AirfoilReader(file, outputpath="./")
reader.read()
resultdict = reader.getresults()

plt.plot(resultdict['upper_x'],resultdict['upper_y'],'r')
plt.plot(resultdict['lower_x'],resultdict['lower_y'],'b')
plt.axis('equal')
plt.show()

reader.output(format='merged')
