import cv2
import serial
import time
import numpy as np
from serial.tools import list_ports


ports = list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")


def auto_detect_bittle_port():
    ports = list_ports.comports()
    for port in ports:
        if "CH340" in port.description or "USB-SERIAL" in port.description or "Bittle" in port.description:
            return port.device
    return None

# --- SERIAL CONFIGURATION ---
SERIAL_PORT =auto_detect_bittle_port()
BAUD_RATE = 115200

# --- DURATIONS (seconds) ---
BACKWARD_DURATION = 1.80
LEFT_DURATION = 1.20
BALANCE_INTERVAL = 5

# --- COMMANDS ---
WALK_GAIT = b'kwk\n'
WALK_BACKWARD = b'kbk\n'
SPIN_LEFT = b'kcrL\n'
BALANCE = b'kbalance\n'
WALK_FORWARD = b'kwkF\n'
SPIN_RIGHT = b'kcrR\n'
REST = b'd\n'

def connect_to_bittle():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Opened port {SERIAL_PORT}, testing communication...")
        time.sleep(2)  # Let the serial settle

        # Try sending a basic command to test communication
        ser.write(BALANCE)
        time.sleep(0.5)
        
        # Attempt to read response (not all commands respond, so this is soft validation)
        if ser.in_waiting:
            response = ser.readline().decode(errors='ignore').strip()
            print(f"Received from Bittle: {response}")
            print(f"✅ Confirmed connection to Bittle on {SERIAL_PORT}")
        else:
            print("⚠️ No response from device — Bittle may not be connected or silent.")

        return ser

    except Exception as e:
        print(f"❌ Failed to connect to Bittle: {e}")
        return None





def log_action(action):
    print(f"# {action}")

def backward_pattern(bittle, step_idx):
    pattern = [
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("left", SPIN_LEFT, LEFT_DURATION, "Sent: SPIN_LEFT"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
        ("left", SPIN_LEFT, LEFT_DURATION, "Sent: SPIN_LEFT"),
        ("backward", WALK_BACKWARD, BACKWARD_DURATION, "Sent: WALK_BACKWARD"),
    ]
    idx = step_idx % len(pattern)
    cmd_type, cmd, duration, msg = pattern[idx]
    bittle.write(cmd)
    log_action(msg)
    time.sleep(duration)
    if cmd_type == "backward":
        bittle.write(WALK_GAIT)
        log_action("Set Gait: WALK")
        time.sleep(0.1)

def main():
    print("STARTING MAIN")
    bittle = connect_to_bittle()
    if not bittle:
        print("⚠️ Could not connect to Bittle. Continuing with GUI only.")

    control_window = np.zeros((200, 400, 3), dtype=np.uint8)
    current_mode = None
    last_balance_time = time.time()
    backward_step = 0

    # NEW: Movement state tracking
    movement_start = 0
    movement_duration = 0
    movement_in_progress = False

    try:
        print("Entering main loop...")
        while True:
            window = control_window.copy()
            cv2.putText(window, "Bittle Driver Control", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(window, "w/s: forward/back", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "a/d: spin L/R", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "space: stop | q: quit", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, f"Balance every {BALANCE_INTERVAL}s", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            if not bittle:
                cv2.putText(window, "Not connected to Bittle", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.imshow("Bittle Control", window)
            key = cv2.waitKey(1) & 0xFF

            # Handle keypresses
            if key != 0xFF:
                if key == ord('w'):
                    current_mode = 'forward'
                elif key == ord('s'):
                    current_mode = 'backward'
                    backward_step = 0
                elif key == ord('a'):
                    current_mode = 'spin_left'
                elif key == ord('d'):
                    current_mode = 'spin_right'
                elif key == 32:  # space
                    current_mode = None
                    movement_in_progress = False
                    if bittle:
                        bittle.write(BALANCE)
                        log_action("Sent: BALANCE (stop)")
                elif key == ord('q'):
                    log_action("Quit and rest")
                    break

            now = time.time()
            if bittle and current_mode != 'backward' and now - last_balance_time > BALANCE_INTERVAL:
                bittle.write(BALANCE)
                log_action("Sent: BALANCE (periodic)")
                last_balance_time = now

            # Movement handling (non-blocking)
            if bittle:
                if not movement_in_progress:
                    if current_mode == 'forward':
                        bittle.write(WALK_GAIT)
                        log_action("Set Gait: WALK")
                        bittle.write(WALK_FORWARD)
                        log_action("Sent: WALK_FORWARD")
                        movement_start = time.time()
                        movement_duration = 0.5
                        movement_in_progress = True

                    elif current_mode == 'backward':
                        backward_pattern(bittle, backward_step)
                        backward_step += 1
                        # No movement_in_progress needed here

                    elif current_mode == 'spin_left':
                        bittle.write(SPIN_LEFT)
                        log_action("Sent: SPIN_LEFT")
                        movement_start = time.time()
                        movement_duration = 0.5
                        movement_in_progress = True

                    elif current_mode == 'spin_right':
                        bittle.write(SPIN_RIGHT)
                        log_action("Sent: SPIN_RIGHT")
                        movement_start = time.time()
                        movement_duration = 0.5
                        movement_in_progress = True

                else:
                    if time.time() - movement_start >= movement_duration:
                        movement_in_progress = False

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Shutting down.")
        if bittle and bittle.is_open:
            try:
                bittle.write(REST)
                log_action("Sent: REST (shutdown)")
                time.sleep(0.5)
                bittle.close()
            except Exception:
                pass
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
