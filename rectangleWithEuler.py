# bittle_automated_square.py
# A script to make Bittle perform a pre-defined, timed sequence of movements
# as one continuous action.

import serial
import time

# --- Bittle Configuration ---
# IMPORTANT: Make sure this is your Bittle's correct serial port!
SERIAL_PORT = '/dev/tty.BittleA9_SSP' # Example port, change if needed
BAUD_RATE = 115200

# --- Command Definitions ---
# These are the basic actions the Bittle can perform.
WALK_FORWARD = b'kwkF\n'
WALK_BACKWARD = b'kbkF\n'
TURN_RIGHT_IN_PLACE = b'kvtR\n'
BALANCE = b'kbalance\n'   # Command to stop current movement and stand still
REST = b'd\n'             # Command to turn off all servos and rest
# --- ADDED: Command to turn off auto-balancing to prevent jittering ---
TURN_OFF_BALANCE = b'gb\n'

# --- Marker Control Commands (using head servos) ---
# We assume the head movement controls the marker.
# The 'm3' command targets the servo on Pin 3.
MARKER_DOWN = b'i3 45\n'
MARKER_UP = b'i3 -45\n'

def connect_to_bittle():
    """
    Tries to connect to the Bittle via the specified serial port.
    Returns the serial connection object if successful, otherwise None.
    """
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        print(f"INFO: Successfully connected to Bittle on {SERIAL_PORT}")
        # Wait a moment for the connection to stabilize
        time.sleep(2)
        # --- ADDED: Turn off auto-balancing to prevent jittering during the sequence ---
        print("INFO: Turning off auto-balancing.")
        ser.write(TURN_OFF_BALANCE)
        time.sleep(0.5)
        return ser
    except serial.SerialException:
        print(f"ERROR: Could not connect to Bittle on {SERIAL_PORT}.")
        print("       Please check the port name and ensure the robot is on.")
        return None
        
def get_yaw_from_bittle(ser):
    """
    Reads yaw from the serial connection.
    Returns yaw as a float, or None if unreadable.
    """
    while ser.in_waiting:
        line = ser.readline().decode(errors="ignore").strip()
        if line.startswith("ICM:") or line.startswith("MCU:"):
            try:
                # Remove label prefix
                line = line.split(":")[1].strip()
                # Split into float values
                values = [float(x) for x in line.split()]
                if len(values) >= 6:
                    yaw = values[3]  # 4th value is yaw (YPR[0])
                    return yaw
            except (ValueError, IndexError):
                continue
    return None


def turn_right_90_degrees(ser):
    """
    Turn right until yaw has changed by ~90 degrees.
    """
    print("ACTION: Turning right 90° based on yaw reading...")

    initial_yaw = None
    while initial_yaw is None:
        initial_yaw = get_yaw_from_bittle(ser)

    target_yaw = (initial_yaw + 90) % 360

    def angle_diff(a, b):
        return ((a - b + 180) % 360) - 180

    while True:
        current_yaw = get_yaw_from_bittle(ser)
        if current_yaw is None:
            continue

        diff = angle_diff(current_yaw, target_yaw)
        print(f"Yaw: {current_yaw:.1f}° → Target: {target_yaw:.1f}° (Δ={diff:.1f}°)")

        if abs(diff) < 5:
            break  # Close enough to 90°

        ser.write(TURN_RIGHT_IN_PLACE)
        time.sleep(0.05)

    ser.write(BALANCE)
    print("90-degree turn complete.\n")
    time.sleep(1.0)


def run_timed_square_sequence(ser):
    """
    Runs the pre-defined, timed sequence of movements.
    This version now alternates commands rapidly inside a loop to ensure
    both movement and marker position are executed simultaneously,
    mimicking how the manual driver works.
    
    Args:
        ser: The active serial connection to the Bittle.
    """
    print("\n--- INFO: Starting the continuous automated sequence in 3 seconds... ---")
    time.sleep(3)

    # Put Bittle in a known state (balanced) before starting.
    print("ACTION: Balancing robot to start.")
    ser.write(BALANCE)
    time.sleep(2.0) # Give it time to get stable

    print("--- SEQUENCE STARTING ---")

    # --- Step 1: Marker DOWN only ---
    print("STEP 1: Holding Marker DOWN for 2.60 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.0:
        ser.write(MARKER_DOWN)
        time.sleep(0.1)  # Continuously send the command
    ser.write(BALANCE) 
    time.sleep(1.5)    

    print("STEP 3: Holding Marker DOWN for 2.60 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.60:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        
        time.sleep(0.1)  # Continuously send the command
    ser.write(BALANCE) 
    time.sleep(1.5)    
    

    # --- Step 2: Backward, marker up ---
    start_time = time.time()
    while time.time() - start_time < 1.30:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE) 
    time.sleep(1.5)    

    # --- Step 3: Turn right, marker up ---
    print("STEP 3: Marker is UP, turning RIGHT for 2.12 seconds.")
    ser.write(MARKER_UP)
    turn_right_90_degrees(ser)
    ser.write(BALANCE) 
    time.sleep(1.5)    

    # --- Step 4: Forward, marker down ---
    print("STEP 4: Marker DOWN, moving FORWARD for 3.40 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.60:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.05)
    ser.write(BALANCE) 
    time.sleep(1.5)    

    # --- Step 5: Backward, marker up ---
    print("STEP 5: Marker UP, moving BACKWARD for 1.30 seconds.")
    start_time = time.time()
    while time.time() - start_time < 1.40:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE) 
    time.sleep(1.5)    
    
    # --- Step 6: Turn right, marker up ---
    start_time = time.time()
    ser.write(MARKER_UP)
    turn_right_90_degrees(ser)
    
    ser.write(BALANCE) 
    time.sleep(1.5)    

    # --- Step 7: Forward, marker down ---
    start_time = time.time()
    while time.time() - start_time < 2.70:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.05)
    ser.write(BALANCE) 
    time.sleep(1.5)    

    # --- Step 8: Backward, marker up ---
    start_time = time.time()
    while time.time() - start_time < 1.40:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE) 
    time.sleep(1.5)   

    # --- Step 9: Turn right, marker up ---
    ser.write(MARKER_UP)
    turn_right_90_degrees(ser)

    ser.write(BALANCE) 
    time.sleep(1.5)    

    start_time = time.time()
    while time.time() - start_time < 5.00:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.05)
    ser.write(BALANCE) 
    time.sleep(1.5)    
    
    print("\n--- INFO: Automated drawing sequence complete! ---")
    time.sleep(1) # Final pause before resting


def main():
    """
    Main function to connect to Bittle and run the automated sequence.
    """
    bittle_serial = connect_to_bittle()
    
    # Only proceed if the connection was successful
    if not bittle_serial:
        return

    try:
        # Run the main sequence
        run_timed_square_sequence(bittle_serial)
    finally:
        # This code will run no matter what, ensuring the robot is safely shut down.
        print("INFO: Putting Bittle to rest...")
        if bittle_serial and bittle_serial.is_open:
            bittle_serial.write(REST)
            time.sleep(0.5)
            bittle_serial.close()
            print("INFO: Serial port closed. Goodbye!")

# This makes the script runnable from the command line
if __name__ == "__main__":
    main()
