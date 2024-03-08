import serial
import time

# Define the serial port (e.g., /dev/ttyS0 for GPIO serial port)
serial_port = '/dev/ttyS0'  # GPIO serial port for Raspberry Pi 3B+

# Define the baud rate
baud_rate = 9600  # Should match the baud rate configured on the Arduino

# Create a serial connection with error handling
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print("Serial port connected successfully.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def send_command(command):
    # Send command over the serial connection
    try:
        ser.write(command.encode())
        print(f"Sent command: {command}")
    except serial.SerialException as e:
        print(f"Error writing to serial port: {e}")

try:
    while True:
        # Check if serial port is open
        if ser.isOpen():
            # Read data from the serial port
            try:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8', 'ignore').strip()  # Decode bytes to string and remove newline characters
                    
                    # Print the received data
                    print("Received data:", data)
                    
                    # Check for specific commands and send corresponding commands to Arduino
                    if data == '/load':
                        send_command('/load\n')
                    elif data == '/wipe':
                        send_command('/wipe\n')
            except serial.SerialException as e:
                print(f"Error reading from serial port: {e}")

        # Add a short delay to avoid excessive CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")

finally:
    # Close the serial connection
    ser.close()
