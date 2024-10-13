import numpy as np
import matplotlib.pyplot as plt

# OCT Simulation Parameters
n_samples = 1024  # Number of samples 
k_min = 2 * np.pi / 880  # Minimum wavenumber
k_max = 2 * np.pi / 820  # Maximum wavenumber
k = np.linspace(k_min, k_max, n_samples)  # Wavenumber vector

# Reflectivity simulation (in the wavenumber domain)
# Simulating two layers with different reflectivities (first layer high, second low)
amp1 = 80  # Reflectivity of the first layer (high)
depth1 = 60000  # Depth of first layer

amp2 = 8  # Reflectivity of the second layer (low)
depth2 = 500000  # Depth of second layer

# Simulating the OCT signal in the k domain as a sum of sine waves
signal = amp1 * np.cos(2 * np.pi * depth1 * k) + amp2 * np.cos(2 * np.pi * depth2 * k)

# Add noise to simulate real OCT conditions
noise_amp = 10  # Noise amplitude
signal += noise_amp * np.random.normal(size=len(k))

# Convert signal to positive 8-bit integer
signal_8bit = signal - np.min(signal)  
signal_8bit = np.clip(signal_8bit, 0, 255)
signal_8bit = np.round(signal_8bit).astype(np.uint8)     

# Plot the raw OCT signal in the k-domain (wavenumber domain)
plt.figure()
plt.plot(k, signal_8bit)
plt.title('Raw OCT Signal (8-bit)')
plt.xlabel('Wavenumber k')
plt.ylabel('Amplitude (8-bit)')
plt.grid(True)
plt.show()

# Perform FFT to get the depth profile (A-scan)
fft_signal = np.fft.fft(signal_8bit)

# Normalize the FFT output by the number of samples
fft_signal_normalized = fft_signal / n_samples

# Multiply the non-DC components by 2
fft_signal_normalized[1:n_samples//2] *= 2

# Extract the frequency bins and compute the depth profile
z = np.fft.fftfreq(n_samples, d=(k[1] - k[0]))  # Convert frequency bins to depth (z)
depth_profile = np.abs(fft_signal_normalized)  # Get magnitude of the normalized FFT

# Plot the depth profile (A-scan) after FFT
plt.figure()
plt.plot(z[:n_samples//2], depth_profile[:n_samples//2])  # Only plot positive depths
plt.title('Depth Profile (A-scan)')
plt.xlabel('Depth (z)')
plt.ylabel('Reflectivity Amplitude')
plt.grid(True)
plt.show()

# Logarithmic representation of the depth profile (for better dynamic range visualization)
log_depth_profile = 20 * np.log10(depth_profile)  # Convert to decibels

# Plot the logarithmic depth profile
plt.figure()
plt.plot(z[:n_samples//2], log_depth_profile[:n_samples//2])
plt.title('Logarithmic Depth Profile (A-scan)')
plt.xlabel('Depth (z)')
plt.ylabel('Log Reflectivity Amplitude (dB)')
plt.grid(True)
plt.show()

# Quantize the log profile to 8-bit for visualization (common in OCT)
min = np.min(log_depth_profile[:n_samples//2])
log_depth_profile_quantized = log_depth_profile[:n_samples//2] - min
max = np.max(log_depth_profile_quantized)
log_depth_profile_quantized = (log_depth_profile_quantized / max) * 255
log_depth_profile_quantized = np.round(log_depth_profile_quantized).astype(np.uint8)

# Plot the 8-bit quantized depth profile
plt.figure()
plt.plot(z[:n_samples//2], log_depth_profile_quantized)
plt.title('8-bit Quantized Logarithmic Depth Profile (A-scan)')
plt.xlabel('Depth (z)')
plt.ylabel('Log Reflectivity Amplitude (8-bit)')
plt.grid(True)
plt.show()

# Truncate the log profile to make better use of the 8-bit for visualization (common in OCT)
min = -10
log_depth_profile_quantized_truncated = log_depth_profile[:n_samples//2] - min
max = 38
log_depth_profile_quantized_truncated = (log_depth_profile_quantized_truncated / max) * 255
log_depth_profile_quantized_truncated = np.clip(log_depth_profile_quantized_truncated, 0, 255)
log_depth_profile_quantized_truncated = np.round(log_depth_profile_quantized_truncated).astype(np.uint8)

# Plot the 8-bit truncated quantized depth profile
plt.figure()
plt.plot(z[:n_samples//2], log_depth_profile_quantized_truncated)
plt.title('8-bit Truncated Quantized Logarithmic Depth Profile (A-scan)')
plt.xlabel('Depth (z)')
plt.ylabel('Log Reflectivity Amplitude (8-bit)')
plt.grid(True)
plt.show()




