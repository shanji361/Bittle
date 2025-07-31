#define BITTLE
#define BiBoard_V0_2
#define QUICK_DEMO
#include "src/OpenCat.h"

#ifdef QUICK_DEMO
bool xqToggle = false;        // Tracks ON/OFF state of the demo
bool xqPrevState = false;     // Tracks whether we already processed XQ
bool xqJustPressed = false;   // Flag for edge detection
#endif

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(SERIAL_TIMEOUT);
  while (Serial.available() && Serial.read())
    ;  // empty buffer
  initRobot();
}

void loop() {
#ifdef VOLTAGE
  lowBattery();
#endif
  readEnvironment();
  dealWithExceptions();
  if (!tQueue->cleared()) {
    tQueue->popTask();
  } else {
    readSignal();  // Update command input
    
#ifdef QUICK_DEMO
    // Debug: Print current command for troubleshooting
    if (cmdLen > 0) {
      Serial.print("DEBUG: Command received: ");
      for (int i = 0; i < cmdLen; i++) {
        Serial.print((char)cmd[i]);
      }
      Serial.println();
    }
    
    // Check for the XQ toggle command
    bool xqCurrentlyPressed = (cmdLen == 2 && cmd[0] == 'X' && cmd[1] == 'Q');
    
    // Edge detection: trigger only on transition from false to true
    xqJustPressed = (xqCurrentlyPressed && !xqPrevState);
    
    if (xqJustPressed) {
      xqToggle = !xqToggle;  // Toggle state
      Serial.print("DEBUG: XQ toggled to: ");
      Serial.println(xqToggle ? "ON" : "OFF");
      
      if (xqToggle) {
        Serial.println("DEBUG: Running quickDemo()");
        quickDemo();  // Run once when toggled ON
      }
    }
    
    // Update previous state for next cycle
    xqPrevState = xqCurrentlyPressed;
#endif
  }
  
#ifdef NEOPIXEL_PIN
  playLight();
#endif
  reaction();
#ifdef WEB_SERVER
  WebServerLoop();
#endif
}

#ifdef QUICK_DEMO
void quickDemo() {
  Serial.println("DEBUG: quickDemo() called - adding rest task");
  tQueue->addTask(T_SKILL, "rest", 1000);  // Do whatever demo action here
}
#endif
