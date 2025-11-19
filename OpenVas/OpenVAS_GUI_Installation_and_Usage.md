# OpenVAS (GVM) GUI Installation and Usage on Kali Linux

## Overview

OpenVAS (Greenbone Vulnerability Management, or GVM) includes a **graphical web interface** called **Greenbone Security Assistant (GSA)**.  
This GUI lets you configure targets, run scans, and view reports — all from a browser.

---

## 1. Install GVM (Includes GUI)

Update your system and install GVM:

```bash
sudo apt update
sudo apt install gvm -y
```

---

## 2. Initialize and Configure OpenVAS

Run the setup script to initialize the system:

```bash
sudo gvm-setup
```

This command will:
- Create users and the PostgreSQL database.
- Sync vulnerability feeds (takes 15–30 minutes).
- Generate login credentials for the web GUI.

When finished, note the printed username and password.

---

## 3. Start the GUI (Greenbone Security Assistant)

Once setup is complete, start all GVM services:

```bash
sudo gvm-start
```

You should see something like:

```
Starting Greenbone Security Assistant: gsad
Starting Greenbone Vulnerability Manager: gvmd
Starting OpenVAS Scanner: ospd-openvas
```

Then open your web browser and navigate to:

👉 **https://127.0.0.1:9392**  
or  
👉 **https://localhost:9392**

Log in with the credentials created during setup.

---

## 4. Check and Manage Services

Verify setup health:

```bash
sudo gvm-check-setup
```

Stop services when needed:

```bash
sudo gvm-stop
```

---

## 5. Using the GUI

### Create a Target

1. Navigate to **Configuration** → **Targets**
2. Click the **star icon** (New Target)
3. Fill in:
   - **Name**: e.g., "linux.vives.live"
   - **Hosts**: Enter the hostname or IP (e.g., `linux.vives.live`)
4. Click **Save**

### Create and Run a Scan Task

1. Navigate to **Scans** → **Tasks**
2. Click the **star icon** (New Task)
3. Fill in:
   - **Name**: e.g., "Scan-linux.vives.live"
   - **Scan Targets**: Select the target you created
   - **Scanner**: Use "OpenVAS Default"
   - **Scan Config**: Choose "Full and fast" (recommended for most scans)
4. Click **Save**
5. Click the **play icon** to start the scan

### View Scan Results

1. Navigate to **Scans** → **Tasks**
2. Wait for the task status to show "Done"
3. Click on the task name to view details
4. Click **Results** tab to see vulnerabilities found
5. Filter by severity: Critical, High, Medium, Low

### Export Reports

1. Go to **Scans** → **Reports**
2. Select the report you want to export
3. Click the **download icon**
4. Choose format: **PDF**, **HTML**, **XML**, or **CSV**
5. Click **OK** to download

---

## 6. Common GUI Features

Once logged in, you can:
- Manage **Targets** (systems to scan)
- Create and schedule **Tasks**
- View **Reports**, **Results**, and **CVEs**
- Export data in **HTML, PDF, XML, or CSV**
- Monitor scan progress through interactive dashboards
- View vulnerability details with CVSS scores
- Access remediation recommendations

---

## 7. Advanced Configuration

### Reset GUI Password (If Lost)

If you forget your admin password, reset it as follows:

```bash
sudo runuser -u _gvm -- gvmd --user=admin --new-password='NewStrongPassword'
```

### Access the GUI Remotely (Optional)

If you're running Kali as a VM or remote server, you can make the GUI accessible from your local network:

```bash
sudo gsad --listen=0.0.0.0 --port=9392
```

Then, access the GUI from another computer using:

```
https://<your-kali-ip>:9392
```

> ⚠️ **Security Warning:** Only expose the GSA web interface in a trusted lab environment. Use firewalls and HTTPS certificates for production use.

---

## 8. Troubleshooting GUI Issues

### GSA not loading on port 9392

Try restarting the service manually:

```bash
sudo gvm-stop
sudo gvm-start
```

If still not accessible, check if `gsad` is running:

```bash
sudo ss -tuln | grep 9392
```

### Feed not synced / missing scan configs

Manually sync feeds:

```bash
sudo greenbone-feed-sync --type GVMD_DATA
sudo greenbone-feed-sync --type SCAP
sudo greenbone-feed-sync --type CERT
```

### Browser Certificate Warnings

The GUI uses a self-signed certificate. You can safely proceed past the browser warning in a lab environment.

---

## 9. Summary Table

| Action | Command | GUI Access |
|--------|----------|------------|
| Install GVM | `sudo apt install gvm` | — |
| Setup | `sudo gvm-setup` | — |
| Start services | `sudo gvm-start` | https://127.0.0.1:9392 |
| Check setup | `sudo gvm-check-setup` | — |
| Stop services | `sudo gvm-stop` | — |
| Reset password | `sudo runuser -u _gvm -- gvmd --user=admin --new-password='NewStrongPassword'` | — |

---

## 10. Safety Reminder

Only scan hosts you have **explicit authorization** to test. Unauthorized scanning can be illegal or unethical.

---

**You now have a full-featured vulnerability management GUI running on Kali Linux!**
