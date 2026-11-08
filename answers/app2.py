import serial
import time

def run_serial_app():
    # 1. Prompt user for setup details
    port = "/dev/pts/3"
    baud = 115200
    
    try:
        # 2. Initialize and open the serial port
        # Setting a timeout is critical so ser.readline() doesn't hang forever
        ser = serial.Serial(port, baud, timeout=2)
        
        # Small delay to give certain microcontrollers (like Arduinos) time to reset upon connection
        time.sleep(1.5)
        
        # 3. Ask the user for the message to send
        message = input("Enter message to send: ")
        
        # Append newline characters typical for text-based serial protocols (expected by ser.readline())
        formatted_message = message + "\r\n"
        
        # 4. Transmit the encoded message (Python strings must be encoded to bytes)
        ser.write(formatted_message.encode('utf-8'))
        print(f"-> Sent: {message!r}")
        
        # 5. Wait for and print the incoming result
        print("Waiting for response...")
        response_bytes = ser.readline()
        
        if response_bytes:
            # Decode the raw bytes back into a readable string
            response_string = response_bytes.decode('utf-8').strip()
            print(f"<- Received: {response_string}")
        else:
            print("<- No response received (timeout reached).")
            
        # 6. Clean up resources
        ser.close()

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except ValueError:
        print("Error: Invalid baud rate entered.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_serial_app()

