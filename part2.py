#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

tracef = "traces_10000x50_int8.bin"
ptextf = "plaintext_10000x16_uint8.bin"



# Part a
# Compute and plot signal of traces

# Plot
plt.subplot(3, 1, 1)
plt.plot(signal, 'black')
plt.title("Signal Response")

# Part b
# Compute and plot noise of traces


# Plot
plt.subplot(3, 1, 2)
plt.plot(noise, 'black')
plt.title("Noise Response")

# Part c
# Compute and plot SNR 
#snr = var(means) / mean(vars)



# Plot
plt.subplot(3, 1, 3)
plt.plot(snr, 'black')
plt.title("SNR Response")


plt.show()