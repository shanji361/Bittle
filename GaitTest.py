# bittle_left_turn_test.py
# A minimal script to test a 90° left turn command on Bittle.

import serial
import time

# --- Bittle Serial Configuration ---
SERIAL_PORT = '/dev/tty.Bittle4E_SSP'  # Change to your Bittle's serial port
BAUD_RATE = 115200

# --- Bittle Commands ---
TURN_LEFT_90 = b'k vtR 40\n'       # Pre-defined 90° left turn
BALANCE = b'kbalance\n'           # Stand still
TURN_OFF_BALANCE = b'gb\n'        # Turn off auto-balancing
TURN_OFF_VOICE = b'XAd\n'         # Disable voice responses
REST = b'd\n'                     # Power down servos

def connect_to_bittle():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        print(f"[INFO] Connected to Bittle at {SERIAL_PORT}")
        time.sleep(2)
        ser.write(TURN_OFF_BALANCE)
        time.sleep(0.3)
        ser.write(TURN_OFF_VOICE)
        time.sleep(0.3)
        return ser
    except serial.SerialException:
        print(f"[ERROR] Could not connect to {SERIAL_PORT}. Check your connection.")
        return None

def test_turn_left_90(ser):
    print("[ACTION] Balancing...")
    ser.write(BALANCE)
    time.sleep(2)

    print("[ACTION] Turning left 90°...")
    ser.write(TURN_LEFT_90)
    time.sleep(3)

    print("[ACTION] Balancing after turn...")
    ser.write(BALANCE)
    time.sleep(2)

def main():
    ser = connect_to_bittle()
    if not ser:
        return

    try:
        test_turn_left_90(ser)
    finally:
        print("[INFO] Resting and closing connection...")
        ser.write(REST)
        time.sleep(0.5)
        ser.close()

if __name__ == "__main__":
    main()
