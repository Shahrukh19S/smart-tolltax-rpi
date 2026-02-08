# Smart Toll Tax System

An automated toll tax system using **Raspberry Pi** and **Arduino**, with a LAMP-style web dashboard (Linux, Apache, MariaDB, PHP) for real-time vehicle and owner information, Thermal printer for receipt generation, baracode scanner and RFID based manual detection.

**Repository:** [github.com/Shahrukh19S/smart-tolltax-rpi](https://github.com/Shahrukh19S/smart-tolltax-rpi)  


**[▶ Smart Toll Tax System Using Raspberry Pi, Arduino – YouTube](https://www.youtube.com/watch?v=n5ErGz2OViQ)**
[![Project Video](https://img.shields.io/badge/Video-Watch%20on%20YouTube-red?style=flat&logo=youtube)](https://www.youtube.com/watch?v=n5ErGz2OViQ)
---

## 📸 LIVE DASHBOARD

![Live Web Dashboard](LIVE%20DASHBOARD.png)

## 📸 PROJECT HARDWARE

![HARDWARE PROTOTYPE](PROJECT%20HARDWARE.png)

## Overview

This project implements a smart toll booth that:

- **Arduino**: Detects vehicles (ultrasonic), reads RFID cards or triggers barcode scanning, controls conveyor motor, barrier servo, and LEDs. Sends owner ID to Raspberry Pi over serial.
- **Raspberry Pi**: Runs Python to receive serial input, update MariaDB, write `owner.txt` for the web dashboard, and print receipts via USB thermal printer.
- **Web dashboard**: PHP page on Apache reads `owner.txt`, queries MariaDB, and displays live vehicle/owner info with auto-refresh.

The full project paradigm (requirements, design, flow) is documented in the root directory:

- **[Smart Tool Tax System (Paradigm).docx](Smart%20Tool%20Tax%20System%20(Paradigm).docx)** — Complete project paradigm document.

---

## Clone

```bash
git clone https://github.com/Shahrukh19S/smart-tolltax-rpi.git
cd smart-tolltax-rpi
```

---

## Repository Structure

```
smart-tolltax-rpi/
├── README.md                 ← You are here
├── BUILD_INSTRUCTIONS.md     ← Build instructions (LAMP, Arduino, wiring)
├── LICENSE                   ← License terms
├── Smart Tool Tax System (Paradigm).docx
├── logo.png                  ← Printer receipt logo
├── Project Receipt(final Design).jpg
├── Black Copper printer BC-95AC (Configs On Rpi USB).txt
├── Object and Barcodes(PICS)/   ← Sample vehicle/barcode images
├── Arduino Final Code/         ← Production Arduino sketch
├── Arduino (Test-Codes)/       ← Test sketches (RFID, Sonar, Servo)
├── Raspberrypi Codes/          ← Python: full project, barcode, SQL, receipt
└── Website Codes/              ← PHP dashboard (LAMP)
```

| Folder | Description |
|--------|-------------|
| **Arduino Final Code** | Final Arduino sketch: RFID, ultrasonic, conveyor, barrier servo, serial to RPi. |
| **Arduino (Test-Codes)** | Standalone test sketches for RFID, sonar/motor, and servo. |
| **Raspberrypi Codes** | All Python: main project loop, barcode/DB update, SQL table setup, receipt printing. |
| **Website Codes** | PHP dashboard (index.php), assets, and LAMP-related files. |

---

## Quick Start

1. **Hardware**: Assemble Arduino (RFID MFRC522, ultrasonic, servos, motors, LEDs) and connect to Raspberry Pi via USB serial. Connect USB thermal printer (BC-95AC) to RPi.
2. **Software**: Set up LAMP on Raspberry Pi (see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)), create MariaDB database and tables (see [Raspberrypi Codes/README.md](Raspberrypi%20Codes/README.md)), deploy website under Apache.
3. **Run**: Upload Arduino final code, run the main Python script on RPi (e.g. `FullProjectCode.py`), open the PHP dashboard in a browser.

For step-by-step build instructions, LAMP setup, and wiring, see **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)**.

---

## Documentation

- **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** — How to build the LAMP stack on Raspberry Pi, install dependencies, and set up Arduino.
- **[Website Codes/README.md](Website%20Codes/README.md)** — Web dashboard (index.php), LAMP stack, and `owner.txt` integration.
- **[Raspberrypi Codes/README.md](Raspberrypi%20Codes/README.md)** — Python scripts: full project, barcode detection, SQL setup, receipt printing.
- **[Arduino Final Code/README.md](Arduino%20Final%20Code/README.md)** — Final Arduino sketch and pinout.
- **[Arduino (Test-Codes)/README.md](Arduino%20(Test-Codes)/README.md)** — Test sketches for RFID, sonar, and servo.

---

## Project Video

**YouTube:** [Smart Toll Tax System – Project Video](https://www.youtube.com/watch?v=n5ErGz2OViQ)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **MCU** | Arduino (serial to RPi) |
| **SBC** | Raspberry Pi (Raspberry Pi OS) |
| **Web server** | Apache |
| **Backend** | PHP (procedural) |
| **Database** | MariaDB (MySQL-compatible) |
| **Frontend** | HTML, CSS, JavaScript / jQuery |
| **Scripting** | Python 3 (serial, MySQL, ESC/POS printer) |

---

## License

See [LICENSE](LICENSE) in this repository. Project materials are for educational and reference use.
