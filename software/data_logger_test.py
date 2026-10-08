import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

# --------------------------------------------------
# POWER QUALITY DATA LOGGER TEST
# --------------------------------------------------

nominal_voltage = 10.0
sample_rate = 10000
frequency = 60
duration = 0.1

# Event thresholds
sag_threshold = 0.90 * nominal_voltage
swell_threshold = 1.10 * nominal_voltage

# Test conditions
test_cases = {
    "Normal Condition": 10.0,
    "Voltage Sag": 7.5,
    "Voltage Swell": 12.0
}

# Create time samples
time = np.arange(0, duration, 1 / sample_rate)

# This list will hold all test results
results = []

for test_name, test_voltage_rms in test_cases.items():

    # Convert RMS voltage to peak voltage
    test_voltage_peak = test_voltage_rms * np.sqrt(2)

    # Generate simulated AC waveform
    test_voltage = test_voltage_peak * np.sin(
        2 * np.pi * frequency * time
    )

    # Calculate measured RMS voltage
    measured_voltage_rms = np.sqrt(
        np.mean(test_voltage ** 2)
    )

    # Determine power quality status
    if measured_voltage_rms < sag_threshold:
        status = "VOLTAGE SAG DETECTED"

    elif measured_voltage_rms > swell_threshold:
        status = "VOLTAGE SWELL DETECTED"

    else:
        status = "NORMAL"

    # Save this test result
    results.append(
        {
            "Timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "Test": test_name,
            "Input Voltage (V RMS)": test_voltage_rms,
            "Measured Voltage (V RMS)": measured_voltage_rms,
            "Status": status
        }
    )

# Convert results into a table
results_table = pd.DataFrame(results)

# Create the data folder path
data_folder = Path("data")

# Create the folder if it does not already exist
data_folder.mkdir(exist_ok=True)

# Choose the CSV filename
output_file = data_folder / "power_quality_event_log.csv"

# Save the results
results_table.to_csv(
    output_file,
    index=False
)

# Display results in Terminal
print()
print("POWER QUALITY DATA LOGGER")
print("-------------------------")
print(results_table.to_string(index=False))
print()
print(f"Data saved to: {output_file}")