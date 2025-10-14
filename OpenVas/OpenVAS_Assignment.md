# OpenVAS 1-Hour Lab — Install on Kali Linux & Scan Assigned Domains

**Duration:** 1 hour lab

## Learning Objectives

- Install and configure GVM/OpenVAS on Kali Linux.
- Run an authenticated (manager) vulnerability scan from the command line.
- Export and interpret scan results (PDF/TXT).
- Produce a short findings summary with remediation suggestions.

> ⚠️ **IMPORTANT — Permission:** Only scan hosts you are explicitly allowed to scan. Do **not** scan public or third-party systems without written permission. The instructor has approved scanning the following domains for this lab:  
> `linux.vives.live`, `vault.vives.live`, `supervisor.vives.live`, `abinet.vives.be`.

---

## Prerequisites (Before Lab)

- Kali Linux (latest) with network access.
- `sudo` privileges.
- 1 hour of uninterrupted time.
- Instructor confirmation that the listed domains are permitted for scanning.

---

## Lab Tasks & Timeline (60 Minutes)

### **0–10 min — Install & Initialize GVM/OpenVAS**

See the CLI or GUI installation guide for detailed installation steps.

---

### **10–15 min — Start Services & Verify**

Ensure all GVM services are running and verify the setup is correct.

---

### **15–35 min — Create Targets & Run Scans**

Create one target per domain and run a single task per target. Scan the following domains:
- `linux.vives.live`
- `vault.vives.live`
- `supervisor.vives.live`
- `abinet.vives.be`

---

### **35–50 min — Export Reports**

Once a task completes, export reports as PDF or TXT for analysis.

---

### **50–60 min — Write Findings & Submit**

Prepare a **1-page findings summary per scanned host** containing:

- Host/domain scanned
- Date & time of scan (UTC)
- Top 5 findings (severity + short description)
- One recommended remediation for each of the top 3 findings
- Screenshots or exported report snippets (attach `report.txt` or `report.xml`)

---

## Deliverables (Submit to Instructor)

1. A single ZIP containing:
   - `report_<domain>.txt` or `report_<domain>.pdf` for each scanned domain.
   - `findings_<domain>.md` (1 page) summarizing the results and remediation suggestions.
   - A short `lab_notes.txt` with the commands you ran and any errors encountered.
2. Optional: screenshots showing a successful `gvm-check-setup` and the scan completion status.

---

## Grading Rubric

| Criteria | Weight | Description |
|-----------|---------|-------------|
| Installation & Setup | 30% | Services running and feeds synced |
| Successful Scans & Reports | 40% | Each required host scanned and reports included |
| Findings Quality | 20% | Clear top-5 findings + sensible remediation |
| Documentation & Submission | 10% | ZIP contains all required files |

---

## Safety / Legal Reminder

By submitting these scans you confirm you have **explicit permission** to scan the listed domains for this lab. Unauthorized scanning may be illegal and unethical.

---

**Good luck — finish in 60 minutes and upload the ZIP to the course submission portal.**
