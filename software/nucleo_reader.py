import serial

nucleo = serial.Serial("COM3", 9600, timeout=2)

print("Connected to NUCLEO!")
print("Reading live voltage...\n")

try:
    while True:
        line = nucleo.readline().decode("utf-8").strip()

        if line.isdigit():
            adc = int(line)
            voltage = adc * 3.3 / 4095

            print(f"ADC: {adc} | Voltage: {voltage:.3f} V")

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    nucleo.close()