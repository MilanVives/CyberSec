
# Lab 4: ChopChop Attack Analysis Using Wireshark (chopchop.cap)

## Objective
Understand the **ChopChop attack**, which targets **WEP encryption** to partially decrypt data packets — without cracking the entire key.

---

## Files Required
- **chopchop.cap** (from Aircrack-ng sample files)

## Tools Needed
- Wireshark

---

## Intro: What is the ChopChop Attack?
The ChopChop attack does **not fully crack the WEP key**.  
Instead, it **tries to decrypt a packet byte-by-byte** without knowing the full key.

This helps students understand:
- Weakness in **RC4 stream cipher**
- Why **WEP replay attacks** work
- Importance of **message integrity checks (ICVs)**

---

## Instructions

### 1. Open the File
Open **chopchop.cap** in Wireshark.

### 2. Apply Filters
```
wlan
wlan.fc.protected == 1
```

### 3. Look for ARP or Data Packets
Find packets marked **"Data"** and examine:
| Field | Notes |
|-------|------|
| IV | Look for patterns |
| ICV | Integrity check value |
| Retry flag | Shows retransmissions |

### 4. Questions for Students
| Question | Student Answer |
|----------|----------------|
| What is the ChopChop attack? | |
| Does it fully crack WEP? Why or why not? | |
| Why is IV reuse dangerous? | |
| What is an ICV and why does it matter? | |
| What makes WPA/WPA2 immune to ChopChop? | |

---

## BONUS (Optional)
Research:
- What is the **PTW method**?
- How does **packet injection** make ChopChop more effective?
- Why was **RC4 deprecated**?

---

## Instructor Notes (Do NOT distribute)
This file should be downloaded from Aircrack-ng’s sample repository.  
No real attack was performed. This is a safe demo capture for education.
