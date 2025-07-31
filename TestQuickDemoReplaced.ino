void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);  // USB serial
  Serial.setTimeout(SERIAL_TIMEOUT);
  //  Serial1.begin(115200); //second serial port
  while (Serial.available() && Serial.read())
    ;  // empty buffer
  initRobot();
}

void loop() {
#ifdef VOLTAGE
  lowBattery();
#endif
  //  //—self-initiative
  //  if (autoSwitch) { //the switch can be toggled on/off by the 'z' token
  //    randomMind();//allow the robot to auto rest and do random stuff in randomMind.h
  //    powerSaver(POWER_SAVER);//make the robot rest after a certain period, the unit is seconds
  //
  //  }
  //  //— read environment sensors (low level)
  readEnvironment();  // update the gyro data
  //  //— special behaviors based on sensor events
  dealWithExceptions();  // low battery, fall over, lifted, etc.
  if (!tQueue->cleared()) {
    tQueue->popTask();
  } else {
    readSignal();
#ifdef QUICK_DEMO
    if (moduleList[moduleIndex] == EXTENSION_QUICK_DEMO)
      quickDemo();
#endif
    //  readHuman();
  }
  //  //— generate behavior by fusing all sensors and instruction
  //  decision();

  //  //— action
  //  //playSound();
#ifdef NEOPIXEL_PIN
  playLight();
#endif
  reaction();

#ifdef WEB_SERVER
  WebServerLoop();  // 处理异步Web请求
#endif
}
