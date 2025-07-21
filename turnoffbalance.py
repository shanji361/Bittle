import cv2
import serial
import time
import numpy as np

# --- SERIAL CONFIGURATION ---
SERIAL_PORT = '/dev/tty.Bittle03_SSP'
BAUD_RATE = 115200

# --- DURATIONS (seconds) ---
BACKWARD_DURATION = 1.80
LEFT_DURATION = 1.20
BALANCE_INTERVAL = 5

TURN_OFF_BALANCE = b'gb\n'

# --- COMMANDS ---
WALK_GAIT = b'kwk\n'
WALK_BACKWARD = b'kbk\n'
SPIN_LEFT = b'kcrL\n'
BALANCE = b'kbalance\n'
WALK_FORWARD = b'kwkF\n'
SPIN_RIGHT = b'kcrR\n'
REST = b'd\n'
# --- Head Movement Commands ---
HEAD_UP = b'm0 -45\n'
HEAD_DOWN = b'm0 45\n'
HEAD_CENTER = b'm0 0\n'

def connect_to_bittle():
    """Establishes a serial connection with the Bittle robot."""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Bittle on {SERIAL_PORT}")
        time.sleep(2)
        ser.write(TURN_OFF_BALANCE)
        return ser
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def log_action(action):
    """Prints a formatted log message to the console."""
    print(f"# {action}")

def backward_pattern(bittle):
    """
    Executes a predefined backward movement pattern.
    This function has its own key listener to allow interruption and head movement.
    """
    pattern = [
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("left", SPIN_LEFT, LEFT_DURATION, "Sent: SPIN_LEFT"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("left", SPIN_LEFT, LEFT_DURATION, "Sent: SPIN_LEFT"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
    ]
    # This inner loop allows the pattern to be interrupted by a key press.
    for cmd_type, cmd, duration, msg in pattern:
        bittle.write(cmd)
        log_action(msg)
        t_start = time.time()
        while time.time() - t_start < duration:
            key = cv2.waitKey(1) & 0xFF
            
            # Handle head movements directly within the pattern loop
            if key == ord('i'):
                bittle.write(HEAD_UP)
                log_action("Sent: HEAD_UP")
            elif key == ord('k'):
                bittle.write(HEAD_DOWN)
                log_action("Sent: HEAD_DOWN")
            elif key == ord('h'):
                bittle.write(HEAD_CENTER)
                log_action("Sent: HEAD_CENTER")
            # If another key is pressed (not a head command), return it to interrupt the pattern
            elif key != 0xFF:
                return key
                
            time.sleep(0.01)
        if cmd_type == "backward":
            bittle.write(WALK_GAIT)
            log_action("Set Gait: WALK")
            time.sleep(0.1)
    return 0xFF # Return a value indicating no key was pressed

def main():
    """Main function to run the Bittle control interface."""
    bittle = connect_to_bittle()
    if not bittle:
        return

    control_window = np.zeros((200, 400, 3), dtype=np.uint8)

    current_mode = None  # 'backward', 'forward', 'spin_left', 'spin_right', None
    
    # --- Individual Timers for each command ---
    command_timers = {
        'forward': None,
        'backward': None,
        'spin_left': None,
        'spin_right': None
    }
    
    def stop_all_timers():
        """Stops any active timer and prints its duration."""
        for mode, start_time in command_timers.items():
            if start_time is not None:
                elapsed = time.time() - start_time
                log_action(f"'{mode.replace('_', ' ')}' command lasted for {elapsed:.2f} seconds.")
                command_timers[mode] = None
        return # Explicit return

    try:
        print("Bittle Driver Control")
        print("w/s = forward/backward | a/d = spin L/R | space = stop | q = quit")
        print("i/k/h = head up/down/center")
        bittle.write(BALANCE)
        log_action("Sent: BALANCE (startup)")
        time.sleep(0.5)

        while True:
            # Create and display the control window
            window = control_window.copy()
            cv2.putText(window, "Bittle Driver Control", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(window, "w/s: forward/back", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "a/d: spin L/R", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "space: stop | q: quit", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "Head: i(Up), k(Down), h(Center)", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.imshow("Bittle Control", window)

            key = cv2.waitKey(1) & 0xFF

            # --- Primary Key Handling ---
            if key != 0xFF:
                new_mode = None
                if key == ord('w'): new_mode = 'forward'
                elif key == ord('s'): new_mode = 'backward'
                elif key == ord('a'): new_mode = 'spin_left'
                elif key == ord('d'): new_mode = 'spin_right'

                # If a new movement key is pressed, handle timers
                if new_mode and new_mode != current_mode:
                    stop_all_timers() # Stop any previously running timer
                    command_timers[new_mode] = time.time()
                    log_action(f"Timer started for '{new_mode.replace('_', ' ')}'.")
                    current_mode = new_mode

                # Head controls (do not affect movement timers)
                elif key == ord('i'):
                    bittle.write(HEAD_UP)
                    log_action("Sent: HEAD_UP")
                elif key == ord('k'):
                    bittle.write(HEAD_DOWN)
                    log_action("Sent: HEAD_DOWN")
                elif key == ord('h'):
                    bittle.write(HEAD_CENTER)
                    log_action("Sent: HEAD_CENTER")
                # Stop command
                elif key == 32:  # space
                    stop_all_timers()
                    current_mode = None
                    bittle.write(BALANCE)
                    log_action("Sent: BALANCE (stop)")
                # Quit command
                elif key == ord('q'):
                    stop_all_timers()
                    log_action("Quit and rest")
                    break

            # --- Mode Execution Logic ---
            if current_mode == 'forward':
                bittle.write(WALK_FORWARD)
                log_action("Sent: WALK_FORWARD")
                time.sleep(0.1)
            elif current_mode == 'backward':
                # This mode has its own key handling, so we need to check for interruptions.
                key_from_pattern = backward_pattern(bittle)
                if key_from_pattern != 0xFF:
                    interrupted_mode = None
                    if key_from_pattern == ord('w'): interrupted_mode = 'forward'
                    elif key_from_pattern == ord('a'): interrupted_mode = 'spin_left'
                    elif key_from_pattern == ord('d'): interrupted_mode = 'spin_right'
                    
                    stop_all_timers() # Stop the backward timer
                    
                    if interrupted_mode:
                        command_timers[interrupted_mode] = time.time()
                        log_action(f"Timer started for '{interrupted_mode.replace('_', ' ')}'.")
                        current_mode = interrupted_mode
                    elif key_from_pattern == 32:  # space
                        current_mode = None
                        bittle.write(BALANCE)
                        log_action("Sent: BALANCE (stop)")
                    elif key_from_pattern == ord('q'):
                        log_action("Quit and rest")
                        break # Exit the main while loop

            elif current_mode == 'spin_left':
                bittle.write(SPIN_LEFT)
                log_action("Sent: SPIN_LEFT")
                time.sleep(0.1)
            elif current_mode == 'spin_right':
                bittle.write(SPIN_RIGHT)
                log_action("Sent: SPIN_RIGHT")
                time.sleep(0.1)
            else:
                # If no mode is active, pause briefly to prevent high CPU usage.
                time.sleep(0.01)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup actions
        print("Resting Bittle and closing connection.")
        try:
            if bittle and bittle.is_open:
                bittle.write(REST)
                log_action("Sent: REST (shutdown)")
                time.sleep(0.5)
                bittle.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()