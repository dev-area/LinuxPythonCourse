import serial
import time

# Configure the serial port
# Replace 'COM3' (Windows) or '/dev/ttyUSB0' (Linux/Mac) with your actual port
SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 9600

try:
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=1
    )
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud (Capitalizing Echo)...")

    while True:
        if ser.in_waiting > 0:
            # Read incoming bytes
            incoming_bytes = ser.read(ser.in_waiting)
            
            try:
                # Decode bytes to text, capitalize, and encode back to bytes
                text_data = incoming_bytes.decode('utf-8')
                capitalized_text = text_data.upper()
                echo_bytes = capitalized_text.encode('utf-8')
                
                # Print to terminal for debugging
                print(f"Received: {text_data.strip()} -> Echoed: {capitalized_text.strip()}")
                
                # Echo the capitalized data back
                ser.write(echo_bytes)
                
            except UnicodeDecodeError:
                # Fallback for non-text / binary data
                print(f"Received non-text binary data: {incoming_bytes}")
                ser.write(incoming_bytes)
            
        time.sleep(0.01)

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
