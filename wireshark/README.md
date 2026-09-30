# Wireshark — Chapter 1 Lab

Packet capture and protocol analysis lab for **Cybersecurity Architecture (ACS), Chapter 1**.

Students capture live traffic and dissect three exchanges — an **ICMP ping**, a
**DNS lookup** and an **HTTP conversation** — then use the HTTP capture to
demonstrate that cleartext protocols break confidentiality.

## Contents

| File | Audience | Purpose |
|------|----------|---------|
| `Lab1_Wireshark_Traffic_Analysis.md` / `.pdf` | Students | The lab. 90 minutes, tasks, report template, rubric |
| `Lab1_Instructor_Solution.md` / `.pdf` | **Instructor only** | Model answers, timing plan, marking guide, common failure modes |
| `chapter1_reference.pcap` | Students | Fallback capture — works with every filter in the lab |
| `make_reference_capture.py` | Instructor | Regenerates the reference capture |
| `dist/Chapter1_Wireshark_Lab_Toledo.zip` | — | Ready-to-upload student bundle (excludes the solution) |

> ⚠️ **Do not publish `Lab1_Instructor_Solution.*` to Toledo.** The Toledo ZIP in
> `dist/` deliberately excludes it.

## The reference capture

`chapter1_reference.pcap` is **synthetic** — assembled frame by frame by
`make_reference_capture.py`, not sniffed from a real network. That is deliberate:
shipping a real capture in a public course repo would mean shipping somebody's real
traffic.

All checksums, sequence numbers, ACK arithmetic and inter-packet timings are valid,
so Wireshark dissects, reassembles and *Follow Stream*s it exactly like a live
capture. 32 frames, 5.67 s:

- ARP who-has / is-at
- DNS `A? neverssl.com` → `34.223.124.45`
- 4× ICMP echo request/reply
- HTTP `GET /` → `200 OK`
- HTTP `POST /login.php` → `302 Found`, carrying `username=student&password=Vives2026!` in cleartext

To regenerate (e.g. to change the credentials or the topology):

```bash
python3 make_reference_capture.py chapter1_reference.pcap
```

Verify it after any change:

```bash
tshark -r chapter1_reference.pcap \
  -o ip.check_checksum:TRUE -o tcp.check_checksum:TRUE \
  -o udp.check_checksum:TRUE \
  -Y 'ip.checksum.status=="Bad" || tcp.checksum.status=="Bad" || udp.checksum.status=="Bad" || icmp.checksum.status=="Bad"'
# no output = all checksums valid
```

## Rebuilding the PDFs and the Toledo ZIP

Requires `pandoc` and `weasyprint`:

```bash
./build.sh
```

---

**Author:** Milan Dima — milan.dima@vives.be · **Licence:** CC BY 4.0
