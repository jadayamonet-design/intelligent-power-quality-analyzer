import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# INTELLIGENT POWER QUALITY ANALYZER
# Software Version 1
# --------------------------------------------------

# Signal settings
frequency = 60          # Hz
sample_rate = 10000     # samples per second
duration = 0.1          # seconds

# Simulated electrical values
nominal_voltage = 10.0
voltage_rms_expected = 10.0     # volts
current_rms_expected = 0.5      # amps
phase_angle = 30                 # degrees

# Convert RMS values to peak values
voltage_peak = voltage_rms_expected * np.sqrt(2)
current_peak = current_rms_expected * np.sqrt(2)

# Convert phase angle from degrees to radians
phase_radians = np.deg2rad(phase_angle)

# Create time samples
time = np.arange(0, duration, 1 / sample_rate)

# Generate simulated 60-Hz voltage and current waveforms
voltage = voltage_peak * np.sin(2 * np.pi * frequency * time)

current = current_peak * np.sin(
    2 * np.pi * frequency * time - phase_radians
)

# Calculate RMS values from the generated samples
voltage_rms = np.sqrt(np.mean(voltage ** 2))
current_rms = np.sqrt(np.mean(current ** 2))

# Calculate real power
real_power = np.mean(voltage * current)

# Calculate apparent power
apparent_power = voltage_rms * current_rms

# Calculate power factor
power_factor = real_power / apparent_power

# Calculate reactive power
reactive_power = np.sqrt(
    max(apparent_power ** 2 - real_power ** 2, 0)
)

# Estimate frequency using positive-going zero crossings
zero_crossings = np.where(
    (voltage[:-1] < 0) & (voltage[1:] >= 0)
)[0]

crossing_times = time[zero_crossings]

periods = np.diff(crossing_times)

measured_period = np.mean(periods)

measured_frequency = 1 / measured_period

# --------------------------------------------------
# FFT AND HARMONIC ANALYSIS
# --------------------------------------------------

# Add a controlled 3rd harmonic for FFT testing
third_harmonic_frequency = 3 * frequency
third_harmonic_percent = 10

third_harmonic_peak = (
    voltage_peak * third_harmonic_percent / 100
)

voltage_with_harmonic = (
    voltage
    + third_harmonic_peak
    * np.sin(2 * np.pi * third_harmonic_frequency * time)
)

# Perform FFT
number_of_samples = len(voltage_with_harmonic)

fft_values = np.fft.rfft(voltage_with_harmonic)

fft_frequencies = np.fft.rfftfreq(
    number_of_samples,
    d=1 / sample_rate
)

fft_magnitude = (
    2 / number_of_samples
) * np.abs(fft_values)

# Find fundamental and 3rd harmonic
fundamental_index = np.argmin(
    np.abs(fft_frequencies - frequency)
)

third_harmonic_index = np.argmin(
    np.abs(fft_frequencies - third_harmonic_frequency)
)

fundamental_magnitude = fft_magnitude[fundamental_index]

third_harmonic_magnitude = fft_magnitude[third_harmonic_index]

# Calculate Total Harmonic Distortion (THD)
thd = (
    third_harmonic_magnitude
    / fundamental_magnitude
) * 100

# --------------------------------------------------
# POWER QUALITY EVENT DETECTION
# --------------------------------------------------

# Define voltage thresholds relative to nominal voltage
sag_threshold = 0.90 * nominal_voltage
swell_threshold = 1.10 * nominal_voltage

# Classify the measured voltage
if voltage_rms < sag_threshold:
    voltage_status = "VOLTAGE SAG DETECTED"
elif voltage_rms > swell_threshold:
    voltage_status = "VOLTAGE SWELL DETECTED"
else:
    voltage_status = "NORMAL"

# Display results
print("INTELLIGENT POWER QUALITY ANALYZER")
print("----------------------------------")
print(f"Frequency: {frequency} Hz")
print(f"Phase Angle: {phase_angle} degrees")
print()
print(f"Expected Vrms: {voltage_rms_expected:.3f} V")
print(f"Calculated Vrms: {voltage_rms:.3f} V")
print()
print(f"Expected Irms: {current_rms_expected:.3f} A")
print(f"Calculated Irms: {current_rms:.3f} A")

print("POWER CALCULATIONS")
print("------------------")
print(f"Real Power (P): {real_power:.3f} W")
print(f"Apparent Power (S): {apparent_power:.3f} VA")
print(f"Reactive Power (Q): {reactive_power:.3f} VAR")
print(f"Power Factor (PF): {power_factor:.3f}")

print()
print("FREQUENCY MEASUREMENT")
print("---------------------")
print(f"Expected Frequency: {frequency:.2f} Hz")
print(f"Measured Frequency: {measured_frequency:.2f} Hz")

print()
print("FFT / HARMONIC ANALYSIS")
print("-----------------------")
print(
    f"Fundamental: {frequency:.0f} Hz, "
    f"Magnitude: {fundamental_magnitude:.3f} V peak"
)
print(
    f"3rd Harmonic: {third_harmonic_frequency:.0f} Hz, "
    f"Magnitude: {third_harmonic_magnitude:.3f} V peak"
)

print()
print("TOTAL HARMONIC DISTORTION")
print("-------------------------")
print(f"THD: {thd:.2f}%")

print()
print("POWER QUALITY STATUS")
print("--------------------")
print(f"Measured Voltage: {voltage_rms:.3f} V RMS")
print(f"Sag Threshold: {sag_threshold:.3f} V")
print(f"Swell Threshold: {swell_threshold:.3f} V")
print(f"Status: {voltage_status}")

# Plot voltage waveform
plt.figure()
plt.plot(time, voltage)
plt.title("Simulated 60-Hz Voltage Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.show()

# Plot current waveform
plt.figure()
plt.plot(time, current)
plt.title("Simulated 60-Hz Current Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Current (A)")
plt.grid(True)
plt.show()

# Plot FFT spectrum
plt.figure()

plt.stem(
    fft_frequencies,
    fft_magnitude
)

plt.xlim(0, 500)

plt.title("Voltage Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V peak)")
plt.grid(True)

plt.show()