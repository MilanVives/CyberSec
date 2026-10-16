# LAB 2 --- IoT Reconnaissance & Vulnerability Assessment (Shodan + Kali)

## Objective

Students will discover IoT devices, fingerprint them, and identify
vulnerabilities that map to OWASP IoT risks.

## Part 1 --- Shodan OSINT

### Step 1 --- Create a Shodan account

Use TOR or privacy methods.

### Step 2 --- Example Shodan queries

- `port:23 "default password"`
- `has_screenshot:true webcam`
- `ssl:"Nest"`

Also see [Shodan IoT Search Strings](Shodan_IoT_Search_Strings.md)

## Part 2 --- Local IoT Scanning

### Step 3 --- Identify devices on LAN

    sudo nmap -sn 192.168.1.0/24

### Fingerprint a device

    sudo nmap -sV -O <IoT-IP>

## Part 3 --- IoTsploit Vulnerability Testing

### Step 4 --- Install IoTsploit

    sudo apt install python3-pip
    pip3 install iotsploit
    iotsploit

### Step 5 --- Run scan

    use scanners/basic_scan
    set target <IoT-IP>
    run

## Part 4 --- Default Credential Testing

Try: - admin:admin\

- admin:1234\
- root:root

## Part 5 --- Defense

- Disable Telnet\
- Firmware updates\
- Strong passwords\
- Disable UPnP\
- Segregate IoT on a DMZ

## Lab Questions

1.  Identify three OWASP IoT Top 10 issues found.\
2.  Map each to the OWASP IoT Attack Surface table.\
3.  Explain how Mirai used default passwords.\
4.  Suggest a segmentation defense.
