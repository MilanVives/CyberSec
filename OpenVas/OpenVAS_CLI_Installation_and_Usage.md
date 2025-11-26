# OpenVAS CLI Installation and Usage on Kali Linux

## Overview

This guide covers installing GVM/OpenVAS on Kali Linux and running vulnerability scans from the command line using `gvm-cli`.

---

## 1. Installation

### Install GVM

Run:

```bash
sudo apt update && sudo apt install gvm -y
sudo gvm-setup
sudo gvm-check-setup   # fix any issues it reports
```

If `gvm-setup` finishes successfully it will show an admin user and password (note them).

### Update Existing Installation

If Kali already has `gvm` installed, update and start services:

```bash
sudo apt update && sudo apt upgrade -y
sudo gvm-start
```

---

## 2. Start Services & Verify

```bash
sudo gvm-start
sudo ss -tuln | grep 9392   # should show the web UI socket
sudo gvm-check-setup        # final check
```

If something isn't running, check logs in `/var/log/gvm/` and restart:

```bash
sudo gvm-stop
sudo gvm-start
```

---

## 3. Command Line Usage Examples

### Create Targets

Create a target for scanning and capture the target ID:

```bash
# create target and capture ID
TARGET_XML=$(gvm-cli socket --xml "<create_target><name>linux.vives.live</name><hosts>linux.vives.live</hosts></create_target>")
TARGET_ID=$(echo "$TARGET_XML" | grep -oP '(?<=id=")[^"]+')
echo "TARGET_ID=$TARGET_ID"
```

Repeat for other domains you want to scan.

### Create a Scan Task

Create a task using the **Full and fast** scan config. Replace `<TARGET_ID>` with the target ID you captured:

```bash
TASK_XML=$(gvm-cli socket --xml "<create_task><name>Scan-linux.vives.live</name><config id='daba56c8-73ec-11df-a475-002264764cea'/> <target id='$TARGET_ID'/></create_task>")
TASK_ID=$(echo "$TASK_XML" | grep -oP '(?<=id=")[^"]+')
echo "TASK_ID=$TASK_ID"
```

### Start the Task

```bash
gvm-cli socket --xml "<start_task task_id='$TASK_ID'/>"
```

### Check Task Status

```bash
gvm-cli socket --xml "<get_tasks/>" | sed -n '1,120p'
# look for <status>Running</status> or <status>Done</status>
```

### List All Tasks

```bash
gvm-cli socket --xml "<get_tasks/>"
```

### Export Reports

Once a task completes, list reports and export as PDF or TXT.

List reports for a task and get a report ID:

```bash
gvm-cli socket --xml "<get_reports filter='task_id=$TASK_ID'/>"
```

Then fetch the report (replace `REPORT-ID` and choose format):

```bash
# Save as TXT report
gvm-cli socket --xml "<get_reports report_id='REPORT-ID-HERE' format_id='a994b278-1f62-11e1-96ac-406186ea4fc5'/>" > report.txt
```

If you cannot produce a direct PDF, export XML or TXT and convert later.

---

## 4. Common Scan Configurations

| Config Name | Config ID |
|-------------|-----------|
| Full and fast | `daba56c8-73ec-11df-a475-002264764cea` |
| Full and very deep | `698f691e-7489-11df-9d8c-002264764cea` |
| System Discovery | `8715c877-47a0-438d-98a3-27c7a6ab2196` |

---

## 5. Additional Commands

### Delete a Target

```bash
gvm-cli socket --xml "<delete_target target_id='TARGET-ID-HERE'/>"
```

### Delete a Task

```bash
gvm-cli socket --xml "<delete_task task_id='TASK-ID-HERE'/>"
```

### Stop a Running Task

```bash
gvm-cli socket --xml "<stop_task task_id='$TASK_ID'/>"
```

### Get Task Details

```bash
gvm-cli socket --xml "<get_tasks task_id='$TASK_ID'/>"
```

---

## 6. Troubleshooting

### Feed Sync Issues

If `gvm-setup` fails because feed sync takes too long, run:

```bash
sudo greenbone-feed-sync --type GVMD_DATA
sudo greenbone-feed-sync --type SCAP
sudo greenbone-feed-sync --type CERT
```

Monitor `/var/log/gvm/` for progress.

### PDF Export Issues

If PDF exports are empty on Kali, export as TXT/XML and convert locally.

### Pagination Issues

If there are too many results, use `ignore_pagination=1` when requesting reports via the API.

### Alternative Transport Methods

> 💡 **Note:** If `gvm-cli` uses a different transport (HTTP/TLS), check `gvm-cli --help` and adapt `socket` → `ssh`/`tls` as needed.

---

## 7. Safety / Legal Reminder

Only scan hosts you have **explicit permission** to scan. Unauthorized scanning may be illegal and unethical.

---

**You now have OpenVAS running from the command line on Kali Linux!**
