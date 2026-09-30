# 🧪 Snort Intrusion Detection System (IDS) Lab

## Objective

In this lab, you will:

- Install and configure Snort on a Linux system.
- Create and enable basic custom Snort rules.
- Test Snort’s detection capabilities.
- Analyze alert logs.

---

## 🧰 Prerequisites

- A Linux-based VM (Ubuntu 22.04 LTS recommended)
- Root or sudo privileges
- Internet access

---

## 1️⃣ Install Snort

### Step 1: Update your system

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install dependencies

```bash
sudo apt install -y build-essential libpcap-dev libpcre3-dev libdumbnet-dev bison flex zlib1g-dev
```

### Step 3: Install Snort

```bash
sudo apt install -y snort
```

> During installation, you may be prompted to set your network interface and home network.  
> Example home network: `192.168.1.0/24`

Check version:

```bash
snort -V
```

---

## 2️⃣ Configure Snort

### Step 1: Identify your network interface

```bash
ip link show
```

Example output: `eth0` or `ens33`

### Step 2: Configure HOME_NET

Edit the configuration file:

```bash
sudo nano /etc/snort/snort.conf
```

Find and set:

```
var HOME_NET 192.168.1.0/24
```

### Step 3: Verify configuration

```bash
sudo snort -T -c /etc/snort/snort.conf
```

---

## 3️⃣ Create Custom Rules

### Step 1: Create a local rules file

```bash
sudo nano /etc/snort/rules/local.rules
```

### Step 2: Add sample rules

```bash
# Detect ICMP ping
alert icmp any any -> $HOME_NET any (msg:"ICMP Ping detected"; sid:1000001; rev:1;)

# Detect HTTP traffic on port 80
alert tcp any any -> $HOME_NET 80 (msg:"HTTP request detected"; sid:1000002; rev:1;)

# Detect Nmap scan (SYN scan)
alert tcp any any -> $HOME_NET any (flags:S; msg:"Possible Nmap scan"; sid:1000003; rev:1;)
```

### Step 3: Include local rules in main config

Ensure this line exists and is **uncommented** in `/etc/snort/snort.conf`:

```
include $RULE_PATH/local.rules
```

---

## 4️⃣ Run Snort in IDS Mode

### Step 1: Start Snort in console alert mode

```bash
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
```

> Replace `eth0` with your actual interface.

Snort is now monitoring traffic in real-time.

---

## 5️⃣ Test the Rules

### Test 1: ICMP Ping

From another host, ping the Snort machine:

```bash
ping <Snort_IP>
```

Snort should display:

```
[**] [1:1000001:1] ICMP Ping detected [**]
```

### Test 2: HTTP Traffic

Open a browser or use curl:

```bash
curl http://<Snort_IP>
```

Expected alert:

```
[**] [1:1000002:1] HTTP request detected [**]
```

### Test 3: Nmap Scan

Run from another machine:

```bash
nmap -sS <Snort_IP>
```

Expected alert:

```
[**] [1:1000003:1] Possible Nmap scan [**]
```

---

## 6️⃣ Viewing Logs

Snort also logs alerts to:

```
/var/log/snort/alert
```

To view logs:

```bash
sudo tail -f /var/log/snort/snort.alert.fast
```

---

## ✅ Cleanup

To stop Snort:

```bash
Ctrl + C
```

To remove Snort:

```bash
sudo apt remove --purge snort -y
```

---

## 📘 Summary

In this lab, you:

- Installed Snort on Linux.
- Configured custom detection rules.
- Tested detection for ping, HTTP, and Nmap.
- Verified alerts via console and log files.

---

## 🧩 Bonus Challenges

1. Create a rule that detects SSH login attempts (port 22).
2. Configure Snort to log to `/var/log/snort/snort.log`.
3. Integrate Snort with a GUI like **Snorby** or **BASE**.

---

**Author:** Milan Dima milan.dima@vives.be
**Version:** 1.0  
**Date:** 2025-10-21
