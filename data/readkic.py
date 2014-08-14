import numpy as np

def iter_loadtxt(filename, delimiter=',', skiprows=0, dtype=float, cols=None, maxlength=None):
    def iter_func():
        with open(filename, 'r') as infile:
            for _ in range(skiprows):
                next(infile)
            for line in infile:
                line = line.rstrip().split(delimiter)
                if cols==None:
                    for item in line:
                        try:
                            yield dtype(item)
                        except:
                            yield 0 
                else:
                    for i in cols:
                        try:
                            yield dtype(line[i])
                        except:
                            yield 0 
        if cols == None:
            iter_loadtxt.rowlength = len(line)
        else:
            iter_loadtxt.rowlength = len(cols)

    data = np.fromiter(iter_func(), dtype=dtype)
    data = data.reshape((-1, iter_loadtxt.rowlength))
    return data

data = iter_loadtxt('short.txt', delimiter='|', skiprows=1, dtype=int, cols=[15])
print data
