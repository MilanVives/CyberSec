# OpenVAS (GVM) — Scanning with the Web Interface

The **Greenbone Security Assistant (GSA)** is the browser interface to OpenVAS: you
define targets, run scan tasks and read or export the reports.

> **Prerequisite:** GVM installed and `sudo gvm-check-setup` reports *installation
> is OK*. If not, follow [OpenVAS_Installation_and_Troubleshooting.md](OpenVAS_Installation_and_Troubleshooting.md) first.

---

## 1. Start and log in

```bash
sudo gvm-start
```

Browse to **https://127.0.0.1:9392**, accept the self-signed certificate warning
(fine in a lab), and log in as `admin` with the password from `gvm-setup`.

## 2. Check the feed first

Go to **Administration → Feed Status**. All rows (NVT, SCAP, CERT, GVMD_DATA) must
show **Current**. While any row says *Update in progress*, wait — scans started now
fail or return nothing.

Then check **Configuration → Scan Configs**: you should see **Full and fast**. If the
list is empty, the feed is still importing.

## 3. Create a target

1. **Configuration → Targets**
2. Click the **New Target** icon (top left)
3. Fill in:
   - **Name**: `linux.vives.live`
   - **Hosts**: *Manual* → `linux.vives.live`
   - **Port List**: `All IANA assigned TCP` (default)
   - **Alive Test**: `Consider Alive` — many internet hosts drop ICMP ping, and with
     the default test OpenVAS then skips the host and reports nothing
4. **Save**

Repeat for every host you are allowed to scan.

## 4. Create and start a task

1. **Scans → Tasks**
2. **New Task** icon → *New Task*
3. Fill in:
   - **Name**: `Scan-linux.vives.live`
   - **Scan Targets**: the target from step 3
   - **Scanner**: `OpenVAS Default`
   - **Scan Config**: `Full and fast`
4. **Save**, then click the **Start** (▶) icon on the task row

Start all your tasks right away — they run in parallel, and one *Full and fast*
scan of an internet host typically takes **15–45 minutes**.

## 5. Read the results

1. **Scans → Tasks**, wait until **Status** shows *Done*
2. Click the date in the **Last Report** column
3. The **Results** tab lists every finding with its severity (CVSS) and QoD
   (Quality of Detection — how sure OpenVAS is; < 70 % means "possibly a false
   positive")
4. Click a result for the **Summary**, **Detection method**, **Impact**,
   **Solution** and **References** (CVE, CERT advisories)

Useful filters (type into the filter bar):

```
severity>7.0                  # only High and Critical
rows=-1 sort-reverse=severity # everything, worst first
```

## 6. Export a report

In the report view, click the **Download** icon and choose a format:

| Format | Notes |
|---|---|
| **PDF** | Needs LaTeX on Kali — if the PDF is empty, see the troubleshooting table |
| **TXT** | Plain text, always works |
| **CSV Results** | One line per finding, handy for a spreadsheet |
| **XML** | Complete raw data |

## 7. Stop

```bash
sudo gvm-stop
```

---

## Safety reminder

Only scan hosts you have **explicit, written authorization** to test. Unauthorized
scanning can be a criminal offence (in Belgium: Art. 550bis Sw.).
