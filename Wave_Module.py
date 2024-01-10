import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks , hilbert
import scipy.fft as ft


############## Calling Data ###############

def Input(data):
    data_frame = pd.read_csv(data, sep="\t"
                            , header=None)
    
    headers = []
    for i in range(1, len(data_frame.columns)+1):
        headers.append('channel'+str(i))
    
    data_frame.columns = headers
    return data_frame

# # we can define a function to call datas from specific sets (in set '1', each data has two channels But in set '2' and '3', each data has one channel)
# def input1(self):  # This function is used to call datas from set '1'
#     data = pd.read_csv(self.data, sep="\t", header=None)
#     data.columns = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']  # Based on original Document (each bearing has two channels respectively)
#     return data

# def input(data):  # This function is used to call datas from set '2' & '3'
#     data = pd.read_csv(data, sep="\t", header=None)
#     data.columns = ['ch1', 'ch2', 'ch3', 'ch4']  # Based on original Document (channels for Bearings 1, 2, 3, 4)
#     return data


############# Wave Transforms #################
# This function Measures the FFT of given data
class wave:

    def __init__(self, data, Fs):
        self.data = data
        self.Fs = Fs  # sampling rate
        L = len(data)
        self.L = L

    def envelope(self, method):
        env = self.Envelope(self.data, self.Fs)
        if method == 'waveform':
            return env.waveform()
        elif method == 'FFT':
            return env.FFT()
        elif method == 'peaks':
            params = input('Define peak parameters (prominence, threshold,'
                            + " height, width, distance). Write 'd' to use default value."
                            + "\nFor instance: 50,130,d,d,30")
            params = params.split(',')

            for i in range(0,len(params)):
                if params[i] == 'd':
                    params[i] = None
                else:
                    params[i] = int(params[i])

            params_dic = {'prominence':params[0], 'threshold':params[1], 'height':params[2], 'width':params[3], 'distance':params[4]}

            return env.peaks(**params_dic)
        else:
            raise NameError(f"There is no method called '{str(method)}'\nYou can only use 'waveform', 'FFT', 'peaks'")


    # To plot the time waveform, we need to arrange a time set with length of our sample duration
    def time(self):
        data = self.data
        Fs = self.Fs # sampling rate
        dt = 1/Fs # sampling interval
        t = np.arange(0, len(data)*dt, dt)
        return t

    def FFT(self):
        data = self.data
        L = self.L
        Fs = self.Fs
        
        # L is equal to len(S)
        S = ft.fft(data)
        # X = np.abs(S)[0:int(len(S)/2)]
        # X = np.abs(S)[0:Fs/2]
        X = np.abs(S[0:L//2])
        freqs = ft.fftfreq(L , d=1/Fs)[:L//2]
        # freqs = freqs[freqs>=0]
        magnitude = 2*X/L
        return freqs, magnitude
    
    # this function measures the peak values inside FFT
    def peaks(self, prominence=None, threshold=None, height=None, width=None, distance=None):
        Fs = self.Fs
        L = self.L
        data = self.data
        
        # En = L/2
        S = ft.fft(data)
        # X = np.abs(S)[0:int(En)]
        X = np.abs(S[0:L//2])
        N = Fs/L
        peaks, _ = find_peaks(X, threshold=threshold, prominence=prominence, height=height, width=width, distance=distance)
        return peaks*N

    ################ Nested Envelope Class #################
    class Envelope():

        def __init__(self, data, Fs):
            wave.__init__(self, data, Fs)
            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)
            self.env_data = amplitude_envelope
            
        def waveform(self):
            data = self.env_data
            return data
        
        def FFT(self):
            data = self.data
            Fs = self.Fs

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            L = len(amplitude_envelope)
            En = L/2
            S = ft.fft(amplitude_envelope)
            # X = np.abs(S)[0:int(En)]
            X = np.abs(S[0:L//2])
            freqs = ft.fftfreq(L , d=1/Fs)[:L//2]
            # freqs = freqs[freqs>=0]
            magnitude = 2*X/L
            return freqs, magnitude   
        
        def peaks(self, prominence=None, threshold=None, height=None, width=None, distance=None):
            Fs = self.Fs
            L = self.L
            data = self.env_data
            
            En = L/2
            S = ft.fft(data)
            # X = np.abs(S)[0:int(En)]
            X = np.abs(S[0:L//2])
            N = Fs/L
            peaks, _ = find_peaks(X, threshold=threshold, prominence=prominence, height=height, width=width, distance=distance)
            return peaks*N


# ################ Envelope Class #################
# class envelope(wave):

#     def __init__(self, data, Fs):
#         super().__init__(data, Fs)
#         analytic_signal = hilbert(data)
#         amplitude_envelope = np.abs(analytic_signal)
#         self.env_data = amplitude_envelope
        
#     def waveform(self):
#         data = self.env_data
#         return data
    
#     def FFT(self):
#         data = self.data
#         Fs = self.Fs

#         analytic_signal = hilbert(data)
#         amplitude_envelope = np.abs(analytic_signal)

#         L = len(amplitude_envelope)
#         En = L/2
#         S = ft.fft(amplitude_envelope)
#         # X = np.abs(S)[0:int(En)]
#         X = np.abs(S[0:L//2])
#         freqs = ft.fftfreq(L , d=1/Fs)[:L//2]
#         # freqs = freqs[freqs>=0]
#         magnitude = 2*X/L
#         return freqs, magnitude   
    
#     def peaks(self, prominence=None, threshold=None, height=None, width=None, distance=None):
#         Fs = self.Fs
#         L = self.L
#         data = self.env_data
        
#         En = L/2
#         S = ft.fft(data)
#         # X = np.abs(S)[0:int(En)]
#         X = np.abs(S[0:L//2])
#         N = Fs/L
#         peaks, _ = find_peaks(X, threshold=threshold, prominence=prominence, height=height, width=width, distance=distance)
#         return peaks*N