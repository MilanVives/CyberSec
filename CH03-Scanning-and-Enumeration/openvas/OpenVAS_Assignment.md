# OpenVAS Lab — Vulnerability Scanning of Assigned Hosts

**Book:** CEH All-in-One, Chapter 3 — *Scanning and Enumeration* (vulnerability scanning)
**Duration:** pre-lab installation at home (~1–2 h, mostly unattended) + 60 min in class

> 🐳 **New to vulnerability scanning?** Start with the
> [OpenVAS Quick Lab with Docker](OpenVAS_Docker_Quick_Lab.md): one container,
> no Kali install, and you scan a local test target.

## Learning Objectives

- Install and configure GVM/OpenVAS on Kali Linux.
- Run vulnerability scans from the web interface **or** the command line.
- Export and interpret scan results (severity, CVSS, Quality of Detection).
- Produce a short findings summary with remediation suggestions.

> ⚠️ **IMPORTANT — Permission:** Only scan hosts you are explicitly allowed to scan.
> Do **not** scan public or third-party systems without written permission. The
> instructor has approved scanning the following hosts for this lab:
> `linux.vives.live`, `vault.vives.live`, `supervisor.vives.live`, `abinet.vives.be`.

---

## Part A — Pre-lab (at home, before class)

Installing GVM and loading the vulnerability feed takes **30–90 minutes**. It
cannot be done during the lab.

1. Give your Kali VM at least **4 GB RAM** (8 GB recommended) and **20 GB** free disk.
2. Follow [OpenVAS_Installation_and_Troubleshooting.md](OpenVAS_Installation_and_Troubleshooting.md), §1 to §7.
3. You are ready when **all three** are true:
   - `sudo gvm-check-setup` ends with *…installation is OK*
   - **Administration → Feed Status** shows **Current** on every row
   - **Configuration → Scan Configs** lists **Full and fast**
4. Take a screenshot of the `gvm-check-setup` result and of the Feed Status page.

If you get stuck, bring the exact error message (and the output of
`sudo gvm-check-setup`) to class.

---

## Part B — In class (60 minutes)

### 0–5 min — Start and verify

```bash
sudo gvm-start
sudo gvm-check-setup
```

### 5–15 min — Create targets and start all scans

Create **one target and one task per host** and start them **all at once** — a
*Full and fast* scan takes 15–45 minutes per host, and they run in parallel.

Use either:
- the web interface — [OpenVAS_GUI_Usage.md](OpenVAS_GUI_Usage.md), §3–4, or
- the command line — [OpenVAS_CLI_Usage.md](OpenVAS_CLI_Usage.md), §1–4 and §7.

Remember **Alive Test = Consider Alive**, or hosts that block ping are skipped.

### 15–45 min — Analyse while scanning

While the scans run, open the first results as they appear. For each finding you
pick, look up: the CVE(s), the CVSS score, the QoD, and the proposed solution.
Discuss: which findings are likely **false positives**, and why?

### 45–55 min — Export reports

When a task shows *Done*, export its report as **TXT or PDF** (and CSV if you want
a spreadsheet).

### 55–60 min — Findings & submission

Finish the findings summary and upload your ZIP.

---

## Deliverables

One ZIP, `lastname_firstname_openvas.zip`, containing:

1. **Pre-lab:** screenshots of `gvm-check-setup` (OK) and Feed Status (Current).
2. **Per host:** `report_<host>.txt` or `report_<host>.pdf`.
3. **Per host:** `findings_<host>.md` (max. 1 page):
   - host scanned and date/time of the scan (UTC)
   - top 5 findings: severity, CVSS, QoD, one-line description
   - one concrete remediation for each of the top 3 findings
   - one finding you consider a possible false positive, and why
4. `lab_notes.txt` — the commands you ran and any errors you hit (and how you fixed them).

---

## Grading Rubric

| Criteria | Weight | Description |
|-----------|---------|-------------|
| Installation & Setup | 25% | Pre-lab screenshots: setup OK, feeds current |
| Successful Scans & Reports | 35% | Every assigned host scanned, reports included |
| Findings Quality | 30% | Correct top-5, sensible remediation, false-positive reasoning |
| Documentation & Submission | 10% | `lab_notes.txt` complete, ZIP correctly named |

---

## Safety / Legal Reminder

By submitting these scans you confirm you scanned **only** the hosts listed above.
Unauthorized scanning can be a criminal offence (in Belgium: Art. 550bis Sw.).
