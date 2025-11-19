# Lab 2: Web Application Testing with Burp Suite (Community)

## Duration: ~2 hours

## Tools: Kali Linux, Firefox ESR, Burp Suite Community Edition, DVWA

## Objective:

Use **Burp Suite** to intercept and manipulate HTTP requests, analyze web traffic, and identify security vulnerabilities in web applications based on CEH v12 methodology.

------------------------------------------------------------------------

## Prerequisites

- Kali Linux VM (2023.x or later)
- DVWA installed and running (or use OWASP Juice Shop as alternative)
- Basic understanding of HTTP protocol
- Administrative privileges on Kali

------------------------------------------------------------------------

## 1. Environment Setup

### A. Install and Start DVWA

**Method 1: Using Kali Package (Recommended - Easiest)**

If you're on Kali Linux, DVWA can be installed directly from the repository:

```bash
# Update package list
sudo apt update

# Install DVWA
sudo apt install -y dvwa

# Start DVWA
sudo dvwa-start
```

Verify DVWA is running:
```bash
curl -I http://localhost/dvwa
```

**To stop DVWA later:**
```bash
sudo dvwa-stop
```

**Method 2: Using Docker (Alternative)**

If DVWA package is not available or you prefer Docker:

```bash
# Install Docker if not present
sudo apt update
sudo apt install -y docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Pull and run DVWA
sudo docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Alternative: If you prefer a persistent setup
sudo docker run -d -p 80:80 --name dvwa vulnerables/web-dvwa
```

Verify DVWA is running:
```bash
curl -I http://localhost
```

**Initial DVWA Setup (Both Methods):**
1. Open Firefox and navigate to `http://localhost/dvwa` (or just `http://localhost` for Docker)
2. Click "Create / Reset Database" button
3. Login with credentials: `admin` / `password`
4. Click "DVWA Security" in left menu and set to **Low**

### B. Launch Burp Suite

```bash
# Launch Burp Suite Community Edition
burpsuite &
```

**Burp Suite Initial Configuration:**
1. Choose "Temporary project" → Next
2. Use "Burp defaults" → Start Burp
3. Wait for Burp to fully load (may take 30-60 seconds)

------------------------------------------------------------------------

## 2. Configure Browser Proxy

### A. Firefox Proxy Configuration

**Method 1: Manual Proxy Settings (Recommended for Lab)**

1. Open Firefox ESR (included in Kali)
2. Click menu (☰) → **Settings** → **General**
3. Scroll down to **Network Settings** → Click **Settings** button
4. Select **Manual proxy configuration**
5. Enter the following:
   - **HTTP Proxy:** `127.0.0.1` **Port:** `8080`
   - **Also use this proxy for HTTPS** (check this box)
   - **No Proxy for:** (leave blank or remove localhost entries)
6. Click **OK**

**Method 2: Using FoxyProxy Extension (Alternative)**

```bash
# This extension makes switching proxies easier
# Install from Firefox Add-ons if desired
```

### B. Install Burp CA Certificate

To intercept HTTPS traffic, you must trust Burp's certificate:

1. **With Firefox proxy configured and Burp running**, navigate to:
   ```
   http://burpsuite
   ```
   Or: `http://127.0.0.1:8080`

2. Click **"CA Certificate"** in top-right corner to download `cacert.der`

3. In Firefox:
   - Menu → **Settings** → **Privacy & Security**
   - Scroll to **Certificates** → Click **View Certificates**
   - Go to **Authorities** tab
   - Click **Import**
   - Select the downloaded `cacert.der` file
   - Check **"Trust this CA to identify websites"**
   - Click **OK**

4. Verify installation:
   ```bash
   # Check certificate was saved
   ls -lh ~/Downloads/cacert.der
   ```

------------------------------------------------------------------------

## 3. Burp Suite Proxy Configuration

### A. Verify Proxy Listener

1. In Burp Suite, go to: **Proxy** → **Proxy settings**
2. Under **Proxy Listeners**, verify an entry exists:
   - **Interface:** `127.0.0.1:8080`
   - **Running:** ✓ (should be checked)
3. If not present, click **Add**:
   - Bind to port: `8080`
   - Bind to address: `127.0.0.1` (loopback only)
   - Click **OK**

### B. Configure Intercept Settings

1. Go to **Proxy** → **Intercept**
2. Ensure "Intercept is on" button shows **ON** (orange)
3. Click **Proxy settings** → **Intercept Client Requests**
4. Verify rules include: `And URL Is in target scope`

------------------------------------------------------------------------

## 4. Lab Exercises

### Exercise 1: Intercept and Analyze HTTP Traffic

**Step 1: Set Target Scope**
1. In Burp, go to **Target** → **Site map**
2. Right-click on `http://localhost` → **Add to scope**
3. When prompted "Do you want to exclude out-of-scope items from Proxy history?", click **Yes**

**Step 2: Intercept a Login Request**

1. Ensure **Proxy** → **Intercept** is **ON**
2. In Firefox, go to DVWA login page: `http://localhost/login.php`
3. Enter credentials:
   - Username: `test`
   - Password: `test123`
4. Click **Login**

5. **Switch to Burp Suite** - you should see the intercepted request:
   ```
   POST /login.php HTTP/1.1
   Host: localhost
   ...
   username=test&password=test123&Login=Login
   ```

**Step 3: Modify the Request**

1. In the intercepted request, change:
   ```
   username=test
   ```
   to:
   ```
   username=admin
   ```

2. Keep password as is
3. Click **Forward** button
4. Click **Intercept is on** to turn it OFF (you'll see the response)

**Step 4: Observe the Result**

- The login will fail because password doesn't match admin account
- This demonstrates request manipulation

**Step 5: Analyze HTTP History**

1. Go to **Proxy** → **HTTP history**
2. Find your modified request
3. Click on it to see:
   - **Request** tab: Shows what you sent
   - **Response** tab: Shows server's response
   - **Headers** tab: HTTP headers
   - **Cookies** tab: Session cookies

**Document this:**
- Take screenshot of the modified request
- Note the response code (likely 200 or 401)
- Identify any session cookies (PHPSESSID)

------------------------------------------------------------------------

### Exercise 2: SQL Injection Detection with Burp

**Step 1: Navigate to SQL Injection Page**

1. Login to DVWA with correct credentials (`admin` / `password`)
2. Click **SQL Injection** in left menu
3. Ensure Security Level is **Low**

**Step 2: Capture a Normal Request**

1. Turn **Intercept ON** in Burp
2. In DVWA SQL Injection field, enter: `1`
3. Click **Submit**
4. In Burp, observe the GET request:
   ```
   GET /vulnerabilities/sqli/?id=1&Submit=Submit HTTP/1.1
   ```
5. Right-click the request → **Send to Repeater**
6. Click **Forward** and turn **Intercept OFF**

**Step 3: Test SQL Injection in Repeater**

1. Go to **Repeater** tab in Burp
2. Modify the `id` parameter to: `1' OR '1'='1`
3. Click **Send**
4. Observe the response - you should see all database entries

**Step 4: Advanced SQL Injection**

Try these payloads in Repeater:
```sql
1' ORDER BY 1--
1' ORDER BY 2--
1' UNION SELECT null, null--
1' UNION SELECT user(), database()--
1' UNION SELECT null, table_name FROM information_schema.tables--
```

**Document findings:**
- Which payloads worked?
- What information was leaked?
- Take screenshots of successful injections

------------------------------------------------------------------------

### Exercise 3: Intruder - Brute Force Attack

**Step 1: Capture Login Request**

1. Logout from DVWA
2. Turn **Intercept ON**
3. Attempt login with `admin` / `wrong`
4. In Burp, right-click the captured POST request → **Send to Intruder**
5. Click **Forward** and turn **Intercept OFF**

**Step 2: Configure Intruder Attack**

1. Go to **Intruder** tab
2. Click **Positions** sub-tab
3. Click **Clear §** to remove all markers
4. Highlight the password value and click **Add §**:
   ```
   username=admin&password=§wrong§&Login=Login
   ```

**Step 3: Set Payload**

1. Click **Payloads** tab
2. Under **Payload settings**, add common passwords:
   ```
   password
   admin
   123456
   letmein
   Password1
   ```
   (Add one per line)

3. Click **Start attack** (Note: Community Edition is throttled)

**Step 4: Analyze Results**

1. Watch the **Length** column - different lengths may indicate success
2. Look for different **Status** codes
3. Sort by Length to find anomalies

**Note:** For educational purposes only. Real attacks are illegal without authorization.

------------------------------------------------------------------------

### Exercise 4: Analyzing Cookies and Session Management

**Step 1: Examine Session Cookies**

1. Login to DVWA successfully
2. In Burp, go to **Proxy** → **HTTP history**
3. Find the successful login POST request
4. Click on it and view **Response** → **Headers**
5. Look for `Set-Cookie: PHPSESSID=...`

**Step 2: Session Hijacking Simulation**

1. Copy the PHPSESSID value
2. Open **Repeater**
3. Create a new request to `http://localhost/index.php`
4. Add the Cookie header:
   ```
   Cookie: PHPSESSID=<copied_value>; security=low
   ```
5. Send the request - you should be authenticated

**Security Weakness Identified:** Session cookies without HttpOnly, Secure, or SameSite flags are vulnerable to theft.

------------------------------------------------------------------------

## 5. Deliverables

Submit a lab report including:

1. **Screenshot 1:** Burp Proxy showing an intercepted and modified HTTP request
2. **Screenshot 2:** Successful SQL injection payload and response in Repeater
3. **Screenshot 3:** Intruder attack results showing password enumeration
4. **Written Analysis (500 words):**
   - Explain Same-Origin Policy (SOP) and how Burp bypasses it
   - Describe CORS and its security implications
   - Identify **three security weaknesses** found in DVWA
   - Recommend fixes for each weakness

5. **Captured Traffic:** Export HTTP history
   - In Burp: **Proxy** → **HTTP history** → Right-click → **Save items**
   - Save as XML or text file

------------------------------------------------------------------------

## 6. Discussion Questions

Answer these in your report:

1. **Why is HTTPS interception harder than HTTP?**
   - Hint: Consider certificate validation and trust

2. **What ethical and legal concerns exist when using Burp Suite?**
   - Discuss CFAA, authorization, responsible disclosure

3. **How can developers defend against request manipulation?**
   - Input validation, server-side controls, CSRF tokens, etc.

4. **What is the difference between Burp Scanner (Pro) and manual testing?**
   - Research automation vs. manual pentesting

5. **How do modern frameworks prevent SQL injection?**
   - Prepared statements, ORMs, input sanitization

------------------------------------------------------------------------

## 7. Cleanup

After completing the lab:

```bash
# If using Kali package:
sudo dvwa-stop

# If using Docker container:
sudo docker stop dvwa
sudo docker rm dvwa

# Disable Firefox proxy
# Go to Settings → Network Settings → Select "No proxy"

# Optional: Remove Burp certificate from Firefox
# Settings → Privacy & Security → Certificates → View Certificates → Authorities
# Find PortSwigger CA → Delete
```

------------------------------------------------------------------------

## 8. Additional Resources

- **Burp Suite Documentation:** https://portswigger.net/burp/documentation
- **DVWA Documentation:** https://github.com/digininja/DVWA
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **CEH v12 Web Application Attacks:** Module 13
- **PortSwigger Web Security Academy:** https://portswigger.net/web-security (Free hands-on labs)

------------------------------------------------------------------------

## Troubleshooting

**Issue: Burp doesn't intercept traffic**
- Verify Firefox proxy settings (127.0.0.1:8080)
- Check Burp Proxy listener is running
- Ensure Intercept is ON

**Issue: HTTPS shows certificate errors**
- Re-import Burp CA certificate
- Trust it for websites
- Restart Firefox

**Issue: DVWA not accessible**
- Check Docker container: `sudo docker ps`
- Verify port 80 is free: `sudo netstat -tlnp | grep :80`
- Check firewall: `sudo ufw status`

**Issue: Burp Intruder is slow**
- Community Edition is rate-limited
- Use smaller wordlists
- Consider upgrading to Pro for real engagements

------------------------------------------------------------------------

## Notes

- **Legal Warning:** Only test systems you own or have written authorization to test
- **CEH Alignment:** This lab covers CEH v12 Module 13 topics: Web app attacks, session hijacking, injection flaws
- **Time Management:** Budget 30 min for setup, 1 hour for exercises, 30 min for documentation
