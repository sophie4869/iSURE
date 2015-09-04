from scipy.interpolate import interp1d
from scipy.signal import butter,lfilter,lfiltic
from scipy.fftpack import fft
import numpy as np
import math
import csv

# moving average
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

f=open('/Users/sophie/Documents/iSURE/GG/data/0810_sitting_gyroscope.csv') # path of the data file
csv_f = csv.reader(f)
l=csv_f.line_num
x=[]
y=[]
z=[]
t=[]
for row in csv_f: # get the data
    x.append(float(row[2]))
    y.append(float(row[3]))
    z.append(float(row[4]))
    t.append(float(row[5]))

# pre-processing of blank data?

res = 0
minimum = min(t)
t[:] = [i-minimum for i in t]

for i in [x, y, z]:
    intervation = 1000.0 / 256
    xx = np.arange(min(t),max(t),intervation) # re-sample rate is 256Hz
    f2 = interp1d(t, i, kind='cubic') # cubic interpolation
    yy = f2(xx)
    output = moving_average(yy) # moving average with window size of 3
    yy = np.transpose(yy)
    output = np.transpose(output)
    n = 4
    Wn = [10.0 / 128, 13.0 / 128] # cut-off frequency at 10-13 Hz normalized
    b, a = butter(n,Wn,btype='bandpass') # butterworth filter of order 4
    tfilt = lfilter(b, a, output)
    res = tfilt*tfilt + res

r = [math.sqrt(i) for i in res] # root mean square of 3 dimensions

# butterworth filter
n = 2 # second order
Wn = [0.75 / 128, 2.5 / 128]
b, a = butter(n, Wn,btype='bandpass')
filt = lfilter(b, a, r)

# fft
f = fft(filt)
f=f[1:] # remove the first component which is the sum of data
n = len(f)
power = np.abs(f[0:math.floor(n / 2)]) 
power = power * power
nyquist = 0.5
freq = [i/(n / 2.0) * nyquist for i in range(1,(n/2)+1)]
period = [1/i for i in freq]
index=np.argmax(power)
mainPeriodStr = period[index] # find the max value
result = 60000 / (period[index] * intervation) # result of heart rate
