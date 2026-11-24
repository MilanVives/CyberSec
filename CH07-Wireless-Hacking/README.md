# Chapter 7 — Wireless Network Hacking

Hands-on wireless security without needing a Wi-Fi adapter. All exercises run from
capture files included here, so they work on **Windows, macOS, or Linux** (Kali or
Docker).

## Lab

- [**Cracking Wireless Encryption (WEP & WPA2)**](WEP_WPA_Cracking_Lab.md) — one
  tiered lab:
  - 🟢 **Tier A** — analyse WEP traffic in Wireshark and see why it's broken
  - 🟡 **Tier B** — recover a WEP key with Aircrack-ng
  - 🔴 **Tier C** — crack a WPA2 passphrase from a captured handshake
  - *Appendix* — how the captures are made (optional, needs a monitor-mode adapter)
- [**Lab 2 — Mapping Wi-Fi From the Air**](Lab2_Campus_WiFi_Mapping.md) — 60 min,
  phones only: passive survey of the campus Wi-Fi (3 SSIDs, many APs) and a walk around
  campus scoring the poorest encryption. Printable worksheet:
  [`Lab2_Campus_WiFi_Mapping.pdf`](Lab2_Campus_WiFi_Mapping.pdf) (rebuild with
  `./build_lab2.sh`; teacher notes in the git-ignored `labsolutions/` tree)

## Data files

| File | Purpose | Secret |
|---|---|---|
| `weplab.pcap` | WEP traffic (PTW method) | key `1F:1F:1F:1F:1F` |
| `weplab.ivs` | Collected WEP IVs | key `12:34:56:78:9A:BC:DE:F1:23:45:67:89:AB` |
| `wpa-handshake.cap` | WPA2 4-way handshake (ESSID `test`) | passphrase in `wordlist.txt` (`biscotte`) |
| `wordlist.txt` | Dictionary for the WPA2 crack | — |
| `create_ivsfile.sh` | Instructor utility that regenerates `weplab.ivs` | — |

The captures are standard teaching samples from the
[Aircrack-ng project](https://github.com/aircrack-ng/aircrack-ng/tree/master/test).
No real network was attacked to create this lab. All keys were verified with
`aircrack-ng` before publishing.
