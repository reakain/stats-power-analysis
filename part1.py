#!/usr/bin/env python3
import numpy as np
from tabulate import tabulate
import time
import mmap

measuref = "measurement_data_2023_uint8.bin"
#data = np.fromfile(measuref, dtype='uint8')
#print(data.shape)
#mm = mmap.mmap(measuref, 0)
# mm[:5]
means = ["Mean"]
variances = ["Variance"]
tdiffs = ["Time"]

runa = True
runb = True
runc = True
rund = True
runall = False



if runa or runall:
    print("a) Naive Approach")
    starta = time.time()
    


    means.append(0)
    variances.append(0)
    tdiffs.append(time.time()-starta)

if runb or runall:
    print("b) Welford's Algorithm")
    startb = time.time()



    means.append(0)
    variances.append(0)
    tdiffs.append(time.time()-startb)

if runc or runall:
    print("c) One-pass arbitrary")
    startc = time.time()



    means.append(0)
    variances.append(0)
    tdiffs.append(time.time()-startc)

if rund or runall:
    print("d) Histogram")
    startd = time.time()



    means.append(0)
    variances.append(0)
    tdiffs.append(time.time()-startd)


if runall:
    print("e) Runtime Differences:")
    print(tabulate([means, varianes, tdiffs], headers = ["","Naive", "Welford", "1Pass", "Histogram"]))

