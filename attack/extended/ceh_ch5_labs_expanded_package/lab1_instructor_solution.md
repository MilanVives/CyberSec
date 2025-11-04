# Lab 1 — Password Cracking: Instructor Solutions & Variations

## Provided files (original)
- `shadow_sample.txt` — 3 SHA-512 crypt hashes (students)
- `rockyou_small.txt` — small wordlist (contains the real passwords: password123, s3cur3!, letmein).

## Instructor solution (step-by-step)
1. Identify hash format:
```bash
cat shadow_sample.txt
# Example line: alice:$6$...$encrypted...:18000:0:...
# $6$ indicates sha512-crypt
```

2. Run John with provided wordlist:
```bash
john --wordlist=rockyou_small.txt --format=sha512crypt shadow_sample.txt
```
**Expected outcome:** John will try entries from the wordlist and should find passwords for the three users because the real passwords are in the list.

3. Show cracked credentials:
```bash
john --show --format=sha512crypt shadow_sample.txt
```
**Expected output** (example; actual salts/hashes differ):
```
alice:password123:...
bob:s3cur3!:...
charlie:letmein:...
3 password hashes cracked, 0 left
```

4. Discussion points (instructor):
- Explain the difference between hash, salt, and salted hash. SHA-512crypt includes the salt value after $6$ in the hash string.
- Talk about rule-based attacks (`--rules`) vs pure wordlists vs incremental brute force.
- Show how to use `john --wordlist=rockyou_small.txt --rules --format=sha512crypt shadow_sample.txt` to try common mutations (e.g., add digits, change case).

## Variations (increasing difficulty)
1. **Larger wordlist + rules** — give students `rockyou_full.txt` (a bigger list) and require use of `--rules` to increase chances.
2. **Different hash algorithms** — provide `shadow_sha256.txt` and `shadow_md5.txt` to teach format differences and tool selection (`--format=sha256crypt` vs `--format=md5crypt`).
3. **Salted vs unsalted** — explain why unsalted hashes (e.g., old NTLM or simple MD5 without salt) are more vulnerable to rainbow tables.
4. **Use of Hashcat (GPU)** — show commands for hashcat when available (demo only):
```bash
# Convert john format to hashcat if needed, then run (example)
hashcat -m 1800 hashes.txt rockyou.txt
```
5. **Hybrid attacks** — combine masks with wordlists to crack passwords with patterns (e.g., `Password` + `123`).

## Additional instructor artifacts included
- `shadow_sha512.txt` — variant SHA-512 shadow file (different salts).
- `shadow_sha256.txt` — SHA-256 example.
- `shadow_md5.txt` — MD5 example.

---
Instructor tip: For grading, provide a unique salt set per student (or VM) and require them to submit the cracked credentials and commands used.
