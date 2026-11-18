# Lab — Cracking Wireless Encryption (WEP & WPA2), No Hardware Needed

**Book:** CEH All-in-One, Chapter 7 — *Wireless Network Hacking*
**Level:** 🟢→🔴 tiered · **Duration:** ~90 min · **Hardware:** none (uses pre‑recorded captures)

Real Wi‑Fi attacks need a wireless adapter that supports *monitor mode* and
*packet injection*, which not everyone has. This lab avoids that completely: you
work from **capture files that are already in this folder**, so every student can
finish it on Windows, macOS, or Linux.

The lab has three tiers. Do as many as your time and level allow:

| Tier | You will… | Tool |
|---|---|---|
| 🟢 **A — Analyse** | Open WEP traffic in Wireshark and see *why* WEP is broken | Wireshark |
| 🟡 **B — Crack WEP** | Recover a WEP key from captured IVs | Aircrack‑ng |
| 🔴 **C — Crack WPA2** | Recover a WPA2 passphrase from a 4‑way handshake | Aircrack‑ng |

> **Optional Appendix** (needs a real adapter) shows how these captures are made in
> the first place. Skip it if you don't have the hardware.

---

## Files in this folder

| File | What it is | Key / secret |
|---|---|---|
| `weplab.pcap` | WEP‑encrypted Wi‑Fi traffic (good for the PTW method) | WEP key `1F:1F:1F:1F:1F` |
| `weplab.ivs` | Collected WEP initialisation vectors only | WEP key `12:34:56:78:9A:BC:DE:F1:23:45:67:89:AB` |
| `wpa-handshake.cap` | A WPA2 4‑way handshake (ESSID `test`) | passphrase is in `wordlist.txt` |
| `wordlist.txt` | A dictionary of candidate passwords | — |

*(These are standard teaching captures from the Aircrack‑ng project. No real
network was attacked to make this lab.)*

---

## Getting the tools

**Wireshark** (Tier A): install from <https://www.wireshark.org/download.html>
(Windows/macOS/Linux).

**Aircrack‑ng** (Tiers B & C) — pick whichever is easiest for you:

- **Kali Linux:** already installed.
- **Any OS with Docker:** build a tiny one‑off image with Aircrack‑ng (takes ~1 min
  the first time, then it's cached). Run this once:

  ```bash
  printf 'FROM debian:bookworm-slim\nRUN apt-get update && apt-get install -y aircrack-ng\n' | docker build -t aircrack -
  ```

  Then, from *inside this folder* (`CH07-Wireless-Hacking`), run Aircrack‑ng against
  the mounted files. On macOS/Linux you can define a short helper:

  ```bash
  air() { docker run --rm -i -v "${PWD}:/data" --entrypoint aircrack-ng aircrack "$@"; }
  air /data/weplab.pcap          # example
  ```

  Without the helper (works everywhere, incl. Windows PowerShell):

  ```bash
  docker run --rm -v "${PWD}:/data" --entrypoint aircrack-ng aircrack /data/weplab.pcap
  ```

- **Windows without Docker:** install the Aircrack‑ng Windows build from
  <https://www.aircrack-ng.org/> and run the commands in a terminal, using the
  file names directly (drop the `/data/` prefix).

> The command examples below use a plain `aircrack-ng …`. If you use Docker,
> prefix the file with `/data/` (e.g. `aircrack-ng /data/weplab.ivs`).

---

## 🟢 Tier A — See why WEP is broken (Wireshark)

1. Open **Wireshark** and load **`weplab.pcap`**.
2. In the display‑filter bar, try each filter and press Enter:
   - `wlan` — all 802.11 frames
   - `wlan.fc.protected == 1` — only encrypted frames
3. Click one data frame and expand **IEEE 802.11 → WEP parameters**. Find the
   **Initialization Vector (IV)** — 3 bytes sent *in clear text* with every packet.
4. Now sort/scan the IVs across packets. WEP's fatal flaw: the IV is only 24 bits
   and is reused, so with enough packets the key leaks. That's what Tier B exploits.

**Answer these (Tier A deliverable):**

| Question | |
|---|---|
| What encryption type does the capture use? | |
| Roughly how many frames are in the capture? (*Statistics → Capture File Properties*) | |
| What is an IV and why is sending it in clear text a problem? | |
| In one sentence, how do WPA2/WPA3 avoid this weakness? | |

---

## 🟡 Tier B — Crack the WEP key (Aircrack‑ng)

WEP keys fall in seconds once you have enough IVs.

**B1 — From the IV file:**

```bash
aircrack-ng weplab.ivs
```

If more than one network is listed, type the number of the target and press Enter.
Expected result:

```
KEY FOUND! [ 12:34:56:78:9A:BC:DE:F1:23:45:67:89:AB ]
```

**B2 — From the full capture using the PTW method:**

```bash
aircrack-ng weplab.pcap
```

Expected result:

```
KEY FOUND! [ 1F:1F:1F:1F:1F ]
```

**Answer these (Tier B deliverable):**

| Question | |
|---|---|
| How long did the crack take, and how many IVs were used? | |
| What is the PTW method, in one line? | |
| Why does collecting *more* IVs make the attack easier? | |
| What single design change makes WPA2 immune to this exact attack? | |

---

## 🔴 Tier C — Crack a WPA2 passphrase (Aircrack‑ng)

WPA2 is **not** broken like WEP. There is no statistical shortcut — the only offline
attack is to **guess the passphrase** and test each guess against a captured
4‑way handshake. So a strong, non‑dictionary passphrase defeats this.

```bash
aircrack-ng -w wordlist.txt -e test wpa-handshake.cap
```

- `-w wordlist.txt` — the dictionary of guesses.
- `-e test` — the network name (ESSID) to target.

Expected result:

```
KEY FOUND! [ biscotte ]
```

**Answer these (Tier C deliverable):**

| Question | |
|---|---|
| Why does WPA2 cracking *need* a wordlist while WEP does not? | |
| What had to be captured for this attack to be possible at all? | |
| Your wordlist found the key — what property of the passphrase made that possible? | |
| Name two things a user/admin can do to make this attack fail. | |

---

## Deliverable

Submit a short report with:

1. The completed question table(s) for each tier you attempted.
2. A screenshot of **one** `KEY FOUND!` result (Tier B or C).
3. 3–4 sentences: *Rank WEP, WPA2‑with‑a‑weak‑password, and WPA2‑with‑a‑strong‑password
   from easiest to hardest to break, and explain why.*

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `aircrack-ng: command not found` | Use the Docker option above, or install Aircrack‑ng. |
| Docker: "permission denied" on the file | Make sure you run the command **inside** `CH07-Wireless-Hacking` so `${PWD}` points here. |
| `No networks found` / `Packets contained no EAPOL data` | For Tier C you must pass `wpa-handshake.cap` (the handshake), not a WEP file. |
| It asks "Index number of target network?" | Type the number next to the target and press Enter. |
| WEP crack says "Failed. Next try with N IVs" repeatedly | You pointed it at the wrong file — use `weplab.ivs` or `weplab.pcap` from this folder. |

---

## Appendix (optional — requires a monitor‑mode Wi‑Fi adapter)

This is **how the capture files above were produced**. Do it only with your own
access point and an adapter that supports monitor mode + injection (e.g. many
Atheros/Ralink USB dongles). On most laptops the built‑in card will not work.

```bash
# 1. Put the adapter into monitor mode
sudo airmon-ng start wlan0

# 2. Find your target AP (note its BSSID and channel)
sudo airodump-ng wlan0mon

# 3. Capture traffic from that AP into files
sudo airodump-ng --bssid <AP-BSSID> -c <channel> -w mycapture wlan0mon

# 4a. (WEP) let IVs accumulate, then crack:
aircrack-ng mycapture-01.cap

# 4b. (WPA2) force a client to reconnect so you capture the 4-way handshake,
#     then crack with a wordlist:
sudo aireplay-ng --deauth 5 -a <AP-BSSID> wlan0mon
aircrack-ng -w wordlist.txt mycapture-01.cap
```

A good guided walk‑through for capturing a WPA handshake:
<https://labex.io/labs/kali-capture-a-wpa-handshake-manually-with-airodump-ng-594455>

> ⚖️ **Only ever do this against a network you own or are explicitly authorised to
> test.** Capturing or deauthenticating other people's Wi‑Fi is illegal in most
> countries, including under Belgian/EU law.

---

## Instructor notes (not for distribution)

- `weplab.pcap` = Aircrack‑ng's `wep_64_ptw.cap`; key `1F:1F:1F:1F:1F`, BSSID `00:12:bf:12:32:29`.
- `weplab.ivs` was generated with `create_ivsfile.sh` (key `12:34:56:78:9A:BC:DE:F1:23:45:67:89:AB`).
- `wpa-handshake.cap` = Aircrack‑ng's `wpa.cap`; ESSID `test`, passphrase `biscotte`.
- All keys verified with `aircrack-ng` before publishing.
