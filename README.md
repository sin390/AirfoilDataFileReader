# AirfoilReader

A python module to handle an airfoil data file. It can parse the statement header, the points in the upper and lower wing.

Two kinds of format in airfoil '.dat' file are considered, those are:

+ i. `seperate` type, it looks like:
  
  ```
    # Some statement words (header part)
    #
    #     0.000  0.000 (upper wing part)
    #     0.010  0.005
    #      ...   ...
    #     1.000  0.001
    #                  (blank here)
    #     0.000  0.000 (lower wing part)
    #     0.010 -0.003
    #      ...    ...
    #     1.000 -0.001
  ```

+ ii. `merged` type, it looks like:
  
  ```
    # Some statement words (header part)
    #
    #     1.000  0.001 
    #     0.990  0.005
    #      ...   ...    (No blank)
    #     0.010  0.012
    #     0.000  0.000
    #     0.010 -0.013
    #      ...    ...
    #     0.995  0.001
    #     1.000 -0.001
  ```
  
  A airfoil data file in either of above two formats could be handled by this module. 

For the example, please refer to [Quick start](#demo).

> The test files in /refAirfoils were downloaded from UIUC Airfoil Coordinates Database.
> (https://m-selig.ae.illinois.edu/ads/coord_database.html)

### Install

```python
pip install git+https://github.com/sin390/AirfoilReader.git
```

### 

### Quick start <a id="demo"></a>

As the `demo.py` file, one can handle an airfoil file like this...

```python
import airfoilreader as ar
import os
import matplotlib.pyplot as plt

file = f'{__file__}/refAirfoils/hs1606.dat'

reader = ar.AirfoilReader(file, outputpath="./")
reader.read()
resultdict = reader.getresults()

plt.plot(resultdict['upper_x'],resultdict['upper_y'],'r')
plt.plot(resultdict['lower_x'],resultdict['lower_y'],'b')
plt.axis('equal')
plt.show()

reader.output(format='merged')
```
