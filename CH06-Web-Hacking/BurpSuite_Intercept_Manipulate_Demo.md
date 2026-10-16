# Burp Suite — Simple demo: intercepting & manipulating requests

> **Audience:** students learning web application testing in a lab environment.

---

## Objective
- Show how to configure a browser to proxy through Burp Suite (Community or Professional).
- Intercept an HTTP request, modify headers and body, forward it and observe server response.
- Demonstrate Repeater for manual request replay and simple Intruder use-cases.
- Emphasize ethics: only test systems you own or have explicit permission to test.

---

## Prerequisites (lab-only)
- A macOS or Linux machine.
- Burp Suite Community or Professional installed (GUI).
  - macOS: `brew install --cask burpsuite` or download from PortSwigger.
  - Linux: download the Burp Suite installer from PortSwigger and run it per their instructions.
- A test webapp you control. Examples:
  - Simple static server: `python3 -m http.server 8000` (useful for GET/HTML demos).
  - Simple echo form (Flask) — see the **Lab server** section below.
- A browser you can configure to use an HTTP proxy (Firefox is easiest for per-profile proxy).

**Safety / Ethics reminder:** Only intercept/modify traffic for systems you own or that are explicitly authorized for testing. Intercepting others' traffic is illegal and unethical.

---

## High-level workflow (what students will see)
1. Start Burp Suite and enable the Intercept proxy listener (default: 127.0.0.1:8080).
2. Configure the browser to use the HTTP proxy at 127.0.0.1:8080.
3. Install Burp's CA certificate into the browser so HTTPS sites can be proxied without TLS errors.
4. Browse the lab site; Burp will capture requests in the Proxy → Intercept tab.
5. Modify a header or request body in Intercept and `Forward` the modified request.
6. Send the same request to Repeater for manual tweaks and observation of responses.
7. Optionally use Intruder for safe, local parameter testing in the lab.

---

## Quick setup steps (proxy & CA)

### 1) Start Burp and confirm proxy listener
- Open Burp Suite.
- Go to **Proxy → Options** and ensure there is an HTTP listener on `127.0.0.1:8080` (default).

### 2) Configure your browser (Firefox recommended for demos)
- Open Firefox and create a new Profile for the lab.
- Preferences → Network Settings → Manual proxy configuration:
  - HTTP Proxy: `127.0.0.1` Port: `8080`
  - Check “Use this proxy server for all protocols” if desired.
- Save and restart the profile (ensures no system-wide changes).

### 3) Install Burp CA certificate into the browser
- In Burp: **Proxy → Intercept** → click the `Open Browser` button (Community edition) or visit `http://burp` in your proxied browser.
- Click **CA Certificate** (or visit `http://burp/cert`) and download the certificate.
- In Firefox: Preferences → Privacy & Security → View Certificates → Import → trust the CA to identify websites.

*Note:* Only import the CA into the lab profile. Do not import Burp CA into your everyday browser profile.

---

## Lab server (minimal Flask echo app)
Run this only in a controlled lab VM. It accepts a POST from a form and echoes back the submitted fields.

```python
# echo_app.py - simple Flask app for Burp demos
from flask import Flask, request, render_template_string
app = Flask(__name__)

FORM = '''
<!doctype html>
<title>Echo form</title>
<h1>Echo form</h1>
<form method="post" action="/echo">
  <label>Name: <input name="name"></label><br>
  <label>Message: <input name="msg"></label><br>
  <button type="submit">Send</button>
</form>
'''

@app.route('/')
def index():
    return FORM

@app.route('/echo', methods=['POST'])
def echo():
    name = request.form.get('name','')
    msg = request.form.get('msg','')
    return f"<h2>Echo</h2><p>Name: {name}</p><p>Message: {msg}</p>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

Run: `python3 echo_app.py` and visit `http://127.0.0.1:5000` in your proxied browser.

---

## Demo: intercepting and modifying a GET request
1. In Burp: Proxy → Intercept → ensure **Intercept is on**.
2. In browser: visit `http://127.0.0.1:5000/` and click to load the page.
3. Burp will capture the GET request and show it in the **Intercept** tab.
4. In the Intercept view you can edit the request line and headers directly. Example edits:
   - Change `User-Agent` to something else.
   - Add a custom header: `X-Demo: classroom`.
5. Click **Forward** to let the modified request reach the server.
6. Observe the server's response in the browser and in Burp's **HTTP history**.

**Teaching point:** show how simple header changes can alter behavior or reveal server-side handling.

---

## Demo: intercepting and manipulating a POST form (body tampering)
1. In the browser, fill the Echo form with `Name = Alice`, `Message = Hello` and submit.
2. Burp will intercept the POST request to `/echo`.
3. In the Intercept tab you will see the request body (e.g., `name=Alice&msg=Hello`).
4. Edit the body to change `name=Bob&msg=Hacked` and press **Forward**.
5. Observe the echoed result showing altered values — the server accepted the modified body.

**Teaching point:** demonstrate how client requests can be altered in transit and why server-side validation is critical.

---

## Using Repeater for iterative testing
1. Right-click the intercepted request → **Send to Repeater**.
2. Switch to **Repeater** tab — here you can tweak the request and hit **Send** repeatedly to observe responses.
3. Use Repeater to test variations safely (e.g., different form values, headers, or paths).

**Teaching point:** Repeater is ideal for manual, controlled exploration of a single request.

---

## Using Intruder (lab-safe example)
- Intruder automates custom payloads against parameters. Use it **only** in lab.
- Example: target the `msg` parameter and try a small list of innocuous test payloads to show how automation works.
- Steps (summary):
  1. Send request to Intruder → Positions: mark the `msg` value as a payload position.
  2. Payloads → load a small list (e.g., `Hello`, `Testing`, `123`).
  3. Start attack and observe results (status, length) to illustrate differences.

**Teaching point:** show controlled automation; stress limits and ethics.

---

## Saving work & reporting
- Save the Burp project (File → Save project) if you want to keep logs and request history for grading/notes.
- Export specific requests/responses as files for inclusion in reports.
- Teach students to document every action, include timestamps, and capture screenshots for reproducibility.

---

## Troubleshooting tips
- **No traffic in Burp:** confirm browser proxy settings point to 127.0.0.1:8080 and Burp listener is enabled.
- **TLS errors:** ensure Burp CA was imported into the browser profile and marked trusted.
- **Requests bypassing Burp:** check if the browser is using system proxy settings or extensions (HTTPS bypass) or HSTS; use the dedicated lab profile.

---

## Teaching notes & safety reminders
- Always emphasize legal & ethical boundaries. Never intercept real user traffic or systems without permission.
- Prefer an isolated VM or local network for demos so students can reproduce steps safely.
- Keep the demo short and interactive: ask students to suggest a header/body change, then execute it in Repeater.

---

## Suggested classroom exercise (5–10 minutes)
1. Student pair runs the Flask echo app.
2. Configure browser profile to proxy through Burp.
3. Intercept a POST, modify the body to swap submitted values, forward, and record the result.
4. Send the request to Repeater and try two additional modifications; document the server behavior.

---

## References / further reading
- PortSwigger — Burp Suite documentation (official). (Students should consult official docs for advanced workflows.)
- OWASP — Web testing guides and legal/ethical testing notes.

---

*File prepared as a classroom demo; adapt timings and depth to your audience.*
