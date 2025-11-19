# Lab 2: Web Application Testing with Burp Suite (Community)

## Duration: \~1 hour

## Tools: Kali Linux, Firefox or Chrome, Burp Suite Community Edition

## Objective:

Use **Burp Suite** for **intercepting HTTP requests** and performing
basic web application security testing.

------------------------------------------------------------------------

## 1. Setup

  Component     Details
  ------------- --------------------
  Web Browser   Firefox preferred
  Burp Suite    Launch from Kali
  Target        DVWA or Juice Shop

**Launch Burp:**

``` bash
burpsuite
```

------------------------------------------------------------------------

## 2. Configure Intercept Proxy

### A. Browser Proxy Setup

Go to:

    Settings → Network Settings → Manual Proxy:
    HTTP Proxy: 127.0.0.1
    Port: 8080

### B. Import Burp Certificate

Visit: `http://burp/cert`

------------------------------------------------------------------------

## 3. Lab Steps

### A. Enable Interception

**Proxy → Intercept ON**

Visit `http://<target-IP>/dvwa` in browser.

### B. Modify a Request

-   Intercept POST login request\
-   Modify username parameter\
-   Forward request

### C. Analyze Cookies & Headers

In Burp: \> HTTP history → Headers

------------------------------------------------------------------------

## 4. Deliverables

1.  Screenshot showing HTTP request modification\
2.  Explanation of Same-Origin Policy\
3.  Identify **one security weakness**

------------------------------------------------------------------------

## 5. Discussion Questions

1.  Why is HTTPS interception harder than HTTP?\
2.  What ethical concerns exist when using Burp Suite?\
3.  How can developers defend against manipulated requests?
