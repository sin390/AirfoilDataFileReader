import os

'''A tool as a python API to read the standard airfoil data file.

It could sort the statement header, the points in the upper and lower wing,
into the basic data type in python, the list.

The test files were downloaded from UIUC Airfoil Coordinates Database.
(https://m-selig.ae.illinois.edu/ads/coord_database.html)

It is assumed that there are two kinds of format in airfoil '.dat' file, those are:
i. seperate type, it looks like:
    # Some statement words (header part)
    #
    #     0.000  0.000 (upper wing part)
    #     0.010  0.005
    #      ...   ...
    #     1.000  0.001
    #
    #     0.000  0.000 (lower wing part)
    #     0.010 -0.003
    #      ...    ...
    #     1.000 -0.001

ii. merged type, it looks like:
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
A airfoil data file in both of the formats above could be handled by this tool. 

For the typical example, please refer to the file 'demo.py'.

=========================
= Author:   Han Zexu    =
= Version:  1.0         =
= Date:     2024/01/21  =
=========================
'''

class airfoilReader():
    results = {'upper_x':[],
               'upper_y':[],
               'lower_x':[],
               'lower_y':[]}
    statementtext = []
    filepath = ''
    outputpath = './RearrangedDataset.dat'    
    ifAvailable = False

    def __init__(self, file:str):
        self.filepath = file
        file_name = os.path.basename(file)
        file_name = os.path.splitext(file_name)[0]
        self.outputpath = f'./{file_name}_Rearranged.dat'
    
    def read(self) -> bool:
        if os.path.exists(self.filepath) == False:
            return False
        
        def iffloat(data:str):
            try:
                value = float(data)
                return True
            except ValueError:
                return False
            
        with open(self.filepath,'r') as datfile:
            index = -1
            lines = datfile.readlines()
            ifMergedFormat = False

            __ifupperwing = True
            __ifnotfirstdata = False

            __last_x = 2

            for index in range(len(lines)):
                # skip blank line
                if not lines[index].strip():                 
                    continue
                
                # check if string in the current line. If true, this line is regarded as a statement.
                data_list = lines[index].split()
                ifdatastr = False
                for data in data_list:                  
                    if iffloat(data) == False:
                        ifdatastr = True
                        break
                if ifdatastr == True:
                    self.statementtext.append(lines[index])
                    continue             
                
                # If current line contains less or more than 2 elements
                if len(data_list) != 2:
                    self.statementtext.append(lines[index])
                    continue

                # Begining of the data part.                             
                float_list = [float(value) for value in data_list ]
                tmp_x, tmp_y = float_list

                if tmp_x > 1 or tmp_x < 0 or tmp_y > 1 or tmp_y < -1:
                    self.statementtext.append(lines[index])
                    continue                    
                
                # Determine the format of the current dataset by the first x-coordinate data.
                if __ifnotfirstdata == False:
                    if tmp_x == 0:                     
                        ifMergedFormat = False
                    else:
                        ifMergedFormat = True


                if ifMergedFormat == False:
                    if (tmp_x == 0) and (__ifnotfirstdata == True):
                        __ifupperwing = False
                    if __ifupperwing == True:
                        self.results['upper_x'].append(tmp_x)
                        self.results['upper_y'].append(tmp_y)                        
                    else:
                        self.results['lower_x'].append(tmp_x)
                        self.results['lower_y'].append(tmp_y)
                
                if ifMergedFormat == True:
                    if tmp_x < __last_x:
                        self.results['upper_x'].append(tmp_x)
                        self.results['upper_y'].append(tmp_y) 
                    else:
                        if __ifupperwing == True:
                            if __last_x != 0:
                                self.results['upper_x'].append(0)
                                self.results['upper_y'].append(0)                                 
                            self.results['lower_x'].append(0)
                            self.results['lower_y'].append(0) 
                            __ifupperwing = False
                        self.results['lower_x'].append(tmp_x)
                        self.results['lower_y'].append(tmp_y)                                                
                    __last_x = tmp_x
                __ifnotfirstdata = True  
        self.ifAvailable = True  
        self.__arrange('upper')
        self.__arrange('lower')                

    def getresults(self)->dict:
        self.__arrange('upper')
        self.__arrange('lower')  
        return self.results

    def __arrange(self,wing:str ='', ifdescending:bool = False):
        assert self.ifAvailable == True
        assert wing in ['upper','lower']
        tmp_x = self.results[f'{wing}_x']
        tmp_y = self.results[f'{wing}_y']
        zipped_list = zip(tmp_x,tmp_y)
        sorted_list = sorted(zipped_list, key=lambda x:(x[0]), reverse = ifdescending)
        self.results[f'{wing}_x'], self.results[f'{wing}_y'] = zip(*sorted_list)
    
    def output(self, savepath:str = 'default', format:str = 'merged'):
        assert format in ('merged', 'seperate')
        if savepath == 'default':
            savepath = self.outputpath
        with open(savepath, 'w') as file:
            for tmp_i in range(len(self.statementtext)):
                file.write(f'{' '.join(self.statementtext[tmp_i])}\n')
            
            if format == 'merged':
                self.__arrange('upper', True)
                self.__arrange('lower', False)              
                for tmp_i in range(len(self.results['upper_x'])-1):
                    file.write(f'{self.results['upper_x'][tmp_i]:>12.8f}{self.results['upper_y'][tmp_i]:>12.8f}\n')
                for tmp_i in range(len(self.results['lower_x'])):
                    file.write(f'{self.results['lower_x'][tmp_i]:>12.8f}{self.results['lower_y'][tmp_i]:>12.8f}\n')  
            
            else:
                self.__arrange('upper', False)
                self.__arrange('lower', False)
                for tmp_i in range(len(self.results['upper_x'])):
                    file.write(f'{self.results['upper_x'][tmp_i]:>12.8f}{self.results['upper_y'][tmp_i]:>12.8f}\n')
                file.write('\n')    
                for tmp_i in range(len(self.results['lower_x'])):
                    file.write(f'{self.results['lower_x'][tmp_i]:>12.8f}{self.results['lower_y'][tmp_i]:>12.8f}\n')                                

if __name__ == '__main__':
    cwd = os.path.split(os.path.realpath(__file__))[0]
    os.system(f'python {cwd}/demo.py')