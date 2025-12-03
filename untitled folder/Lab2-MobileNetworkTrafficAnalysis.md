# Lab 2: Mobile Network Traffic Analysis and Man-in-the-Middle Attack

## Objective
Learn to intercept and analyze mobile application network traffic using a MITM proxy to identify insecure communications, unencrypted data transmission, and certificate validation vulnerabilities.

## Prerequisites
- Kali Linux system
- Android smartphone with WiFi
- Both devices on the same network
- Completed Lab 1 (recommended but not required)

## Lab Duration
Approximately 60-90 minutes

## Learning Outcomes
After completing this lab, you will be able to:
1. Set up a Man-in-the-Middle proxy (Burp Suite/mitmproxy)
2. Configure mobile device to use proxy
3. Install custom CA certificates on Android
4. Intercept and analyze HTTP/HTTPS traffic
5. Identify insecure API endpoints
6. Detect sensitive data transmission
7. Understand SSL/TLS pinning and bypasses

## Required Tools
- `mitmproxy` (recommended) or `Burp Suite Community Edition`
- `adb` - Android Debug Bridge
- Wireshark (optional)
- Your Android device

## Part 1: Proxy Server Setup (20 minutes)

### Step 1: Install mitmproxy

```bash
# Update system
sudo apt update

# Install mitmproxy
sudo apt install -y mitmproxy

# Verify installation
mitmproxy --version

# Alternative: Install Burp Suite (if not already installed)
# sudo apt install -y burpsuite
```

### Step 2: Configure Network

**Find your Kali IP address:**
```bash
# Get IP address
ip addr show | grep -E "inet.*wlan0|inet.*eth0"

# Or simpler
hostname -I
```

**Example output:**
```
192.168.1.100
```

**Note this IP address** - you'll need it to configure your phone.

### Step 3: Start mitmproxy

**Terminal-based (mitmproxy):**
```bash
# Start mitmproxy on port 8080
mitmproxy --listen-host 0.0.0.0 --listen-port 8080
```

**Or use mitmweb (Web Interface):**
```bash
# Start mitmweb - provides web interface
mitmweb --listen-host 0.0.0.0 --listen-port 8080 --web-host 0.0.0.0
```

**Access web interface at:** http://localhost:8081

**Or use Burp Suite:**
```bash
# Start Burp Suite
burpsuite &

# Configure:
# 1. Go to Proxy > Options
# 2. Edit proxy listener
# 3. Set binding to: All interfaces (0.0.0.0)
# 4. Port: 8080
```

### Step 4: Verify Proxy is Running

```bash
# In another terminal, check if port is listening
sudo netstat -tlnp | grep 8080

# Or
sudo ss -tlnp | grep 8080
```

## Part 2: Mobile Device Configuration (15 minutes)

### Step 5: Connect Phone to Same Network

**On your Android device:**
1. Ensure phone is connected to same WiFi network as Kali
2. Go to Settings > Network & Internet > WiFi
3. Long-press on connected network
4. Select "Modify network" or "Manage network settings"

### Step 6: Configure Proxy Settings

**On your Android device:**
1. Tap "Advanced options"
2. Set Proxy to "Manual"
3. Enter:
   - **Proxy hostname:** [Your Kali IP, e.g., 192.168.1.100]
   - **Proxy port:** 8080
4. Save settings

### Step 7: Test Basic Connectivity

**On Android:**
1. Open browser
2. Navigate to: http://example.com
3. Check Kali terminal - you should see the request in mitmproxy

**Expected in mitmproxy:**
```
GET http://example.com/
```

## Part 3: SSL/TLS Certificate Installation (20 minutes)

### Step 8: Generate and Download CA Certificate

**Using mitmproxy:**

**On Android browser, navigate to:**
```
http://mitm.it
```

This will show certificate download page.

**Alternative method - Manual certificate extraction:**
```bash
# Certificate is automatically created in
ls ~/.mitmproxy/

# Files present:
# mitmproxy-ca.pem
# mitmproxy-ca-cert.pem
# mitmproxy-ca-cert.p12

# Copy certificate to web directory
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /var/www/html/mitmproxy-ca-cert.crt

# Start simple HTTP server
cd /var/www/html
python3 -m http.server 8000
```

**Download from phone:**
Navigate to: http://[Kali-IP]:8000/mitmproxy-ca-cert.crt

### Step 9: Install Certificate on Android

**For Android 11+:**
1. Download certificate (should be in Downloads folder)
2. Go to Settings > Security > Encryption & credentials
3. Tap "Install a certificate"
4. Select "CA certificate"
5. Tap "Install anyway" (warning will appear)
6. Navigate to Downloads folder
7. Select the downloaded certificate
8. Name it "mitmproxy" or "Burp Suite"
9. Tap OK

**For Android 10 and below:**
1. Settings > Security > Install from storage
2. Select the certificate file
3. Name it and save

### Step 10: Verify Certificate Installation

```bash
# Test HTTPS interception
# On Android, open browser and go to:
https://www.google.com
```

**Check mitmproxy console** - you should now see HTTPS traffic!

## Part 4: Traffic Analysis (25 minutes)

### Step 11: Install Test Applications

**Option A: Use previously analyzed DIVA app**
```bash
adb install diva-beta.apk
```

**Option B: Use any social media or news app from phone**

### Step 12: Intercept Application Traffic

**Start capturing:**
```bash
# If using mitmproxy, it's already capturing
# Press 'i' to set intercept filter if needed

# In mitmweb, flows appear automatically in web interface
```

**On your phone:**
1. Open the test application
2. Perform login (use test credentials!)
3. Navigate through different screens
4. Submit some data

### Step 13: Analyze HTTP Traffic

**In mitmproxy, use keyboard shortcuts:**
- `Enter` - View flow details
- `Tab` - Switch between Request/Response
- `e` - Edit request/response
- `q` - Back to flow list
- `f` - Set filter

**Useful filters:**
```
# Filter by domain
~d example.com

# Filter by method
~m POST

# Filter by response code
~c 200

# Filter by URL path
~u /api/
```

### Step 14: Identify Security Issues

**Look for:**

**1. Unencrypted HTTP Requests:**
```
GET http://api.insecureapp.com/login
```
❌ Critical: Credentials sent over HTTP

**2. Sensitive Data in URLs:**
```
GET https://api.app.com/user?password=123456&ssn=123-45-6789
```
❌ High: Sensitive data in URL parameters (logged in server logs)

**3. API Keys in Headers:**
```
Authorization: Bearer hardcoded_api_key_12345
X-API-Key: sk_live_abc123def456
```
❌ Medium: Check if keys are hardcoded

**4. Personal Information Leakage:**
```json
{
  "user": {
    "email": "user@example.com",
    "phone": "+1234567890",
    "ssn": "123-45-6789",
    "credit_card": "4111111111111111"
  }
}
```
❌ Critical: PII sent without proper protection

**5. Session Token Security:**
```
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict
```
✅ Good: Proper flags set

```
Set-Cookie: session_id=abc123
```
❌ Medium: Missing security flags

### Step 15: Test for SQL Injection via Mobile App

**In mitmproxy:**
1. Intercept a POST request to login endpoint
2. Press `e` to edit
3. Modify the password field:
   ```json
   {
     "username": "admin",
     "password": "' OR '1'='1"
   }
   ```
4. Forward the request
5. Check response for success or error

### Step 16: Save Traffic Capture

**In mitmproxy:**
```bash
# Save all flows to file
# Press: Shift + S
# Or from command line when starting:
mitmproxy -w capture.mitm

# Convert to HAR format (HTTP Archive)
mitmdump -r capture.mitm -w capture.har
```

**In mitmweb:**
- Click "File" > "Save"
- Choose location and format

## Part 5: SSL Pinning Detection (15 minutes)

### Step 17: Identify Apps with SSL Pinning

**Test different apps:**

1. Banking apps (usually have pinning)
2. Social media apps (may have pinning)
3. News/weather apps (usually no pinning)

**Signs of SSL Pinning:**
- App fails to connect when proxy is configured
- Error messages like "Connection failed" or "Certificate error"
- No traffic appears in mitmproxy

### Step 18: Document SSL Pinning Behavior

**Create a table:**
```markdown
| App Name | Package Name | SSL Pinning | Error Message |
|----------|--------------|-------------|---------------|
| DIVA     | jakhar.aseem.diva | No | N/A |
| Banking App | com.bank.app | Yes | "Connection Secure Error" |
```

### Step 19: Basic SSL Pinning Bypass (Conceptual)

**Tools for bypassing (requires root):**
```bash
# Install Frida (dynamic instrumentation)
pip3 install frida-tools

# Download Frida server for Android
# https://github.com/frida/frida/releases

# Check if your device is rooted
adb shell su -c "id"
```

**Note:** SSL pinning bypass requires rooted device and is beyond scope of basic lab. Mentioned here for awareness.

## Part 6: Traffic Analysis Report (10 minutes)

### Step 20: Create Analysis Report

**Template:**
```markdown
# Mobile Application Network Traffic Analysis Report

**Application Tested:** [App Name]
**Test Date:** [Date]
**Analyst:** [Your Name]
**Proxy Used:** mitmproxy / Burp Suite

## Network Security Assessment

### 1. Protocol Usage
- [ ] HTTPS used for all communications
- [ ] HTTP used for some/all communications
- [ ] Certificate pinning implemented
- [ ] Certificate pinning NOT implemented

### 2. Authentication & Session Management
**Finding:** [Description]
- Login endpoint: [URL]
- Credentials transmission method: [GET/POST/Headers]
- Session token format: [Cookie/Bearer/Custom]
- Token security flags: [HttpOnly/Secure/SameSite]

### 3. Data Transmission Security
**Sensitive Data Identified:**
- Personal Information: [Yes/No] - [Details]
- Financial Data: [Yes/No] - [Details]
- Authentication Credentials: [Yes/No] - [Details]
- API Keys: [Yes/No] - [Details]

### 4. API Endpoints Discovered
| Endpoint | Method | Purpose | Security |
|----------|--------|---------|----------|
| /api/login | POST | Authentication | HTTP ❌ |
| /api/user/profile | GET | User data | HTTPS ✅ |

### 5. Vulnerabilities Identified
1. **[Vulnerability Name]**
   - Severity: Critical/High/Medium/Low
   - Evidence: [Request/Response snippet]
   - Impact: [Description]
   - Recommendation: [Fix]

## Conclusion
[Overall assessment]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

## Challenge Questions

1. **What is the difference between HTTP and HTTPS traffic in mitmproxy?**
2. **Why do we need to install a CA certificate on the mobile device?**
3. **What is SSL/TLS certificate pinning and why do apps use it?**
4. **List 3 security issues you can identify by analyzing network traffic.**
5. **What HTTP methods did you observe? (GET, POST, PUT, DELETE, etc.)**
6. **Did you find any API keys or tokens? Where were they located?**
7. **What information can an attacker gather from HTTP traffic?**
8. **How can session hijacking be performed using intercepted traffic?**
9. **What are the security implications of sending data over HTTP vs HTTPS?**
10. **How would you protect against MITM attacks as a developer?**

## Additional Exercises

### Exercise 1: Modify Requests
```bash
# In mitmproxy:
# 1. Intercept a POST request
# 2. Press 'e' to edit
# 3. Change parameter values
# 4. Forward modified request
# 5. Observe response
```

### Exercise 2: Replay Attacks
```bash
# 1. Capture a successful login request
# 2. Save it
# 3. Replay it later
# 4. Check if it still works (session management test)
```

### Exercise 3: Response Manipulation
```bash
# 1. Intercept response from server
# 2. Modify JSON data (e.g., account balance)
# 3. Forward to app
# 4. Observe if app accepts modified data
```

## Common Issues & Solutions

**Problem:** Phone can't connect to internet with proxy
- **Solution:** Verify Kali IP is correct and proxy is running

**Problem:** Can't see HTTPS traffic
- **Solution:** Ensure CA certificate is properly installed

**Problem:** mitmproxy shows SSL errors
- **Solution:** App may have certificate pinning

**Problem:** App detects proxy and refuses to work
- **Solution:** Some apps detect proxy environment

**Problem:** Certificate installation fails
- **Solution:** Android 11+ requires different installation method (Settings > Security > Encryption & credentials)

## Best Practices for Developers

Based on this lab, developers should:

1. ✅ **Always use HTTPS** for all communications
2. ✅ **Implement certificate pinning** for sensitive apps
3. ✅ **Never send credentials in URL parameters**
4. ✅ **Use secure session management** (HttpOnly, Secure, SameSite flags)
5. ✅ **Implement root/jailbreak detection**
6. ✅ **Encrypt sensitive data** before transmission
7. ✅ **Implement request signing** to prevent tampering
8. ✅ **Use short-lived tokens** with refresh mechanism
9. ✅ **Log and monitor** for suspicious activity
10. ✅ **Implement rate limiting** on API endpoints

## Advanced Topics (Optional)

### Automated Traffic Analysis
```bash
# Use mitmproxy scripts
mitmproxy -s analysis_script.py

# Example script to extract credentials
cat > extract_credentials.py << 'EOF'
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if "login" in flow.request.pretty_url.lower():
        print(f"[*] Login attempt to: {flow.request.pretty_url}")
        if flow.request.method == "POST":
            print(f"[*] POST Data: {flow.request.content}")
EOF

mitmproxy -s extract_credentials.py
```

### Network Packet Analysis with Wireshark
```bash
# Capture traffic
sudo tcpdump -i wlan0 -w mobile_traffic.pcap

# Analyze in Wireshark
wireshark mobile_traffic.pcap
```

## Lab Submission Requirements

Submit the following:

1. **Network Traffic Analysis Report** (using template above)
2. **Screenshots showing:**
   - mitmproxy/Burp interface with captured traffic
   - Mobile device proxy configuration
   - Installed CA certificate
   - At least 3 different API requests
   - One example of sensitive data transmission
3. **Answers to all 10 challenge questions**
4. **Exported traffic capture file** (.mitm or .har format)

## Grading Rubric

- Proxy setup and configuration: 20%
- Certificate installation: 15%
- Traffic capture and analysis: 30%
- Vulnerability identification: 20%
- Report quality: 10%
- Challenge questions: 5%

## Cleanup

After lab completion:

**On Android device:**
1. Remove proxy configuration (set to None)
2. Remove CA certificate:
   - Settings > Security > Trusted credentials
   - User tab > Find mitmproxy/Burp cert
   - Remove

**On Kali:**
```bash
# Stop mitmproxy (Ctrl+C)

# Optional: Remove certificates
rm -rf ~/.mitmproxy/
```

## Additional Resources

- mitmproxy Documentation: https://docs.mitmproxy.org/
- OWASP Mobile Top 10 - M3 Insecure Communication: https://owasp.org/www-project-mobile-top-10/
- Burp Suite Mobile Testing: https://portswigger.net/burp/documentation/desktop/mobile
- Android Network Security Config: https://developer.android.com/training/articles/security-config

---
**Lab Created for:** Cybersecurity Architecture Course - CEH Chapter 8
**Difficulty Level:** Intermediate to Advanced
**Last Updated:** December 2025
**Note:** Always obtain proper authorization before testing applications you don't own!
