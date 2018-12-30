import wave  
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as scisignal
from scipy.signal.windows import hann
import os
import warnings


def _wav2array(nchannels, sampwidth, data):
    num_samples, remainder = divmod(len(data), sampwidth * nchannels)
    if remainder > 0:
        raise ValueError('The length of data is not a multiple of '
                         'sampwidth * num_channels.')
    if sampwidth > 4:
        raise ValueError("sampwidth must not be greater than 4.")

    if sampwidth == 3:
        a = np.empty((num_samples, nchannels, 4), dtype=np.uint8)
        raw_bytes = np.frombuffer(data, dtype=np.uint8)
        a[:, :, :sampwidth] = raw_bytes.reshape(-1, nchannels, sampwidth)
        a[:, :, sampwidth:] = (a[:, :, sampwidth - 1:sampwidth] >> 7) * 255
        result = a.view('<i4').reshape(a.shape[:-1])
    else:
        # 8 bit samples are stored as unsigned ints; others as signed ints.
        dt_char = 'u' if sampwidth == 1 else 'i'
        a = np.frombuffer(data, dtype='<%s%d' % (dt_char, sampwidth))
        result = a.reshape(-1, nchannels)
    return result


def readwav(file):
    wav = wave.open(file)
    rate = wav.getframerate()
    nchannels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    nframes = wav.getnframes()
    data = wav.readframes(nframes)
    wav.close()
    array = _wav2array(nchannels, sampwidth, data)
    return rate, sampwidth, array


def hps(x, Nfft, fs):
	f = np.arange(Nfft) / Nfft
	xf = np.fft.fft(x, Nfft)
	
	xf = np.abs(xf)
	N = f.size

	n = 5
	smallestLength = int(np.ceil(N / n))
	y = xf[:smallestLength].copy()
	for i in range(2, n+1):
		y *= xf[::i][:smallestLength]
	f = f[:smallestLength] * fs
	return (y, f)


def load3(path_to_file):
    rate, sampwidth,array = readwav(path_to_file)
    # a = array.T[0]
    if (array.shape[1] == 2):
        a = array[:,0] + array[:,1]
    else:
        a = array[:,0]

    signal = a
    n = len(signal)

    fig = plt.figure(figsize=(15, 6), dpi=80)   
    ax = fig.add_subplot(121)
    base_t = np.arange(0, n, 1)
    base_signal = signal
    ax.plot(base_t, base_signal, linestyle='-', color='red')
    ax.set_ylim([min(base_signal), max(base_signal)])

    
    ax = fig.add_subplot(122)
    [hpsS, hpsF] = hps(a * hann(len(a)), a.size, rate)
    ax.plot(hpsF, hpsS)

    newhpsS = hpsS[len(hpsF[hpsF<80]):len(hpsF[hpsF<300])]
    newhpsF = hpsF[len(hpsF[hpsF<80]):len(hpsF[hpsF<300])]

    temp = np.argmax(newhpsS)
    wynik = newhpsF[temp]
    return wynik

    # plt.show()
def gender(vale):
    if(vale < 175):
        return 'M'
    else:
        return 'K'

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    files = os.listdir('./trainall')
    full = len(files)
    results = 0
    if(sys.argv[1] == 'test'):
        for item in files:
            try:
                if('M' in item and 'M' == gender(load3('./trainall/'+item))):
                    results+=1
                elif('K' in item and 'K' == gender(load3('./trainall/'+item))):
                    results+=1
            except RuntimeWarning:
                print('Warning')
        print(results/full)        
    else:
        print(gender(load3(sys.argv[1])))