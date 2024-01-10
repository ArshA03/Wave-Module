# Help

## Fast Fourier Transform

### 1. How FFT Works

Please watch this helpful [Video](https://www.youtube.com/watch?v=mkGsMWi_j4Q) on youtube to understand how FFT works:

* The number of frequency points in FFT spectrum is related to the number sample points of waveform.

$$
Number\ of\ Frequency \ Points = \frac{N=Number\ Data\ Points}{2} \\
$$

* After deleting the data behind the Nyquist limit, the magnitudes should be doubled and divided by the number of samples.

---

### 2. Frequency Resolution

The output of `find_peaks` method itself doesn't match with the real data and there is an offset while plotting the raw results. Therefore the results should be corrected.

The problem is apparently the fact that the `find_peaks` method in `scipy.signal` has a frequency resolution of  1 Hz, therefore since we are dealing with a continuous frequency spectrum, the frequency resolution should be reformed by multiplying the obtained peak frequencies by the frequency resolution of our present waveform.

$$
\Delta F\ (Frequency\ Resolution) = \frac{Fs= Sample\ Rate}{N=number\  of\ sample\  points}
$$

$$
Corrected\ Peak\ Values=(Current\ Peak\ Values)\times\Delta F
$$

>For further details please check [Frequency Resolution in FFT Spectrum](https://www.onosokki.co.jp/English/hp_e/c_support/faq/fft_common/fft_general_4.htm)