import tkinter as tk
from tkinter import ttk

# --------------------------------------------------
# INTELLIGENT POWER QUALITY ANALYZER
# Dashboard Version 1
# --------------------------------------------------

# Simulated measurements for dashboard testing
voltage_rms = 10.000
current_rms = 0.500
real_power = 4.330
reactive_power = 2.500
apparent_power = 5.000
power_factor = 0.866
frequency = 59.97
thd = 10.00
power_quality_status = "NORMAL"


# --------------------------------------------------
# CREATE MAIN WINDOW
# --------------------------------------------------

root = tk.Tk()

root.title("Intelligent Power Quality Analyzer")
root.geometry("1000x650")
root.minsize(900, 600)

# Main heading
title = tk.Label(
    root,
    text="INTELLIGENT POWER QUALITY ANALYZER",
    font=("Arial", 22, "bold")
)

title.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="Real-Time Electrical Monitoring & Power Quality Analysis",
    font=("Arial", 11)
)

subtitle.pack(pady=(0, 25))


# --------------------------------------------------
# MEASUREMENT SECTION
# --------------------------------------------------

measurement_frame = ttk.LabelFrame(
    root,
    text=" Electrical Measurements "
)

measurement_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


def create_measurement(parent, label, value, row, column):

    frame = ttk.Frame(parent)

    frame.grid(
        row=row,
        column=column,
        padx=30,
        pady=20,
        sticky="nsew"
    )

    name_label = ttk.Label(
        frame,
        text=label,
        font=("Arial", 10)
    )

    name_label.pack()

    value_label = ttk.Label(
        frame,
        text=value,
        font=("Arial", 18, "bold")
    )

    value_label.pack(pady=5)


# Allow columns to expand evenly
for column in range(4):
    measurement_frame.columnconfigure(
        column,
        weight=1
    )


# First row
create_measurement(
    measurement_frame,
    "RMS Voltage",
    f"{voltage_rms:.3f} V",
    0,
    0
)

create_measurement(
    measurement_frame,
    "RMS Current",
    f"{current_rms:.3f} A",
    0,
    1
)

create_measurement(
    measurement_frame,
    "Real Power",
    f"{real_power:.3f} W",
    0,
    2
)

create_measurement(
    measurement_frame,
    "Reactive Power",
    f"{reactive_power:.3f} VAR",
    0,
    3
)


# Second row
create_measurement(
    measurement_frame,
    "Apparent Power",
    f"{apparent_power:.3f} VA",
    1,
    0
)

create_measurement(
    measurement_frame,
    "Power Factor",
    f"{power_factor:.3f}",
    1,
    1
)

create_measurement(
    measurement_frame,
    "Frequency",
    f"{frequency:.2f} Hz",
    1,
    2
)

create_measurement(
    measurement_frame,
    "THD",
    f"{thd:.2f} %",
    1,
    3
)


# --------------------------------------------------
# POWER QUALITY STATUS
# --------------------------------------------------

status_frame = ttk.LabelFrame(
    root,
    text=" Power Quality Status "
)

status_frame.pack(
    padx=30,
    pady=20,
    fill="x"
)

status_label = tk.Label(
    status_frame,
    text=power_quality_status,
    font=("Arial", 24, "bold")
)

status_label.pack(pady=25)


# --------------------------------------------------
# SYSTEM INFORMATION
# --------------------------------------------------

info_frame = ttk.LabelFrame(
    root,
    text=" System Information "
)

info_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)

info_text = ttk.Label(
    info_frame,
    text=(
        "Signal Source: Simulated Data\n"
        "Nominal Frequency: 60 Hz\n"
        "Nominal Voltage: 10 V RMS\n"
        "Analyzer Status: Running"
    ),
    font=("Arial", 10),
    justify="left"
)

info_text.pack(
    padx=20,
    pady=15,
    anchor="w"
)


# --------------------------------------------------
# START DASHBOARD
# --------------------------------------------------

root.mainloop()