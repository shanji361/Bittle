import cv2
import serial
import time
import numpy as np

# --- SERIAL CONFIGURATION ---
SERIAL_PORT = '/dev/tty.BittleB3_SSP'
BAUD_RATE = 115200

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
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Bittle on {SERIAL_PORT}")
        time.sleep(2)
        return ser
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def log_action(action):
    print(f"# {action}")

def run_command(bittle, command, duration, message):
    bittle.write(command)
    log_action(message)
    time.sleep(duration)
    bittle.write(BALANCE)
    log_action("Sent: BALANCE (stop)")

def run_triangle_2_script(bittle):
    sequence = [
        (WALK_FORWARD, 3.55, "Sent: WALK_FORWARD"),
        (WALK_BACKWARD, 2.01, "Sent: WALK_BACKWARD"),
        (WALK_BACKWARD, 1.62, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 5.27, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 1.62, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 4.36, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 1.09, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 8.64, "Sent: SPIN_RIGHT"),
        (WALK_FORWARD, 3.20, "Sent: WALK_FORWARD"),
        (WALK_BACKWARD, 1.38, "Sent: WALK_BACKWARD"),
        (WALK_BACKWARD, 1.92, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 4.82, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 1.92, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 4.25, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 2.12, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 2.52, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 1.80, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 3.09, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 1.69, "Sent: WALK_BACKWARD"),
        (WALK_BACKWARD, 1.69, "Sent: WALK_BACKWARD"),
        (SPIN_LEFT, 2.17, "Sent: SPIN_LEFT"),
        (WALK_BACKWARD, 1.25, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 3.44, "Sent: SPIN_RIGHT"),
        (WALK_BACKWARD, 6.61, "Sent: WALK_BACKWARD"),
        (SPIN_RIGHT, 1.71, "Sent: SPIN_RIGHT"),
        (SPIN_LEFT, 5.63, "Sent: SPIN_LEFT"),
        (SPIN_RIGHT, 1.59, "Sent: SPIN_RIGHT"),
        (WALK_FORWARD, 1.94, "Sent: WALK_FORWARD"),
        (SPIN_RIGHT, 1.01, "Sent: SPIN_RIGHT"),
        (WALK_FORWARD, 3.55, "Sent: WALK_FORWARD"),
    ]
    for cmd, duration, msg in sequence:
        run_command(bittle, cmd, duration, msg)

def main():
    bittle = connect_to_bittle()
    if not bittle:
        return

    control_window = np.zeros((200, 400, 3), dtype=np.uint8)

    try:
        print("Bittle Driver Control")
        print("Press 'w' to run Triangle 2 script")
        print("Press 'q' to quit at any time")
        bittle.write(BALANCE)
        log_action("Sent: BALANCE (startup)")
        time.sleep(0.5)

        while True:
            window = control_window.copy()
            cv2.putText(window, "Bittle Script Runner", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(window, "w: run Triangle 2", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "i/k/h: Head Up/Down/Center", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(window, "q: quit", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.imshow("Bittle Control", window)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                log_action("Quit and rest")
                break
            elif key == ord('w'):
                log_action("Running Triangle 2 Script...")
                run_triangle_2_script(bittle)
            elif key == ord('i'):
                bittle.write(HEAD_UP)
                log_action("Sent: HEAD_UP")
            elif key == ord('k'):
                bittle.write(HEAD_DOWN)
                log_action("Sent: HEAD_DOWN")
            elif key == ord('h'):
                bittle.write(HEAD_CENTER)
                log_action("Sent: HEAD_CENTER")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
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
