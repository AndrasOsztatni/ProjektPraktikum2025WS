import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os

#Predefinied Functions
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


def main(source, starting_index):
    #Global Constants
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_NAME = source
    FOLDER_NAME = source[:-4]
    OPNENING_TYPE = FILE_NAME.split("_")[0]
    INCLINE = FILE_NAME.split("_")[1][2:]
    VERSION = FILE_NAME.split("_")[2][:-4]
    FOLDER_PATH = os.path.join(SCRIPT_DIR, OPNENING_TYPE, FOLDER_NAME)
    FILE_PATH = os.path.join(SCRIPT_DIR, OPNENING_TYPE, FOLDER_NAME, FILE_NAME)
    N_SEGMENTS = 10

    #Fileread
    df = pd.read_csv(FILE_PATH, delimiter=";")

    timestamp_ms = df['Timestamp'].values
    pressure_data = df['Pressure_data'].values


    #File process
    start=first_true_min(pressure_data)
    end=binarySearch(timestamp_ms, starting_index)
    timestamp_ms=timestamp_ms[start:end]
    pressure_data=pressure_data[start:end]


    total_length = len(pressure_data)
    segment_length = total_length // N_SEGMENTS
    Fs = 140
    fig, axes = plt.subplots(N_SEGMENTS, 1, figsize=(10, 2 * N_SEGMENTS), sharex=True)
    fig.suptitle(f'Frequency Spectrum of {N_SEGMENTS} Data Segments (SFFT)\n(30mm 45° 1.0)', fontsize=16)
    f_dominants = []

    # 3. Iterate through each segment
    for i in range(N_SEGMENTS):
        start_idx = i * segment_length
        end_idx = (i + 1) * segment_length
        
        pre_correction_segment = pressure_data[start_idx:end_idx]
        segment = pre_correction_segment-np.mean(pre_correction_segment)
        
        window = np.hanning(len(segment))
        windowed_segment = segment * window

        N = len(windowed_segment)
        yf = np.fft.fft(windowed_segment)
        
        xf = np.fft.fftfreq(N, 1/Fs)
        
        N_half = N // 2
        xf_positive = xf[:N_half]
        
        yf_magnitude = np.abs(yf[:N_half]) * 2 / N  

        f_dominants.append(xf[np.argmax(yf_magnitude)])

        #Plot the spectrum
        ax = axes[i]
        ax.plot(xf_positive, yf_magnitude)
        ax.set_title(f'Segment {i+1} (Time: {timestamp_ms[start_idx]/1000:.2f}s - {timestamp_ms[end_idx-1]/1000:.2f}s)', fontsize=8)
        ax.set_ylabel('Magnitude', fontsize=8)
        ax.grid(True, alpha=0.5)


    axes[-1].set_xlabel('Frequency (Hz)', fontsize=12)
    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    plt.savefig(os.path.join(SCRIPT_DIR, "30mm_in45_1.0_sfft.pdf"), format="pdf")
    plt.clf()

    linsp = [i for i in range(1, N_SEGMENTS+1)]

    '''plt.figure(figsize=(12, 6))
    plt.plot(linsp, f_dominants)
    plt.xlabel("Segments")
    plt.ylabel("Dominant Frequency (Hz)")
    plt.grid()
    plt.title("Dominant Frequencies in the Segments \n (30mm 45° 1.0)")
    plt.savefig(os.path.join(SCRIPT_DIR, "30mm_in45_1.0_f(segments).pdf"), format="pdf")
    plt.clf()'''



