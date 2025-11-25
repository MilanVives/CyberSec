
# Lab 3: Virtual WEP Crack Using Aircrack-ng (No Hardware Required)

## Objective
Simulate a WEP key recovery attack using a pre-captured `.ivs` file. No real network or hardware needed.

## Tools Needed
- Kali Linux (VM or native)
- Aircrack-ng installed
- Provided file: `weplab.ivs`

## Instructions

### 1. Open Terminal
Run the following command in the folder with `weplab.ivs`:

```
aircrack-ng weplab.ivs
```

### 2. Observe Output
Aircrack-ng will attempt to recover the key. Students should **not expect a real key** — this is a demo file.

### 3. Questions to Answer
| Question | Student Answer |
|----------|----------------|
| How many IVs were captured? | |
| Did Aircrack-ng recover a key? Why or why not? | |
| What type of attack is used internally? | |
| Why is statistical analysis key to cracking WEP? | |

### 4. Mitigation Discussion
Students must list **at least three** defenses against WEP attacks (e.g., WPA2, 802.1X, IDS monitoring).

### 5. Bonus (Optional)
Research:
- What is the FMS attack?
- What statistical method does Aircrack-ng use?
