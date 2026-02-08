# Raspberry Pi Codes — Smart Toll Tax System

This folder contains all **Python** scripts used on the Raspberry Pi: the full project application, barcode detection and database update, SQL table creation and sample data, and receipt printing for the thermal printer.

---

## Overview

The Pi:

- Talks to the **Arduino** over **serial** (e.g. `/dev/ttyUSB0`, 9600 baud) to receive owner IDs (e.g. from RFID).
- Can also accept **barcode** input from stdin (e.g. from a barcode scanner).
- Updates **MariaDB** (database `ToolTax`): deducts toll, inserts bill, updates current credit.
- Writes the current **owner ID** to `/var/www/html/owner.txt` so the PHP dashboard shows the right vehicle.
- Prints a **receipt** via USB thermal printer (ESC/POS, e.g. Black Copper BC-95AC).
- Sends a **barrier-open** command back to the Arduino over serial (e.g. `"1"`) after a successful transaction.

---

## Scripts in This Folder

| Script | Purpose |
|--------|--------|
| **FullProjectCode.py** | **Main application.** Listens on serial (Arduino) and stdin (barcode). On valid owner ID: updates DB, writes `owner.txt`, prints receipt, signals Arduino to open barrier. |
| **detect-barcode-update-database(Final-WorkingVer).py** | Barcode-based flow: read barcode → map to owner → update DB and (optionally) receipt. Standalone variant of the core logic. |
| **Project Receipt Code( final design).py** | **Receipt-only** script: prints a sample toll receipt (logo, date/time, owner, vehicle, station, amount, barcode) using `python-escpos` and USB printer. |
| **sql-building-table-Insert-values(test1).py** | **SQL setup (variant 1).** Connects to MariaDB, uses `ToolTax`, creates (when uncommented) `Owner`, `Owner_Info`, `Owner_Bill` and inserts sample owners/vehicles/credits/bills. |
| **sql-building-table-Insert-values(test2).py** | **SQL setup (variant 2).** Same idea with slightly different table definitions (e.g. `Arrival_time` as TIME). Use one of the two to build your DB and initial data. |

---

## FullProjectCode.py (main flow)

- **Serial**: Reads from Arduino (e.g. RFID sends `"3"`, `"4"` for owner 3 or 4).
- **Stdin**: Reads barcode lines (e.g. from scanner); maps barcode to owner ID (1–4).
- On valid owner:
  1. **Database**: Checks `Curr_Credit` in `Owner_Info`; if balance &gt; 0: inserts into `Owner_Bill`, updates `Curr_Credit`.
  2. **Web**: Writes owner ID to `/var/www/html/owner.txt`.
  3. **Receipt**: Prints receipt (logo, owner/vehicle/balance, barcode) via USB printer.
  4. **Arduino**: Sends `"1"` on serial to open barrier.
- Uses **threading** for DB update and receipt so the main loop can keep reading serial/stdin.

Database user/password and serial port are in the script (e.g. `admin` / `qwerty123` or `Apetite` in receipt section; `/dev/ttyUSB0`). Match these to your [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md) and LAMP setup.

---

## Barcode → Owner mapping (in FullProjectCode)

| Barcode      | Owner ID | Name   |
|-------------|----------|--------|
| 234953778376 | 1 | Mahwish |
| 247249535553 | 2 | Sayeem  |
| 228853545947 | 3 | Areeba  |
| (else)      | 4 | Maheen  |

RFID from Arduino sends character `"3"` or `"4"` for owner 3 or 4 (UIDs in Arduino sketch).

---

## Database (MariaDB)

- **Database**: `ToolTax`
- **Tables**: `Owner` (owner_id, owner_name, barcode), `Owner_Info` (vehicle_Brand, vehicle_No, Curr_Credit, owner_id), `Owner_Bill` (Cr_Amount, Amount_Deducted, Arrival_time, Arrival, owner_id).

Create tables and insert initial data using the **sql-building-table-Insert-values** scripts: uncomment the `CREATE TABLE` and `INSERT` lines, run once, then comment them again to avoid duplicates. See [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md) for a full SQL summary.

---

## Receipt and printer

- **Project Receipt Code( final design).py**: Standalone receipt print (logo, date/time, sample owner/vehicle, station, toll amount, balance, barcode, cut).
- **FullProjectCode.py** and **detect-barcode-update-database(Final-WorkingVer).py**: Call similar receipt logic with live owner/vehicle/balance from DB.
- **Printer**: USB ESC/POS (e.g. Black Copper BC-95AC). VendorID/ProductID in repo: **Black Copper printer BC-95AC (Configs On Rpi USB).txt** (0483, 5743). Python uses `Usb(0x0483, 0x5743, 0)`.
- **Logo**: Scripts expect `logo.png` in the working directory (or adjust path); use the **logo.png** from the project root.

---

## Dependencies (Python 3)

```bash
pip3 install mysql-connector-python pyserial python-escpos
```

- **mysql-connector-python**: MariaDB/MySQL.
- **pyserial**: Serial communication with Arduino.
- **python-escpos**: USB thermal printer.

---

## Running the main application

1. LAMP and DB set up (see [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)).
2. Arduino connected to Pi over USB (serial); printer connected to Pi USB.
3. From this folder (or with paths adjusted for `logo.png` and DB):

   ```bash
   python3 FullProjectCode.py
   ```

4. Trigger via barcode (stdin) or RFID (Arduino); check `owner.txt` and the PHP dashboard for live updates.

For LAMP install, wiring, and Arduino setup, see **[BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)**.

**Repository:** [github.com/Shahrukh19S/smart-tolltax-rpi](https://github.com/Shahrukh19S/smart-tolltax-rpi)
