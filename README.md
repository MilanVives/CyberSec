# CEH/Cyber Security Course Materials

This repository contains course materials, practical labs, and assignments for the **Certified Ethical Hacker (CEH)** and **Cyber Security** courses.

## Contents

This repository includes:

- **Practical Lab Exercises** - Hands-on labs for vulnerability scanning, penetration testing, and security assessment tools
- **Course Assignments** - Structured exercises and projects for students
- **Installation Guides** - Step-by-step setup instructions for security tools
- **Documentation** - Technical guides and reference materials

## Labs by Chapter

Labs are organised by chapter of the course textbook, *CEH Certified Ethical Hacker
All-in-One Exam Guide, 5th Edition* (Matt Walker), matching the course slides.
Chapters without a folder have no lab yet.

### Chapter 1 — Getting Started: Essential Knowledge

- [**Wireshark: Packet Capture and Protocol Analysis**](CH01-Getting-Started/wireshark/Lab1_Wireshark_Traffic_Analysis.md) — 90-minute lab with report template and rubric ([folder README](CH01-Getting-Started/wireshark/README.md))

### Chapter 3 — Scanning and Enumeration

- [**OpenVAS Lab Assignment**](CH03-Scanning-and-Enumeration/openvas/OpenVAS_Assignment.md) — pre-lab install + 60-minute scan
- [OpenVAS Installation and Troubleshooting (Kali)](CH03-Scanning-and-Enumeration/openvas/OpenVAS_Installation_and_Troubleshooting.md)
- [OpenVAS Web Interface Usage](CH03-Scanning-and-Enumeration/openvas/OpenVAS_GUI_Usage.md)
- [OpenVAS Command Line Usage (`gvm-cli`)](CH03-Scanning-and-Enumeration/openvas/OpenVAS_CLI_Usage.md)

### Chapter 4 — Sniffing and Evasion

- [**Snort IDS Lab**](CH04-Sniffing-and-Evasion/snort/snort_lab_guide.md)
- [iptables Lab (Ubuntu 24.04)](CH04-Sniffing-and-Evasion/iptables/ubuntu-24.04-iptables-fun-lab.md)
- [UFW Lab (Ubuntu 24.04)](CH04-Sniffing-and-Evasion/ufw/ubuntu-24.04-ufw-fun-lab.md)

### Chapter 5 — Attacking a System

- [**Lab 1 — Password Cracking (John the Ripper)**](CH05-Attacking-a-System/lab1_password_cracking.md)
- [**Lab 2 — Steganography**](CH05-Attacking-a-System/lab2_steganography.md)
- Extended versions: [password cracking](CH05-Attacking-a-System/extended/lab1_student.md), [steganography](CH05-Attacking-a-System/extended/lab2_student.md)

### Chapter 6 — Web-Based Hacking: Servers and Applications

- [**Lab 1 — Web Vulnerability Assessment with Nikto**](CH06-Web-Hacking/nikto_lab.md)
- [**Lab 2 — Web Application Testing with Burp Suite**](CH06-Web-Hacking/burpsuite_lab.md)
- [Burp Suite demo: intercepting & manipulating requests](CH06-Web-Hacking/BurpSuite_Intercept_Manipulate_Demo.md) (target app in `phptest/`)

### Chapter 7 — Wireless Network Hacking

- [**Wireshark Analysis of WEP Traffic**](CH07-Wireless-Hacking/Lab1.md)
- [**Virtual WEP Crack with Aircrack-ng**](CH07-Wireless-Hacking/Lab2.md)
- [**ChopChop Attack Analysis**](CH07-Wireless-Hacking/lab_chopchop.md)

### Chapter 8 — Mobile Communications and the IoT

- [**Mobile App Security Analysis (APKTool, Jadx)**](CH08-Mobile-and-IoT/Lab1-MobileAppSecurityAnalysis.md)
- [**Mobile Network Traffic Analysis & MitM**](CH08-Mobile-and-IoT/Lab2-MobileNetworkTrafficAnalysis.md)
- [**Mobile Device Attacks & Bluetooth**](CH08-Mobile-and-IoT/Lab3_Mobile_Bluetooth.md)
- [**IoT Reconnaissance (Shodan)**](CH08-Mobile-and-IoT/Lab4_IoT_Recon.md) — with [Shodan search strings](CH08-Mobile-and-IoT/Shodan_IoT_Search_Strings.md)

### Chapter 11 — Cryptography 101

- [RSA public/private key encryption demo (OpenSSL)](CH11-Cryptography/privpubkeyencrypt.sh)

### Instructor solutions

Model answers and marking guides are kept in a local, git-ignored `labsolutions/`
folder that mirrors this chapter structure. They are not published in this repository.

## Usage

Students should follow the assignment instructions provided in each lab folder. Ensure you have proper authorization before scanning or testing any systems.

## Author

**Milan Dima**  
📧 milan.dima@vives.be

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

[![CC BY 4.0](https://i.creativecommons.org/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit to Milan Dima (milan.dima@vives.be), provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

## Disclaimer

⚠️ **Important:** The tools and techniques covered in this course are for educational purposes only. Always obtain explicit written permission before performing security testing on any systems. Unauthorized access to computer systems is illegal and unethical.

---

**VIVES University of Applied Sciences**
