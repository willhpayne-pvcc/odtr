import serial
import time

# Define the serial port (e.g., /dev/ttyS0 for GPIO serial port)
serial_port = '/dev/ttyS0'  # GPIO serial port for Raspberry Pi 3B+

# Define the baud rate
baud_rate = 9600  # Should match the baud rate configured on the Arduino

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_command(command):
    # Send command over the serial connection
    ser.write(command.encode())
    print(f"Sent command: {command}")

try:
    while True:
        # Read data from the serial port
        if ser.in_waiting > 0:
            try:
                # Decode bytes to string and remove newline characters
                data = ser.readline().decode('utf-8', errors='replace').strip()
                # Print the received data
                print("Received data:", data)
                
                # Check for specific commands and send corresponding commands to Arduino
                if data == '/load':
                    send_command('/load\n')
                elif data == '/wipe':
                    send_command('/wipe\n')
            except UnicodeDecodeError:
                print("Error decoding data:", ser.readline())

        # Add a short delay to avoid excessive CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")

finally:
    # Close the serial connection
    ser.close()
