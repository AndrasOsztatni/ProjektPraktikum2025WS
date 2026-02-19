import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

#Definition of used Functions
def first_max(list):
    for i in range(0, len(list)):
        if list[i]<list[i+1] and list[i+2]<list[i+1]:
            return i+1

def first_true_min(list):
    for i in range(first_max(list), len(list)):
        if list[i]>list[i+1] and list[i+2]>list[i+1] and list[i]<95000:
            return i+1

def binarySearch(list, target):
    left = 0
    right = len(list) - 1
    while left <= right:
        mid = (left + right) // 2
        if list[mid] == target:
            return mid
        if list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def good_max(list, control):
    index, amplitude, frequency=0, 0, 0
    start = first_true_min(list)
    index = np.argmax(list[start:])+start
    amplitude = list[index]
    frequency = control[index]
    return index, amplitude, frequency

def opt_line(x: float, sl: float, inter: float):
    return sl*x+inter


def main(source, start_time, end_time):
    #Global Constants
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_NAME = source
    FOLDER_NAME = source[:-4]
    OPNENING_TYPE = FILE_NAME.split("_")[0]
    INCLINE = FILE_NAME.split("_")[1][2:]
    VERSION = FILE_NAME.split("_")[2][:-4]
    FOLDER_PATH = os.path.join(SCRIPT_DIR, OPNENING_TYPE, FOLDER_NAME)
    FILE_PATH = os.path.join(SCRIPT_DIR, OPNENING_TYPE, FOLDER_NAME, FILE_NAME)

    #file read
    df = pd.read_csv(FILE_PATH, delimiter=";")
    if start_time: 
        start_index = binarySearch(df['Timestamp'].values, start_time)
        timestamp_ms = df['Timestamp'].values[start_index:]
        pressure_data = df['Pressure_data'].values[start_index:]
    else:
        timestamp_ms = df['Timestamp'].values
        pressure_data = df['Pressure_data'].values
    #file process
    start=first_true_min(pressure_data)
    end=binarySearch(timestamp_ms, end_time)
    timestamp_ms=timestamp_ms[start:end]
    pressure_data=pressure_data[start:end]
    correction=np.mean(pressure_data)
    
    
    #Graph of Pressure change in time

    plt.plot(timestamp_ms, pressure_data)
    plt.title(f"Pressure change in time ({OPNENING_TYPE} {INCLINE}° {VERSION})")
    plt.ylabel("Pressure (kPa)")
    plt.xlabel("Time (ms)")
    plt.grid()
    plt.savefig(os.path.join(FOLDER_PATH, FOLDER_NAME+"_p(t).pdf") , format="pdf")
    plt.clf()
    #Fourier Transform of Pressureoscillation
    pre_fourier_pressure=pressure_data-correction
    slope, intercept, r, p, std_err = stats.linregress(timestamp_ms, pre_fourier_pressure)
    
    for i in range(len(timestamp_ms)):
        pre_fourier_pressure[i]-=opt_line(timestamp_ms[i], slope, intercept)

    yf0 = np.fft.fft(pre_fourier_pressure)
    xf0 = np.fft.fftfreq(len(pre_fourier_pressure), 1/56)
    xf=xf0[:math.ceil(len(xf0)/2)]
    yf=yf0[:math.ceil(len(xf0)/2)]
    #Graph of Fourier Transform
    plt.plot(xf, yf)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.title(f"Frequency spectrum of the \nPressure oscillation ({OPNENING_TYPE} {INCLINE}° {VERSION})")
    plt.tight_layout()
    plt.savefig(os.path.join(FOLDER_PATH, FOLDER_NAME+"_fft.pdf"), format="pdf")
    plt.clf()


    N = len(pre_fourier_pressure)
    power_spectrum = (np.abs(yf)**2)/(N*140)

    f_dominant_index, max_amplitude, f_dominant = good_max(power_spectrum, xf)

    plt.plot(xf, power_spectrum)
    plt.plot(f_dominant, max_amplitude, 'ro',markersize=4)
    plt.title(f"Frequency Power Spectrum of Pressure\n Oscillation ({OPNENING_TYPE} {INCLINE}° {VERSION})")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("|Amplitude|^2")
    plt.annotate(
        f'x = {f_dominant:.2f} Hz',
        (f_dominant, max_amplitude),
        textcoords="offset points",
        xytext=(50, 0),
        ha='center',
        fontsize=14
    )
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(FOLDER_PATH, FOLDER_NAME+"_powspec.pdf"), format="pdf")
    plt.clf()





