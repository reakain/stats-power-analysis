#!/usr/bin/env python3
import numpy as np

tracef = "traces_10000x50_int8.bin"
ptextf = "plaintext_10000x16_uint8.bin"
traces = np.fromfile(tracef, dtype='uint8').reshape((10000,50))
ptext = np.fromfile(ptextf, dtype='uint8').reshape((10000,16))
# Perform cpa on traces

print("Task 3")

