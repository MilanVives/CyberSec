
# Lab 2: Wireshark Analysis of WEP Traffic (Using ptw.cap / weplab.pcap)

## Objective
Analyze WEP-encrypted network traffic, identify IV fields, and understand weaknesses in WEP’s protocol design — without using any real hardware.

## Files Required
- **weplab.pcap** (originally `ptw.cap` from Aircrack-ng samples)

## Tools Needed
- Wireshark

---

## Instructions

### 1. Open the Capture
1. Launch Wireshark.
2. Open **weplab.pcap**.

### 2. Apply Wireless Filters
Try each of the following:
```
wlan
wlan.fc.protected == 1
```

### 3. Inspect Packet Details
Look for:
- **Source Address (SA)**
- **Destination Address (DA)**
- **WEP Initialization Vector (IV)**
- **Authentication Frames**

### 4. Questions for Students
| Question | Student Answer |
|----------|----------------|
| What encryption type is used? | |
| How many packets are in the capture? | |
| Why is the IV important in WEP? | |
| What is the vulnerability in WEP? | |
| How does WPA/WPA2 improve security? | |

---

## Instructor Notes (Do NOT distribute)
This file originally came from `ptw.cap` on Aircrack-ng’s sample page.  
It was renamed to **weplab.pcap**.  
It is safe to distribute to students. No real wireless attack was performed.
