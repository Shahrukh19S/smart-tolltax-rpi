# Arduino Test Codes — Smart Toll Tax System

Standalone test sketches used during development. They are **not** the final integration; use **Arduino Final Code** for the full system.

---

## Folders and Sketches

| Folder | Sketch | Purpose |
|--------|--------|---------|
| **RFID__TEST_** | RFID__TEST_.ino | Basic MFRC522 RFID: read card UID, print to Serial, control LED/buzzer/servo on success. |
| **RFID__TEST_without-Serial-Print_** | RFID__TEST_without-Serial-Print_.ino | Same RFID logic without Serial print (e.g. for quieter or production-like testing). |
| **Sonar_and_Motor_Test_ToolTax_** | Sonar_and_Motor_Test_ToolTax_.ino | Ultrasonic (NewPing) + conveyor motor + two servos (scanner + barrier): detect object at 1–20 cm, stop motor, move servos. Different pins than final (e.g. sonar 12/11, servos 9/10). |
| **Sweep_VarServo_Library_Test_** | Sweep_VarServo_Library_Test_.ino | VarSpeedServo library test: sweep a servo (speed/position). |

---

## Usage

1. Open the `.ino` file in the Arduino IDE (each folder is one sketch).
2. Install any required libraries (e.g. **MFRC522**, **NewPing**, **VarSpeedServo**).
3. Select board and port, then upload.
4. Use Serial Monitor where applicable (e.g. 9600 or 115200 for Sonar test).

These sketches help verify RFID, ultrasonic, motor, and servo behavior before running the **Arduino Final Code** and the full Pi + Arduino + LAMP pipeline. For the production sketch, see **[Arduino Final Code/README.md](../Arduino%20Final%20Code/README.md)**. For full build steps, see **[BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)**.

**Repository:** [github.com/Shahrukh19S/smart-tolltax-rpi](https://github.com/Shahrukh19S/smart-tolltax-rpi)
