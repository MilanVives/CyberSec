
# Lab 3: Virtual WEP Crack Using Aircrack-ng (test.ivs / weplab.ivs)

## Objective
Perform a simulated WEP key recovery using a pre-captured `.ivs` file. No hardware or network required.

## Files Required
- **weplab.ivs** (originally `test.ivs` from Aircrack-ng sample files)

## Tools Needed
- Kali Linux or any system with **Aircrack-ng** installed

---

## Instructions

### 1. Cracking the Key
Run:
```
aircrack-ng weplab.ivs
```

Expected Output:
```
KEY FOUND! [ AE:5B:7F:3A:03:D0:AF:9B:F6:8D:A5:E2:C7 ]
```

### 2. Questions for Students
| Question | Student Answer |
|----------|----------------|
| How many IVs were captured? | |
| What statistical method does Aircrack-ng use? | |
| Why is WEP vulnerable? | |
| What security protocol replaces WEP? | |
| Why does WPA/WPA2 use TKIP/CCMP instead of IV-based RC4? | |

---

## Instructor Notes (Do NOT distribute)
File originally named `test.ivs` from Aircrack-ng site.  
Renamed to **weplab.ivs** for consistency with the lab instructions.
