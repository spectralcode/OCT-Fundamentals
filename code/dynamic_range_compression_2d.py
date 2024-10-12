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
noise_amp = 10  # Noise amplitude

# Define the number of lines (rows) for the 2D data
n_lines = 100

# Create a new 2D signal array where each row has independent noise
signal_2d_with_noise = np.zeros((n_lines, n_samples))

for i in range(n_lines):
    # Recalculate the noise for each row
    noisy_signal = amp1 * np.cos(2 * np.pi * depth1 * k) + amp2 * np.cos(2 * np.pi * depth2 * k)
    noisy_signal += noise_amp * np.random.normal(size=len(k))
    signal_2d_with_noise[i, :] = noisy_signal

# Rescale each row of the signal to 8-bit range between 0 and 255
signal_2d_8bit = np.zeros_like(signal_2d_with_noise)
for i in range(n_lines):
    signal_8bit = signal_2d_with_noise[i, :] - np.min(signal_2d_with_noise[i, :])  # Shift to make all values positive
    signal_8bit = np.clip(signal_8bit, 0, 255)
    signal_2d_8bit[i, :] = signal_8bit

# Create a 2D grayscale image of the raw signal with recalculated noise for each line
plt.figure()
plt.imshow(signal_2d_8bit, cmap='gray', aspect='auto')
plt.axis('off')  # Remove the axes
plt.title('2D Grayscale Image of Raw OCT Signal')
plt.show()

# Now recompute the FFT and depth profiles for each line with independent noise
depth_profile_2d_with_noise = np.zeros((n_lines, n_samples//2))

for i in range(n_lines):
    fft_signal = np.fft.fft(signal_2d_8bit[i, :])
    fft_signal_normalized = fft_signal / n_samples
    fft_signal_normalized[1:n_samples//2] *= 2  # Multiply the non-DC components by 2
    depth_profile = np.abs(fft_signal_normalized[:n_samples//2])  # Only positive depth
    depth_profile_2d_with_noise[i, :] = depth_profile

# Create a 2D grayscale image of the linear depth profile with recalculated noise for each line
plt.figure()
plt.imshow(depth_profile_2d_with_noise, cmap='gray', aspect='auto')
plt.axis('off')  # Remove the axes
plt.title('Linear Depth Profile')
plt.show()

# Recalculate the logarithmic depth profile for each line with independent noise
log_depth_profile_2d_with_noise = np.zeros((n_lines, n_samples//2))

for i in range(n_lines):
    # Compute the log of the depth profile
    log_depth_profile = 20 * np.log10(depth_profile_2d_with_noise[i, :])  # Convert to decibels
    log_depth_profile_2d_with_noise[i, :] = log_depth_profile

# Quantize the log profile to 8-bit for visualization
min_log = np.min(log_depth_profile_2d_with_noise)
log_depth_profile_quantized_with_noise = log_depth_profile_2d_with_noise - min_log
max_log = np.max(log_depth_profile_quantized_with_noise)
log_depth_profile_quantized_with_noise = (log_depth_profile_quantized_with_noise / max_log) * 255
log_depth_profile_quantized_with_noise = np.round(log_depth_profile_quantized_with_noise).astype(np.uint8)

# Create a 2D grayscale image of the log depth profile with different noise per line
plt.figure()
plt.imshow(log_depth_profile_quantized_with_noise, cmap='gray', aspect='auto')
plt.axis('off')  # Remove the axes
plt.title('Logarithmic Depth Profile')
plt.show()

# Truncate and quantize the log depth profile to 8-bit for better use of dynamic range
min_trunc = -10
log_depth_profile_quantized_truncated_with_noise = log_depth_profile_2d_with_noise - min_trunc
max_trunc = 38
log_depth_profile_quantized_truncated_with_noise = (log_depth_profile_quantized_truncated_with_noise / max_trunc) * 255
log_depth_profile_quantized_truncated_with_noise = np.clip(log_depth_profile_quantized_truncated_with_noise, 0, 255)
log_depth_profile_quantized_truncated_with_noise = np.round(log_depth_profile_quantized_truncated_with_noise).astype(np.uint8)

# Create a 2D grayscale image of the truncated log depth profile with different noise per line
plt.figure()
plt.imshow(log_depth_profile_quantized_truncated_with_noise, cmap='gray', aspect='auto')
plt.axis('off')  # Remove the axes
plt.title('Logarithmic Depth Profile with Min-Max Scaling')
plt.show()
