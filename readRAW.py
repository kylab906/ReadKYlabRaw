# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 17:51:04 2018

@author: KYLAB
"""
#%% Get the files pathway

import tkinter as tk  
from tkinter import filedialog  
##import numpy as np
import math
import matplotlib.pyplot as plt

'''  
root = tk.Tk()                #windows適用        
root.withdraw()             # we don't want a full GUI, so keep the root window from appearing
 
default_dir = r"D:\Python"  # Setting default Folder

fname = filedialog.askopenfilename(title = u'選擇文件', 
                                           initialdir = default_dir,
                                           filetypes = [("raw files", "*.raw"), ("allfiles", "*")]
                                           )
#print(fname)
#print (filedialog.askdirectory())  # 返回目录路径
'''
#%% Open RAW file in python

Raw_Data = open('/Users/hanli/onedrive/EEGdevicetest/190226.raw', "rb").read()

RAW = []
for s in Raw_Data:
    RAW.append(s)

header = RAW[0:512]             #RAW files header
#RAW = RAW[512:len(RAW)]         #RAW data

header2 = []                    #RAW files header to String
for s in header:
    header2.append(chr(s))

#%% Acquisition sampling rate ratio
    
splr = header2[39:54]   
splr2 = ''.join(splr)
splr2 = float(splr2)        #Sampling Rate

start = 55
SRn = []
for i in range(header[36]):     #Acquisition sampling rate ratio SRn
    SRtemp = header2[start+i*15+i:start+(i+1)*15+i]
    splrtemp = ''.join(SRtemp)
    splr_float = float(splrtemp)
    SRn.append(splr2/splr_float)

maxi = int(max(SRn))

#%%  Find the Channel 


#matrix = np.zeros([maxi,header[36]])
channel=[]
for i in range(maxi) :
    for j in range(header[36]):
        #matrix[i][j] = i
        if i % SRn[j] == 0:
            channel.append(j)

#%% Data segmentation
#Data = np.zeros([header[36],])
Data = []
cont = []
for i in range(header[36]):
    Data.append([])
    cont.append(1)
           
Raw_Data = RAW[512:math.floor((len(RAW)-512)/len(channel))*len(channel)+512]
for i in range(0, len(Raw_Data), len(channel)*2):
    for j in range(len(channel)):
        Data[channel[j]].append(Raw_Data[i + 2*j+1]*256+Raw_Data[i + 2*j])
    
data = []
data1 = []
for i in Data[0]:      #數值校正
    j = i/65535*1.8/2000
    data.append(j)
for i in Data[1]:      #數值校正
    j = i/65535*1.8/2000
    data1.append(j)

plt.subplot(2,1,1)
plt.plot(data, 'k')
plt.xlabel('Point(CH1)')
plt.ylabel('Volts')
plt.subplot(2,1,2)
plt.plot(data1, 'k')
plt.xlabel('Point(CH2)')
plt.ylabel('Volts')


#with open (fname,'r', errors='ignore') as f:
#    content = f.readline(512)
# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content]

