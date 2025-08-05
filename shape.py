import serial
import time

# --- Bittle Configuration ---
# IMPORTANT: Make sure this is your Bittle's correct serial port!
SERIAL_PORT = '/dev/tty.BittleC4_SSP' # Example port, change if needed
BAUD_RATE = 115200

##--- ADDED: Durations for the new backward pattern ---
BACKWARD_DURATION = 2.0
LEFT_DURATION = 1.5

# --- Command Definitions ---
# These are the basic actions the Bittle can perform.
WALK_FORWARD = b'kwkF\n'
WALK_BACKWARD = b'kbkF\n' # Corrected typo from original
TURN_RIGHT_90= b'k vtR 90\n' # Corrected command format
BALANCE = b'kbalance\n'   # Command to stop current movement and stand still
REST = b'd\n'             # Command to turn off all servos and rest
# --- ADDED: Command to turn off auto-balancing to prevent jittering ---
TURN_OFF_BALANCE = b'gb\n'
##--- ADDED: New command for the pattern function ---
SPIN_LEFT = b'k vtL 90\n'

# --- Marker Control Commands (using head servos) ---
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

##--- ADDED: The requested backward_pattern function ---
def backward_pattern(bittle):
    """
    Executes a predefined backward movement pattern.
    This function is not called by the main script but is available for use.
    """
    pattern = [
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("left", SPIN_LEFT, LEFT_DURATION, "Sent: SPIN_LEFT"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("left", SPIN_LEFT, LEFT_DURATION, "Sent: SPIN_LEFT"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
    ]

    print("\n--- EXECUTING BACKWARD PATTERN ---")
    for name, command, duration, message in pattern:
        print(f"  - {message} for {duration} seconds.")
        bittle.write(command)
        time.sleep(duration)
        bittle.write(BALANCE) # Balance after each step
        time.sleep(1.0)
    print("\n--- BACKWARD PATTERN COMPLETE ---")

def run_timed_triangle_sequence(ser):
    """
    Executes a triangle-drawing movement using fixed steps (no loop),
    matching the structure of run_timed_square_sequence.
    """
    print("\n--- INFO: Starting triangle drawing sequence in 3 seconds... ---")
    time.sleep(3)

    # Initial balance
    print("ACTION: Balancing robot to start.")
    ser.write(BALANCE)
    time.sleep(2.0)

    # Lower the marker
    print("STEP 1: Lowering marker for 2.0 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.0:
        ser.write(MARKER_DOWN)
        time.sleep(0.1)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- SIDE 1 ---
    print("STEP 2: Marker DOWN, moving FORWARD for 2.6 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.6:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.1)
    ser.write(BALANCE)
    time.sleep(1.5)

    start_time = time.time()
    while time.time() - start_time < 0.6:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE)
    time.sleep(1.5)

    print("STEP 3: Marker UP, turning RIGHT 120°.")
    ser.write(b'k vtR 120\n')  # <-- Turn 120 degrees
    time.sleep(0.05)
    ser.write(MARKER_UP)
    time.sleep(6.0)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- SIDE 2 ---
    print("STEP 4: Marker DOWN, moving FORWARD for 2.6 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.6:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.1)
    ser.write(BALANCE)
    time.sleep(1.5)


    start_time = time.time()
    while time.time() - start_time < 0.6:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE)
    time.sleep(1.5)

    print("STEP 5: Marker UP, turning RIGHT 120°.")
    ser.write(b'k vtR 120\n')
    time.sleep(0.05)
    ser.write(MARKER_UP)
    time.sleep(6.0)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- SIDE 3 ---
    print("STEP 6: Marker DOWN, moving FORWARD for 2.6 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.6:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.1)
    ser.write(BALANCE)
    time.sleep(1.5)

    print("STEP 7: Marker UP to finish.")
    start_time = time.time()
    while time.time() - start_time < 2.0:
        ser.write(MARKER_UP)
        time.sleep(0.1)

    print("\n--- INFO: Triangle drawing complete! ---")
    time.sleep(1.0)


def run_timed_square_sequence(ser):
    
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

    # --- Step 2: Forward, marker down ---
    print("STEP 2: Marker is DOWN, moving FORWARD for 2.60")
    start_time = time.time()
    while time.time() - start_time < 2.60:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)

        time.sleep(0.1)  # Continuously send the command
    ser.write(BALANCE)
    time.sleep(1.5)


    # --- Step 3: Backward, marker up ---
    print("STEP 3: Marker is UP, moving BACKWARD for 0.6 seconds.")
    start_time = time.time()
    while time.time() - start_time < 0.6:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- Step 4: Turn right, marker up ---
    print("STEP 4: Marker is UP, turning RIGHT.")
    start_time = time.time()
    
    ser.write(TURN_RIGHT_90)
    time.sleep(0.05)
    ser.write(MARKER_UP)
    time.sleep(5)
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
    print("STEP 5: Marker UP, moving BACKWARD for 0.8 seconds.")
    start_time = time.time()
    while time.time() - start_time < 0.8:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- Step 6: Turn right, marker up ---
    print("STEP 6: Marker UP, turning RIGHT.")
    ser.write(TURN_RIGHT_90)
    time.sleep(0.05)
    ser.write(MARKER_UP)
    time.sleep(5)
    ser.write(BALANCE)
    time.sleep(1.5)


    # --- Step 7: Forward, marker down ---
    print("STEP 7: Marker DOWN, moving FORWARD for 2.60 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.60:
        ser.write(WALK_FORWARD)
        time.sleep(0.05)
        ser.write(MARKER_DOWN)
        time.sleep(0.05)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- Step 8: Backward, marker up ---
    print("STEP 8: Marker UP, moving BACKWARD for 0.6 seconds.")
    start_time = time.time()
    while time.time() - start_time < 0.6:
        ser.write(WALK_BACKWARD)
        time.sleep(0.05)
        ser.write(MARKER_UP)
        time.sleep(0.05)
    ser.write(BALANCE)
    time.sleep(1.5)

    # --- Step 9: Turn right, marker up ---
    print("STEP 9: Marker UP, turning RIGHT.")
    ser.write(TURN_RIGHT_90)
    time.sleep(0.05)
    ser.write(MARKER_UP)
    time.sleep(5)
    ser.write(BALANCE)
    time.sleep(1.5)


    print("STEP 7: Marker DOWN, moving FORWARD for 2.8 seconds.")
    start_time = time.time()
    while time.time() - start_time < 2.80:
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
        #run_timed_square_sequence(bittle_serial)
        run_timed_triangle_sequence(bittle_serial)
        
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
