import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ncycles = 18
efficiency = 0.8
n0 = 1 # initial number of transcripts

Ncycles= np.arange(0,ncycles)+1
nf = np.array([0.0] * len(Ncycles))

N0 = np.array([0.0]) * len(n0)
nf =  n0 * np.power(2,efficiency*ncycles)

plt.figure()
plt.plot(Ncycles, nf, '-ro')