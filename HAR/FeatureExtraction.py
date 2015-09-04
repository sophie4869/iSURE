# usage: python FeatureExtraction.py <input.csv> <output.arff>
# attention: the input file must be with single label data

import csv,math
import sys
win_len=60
win_half=win_len/2
f=open(sys.argv[1])
csv_f = csv.reader(f)
xs=[]
ys=[]
zs=[]
label=[]
for row in csv_f:
	label.append(row[0])
	xs.append(row[1])
	ys.append(row[2])
	zs.append(row[3])

l=csv_f.line_num
lh=l/2

mean={'x':[],'y':[],'z':[]} # mean
new_label=[] # label
rms={'x':[],'y':[],'z':[]} # root mean square
sd={'x':[],'y':[],'z':[]} # standard deviation
var={'x':[],'y':[],'z':[]} # variance
mad={'x':[],'y':[],'z':[]} # mean absolute deviation

for i in range(0,l-win_len,win_half):
	sum={'x':0,'y':0,'z':0}
	sum2={'x':0,'y':0,'z':0} #squre
	sum3={'x':0,'y':0,'z':0} #SD
	sum4={'x':0,'y':0,'z':0} #mad
	for j in range(i,i+win_len):
		sum['x']+=float(xs[j])
		sum['y']+=float(ys[j])
		sum['z']+=float(zs[j])
		sum2['x']+=float(xs[j])*float(xs[j])
		sum2['y']+=float(ys[j])*float(ys[j])
		sum2['z']+=float(zs[j])*float(zs[j])
	mean['x'].append(sum['x']/win_len)
	mean['y'].append(sum['y']/win_len)
	mean['z'].append(sum['z']/win_len)
	rms['x'].append(math.sqrt(sum2['x']/win_len))
	rms['y'].append(math.sqrt(sum2['y']/win_len))
	rms['z'].append(math.sqrt(sum2['z']/win_len))
	for j in range(i,i+win_len):
		sum3['x']+=(float(xs[j])-mean['x'][i/win_half])**2
		sum3['y']+=(float(ys[j])-mean['y'][i/win_half])**2
		sum3['z']+=(float(zs[j])-mean['z'][i/win_half])**2
		sum4['x']+=abs(float(xs[j])-mean['x'][i/win_half])
		sum4['y']+=abs(float(ys[j])-mean['y'][i/win_half])
		sum4['z']+=abs(float(zs[j])-mean['z'][i/win_half])
	var['x'].append(sum3['x']/(win_len-1))
	var['y'].append(sum3['y']/(win_len-1))
	var['z'].append(sum3['z']/(win_len-1))
	sd['x'].append(math.sqrt(sum3['x']/(win_len-1)))
	sd['y'].append(math.sqrt(sum3['y']/(win_len-1)))
	sd['z'].append(math.sqrt(sum3['z']/(win_len-1)))
	mad['x'].append(math.sqrt(sum4['x']/(win_len-1)))
	mad['y'].append(math.sqrt(sum4['y']/(win_len-1)))
	mad['z'].append(math.sqrt(sum4['z']/(win_len-1)))
	new_label.append(label[i])

# rms sd var mad
rows=[]
for i in range(0,len(new_label)-1):
	row=[new_label[i],mean['x'][i],mean['y'][i],mean['z'][i],rms['x'][i],rms['y'][i],rms['z'][i],sd['x'][i],sd['y'][i],sd['z'][i],var['x'][i],var['y'][i],var['z'][i],mad['x'][i],mad['y'][i],mad['z'][i]]
	rows.append(row)

# print rows
fo=open(sys.argv[2],'wb')
writer=csv.writer(fo)
writer.writerow(["label","mean_x","mean_y","mean_z","RMS_x","RMS_y","RMS_z","SD_x","SD_y","SD_z","VAR_x","VAR_y","VAR_z","MAD_x","MAD_y","MAD_z"])
writer.writerows(rows)
fo.close()