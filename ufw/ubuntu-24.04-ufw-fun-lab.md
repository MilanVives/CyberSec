# 🔥 Ubuntu 24.04 *Fun* UFW Lab (GUI-friendly, instant feedback)

> **Goal:** Learn to *see* and *feel* what UFW (Uncomplicated Firewall) does under the hood — with fast, visual, and undoable experiments. Everything works on Ubuntu **24.04 Desktop (GUI)**.

---

## 🧰 What you’ll need

- Ubuntu 24.04 desktop (GNOME or similar)
- Terminal window and browser
- Sudo privileges

---

## 🚀 Step 1: Get a clean baseline

Check that UFW is installed and inactive:

```bash
sudo apt install ufw -y
sudo ufw status verbose
```

If it’s active, disable it for a clean start:

```bash
sudo ufw disable
```

---

## 🧯 Step 2: Create a quick safety snapshot

UFW rules can be easily reset, but let’s save a copy anyway.

```bash
sudo cp /etc/ufw/user.rules ~/ufw-backup.rules
```

To restore later:

```bash
sudo cp ~/ufw-backup.rules /etc/ufw/user.rules
sudo ufw reload
```

---

## 🧪 Exercise 1 — “Lock yourself out (gently)”

Let’s block *all* outbound web browsing (port 80 + 443) just for fun, then poke holes back in.

### 1) Enable UFW and start fresh

```bash
sudo ufw reset
sudo ufw default deny outgoing
sudo ufw default allow incoming
sudo ufw enable
```

Now try visiting **https://example.com** — it should fail immediately (no internet).

### 2) Allow only one site (Wikipedia)

Let’s allow outbound traffic only to Wikipedia:

```bash
WIKI_IPS=$(getent ahostsv4 en.wikipedia.org | awk '{print $1}' | sort -u)
for IP in $WIKI_IPS; do
  echo "Allowing Wikipedia ($IP)"
  sudo ufw allow out to $IP port 443 proto tcp comment 'Wikipedia only'
done
```

Now, **Wikipedia loads**, but every other site fails!

To open everything again:

```bash
sudo ufw default allow outgoing
sudo ufw reload
```

---

## 🎨 Exercise 2 — “Mini web server trap”

This one’s **visual**: you’ll hijack local web requests (port 8080) and make them visible in your browser.

### 1) Start a quick Python server

```bash
mkdir -p ~/ufw-lab && cd ~/ufw-lab
cat > index.html <<'HTML'
<!doctype html>
<html><body style="font-family:sans-serif; margin:2rem;">
<h1>👋 You hit my local UFW trap!</h1>
<p>This is served from <code>localhost:8080</code>.</p>
</body></html>
HTML

python3 -m http.server 8080
```

### 2) Restrict inbound access

```bash
sudo ufw reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow in 8080/tcp comment 'local demo web'
sudo ufw enable
```

### 3) Visit in browser

Go to **http://localhost:8080** → it should show your page.

Try another port, e.g. **http://localhost:9090** → **Connection refused** (blocked by UFW).

**Turn it off:**

```bash
sudo ufw disable
```

---

## ⚙️ Exercise 3 — “Allow SSH only from one IP”

Simulate letting a friend connect while blocking everyone else.

### 1) Deny all SSH first

```bash
sudo ufw reset
sudo ufw default deny incoming
sudo ufw allow out on any
sudo ufw enable
```

### 2) Allow SSH from your other device (replace with real IP)

```bash
sudo ufw allow from 192.168.1.42 to any port 22 proto tcp comment 'Friend SSH only'
```

You can confirm with:

```bash
sudo ufw status numbered
```

---

## 🧩 Exercise 4 — “Rate-limit bad login attempts”

UFW has built-in **rate limiting** (behind the scenes it uses iptables `hashlimit`), perfect for brute-force prevention.

Enable it for SSH:

```bash
sudo ufw reset
sudo ufw default deny incoming
sudo ufw allow out on any
sudo ufw limit 22/tcp comment 'Rate limit SSH brute force'
sudo ufw enable
```

Now if you hammer port 22 with multiple login attempts in a short time, they’ll start getting dropped.

---

## 🧹 Cleanup

```bash
sudo ufw reset
sudo ufw disable
sudo ufw default allow outgoing
sudo ufw default allow incoming
```

---

## 🧠 What you learned

- How **UFW** simplifies firewall control with human-friendly commands.
- Outbound vs inbound control.
- Allowlisting specific IPs.
- Visual confirmation of open/closed ports.
- Using built-in **rate limiting** for brute-force protection.

**Next steps:**  
- Pair this with `ufw logging on` + `sudo tail -f /var/log/ufw.log` to *see* blocked packets live.  
- Try per-app profiles under `/etc/ufw/applications.d/`.  
- Mix it with `network namespaces` or VMs for more advanced play!

🧑‍💻 Have fun — and remember, UFW makes the *uncomplicated* kind of chaos!