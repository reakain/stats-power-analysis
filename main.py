#!/usr/bin/env python3
import numpy as np
from tabulate import tabulate
import time
import mmap
import math
import matplotlib.pyplot as plt

print("# Assignment 2")
print('')
print('')
print("Install the packages from requirements.txt through pip. To run and get output use:")
print('')
print("```")
print("python3 main.py > output.md")
print("```")
print('')
print('')



measuref = "measurement_data_2023_uint8.bin"
length_grab = 100000
chunks = int(1000000000/length_grab)

means = ["Mean"]
variances = ["Variance"]
tdiffs = ["Time"]

# Task 1 run commands
runall = True
runa = False
runb = False
runc = False
rund = False

# Task 2 and 3 run commands
run_task2 = True
run_task3 = True


print("## Task 1")
print('')

if runa or runall:
    print("### a) Naive Approach")
    startt = time.time()
    mean = 0
    variance = 0
    sums = np.zeros(chunks)
    sumsquares = np.zeros(chunks)
    summ = 0
    sumsquare = 0

    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        vals = np.zeros(length_grab)
        for i in range(chunks):
            vals = np.array(list(mm[length_grab * i:length_grab * (i + 1)]))
            sums[i] = np.sum(vals)
            sumsquares[i] = np.sum(np.square(vals))
        summ = np.sum(sums)
        sumsquare = np.sum(sumsquares)
        mean = summ/mm.size()
        variance = (sumsquare - mean*summ)/mm.size()
        mm.close()

    tdiffs.append(time.time() - startt)
    means.append(mean)
    variances.append(math.sqrt(variance))
    print('')
    print("Mean: {:.1f}".format(mean))
    print('')
    print("Variance: {:.3f}".format(math.sqrt(variance)))
    print('')


if runb or runall:
    print("### b) Welford's Algorithm")
    startt = time.time()
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
        for i in range(length_grab,vals.shape[0]):
            diff = int(vals[i]) - mean
            mean = mean + diff/i
            M2 = M2 + diff * (int(vals[i]) - mean)
            variance = M2/i
        mm.close()

    tdiffs.append(time.time() - startt)
    means.append(mean)
    variances.append(math.sqrt(variance))
    print('')
    print("Mean: {:.1f}".format(mean))
    print('')
    print("Variance: {:.3f}".format(math.sqrt(variance)))
    print('')


if runc or runall:
    print("### c) One-pass arbitrary")
    startt = time.time()
    mean = 0
    variance = 0
    M1_chunks = np.zeros(chunks)
    CS2_chunks = np.zeros(chunks)

    def getM1CS2Chunk(vals,n):
        M1 = 0
        CS2 = 0
        for i in range(n):
            d = vals[i] - M1
            M1 += d/(i+1)
            CS2 += d*d*i/(i+1)
        return M1, CS2


    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        vals = np.zeros(length_grab)

        for i in range(chunks):
            vals = np.array(list(mm[length_grab*i:length_grab*(i+1)]))
            m1, cs2 = getM1CS2Chunk(vals,length_grab)
            M1_chunks[i] = m1
            CS2_chunks[i] = cs2

        mean = np.sum(length_grab*M1_chunks)/mm.size()
        variance = np.sum(CS2_chunks)/mm.size()
        mm.close()


    tdiffs.append(time.time() - startt)
    means.append(mean)
    variances.append(math.sqrt(variance))
    print('')
    print("Mean: {:.1f}".format(mean))
    print('')
    print("Variance: {:.3f}".format(math.sqrt(variance)))
    print('')

if rund or runall:
    print("### d) Histogram")
    startt = time.time()
    hist = np.zeros(256)
    bin_vals = np.arange(256)
    with open(measuref, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        vals = np.zeros(length_grab)
        for i in range(chunks):
            vals = np.array(list(mm[length_grab * i:length_grab * (i + 1)]))
            hist += np.bincount(vals, minlength=256)
        mm.close()

    counts = np.sum(hist)
    histvals = hist*bin_vals
    squarevals = np.square(bin_vals)*hist
    squaresum = np.sum(squarevals)
    histsum = np.sum(histvals)
    mean = histsum/counts
    meansum = mean*histsum
    variance = (squaresum-meansum)/counts

    tdiffs.append(time.time() - startt)
    means.append(mean)
    variances.append(math.sqrt(variance))
    print('')
    print("Mean: {:.1f}".format(mean))
    print('')
    print("Variance: {:.3f}".format(math.sqrt(variance)))
    print('')


if runall:
    print("## e) Runtime Differences:")
    print('')
    print("```")
    print(tabulate([means, variances, tdiffs], headers = ["","Naive", "Welford", "1Pass", "Histogram"]))
    print("```")
    print('')



tracef = "traces_10000x50_int8.bin"
ptextf = "plaintext_10000x16_uint8.bin"

N_traces = 10000
T_length = 50

traces = np.fromfile(tracef, dtype='uint8').reshape((N_traces,T_length))
ptext = np.fromfile(ptextf, dtype='uint8').reshape((N_traces,16))

signals = np.zeros((16,50))
noises = np.zeros((16,50))
snrs = np.zeros((16,50))


def oneByteSNR(byte):
    p0 = ptext[:,byte]
    Es = np.zeros((255,T_length))
    variances = np.zeros((255,T_length))

    for p in range(255):
        bools = np.where(p0 != p, 0, 1)
        c = np.transpose(np.transpose(traces)*bools)
        Es[p] = np.mean(c, axis=0, where= c!=0)
        variances[p] = np.var(c, axis=0, where= c!=0)
    signal = np.var(Es, axis=0)
    noise = np.mean(variances, axis=0)
    snr = signal / noise
    return signal, noise, snr


if run_task2:
    print("## Task 2 -- SNR Plotting")
    print('')
    for i in range(16):
        signal, noise, snr = oneByteSNR(i)
        signals[i] = signal
        noises[i] = noise
        snrs[i] = snr

    signals = np.transpose(signals)
    noises = np.transpose(noises)
    snrs = np.transpose(snrs)

    # Part a
    # Compute and plot signal of traces
    plt.plot(signals)
    plt.title("Signal Response")
    plt.legend(np.arange(16))
    plt.savefig('signal.png', dpi=300)
    plt.clf()
    print("### Part A")
    print('')
    print("[Signal Response Plot](./signal.png)")
    print('')

    # Part b
    # Compute and plot noise of traces
    plt.plot(noises)
    plt.title("Noise Response")
    plt.legend(np.arange(16))
    plt.savefig('noise.png', dpi=300)
    plt.clf()
    print("### Part B")
    print('')
    print("[Noise Response Plot](./noise.png)")
    print('')


    # Part c
    # Compute and plot SNR
    plt.plot(snrs)
    plt.title("SNR Response")
    plt.legend(np.arange(16))
    plt.savefig('snr.png', dpi=300)
    plt.clf()
    print("### Part C")
    print('')
    print("[SNR Response Plot](./SNR.png)")
    print('')



if run_task3:
    print("### Task 3 -- CPA")
    print('')
    sbox = np.array([
        0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
        0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
        0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
        0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
        0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
        0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
        0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
        0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
        0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
        0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
        0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
        0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
        0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
        0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
        0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
        0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
        ])

    # Convert the sbox to hamming weights
    hw_sbox = np.zeros(256)
    for i in range(256):
        hw_sbox[i] = sbox[i].bit_count()

    key = np.zeros(16)

    # Yes, I'm a monster just inject functions in the middle
    def oneByteCPA(byte):
        corrs = np.zeros(T_length)
        max_corr = np.zeros(256)
        for k in range(256):
            hw = hw_sbox[np.bitwise_xor(ptext[:, byte], k)]
            for i in range(T_length):
                corrs[i] = np.corrcoef(hw,traces[:,i])[0,1]
            max_corr[k] = np.max(corrs)
        return np.argmax(max_corr)


    startt = time.time()
    for i in range(16):
        key[i] = oneByteCPA(i)
    stopt = time.time()

    print('Run time is {:.2f} seconds'.format(stopt-startt))
    print('')
    print('Key is: {}'.format(key))