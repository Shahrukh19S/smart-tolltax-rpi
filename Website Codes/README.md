# Website Codes — Smart Toll Tax System

PHP-based web dashboard for the Raspberry Pi–hosted Smart Toll Tax System. The application uses **Apache**, **PHP**, and **MariaDB** to display vehicle and owner information from the database, with updates driven by hardware (via `owner.txt`) and automatic page refresh.

---

## Stack (LAMP-style on Raspberry Pi)

| Layer            | Technology              |
|------------------|-------------------------|
| OS               | Linux (Raspberry Pi OS) |
| Web server       | Apache                  |
| Backend          | PHP (procedural)        |
| Database         | MariaDB (MySQL-compatible) |
| Frontend         | HTML + CSS              |
| Client-side JS   | Vanilla JavaScript + jQuery |
| Hardware link    | Raspberry Pi + `owner.txt` |

This is a **LAMP-style stack** (Linux, Apache, MySQL/MariaDB, PHP) adapted for Raspberry Pi. The page is a single PHP file with inline CSS and mixed PHP/HTML (monolithic style).

---

## What `index.php` Does

The page is **not static**. It acts as a **live dashboard** driven by the current database and hardware state.

1. **Reads** the current owner ID from the local file `owner.txt`.
2. **Connects** to the MariaDB database (`ToolTax`).
3. **Queries**:
   - Owner name (`Owner` table)
   - Vehicle brand, vehicle number, current credit (`Owner_Info` table)
   - Arrival time (`Owner_Bill` table)
4. **Renders**:
   - Vehicle image (by brand)
   - Owner and vehicle info
   - Toll deduction summary (amount deducted, balance, arrival)
5. **Auto-refreshes** the page every 3 seconds (client-side reload).

So the “state” of the dashboard is determined by whatever owner ID is written to `owner.txt` (by the Python process on the Pi) and the corresponding rows in the database.

---

## The `owner.txt` File

In `index.php`:

```php
$owner = file_get_contents('owner.txt');
```

This means:

- The system is **hardware-driven**: another process (the Python script on the Pi) updates `owner.txt` when a vehicle is detected (barcode or RFID).
- The PHP page **reacts** to that state by reading the file and querying the database.
- This is a typical **embedded–web integration** pattern: hardware updates a simple file, and the web UI reflects it.

For the dashboard to work:

1. `owner.txt` must exist under the web root (e.g. `/var/www/html/owner.txt`).
2. It must contain a single value: the **owner ID** (e.g. `1`, `2`, `3`, `4`).
3. The web server (and PHP) must have read permission; the Python script must have write permission (see [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)).

---

## Files in This Folder

| File / asset      | Purpose |
|-------------------|--------|
| `index.php`       | Main dashboard: reads `owner.txt`, queries MariaDB, outputs HTML and refresh script. |
| `owner.txt`       | Written by Python on the Pi; contains current owner ID. Create/configure on server. |
| `background.jpg`  | Background image for the page. |
| `page template.html` / `page template.png` | Template/reference for layout. |
| Vehicle images    | e.g. `honda-accord.jpg`, `Mitsubishi-Lancer.jpg`, `Suzuki-Swift.jpg`, `toyota-corolla.jpg`, `toyota-vitz.jpg` — must match `vehicle_Brand` values in DB. |

Database user/password in `index.php` must match your MariaDB setup (e.g. `admin` / `qwerty123` as in [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)).

---

## Deployment (summary)

1. Copy all files from **Website Codes** to the Apache document root on the Pi (e.g. `/var/www/html/`).
2. Create `owner.txt` and set permissions so PHP can read it and Python can write it (see [BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)).
3. Ensure MariaDB has the `ToolTax` database and `Owner`, `Owner_Info`, `Owner_Bill` tables populated.
4. Open `http://<raspberry-pi-ip>/index.php` in a browser.

For full LAMP and project build steps, see the root **[BUILD_INSTRUCTIONS.md](../BUILD_INSTRUCTIONS.md)**.

**Repository:** [github.com/Shahrukh19S/smart-tolltax-rpi](https://github.com/Shahrukh19S/smart-tolltax-rpi)
