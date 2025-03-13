import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

fs = 48000
time = 1
samples = int(fs * time)

white_noise = np.random.normal(0, 1, samples)

fc_lpf = 3000
order_lpf = 6
rp_lpf = 0.5
rs_lpf = 50
sos_lpf = scipy.signal.ellip(order_lpf, rp_lpf, rs_lpf, fc_lpf, btype='low', fs=fs, output='sos')
lpf_output = scipy.signal.sosfiltfilt(sos_lpf, white_noise)

f1_bpf = 3000
f2_bpf = 6000
order_bpf = 6
rp_bpf = 0.5
rs_bpf = 50
sos_bpf = scipy.signal.ellip(order_bpf, rp_bpf, rs_bpf, [f1_bpf, f2_bpf], btype='bandpass', fs=fs, output='sos')
bpf_output = scipy.signal.sosfiltfilt(sos_bpf, white_noise)

plt.figure(figsize=(12, 8))

plt.subplot(3, 2, 1)
plt.plot(white_noise[:1000])
plt.title('Реализация белого шума')
plt.grid(True)

plt.subplot(3, 2, 3)
plt.plot(lpf_output[:1000])
plt.title('Реализация СП на выходе ФНЧ')
plt.grid(True)

plt.subplot(3, 2, 5)
plt.plot(bpf_output[:1000])
plt.title('Реализация СП на выходе ПФ')
plt.grid(True)

lags = np.arange(-50, 51)

acf_white_noise = np.correlate(white_noise, white_noise, mode='full')
acf_white_noise = acf_white_noise[len(white_noise)-50-1:len(white_noise)+50]

acf_lpf = np.correlate(lpf_output, lpf_output, mode='full')
acf_lpf = acf_lpf[len(lpf_output)-50-1:len(lpf_output)+50]

acf_bpf = np.correlate(bpf_output, bpf_output, mode='full')
acf_bpf = acf_bpf[len(bpf_output)-50-1:len(bpf_output)+50]

plt.subplot(3, 2, 2)
plt.stem(lags, acf_white_noise)
plt.title('АКФ белого шума')
plt.grid(True)

plt.subplot(3, 2, 4)
plt.stem(lags, acf_lpf)
plt.title('АКФ СП на выходе ФНЧ')
plt.grid(True)

plt.subplot(3, 2, 6)
plt.stem(lags, acf_bpf)
plt.title('АКФ СП на выходе ПФ')
plt.grid(True)

plt.tight_layout()
#plt.show()

nperseg = 256
overlap = 128

freq_wn, psd_wn = scipy.signal.welch(white_noise, fs, nperseg=nperseg, noverlap=overlap)
freq_lpf, psd_lpf = scipy.signal.welch(lpf_output, fs, nperseg=nperseg, noverlap=overlap)
freq_bpf, psd_bpf = scipy.signal.welch(bpf_output, fs, nperseg=nperseg, noverlap=overlap)

plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.plot(freq_wn, psd_wn)
plt.title('СПМ белого шума')
plt.xlabel('Частота, Гц')
plt.ylabel('СПМ')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(freq_lpf, psd_lpf)
plt.title('СПМ СП на выходе ФНЧ')
plt.xlabel('Частота, Гц')
plt.ylabel('СПМ')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.plot(freq_bpf, psd_bpf)
plt.title('СПМ СП на выходе ПФ')
plt.xlabel('Частота, Гц')
plt.ylabel('СПМ')
plt.grid(True)

plt.tight_layout()
plt.show()