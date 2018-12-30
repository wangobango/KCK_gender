# !/usr/local/bin/python3.7
import matplotlib as mp
import numpy as np
import math as mt
import wave
import struct
import functools
import os
import sys

# import pydub as pd
import subprocess

# from ipywidgets import *
import scipy.signal as ss
import soundfile as sf

def read_wave(name):
    name = './trainall/'+name
    data, samplerate = sf.read(name)
    return np.asarray(data), samplerate

def decimate(wave):
    temp = np.fft.fft(wave)
    return np.asarray(ss.decimate(temp,13,zero_phase = False))

if __name__ == "__main__":
    if(sys.argv[1] == 'test'):
        files = os.listdir('./trainall')
        males = 0
        females = 0
        errors = 0
        allV = len(files)
        for item in files:
            data, rate = read_wave(item)
            signals = []
            signals.append(data)
            for i in range(7):
                data = decimate(data)
                signals.append(data)

            valueErr = False

            for i in range(1,7):
                try:
                    signals[0] = np.multiply(signals[0],signals[i])
                except ValueError:
                    print("VALUE ERROR")
                    errors+=1
                    valueErr = True
                    break

            if(not(valueErr)):
                result = np.argmax(signals[0])/rate
                if(result < 2 and 'M' in item):
                    males+=1
                elif(result > 2 and 'K' in item):
                    females +=1
                # print(np.argmax(signals[0])/rate)
        
        print((males+females)/allV)
        print(males)
        print(females)
        print(allV)
        print(errors)

    else:
        data, rate = read_wave(sys.argv[1])
        signals = []
        signals.append(data)
        for i in range(7):
            data = decimate(data)
            signals.append(data)

        valueErr = False

        for i in range(1,7):
            try:
                signals[0] = np.multiply(signals[0],signals[i])
            except ValueError:
                print("VALUE ERROR")
                valueErr = True
                break

        if(not(valueErr)):
            print(np.argmax(signals[0])/rate)

   