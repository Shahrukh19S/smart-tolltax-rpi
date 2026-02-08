# Build Instructions — Smart Toll Tax System

**Repository:** [github.com/Shahrukh19S/smart-tolltax-rpi](https://github.com/Shahrukh19S/smart-tolltax-rpi)

This document describes how to set up the **LAMP stack on Raspberry Pi**, Arduino environment, Python dependencies, and wiring so you can run the full Smart Toll Tax System.

---

## Prerequisites

- **Raspberry Pi** (e.g. 3B/4) with Raspberry Pi OS (Linux).
- **Arduino** (Uno or compatible) with USB cable to connect to the Pi.
- **USB thermal printer** (Black Copper BC-95AC or compatible ESC/POS; configs in repo).
- **Hardware**: MFRC522 RFID, ultrasonic sensor (e.g. HC-SR04), servos, DC motor for conveyor, LEDs, barcode scanner (optional, for barcode input).

---

## 1. LAMP Stack on Raspberry Pi

LAMP = **L**inux, **A**pache, **M**ariaDB, **P**HP.

### 1.1 Update system

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 Install Apache

```bash
sudo apt install apache2 -y
```

- Default web root: `/var/www/html/`
- Test: open `http://<raspberry-pi-ip>/` in a browser.

### 1.3 Install MariaDB (MySQL-compatible)

```bash
sudo apt install mariadb-server mariadb-client -y
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

Secure installation (optional but recommended):

```bash
sudo mysql_secure_installation
```

Create database user and database (adjust username/password as needed; must match PHP and Python config):

```bash
sudo mysql -u root -p
```

In MySQL shell:

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'qwerty123';
CREATE DATABASE ToolTax DEFAULT CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON ToolTax.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 1.4 Install PHP and Apache PHP module

```bash
sudo apt install php php-mysql php-mbstring -y
```

- PHP connects to MariaDB via `php-mysql`; `index.php` uses `mysqli` with user `admin` and the database `ToolTax`.

### 1.5 Deploy website files

1. Copy contents of **Website Codes** (e.g. `index.php`, `background.jpg`, vehicle images, etc.) to `/var/www/html/`.
2. Create the `owner.txt` file that the PHP page reads (Python will write to it):

   ```bash
   sudo touch /var/www/html/owner.txt
   sudo chmod 666 /var/www/html/owner.txt
   ```

3. Ensure Apache can read the files: `sudo chown -R www-data:www-data /var/www/html` if needed.

The dashboard will read `owner.txt` for the current owner ID and query MariaDB for owner/vehicle/balance/arrival; it auto-refreshes every 3 seconds.

---

## 2. Database tables (MariaDB)

The Python scripts expect a database **ToolTax** and tables **Owner**, **Owner_Info**, **Owner_Bill**. You can create them using the commented SQL in the Raspberry Pi scripts or run the following (after connecting as `admin` to `ToolTax`):

```sql
USE ToolTax;

CREATE TABLE Owner (
  owner_id INT NOT NULL AUTO_INCREMENT,
  owner_name VARCHAR(255),
  barcode VARCHAR(255),
  INDEX USING BTREE(owner_name),
  PRIMARY KEY(owner_id)
);

CREATE TABLE Owner_Info (
  o_info_id INT NOT NULL AUTO_INCREMENT,
  vehicle_Brand VARCHAR(255),
  vehicle_No VARCHAR(255),
  Curr_Credit INT,
  owner_id INT,
  INDEX USING BTREE(vehicle_Brand),
  PRIMARY KEY(o_info_id),
  CONSTRAINT FOREIGN KEY(owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Owner_Bill (
  bill_No INT NOT NULL AUTO_INCREMENT,
  Cr_Amount INT,
  Amount_Deducted INT,
  Arrival_time TIME(0),
  Arrival TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  owner_id INT,
  INDEX USING BTREE(Arrival_time),
  PRIMARY KEY(bill_No),
  CONSTRAINT FOREIGN KEY(owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;
```

Then insert sample owners and credits (see **Raspberrypi Codes/README.md** and the `sql-building-table-Insert-values(test1).py` / `test2` scripts for exact INSERT statements).

---

## 3. Python environment on Raspberry Pi

### 3.1 Python 3 and pip

```bash
sudo apt install python3 python3-pip -y
```

### 3.2 Required packages

- `mysql-connector-python` — MariaDB/MySQL access.
- `pyserial` — Serial communication with Arduino.
- `python-escpos` — USB thermal printer (ESC/POS).

```bash
pip3 install mysql-connector-python pyserial python-escpos
```

(Use `pip3 install --user` or a virtualenv if you prefer.)

### 3.3 Serial and printer

- **Arduino**: Connect Arduino to Raspberry Pi via USB; the Python code uses `/dev/ttyUSB0` at 9600 baud (adjust in code if your device is different, e.g. `ttyACM0`).
- **Printer**: Plug the Black Copper BC-95AC (or compatible) into a RPi USB port. The repo includes **Black Copper printer BC-95AC (Configs On Rpi USB).txt** (VendorID: 0483, ProductID: 5743). The Python receipt scripts use `Usb(0x0483, 0x5743, 0)`.

---

## 4. Arduino setup

### 4.1 IDE and board

- Install [Arduino IDE](https://www.arduino.cc/en/software) (or use Arduino CLI).
- Select the correct board (e.g. Arduino Uno) and port.

### 4.2 Libraries (Final Code)

- **NewPing** — Ultrasonic (HC-SR04).
- **VarSpeedServo** — Servo control (scanner and barrier).
- **MFRC522** (by GithubCommunity) — RFID.
- **SPI** — Built-in.

Install via Sketch → Include Library → Manage Libraries (search by name).

### 4.3 Upload

- Open **Arduino Final Code/SmartTollTax_Final-Code_.ino**.
- Upload to the Arduino.
- Connect Arduino to the Raspberry Pi via USB so the Pi receives serial data (e.g. owner ID `"3"`, `"4"` for RFID, or barcode flow handled on RPi side).

---

## 5. Wiring (Arduino — reference only)

The final sketch uses (see **Arduino Final Code/README.md** for full pinout):

| Component        | Pin(s) / Notes                    |
|-----------------|------------------------------------|
| MFRC522 RFID    | SS: 10, RST: 9, SPI                |
| Ultrasonic      | Trigger: 8, Echo: 7                |
| Conveyor motor  | 2, 3                               |
| Red LED         | 5                                  |
| Green LED       | 4                                  |
| Scanner servo   | 6                                  |
| Barrier servo   | 9 (same as RST in code — verify)   |
| RFID manual pin | A0 (INPUT_PULLUP)                  |

Double-check pin definitions in the sketch and your actual wiring.

---

## 6. Running the system

1. **Arduino**: Powered and connected to RPi via USB; running the final sketch.
2. **Raspberry Pi**:
   - Apache and MariaDB running (`sudo systemctl status apache2`, `sudo systemctl status mariadb`).
   - Website deployed under `/var/www/html/`, `owner.txt` writable.
   - Run the main Python script (e.g. from **Raspberrypi Codes**):

     ```bash
     cd /path/to/Raspberrypi\ Codes
     python3 FullProjectCode.py
     ```

   - Ensure serial port is correct (`/dev/ttyUSB0` or `/dev/ttyACM0`) and printer is connected.
3. **Web dashboard**: Open `http://<raspberry-pi-ip>/index.php` in a browser to see live owner/vehicle/balance and arrival info.

For details on each Python script (barcode detection, SQL setup, receipt design), see **[Raspberrypi Codes/README.md](Raspberrypi%20Codes/README.md)**.

---

## 7. Troubleshooting

- **PHP “Connection failed”**: Check MariaDB is running, user `admin` and password match in `index.php`, and database `ToolTax` and tables exist.
- **Blank or wrong dashboard**: Ensure `owner.txt` contains a valid owner ID (e.g. 1–4) and that the Python script has written to it; check file permissions.
- **Python “Access denied” for MySQL**: Use the same user/password as in the PHP and SQL setup (`admin` / `qwerty123` or your choice).
- **Serial not found**: Run `ls /dev/ttyUSB* /dev/ttyACM*` with Arduino plugged in; update the port in the Python script.
- **Printer not found**: Confirm USB IDs (0483:5743 for BC-95AC) and that the printer is powered and detected (`lsusb`).

For project paradigm and high-level design, see the root **README.md** and **Smart Tool Tax System (Paradigm).docx**.
