# Lab 1: Web Vulnerability Assessment using Nikto

## Duration: \~1 hour

## Tools: Kali Linux (Nikto pre-installed), DVWA or OWASP Juice Shop

## Objective:

Introduce students to **Nikto**, a web vulnerability scanner, and
understand how to enumerate and assess web server vulnerabilities.

------------------------------------------------------------------------

## 1. Setup

  Component    Details
  ------------ --------------------------------------------------------
  Kali Linux   Attacker machine
  Target       DVWA (Damn Vulnerable Web App) or OWASP Juice Shop
  Network      Both must be on the same network (or local VM network)

**Start DVWA**:

``` bash
cd /var/www/html/dvwa
service apache2 start
mysql -u root -p
```

Access DVWA at:\
`http://<target-IP>/dvwa`

------------------------------------------------------------------------

## 2. Lab Steps

### A. Verify Nikto installation

``` bash
nikto -Help
```

### B. Scan Target Website

``` bash
nikto -h http://<target-IP>/dvwa
```

### C. Save scan results

``` bash
nikto -h http://<target-IP>/dvwa -o nikto_report.html -Format html
```

### D. Analyze Results

Students should identify: - Potential vulnerabilities\
- Missing security headers\
- Files/directories exposed

------------------------------------------------------------------------

## 3. Deliverables

Students must submit: 1. A short report summarizing findings.\
2. At least **three actionable security recommendations**.

------------------------------------------------------------------------

## 4. Discussion Questions

1.  What vulnerabilities are considered "false positives"?\
2.  What are the limitations of Nikto?\
3.  How is Nikto different from Nessus or Burp Suite?
