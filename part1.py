#!/usr/bin/env python3
import numpy as np
from tabulate import tabulate
import time
import mmap

measuref = "measurement_data_2023_uint8.bin"
length_grab = 100000
chunks = int(1000000000/length_grab)

means = ["Mean"]
variances = ["Variance"]
tdiffs = ["Time"]

runa = False
runb = False
runc = True
rund = False
runall = False

vals = None

# with open(measuref, "r+b") as f:
#     # memory-map the file, size 0 means whole file
#     mm = mmap.mmap(f.fileno(), 0)
#     # read content via standard file methods
#     print(mm.readline())  # prints b"Hello Python!\n"
#     # read content via slice notation
#     print(mm[:5])  # prints b"Hello"
#     # update content using slice notation;
#     # note that new content must have same size
#     #mm[6:] = b" world!\n"
#     # ... and read again using standard file methods
#     mm.seek(0)
#     print(mm.readline())  # prints b"Hello  world!\n"
#     # close the map
#     mm.close()
# with open(measuref, "r+b") as f:
#     mm = mmap.mmap(f.fileno(), 0)
#     vals = np.zeros(mm.size())
#     for i in range(mm.size()):
#         vals[i] = mm.read_byte()
#     #print(mm.size())
#     mm.close()
#     print(vals)
#     #tempsum = np.array(mm[:length_grab])
#     #print(tempsum.shape)

if runa or runall:
    print("a) Naive Approach")
    starta = time.time()
    mean = 0
    variance = 0
    summ = 0
    sumsquare = 0

    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        for i in range(mm.size()):
            val = mm.read_byte()
            summ = summ + val
            sumsquare = sumsquare + val*val
        mean = summ/mm.size()
        variance = (sumsquare - mean*summ)/mm.size()
        mm.close()
    means.append(mean)
    variances.append(variance)
    tdiffs.append(time.time()-starta)

if runb or runall:
    print("b) Welford's Algorithm")
    startb = time.time()
    mean = 0
    M2 = 0
    variance = 0
    svar = 0
    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        vals = np.array(list(mm[0:length_grab]))
        mean = np.sum(vals)/vals.shape[0]
        M2 = np.sum(np.square(vals)) - mean*np.sum(vals)
        variance = M2/vals.shape[0]
        count = vals.shape[0]
        vals = np.array(list(mm[length_grab:]))
        # for i in range(1, chunks):
        #     vals = np.array(list(mm[i*length_grab:(i+1)*length_grab]))
        #     count = count + length_grab
        #     diff = np.sum(vals - mean)
        #     mean = mean + diff/count
        #     M2 = M2 + diff*(np.sum(vals - mean))
        #     variance = M2/count
        #     svar = M2/(count-1)
        for i in range(length_grab,vals.shape[0]):
            diff = int(vals[i]) - mean
            mean = mean + diff/i
            M2 = M2 + diff * (int(vals[i]) - mean)
            variance = M2/i
        mm.close()
    means.append(mean)
    variances.append(variance)
    tdiffs.append(time.time()-startb)

if runc or runall:
    print("c) One-pass arbitrary")
    startc = time.time()
    mean = 0
    variance = 0
    svar = 0
    summ = 0
    sumsquare = 0

    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        vals = np.array(list(mm[:]))

    means.append(0)
    variances.append(0)
    tdiffs.append(time.time()-startc)

if rund or runall:
    print("d) Histogram")
    startd = time.time()
    # TODO: check if bincount is acceptable
    # hist = np.zeros(256)
    # for i in range(256):
    #     hist[i] = np.sum(np.where(vals == i, 1, 0))
    vals = None
    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        vals = np.array(list(mm[:]))
    hist = np.bincount(vals)
    counts = np.sum(hist)
    histvals = hist*np.arange(hist.shape[0])
    squaresum = np.sum(np.square(np.arange(hist.shape[0]))*hist)
    histsum = np.sum(histvals)
    mean = histsum/counts
    meansum = mean*histsum
    variance = (squaresum-meansum)/(counts)
    means.append(mean)
    variances.append(variance)
    tdiffs.append(time.time()-startd)


if runall:
    print("e) Runtime Differences:")
    print(tabulate([means, variances, tdiffs], headers = ["","Naive", "Welford", "1Pass", "Histogram"]))

