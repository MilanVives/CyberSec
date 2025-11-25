
# Lab 2: Packet Analysis Using Wireshark (No Hardware Required)

## Objective
Understand WEP wireless packet structures, IVs, and vulnerabilities using a pre-captured `.pcap` file.

## Tools Needed
- Wireshark (installed on student laptops)
- Provided file: `weplab.pcap`

## Instructions

### 1. Open the PCAP File
1. Launch Wireshark.
2. Open the file: **weplab.pcap**
3. Apply this display filter to show only wireless frames:
```
wlan
```

### 2. Identify WEP Traffic
Use the following filter to find encrypted traffic:
```
wlan.fc.protected == 1
```

### 3. Inspect IVs (Initialization Vectors)
Look for fields such as:
- **IV length**
- **SA (Source Address)**
- **DA (Destination Address)**

### 4. Questions to Answer
| Question | Student Answer |
|----------|----------------|
| What encryption type is used? | |
| What is the IV field and why is it important? | |
| How many packets are captured? | |
| Why is WEP vulnerable? | |

### 5. Report Submission
Students must submit a brief report summarizing the vulnerabilities observed and how WEP is compromised.
