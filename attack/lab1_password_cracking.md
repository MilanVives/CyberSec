# Lab 1 — Password Cracking (John the Ripper)

**Objective:** Crack sample password hashes using John the Ripper and wordlists.  
**Prerequisites:** Kali Linux VM with `john` installed (or install with `apt install john`).

## Files provided
- `shadow_sample.txt` — sample `/etc/shadow`-style file containing 3 user hashes.
- `rockyou_small.txt` — small wordlist (contains the real passwords among decoys).
- `john_usage.txt` — quick usage notes.

## Tasks
1. Inspect the shadow file:
```bash
cat shadow_sample.txt
```

2. Identify the hash format (look for `$6$` which indicates SHA-512 crypt).

3. Run John the Ripper using the provided wordlist:
```bash
john --wordlist=rockyou_small.txt --format=sha512crypt shadow_sample.txt
```

4. Show cracked passwords:
```bash
john --show --format=sha512crypt shadow_sample.txt
```

5. (Optional) Try incremental or hybrid attacks:
```bash
john --incremental --format=sha512crypt shadow_sample.txt
```

## Instructor notes
- The sample passwords included in `rockyou_small.txt` are: password123, s3cur3!, letmein
- Discuss salt usage and why SHA-512crypt includes a salt value.
- Explain why using a strong wordlist and rules improves success rates.

## Hints for students
- Use `john --list=formats` to see supported formats.
- If John doesn't detect format automatically, specify `--format=sha512crypt`.
