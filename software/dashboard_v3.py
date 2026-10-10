import tkinter as tk
from tkinter import ttk
import serial
import csv
from datetime import datetime
from collections import deque
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --------------------------------------------------
# INTELLIGENT POWER QUALITY ANALYZER
# Dashboard Version 2
# --------------------------------------------------

# NUCLEO live connection
try:
    nucleo = serial.Serial("COM3", 9600, timeout=0.1)
    nucleo_connected = True
except serial.SerialException:
    nucleo = None
    nucleo_connected = False
# --------------------------------------------------
# AUTOMATIC DATA LOGGING
# --------------------------------------------------

log_file = open("nucleo_voltage_log.csv", "a", newline="")
log_writer = csv.writer(log_file)

if log_file.tell() == 0:
    log_writer.writerow(["Timestamp", "ADC Value", "Voltage (V)"])
    log_file.flush()
# Simulated measurements
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
# SIMULATED WAVEFORMS
# --------------------------------------------------

sample_rate = 10000
duration = 0.1

time = np.arange(0, duration, 1 / sample_rate)

voltage_peak = voltage_rms * np.sqrt(2)
current_peak = current_rms * np.sqrt(2)

phase_angle = np.deg2rad(30)

voltage = voltage_peak * np.sin(
    2 * np.pi * 60 * time
)

current = current_peak * np.sin(
    2 * np.pi * 60 * time - phase_angle
)

# Add a 3rd harmonic to voltage
voltage += (
    0.10
    * voltage_peak
    * np.sin(2 * np.pi * 180 * time)
)

# --------------------------------------------------
# FFT
# --------------------------------------------------

fft_values = np.fft.rfft(voltage)
fft_frequency = np.fft.rfftfreq(
    len(voltage),
    1 / sample_rate
)

fft_magnitude = (
    2 / len(voltage)
) * np.abs(fft_values)

# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

root = tk.Tk()

root.title("Intelligent Power Quality Analyzer")
root.geometry("1250x850")
root.minsize(1100, 750)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

title = tk.Label(
    root,
    text="INTELLIGENT POWER QUALITY ANALYZER",
    font=("Arial", 22, "bold")
)

title.pack(pady=(15, 2))

subtitle = tk.Label(
    root,
    text="Real-Time Electrical Monitoring & Power Quality Analysis",
    font=("Arial", 11)
)

subtitle.pack(pady=(0, 10))

# --------------------------------------------------
# CONNECTION BAR
# --------------------------------------------------

connection_frame = ttk.Frame(root)

connection_frame.pack(
    fill="x",
    padx=25,
    pady=5
)

source_label = ttk.Label(
    connection_frame,
text="DATA SOURCE: NUCLEO (LIVE DC) + SIMULATED AC",    font=("Arial", 10, "bold")
)

source_label.pack(side="left")

connection_label = ttk.Label(
    connection_frame,
    text="SYSTEM STATUS: RUNNING",
    font=("Arial", 10, "bold")
)

connection_label.pack(side="right")

# --------------------------------------------------
# MEASUREMENT CARDS
# --------------------------------------------------

measurement_frame = ttk.LabelFrame(
    root,
    text=" Live Electrical Measurements "
)

measurement_frame.pack(
    fill="x",
    padx=25,
    pady=8
)

for column in range(8):
    measurement_frame.columnconfigure(
        column,
        weight=1
    )


def measurement_card(parent, name, value, column):

    frame = ttk.Frame(parent)

    frame.grid(
        row=0,
        column=column,
        padx=10,
        pady=12,
        sticky="nsew"
    )

    ttk.Label(
        frame,
        text=name,
        font=("Arial", 9)
    ).pack()

    ttk.Label(
        frame,
        text=value,
        font=("Arial", 14, "bold")
    ).pack(pady=4)


measurement_card(
    measurement_frame,
    "Voltage",
    f"{voltage_rms:.3f} V",
    0
)

measurement_card(
    measurement_frame,
    "Current",
    f"{current_rms:.3f} A",
    1
)

measurement_card(
    measurement_frame,
    "Real Power",
    f"{real_power:.3f} W",
    2
)

measurement_card(
    measurement_frame,
    "Reactive Power",
    f"{reactive_power:.3f} VAR",
    3
)

measurement_card(
    measurement_frame,
    "Apparent Power",
    f"{apparent_power:.3f} VA",
    4
)

measurement_card(
    measurement_frame,
    "Power Factor",
    f"{power_factor:.3f}",
    5
)

measurement_card(
    measurement_frame,
    "Frequency",
    f"{frequency:.2f} Hz",
    6
)

measurement_card(
    measurement_frame,
    "THD",
    f"{thd:.2f} %",
    7
)

# --------------------------------------------------
# LIVE NUCLEO VOLTAGE DISPLAY
# --------------------------------------------------

live_voltage_label = ttk.Label(
    root,
    text="NUCLEO Live Voltage: Waiting for data...",
    font=("Arial", 14, "bold")
)

live_voltage_label.pack(pady=8)

# --------------------------------------------------
# GRAPH AREA
# --------------------------------------------------

graph_frame = ttk.Frame(root)

graph_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=5
)

# Store the latest 100 NUCLEO voltage readings
live_voltage_history = deque([0.0] * 100, maxlen=100)

graph_frame.columnconfigure(0, weight=1)
graph_frame.columnconfigure(1, weight=1)
graph_frame.rowconfigure(0, weight=1)

# --------------------------------------------------
# WAVEFORM GRAPH
# --------------------------------------------------

waveform_box = ttk.LabelFrame(
    graph_frame,
    text=" Voltage & Current Waveforms "
)

waveform_box.grid(
    row=0,
    column=0,
    padx=(0, 6),
    pady=5,
    sticky="nsew"
)

waveform_figure = Figure(
    figsize=(6, 2.5),
    dpi=100
)

waveform_plot = waveform_figure.add_subplot(111)

waveform_plot.plot(
    time,
    voltage,
    label="Voltage (V)"
)

waveform_plot.plot(
    time,
    current,
    label="Current (A)"
)

waveform_plot.set_xlabel("Time (seconds)")
waveform_plot.set_ylabel("Amplitude")
waveform_plot.set_title("Real-Time Waveforms")
waveform_plot.grid(True)
waveform_plot.legend()

waveform_figure.tight_layout()

waveform_canvas = FigureCanvasTkAgg(
    waveform_figure,
    master=waveform_box
)

waveform_canvas.draw()

waveform_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)

# --------------------------------------------------
# FFT GRAPH
# --------------------------------------------------

fft_box = ttk.LabelFrame(
    graph_frame,
    text=" Harmonic Spectrum "
)

fft_box.grid(
    row=0,
    column=1,
    padx=(6, 0),
    pady=5,
    sticky="nsew"
)

fft_figure = Figure(
    figsize=(6, 2.5),
    dpi=100
)

fft_plot = fft_figure.add_subplot(111)

fft_plot.stem(
    fft_frequency,
    fft_magnitude
)

fft_plot.set_xlim(0, 500)

fft_plot.set_xlabel("Frequency (Hz)")
fft_plot.set_ylabel("Magnitude (V peak)")
fft_plot.set_title("Voltage Frequency Spectrum")
fft_plot.grid(True)

fft_figure.tight_layout()

fft_canvas = FigureCanvasTkAgg(
    fft_figure,
    master=fft_box
)

fft_canvas.draw()

fft_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)

# --------------------------------------------------
# LIVE NUCLEO VOLTAGE GRAPH
# --------------------------------------------------

live_graph_box = ttk.LabelFrame(
    root,
    text=" Live NUCLEO DC Voltage "
)

live_graph_box.pack(
    fill="x",
    padx=25,
    pady=5
)

live_figure = Figure(figsize=(10, 1.0), dpi=100)
live_plot = live_figure.add_subplot(111)

live_line, = live_plot.plot(
    list(live_voltage_history),
    label="Measured DC Voltage"
)

live_plot.set_ylim(0, 3.3)
live_plot.set_ylabel("Voltage (V)")
live_plot.set_xlabel("Recent Samples")
live_plot.grid(True)

live_figure.tight_layout()

live_canvas = FigureCanvasTkAgg(
    live_figure,
    master=live_graph_box
)

live_canvas.draw()

live_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)

# --------------------------------------------------
# STATUS AREA
# --------------------------------------------------

bottom_frame = ttk.Frame(root)

bottom_frame.pack(
    fill="x",
    padx=25,
    pady=(5, 15)
)

bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)

# Power quality status
status_box = ttk.LabelFrame(
    bottom_frame,
    text=" Power Quality Status "
)

status_box.grid(
    row=0,
    column=0,
    padx=(0, 6),
    sticky="nsew"
)

status_label = tk.Label(
    status_box,
    text=power_quality_status,
    font=("Arial", 20, "bold")
)

status_label.pack(pady=15)

# Event information
event_box = ttk.LabelFrame(
    bottom_frame,
    text=" Event Detection "
)

event_box.grid(
    row=0,
    column=1,
    padx=(6, 0),
    sticky="nsew"
)

event_text = ttk.Label(
    event_box,
    text=(
        "Sag Threshold: 9.000 V RMS\n"
        "Swell Threshold: 11.000 V RMS\n"
        "Active Event: None"
    ),
    font=("Arial", 10),
    justify="left"
)

event_text.pack(
    padx=20,
    pady=10,
    anchor="w"
)

# --------------------------------------------------
# START DASHBOARD
# --------------------------------------------------

def update_nucleo_voltage():
    if nucleo_connected and nucleo:
        try:
            while nucleo.in_waiting:
                line = nucleo.readline().decode(
                    "utf-8", errors="ignore"
                ).strip()

                if line.isdigit():
                    adc = int(line)

                    if 0 <= adc <= 4095:
                        voltage_dc = adc * 3.3 / 4095
                        log_writer.writerow([
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                            adc,
                            round(voltage_dc, 3)
                        ])
                        log_file.flush()
                        live_voltage_history.append(voltage_dc)
                        live_line.set_ydata(list(live_voltage_history))
                        live_canvas.draw_idle()

                        live_voltage_label.config(
                            text=f"NUCLEO Live Voltage: {voltage_dc:.3f} V | ADC: {adc}"
                        )

        except serial.SerialException:
            live_voltage_label.config(
                text="NUCLEO connection lost"
            )

    root.after(200, update_nucleo_voltage)


update_nucleo_voltage()

root.mainloop()