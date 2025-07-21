# 🐶 How to Set Up Bittle

This guide walks you through setting up the Petoi **Bittle** robot using the BiBoard V0, Arduino IDE, and the `pyBittle` Python library.

## 1. Install Arduino IDE 1.8.18

Bittle requires Arduino IDE **1.8.18** (not the 2.x versions).

👉 [Download Arduino 1.8.18](https://www.arduino.cc/en/software/OldSoftwareReleases/)

> 💡 Choose the correct version for your operating system (Windows, macOS, or Linux).

## 2. Set Up the BiBoard V0

Follow Petoi’s official documentation to understand the BiBoard’s layout and wiring.

📘 [BiBoard V0 Guide](https://docs.petoi.com/biboard/biboard-v0#id-2.-modules-and-functions)

> 🛠️ This explains wiring, power setup, and module functions.

## 3. Upload Code to the BiBoard

Use the Arduino IDE to upload a sketch to Bittle’s BiBoard.

📥 [Upload Sketch to BiBoard Guide](https://docs.petoi.com/arduino-ide/upload-sketch-for-biboard)

> 📌 Make sure you install the necessary board definitions and libraries.

## 4. Install `pyBittle` (Python Library)

`pyBittle` lets you communicate with Bittle via Python scripts over a serial connection.

Open a terminal and run:

```bash
pip install pyBittle
