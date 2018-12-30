# !/usr/local/bin/python3.7
from matplotlib import pyplot as plt
import matplotlib as mp
import numpy as np
import math as mt

from pylab import *
from scipy import *

import wave
import numpy
import struct
import functools
import os
import sys

# import pydub as pd
import subprocess

# from ipywidgets import *
import scipy.io.wavfile
import soundfile as sf
# from soundfile import *
import pyaudio as pa


def read_wave(name):
    fs, dat = scipy.io.wavfile.read(name)
    # print(dat.shape)
    # return [d[0] for d in dat]
    return dat


if __name__ == "__main__":
    # s = pd.AudioSegment.from_file("/train/trainall/001_K.wav", format="wav")
    # w = wave.open('./train/trainall/001_K.wav', 'r')
    # for i in range(w.getnframes()):
    #     frame = w.readframes(i)
    #     print(frame)

    # w, signal = scipy.io.wavfile.read('./train/trainall/001_K.wav')
    # print(signal)

    
    # data, samplerate = sf.read('./train/trainall/002_M.wav')
    # print(samplerate);
    # read_wave('./train/trainall/002_M.wav');