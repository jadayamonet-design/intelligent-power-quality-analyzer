import numpy as np

# --------------------------------------------------
# AUTOMATIC POWER QUALITY EVENT TEST
# --------------------------------------------------

nominal_voltage = 10.0
sample_rate = 10000
frequency = 60
duration = 0.1

# Voltage thresholds
sag_threshold = 0.90 * nominal_voltage
swell_threshold = 1.10 * nominal_voltage

# Test cases
test_cases = {
    "Normal Condition": 10.0,
    "Voltage Sag": 7.5,
    "Voltage Swell": 12.0
}

print("AUTOMATIC POWER QUALITY EVENT TEST")
print("----------------------------------")
print(f"Nominal Voltage: {nominal_voltage:.3f} V RMS")
print(f"Sag Threshold: {sag_threshold:.3f} V")
print(f"Swell Threshold: {swell_threshold:.3f} V")
print()

# Create time samples
time = np.arange(0, duration, 1 / sample_rate)

# Automatically test every condition
for test_name, test_voltage_rms in test_cases.items():

    # Convert RMS test voltage to peak voltage
    test_voltage_peak = test_voltage_rms * np.sqrt(2)

    # Generate simulated AC waveform
    test_voltage = test_voltage_peak * np.sin(
        2 * np.pi * frequency * time
    )

    # Measure RMS voltage from waveform samples
    measured_voltage_rms = np.sqrt(
        np.mean(test_voltage ** 2)
    )

    # Classify voltage condition
    if measured_voltage_rms < sag_threshold:
        status = "VOLTAGE SAG DETECTED"

    elif measured_voltage_rms > swell_threshold:
        status = "VOLTAGE SWELL DETECTED"

    else:
        status = "NORMAL"

    # Display test result
    print(test_name)
    print("--------------------")
    print(
        f"Input Voltage: {test_voltage_rms:.3f} V RMS"
    )
    print(
        f"Measured Voltage: {measured_voltage_rms:.3f} V RMS"
    )
    print(f"Status: {status}")
    print()