# Arduino Final Code — Smart Toll Tax System

Production Arduino sketch for the Smart Toll Tax System: **RFID** (MFRC522), **ultrasonic** vehicle detection, **conveyor motor**, **scanner servo**, **barrier servo**, and **LEDs**. Communicates with the Raspberry Pi over **serial** (9600 baud).

---

## File

- **SmartTollTax_Final-Code_.ino** — Single sketch; open this in the Arduino IDE.

---

## Pinout (as in sketch)

| Function | Pin | Notes |
|----------|-----|--------|
| MFRC522 SS | 10 | SPI chip select |
| MFRC522 RST | 9 | Reset (note: barrier servo also uses 9 in this sketch — verify your wiring; you may need to move one to another pin) |
| Ultrasonic trigger | 8 | HC-SR04 |
| Ultrasonic echo | 7 | HC-SR04 |
| Conveyor motor | 2, 3 | Direction control |
| Red LED | 5 | Status |
| Green LED | 4 | Status |
| Scanner servo | 6 | Barcode scanner rotation |
| Barrier servo | 9 | Barrier open/close |
| RFID manual switch | A0 | INPUT_PULLUP; LOW = use RFID |

---

## Behavior

1. **Loop (no serial from Pi)**  
   - Run conveyor (forward).  
   - Read ultrasonic distance.  
   - Red LED on, Green LED off.  
   - If **distance 1–20 cm** and **A0 HIGH** (no manual RFID): stop conveyor, run **scanner servo** (simulate barcode scan).  
   - If **distance 1–20 cm** and **A0 LOW** (manual RFID): stop conveyor, run **detectRFIDOwner()** and send owner ID on serial (e.g. `"3"`, `"4"`).  
   - Otherwise keep conveyor running.

2. **Serial from Pi**  
   - When Pi sends `'1'`: open barrier (servo 90°), green LED on, red off, conveyor forward for ~6 s, then close barrier and revert LEDs.

3. **RFID**  
   - **detectRFIDOwner()**: Reads MFRC522; if UID matches Areeba card → send `"3"`; if Maheen card → send `"4"`. Other cards: no serial, barrier stays closed.  
   - Change the UID strings in code to match your RFID cards.

---

## Libraries (Arduino IDE)

- **NewPing** — Ultrasonic (HC-SR04).
- **VarSpeedServo** — Servo speed/position (scanner and barrier).
- **MFRC522** — RFID (SPI).
- **SPI** — Built-in.

Install via **Sketch → Include Library → Manage Libraries** (search by name).

---

## Serial protocol

- **Baud rate**: 9600.
- **Arduino → Pi**: Sends single character for owner ID (e.g. `'3'`, `'4'`) when RFID is used.
- **Pi → Arduino**: Sends `'1'` to open barrier after a successful toll transaction.

Connect Arduino to the Raspberry Pi via USB; the Pi Python script uses the same serial port (e.g. `/dev/ttyUSB0`).

---

## Wiring note

In the sketch, **barrier** and **MFRC522 RST** are both on pin **9**. If you see conflicts, move the barrier servo to another free digital pin (e.g. 11) and update `barrier` in the code.

For test sketches (RFID only, sonar+motor, servo sweep), see **[Arduino (Test-Codes)/README.md](../Arduino%20(Test-Codes)/README.md)**. For full system build, see **[BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)**.

**Repository:** [github.com/Shahrukh19S/smart-tolltax-rpi](https://github.com/Shahrukh19S/smart-tolltax-rpi)
