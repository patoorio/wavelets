# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 09:58:47 2016

@author: porio
"""


from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import wavelets

#%% Build and plot a signal to work with

dt=0.005
time=np.arange(0,50,dt)

fbasal1,fbasal2=25,15
amp1,amp2=1,2
bias=55
ampruido=0.2
chrpini,chrpstp=15,30

x=bias + amp1*np.sin(2*np.pi*fbasal1*time) + amp2*np.sin(2*np.pi*fbasal2*time)
x+=np.random.normal(size=len(x))*ampruido

x2=1.2*np.cos(2*np.pi*0.8*(time-chrpini)**2) * (time-chrpini)*np.exp(-(time-chrpini)/10)
x2[(time<chrpini)+(time>chrpstp)]=0
x+=x2

#%%  Wavelet transfom - linearly spaced scales

desiredFreq=np.arange(1,40,0.2)  # Frequencies we want to analyse
desiredPeriods=1/(desiredFreq*dt)
scales=desiredPeriods/wavelets.Morlet.fourierwl  # scales

wavel1=wavelets.Morlet(x,scales=scales)

pwr1=np.sqrt(wavel1.getnormpower())  # Normalized power

fmin=min(desiredFreq)
fmax=max(desiredFreq)


#%% Plot the results  -  add a spectrogram for comparison

plt.figure(1,figsize=(12,4)) 
plt.clf()
plt.subplot(311)
plt.plot(time,x,alpha=1)
plt.xlabel('Time (s)')
plt.xlim((0,50))

plt.subplot(312)
plt.specgram(x-np.mean(x),Fs=1/dt,NFFT=128,noverlap=64);
plt.ylim((0,50))
ax1=plt.subplot(313)

plt.imshow(pwr1,cmap='RdBu',vmax=np.max(pwr1),vmin=-np.max(pwr1),
           extent=(min(time),max(time),fmin,fmax),origin='lower', 
           interpolation='none',aspect='auto')
#ax1.set_yscale('log')
ax1.set_ylabel('Frequency (Hz)')

#%%  Wavelet transfom - log-spaced scales

desiredFreq=np.logspace(0.5,2,60)  # Frequencies we want to analyse - from ~3 to 100
desiredPeriods=1/(desiredFreq*dt)
scales=desiredPeriods/wavelets.Morlet.fourierwl  # scales

wavel1=wavelets.Morlet(x,scales=scales)

pwr1=wavel1.getnormpower()  # Normalized power

fmin=min(desiredFreq)
fmax=max(desiredFreq)

#%% Plot the results

plt.figure(2,figsize=(12,4)) 
plt.clf()
plt.subplot(211)
plt.plot(time,x,alpha=1)
plt.xlabel('Time (s)')
plt.xlim((0,50))

ax1=plt.subplot(212)

plt.imshow(pwr1,cmap='RdBu',vmax=np.max(pwr1),vmin=-np.max(pwr1),
           extent=(min(time),max(time),fmin,fmax),origin='lower', 
           interpolation='none',aspect='auto')
ax1.set_yscale('log')
ax1.set_ylabel('Frequency (Hz)')



#%% Changing _omega
#  *** ESTO NO FUNCIONA BIEN TODAVÍA ***

omega=5
wavelets.Morlet._omega0=omega

desiredFreq=np.arange(1,40,0.2)  # Frequencies we want to analyse
desiredPeriods=1/(desiredFreq*dt)
fourierwl=4* np.pi/(omega + np.sqrt(2.0 + omega**2))
scales=desiredPeriods/fourierwl  # scales

wavel1=wavelets.Morlet(x,scales=scales)

pwr1=np.sqrt(wavel1.getnormpower())  # Normalized power

fmin=min(desiredFreq)
fmax=max(desiredFreq)

#%% Plot the results  -  add a spectrogram for comparison

plt.figure(3,figsize=(12,4)) 
plt.clf()
plt.subplot(211)
plt.plot(time,x,alpha=1)
plt.xlabel('Time (s)')
plt.xlim((0,50))

ax1=plt.subplot(212)

plt.imshow(pwr1,cmap='RdBu',vmax=np.max(pwr1),vmin=-np.max(pwr1),
           extent=(min(time),max(time),fmin,fmax),origin='lower', 
           interpolation='none',aspect='auto')
# ax1.set_yscale('log')
ax1.set_ylabel('Frequency (Hz)')
