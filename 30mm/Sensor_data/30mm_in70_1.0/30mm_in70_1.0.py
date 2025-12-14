import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

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

script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "30mm_in70_1.0.csv"
#Global Constants
FILE_PATH=os.path.join(script_dir, file_name)

#file read
df = pd.read_csv(FILE_PATH, delimiter=";")


timestamp_ms = df['Timestamp'].values
pressure_data = df['Pressure_data'].values


#file process
start=first_true_min(pressure_data)
end=binarySearch(timestamp_ms, 20507)
timestamp_ms=timestamp_ms[start:end]
pressure_data=pressure_data[start:end]
correction=np.mean(pressure_data)

#Graph of Pressure change in time

plt.plot(timestamp_ms, pressure_data)
plt.title("Pressure change in time (30mm 70° 1.0)")
plt.ylabel("Pressure (kPa)")
plt.xlabel("Time (ms)")
plt.grid()
plt.savefig(os.path.join(script_dir, "30mm_in70_1.0_p(t).pdf"), format="pdf")
plt.clf()
#Fourier Transform of Pressureoscillation
pre_fourier_pressure=pressure_data-correction

yf0 = np.fft.fft(pre_fourier_pressure)
xf0 = np.fft.fftfreq(len(pre_fourier_pressure), 1/140)
xf=xf0[:math.ceil(len(xf0)/2)]
yf=yf0[:math.ceil(len(xf0)/2)]
#Graph of Fourier Transform
plt.plot(xf, yf)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.grid()
plt.title("Frequency spectrum of the \nPressure oscillation (30mm 70° 1.0)")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "30mm_in70_1.0_fft.pdf"), format="pdf")
plt.clf()


N = len(pre_fourier_pressure)
power_spectrum = (np.abs(yf)**2)/(N*140)

f_dominant_index, max_amplitude, f_dominant = good_max(power_spectrum, xf)

plt.plot(xf, power_spectrum)
plt.plot(f_dominant, max_amplitude, 'ro',markersize=4)
plt.title("Frequency Power Spectrum of Pressure\n Oscillation (30mm 70° 1.0)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|Amplitude|^2")
plt.annotate(
    f'x = {f_dominant:.2f} Hz',
    (f_dominant, max_amplitude),
    textcoords="offset points",
    xytext=(0, 5),
    ha='center',
)
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "30mm_in70_1.0_powspec.pdf"), format="pdf")
plt.clf()





