from scipy.interpolate import interp1d
from scipy.signal import butter,lfilter,lfiltic
from scipy.fftpack import fft
import numpy as np
import math
import time
import csv
import os
import mysql.connector
import sys
# connect to database
config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': '8889',
  'database': 'sensorData',
}
cnx = mysql.connector.connect(**config)#???

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def read():
	cursor=cnx.cursor()
	sql = "SELECT x, y, z, time FROM sensor0 WHERE type = 'Gyroscope'" # get Gyroscope data
	cursor.execute(sql,[])
	xdata=[]
	ydata=[]
	zdata=[]
	tdata=[]
	for (x, y, z, time) in cursor:
		xdata.append(float(x))
		ydata.append(float(y))
		zdata.append(float(z))
		tdata.append(float(time))
	sql = "DELETE FROM sensor0 WHERE time < %s" # delete old data
	list=[]
	list.append(tdata[0]+1000)
	cursor.execute(sql,list)
	cnx.commit()
	cursor.close()
	# cnx.close()
	return xdata[0:200],ydata[0:200],zdata[0:200],tdata[0:200] # return data of fixed window length


def HR(x,y,z,t):
    res = 0
    minimum = min(t)
    t[:] = [i-minimum for i in t]
    #%

    for i in [x, y, z]:
        intervation = 1000.0 / 256
        xx = np.arange(min(t),max(t),intervation)
        # print len(t)
        f2 = interp1d(t, i, kind='cubic')
        yy = f2(xx)
        output = moving_average(yy)
        yy = np.transpose(yy)
        output = np.transpose(output)
        n = 4
        Wn = [10.0 / 128, 13.0 / 128]
        b, a = butter(n,Wn,btype='bandpass')
        filt = lfilter(b, a, output)
        res = filt*filt + res

    r = [math.sqrt(i) for i in res]
    # butterworth filter
    n = 2
    # Wn = [0.75 2.5];
    Wn = [0.75 / 128, 2.5 / 128]
    b, a = butter(n, Wn,btype='bandpass')#,ftype);
    filt = lfilter(b, a, r)
    #% fft
    f = fft(filt)
    f=f[1:]#remove the first component which is the sum of data
    n = len(f)
    power = np.abs(f[0:math.floor(n / 2)]) 
    power = power * power
    nyquist = 0.5
    freq = [i/(n / 2.0) * nyquist for i in range(1,(n/2)+1)]
    period = [1/i for i in freq]
    index=np.argmax(power)
    mainPeriodStr = period[index]
    result = 60000 / (period[index] * intervation)
    return result

if __name__ == "__main__":
	while True:
		x,y,z,t=read()
		print HR(x,y,z,t)
		time.sleep(1)