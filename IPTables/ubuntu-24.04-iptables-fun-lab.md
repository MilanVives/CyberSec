# 🚦 Ubuntu 24.04 *Fun* iptables Lab (GUI-friendly, instant feedback)

> **Goal:** Learn (and *feel*) how Linux packet filtering works using `iptables` on Ubuntu **24.04** with quick, visual tests you can try from your desktop browser and terminal. Everything is reversible and sandboxed to your own machine.

---

## 🧰 What you’ll need (5–10 min setup)

- Ubuntu **24.04** desktop (GNOME or similar).
- An admin user (sudo access).
- A browser (Firefox/Chromium) and a terminal window.
- Internet connection (for some exercises).

> **Note on Ubuntu 24.04:** Ubuntu uses the **nftables** backend by default; `iptables` on 24.04 is actually the **iptables-nft** front-end. That’s totally fine for this lab.

```bash
# Confirm we're using the nft backend:
sudo iptables -V
# Look for: "iptables v1.8.x (nf_tables)"
```

If you previously used UFW, it may inject rules; that’s okay. We’ll work alongside it.

---

## 🧯 Safety first — quick save/restore

Before playing, snapshot your current rules so you can restore with one command.

```bash
mkdir -p ~/iptables-lab
sudo iptables-save | tee ~/iptables-lab/backup.rules >/dev/null
echo 'Saved to ~/iptables-lab/backup.rules'
```

To restore at any time:

```bash
sudo iptables-restore < ~/iptables-lab/backup.rules
```

To completely **flush** current rules (both filter + nat) and reset policies to ACCEPT (only if you want a clean slate):

```bash
# FILTER & NAT flush and ACCEPT defaults
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -F
sudo iptables -t nat -F
```

---

## 🧪 Exercise 1 — “Hijack HTTP to your own local page” (visual in your GUI browser)

Make any **HTTP (port 80)** request from *your* user automatically redirect to a tiny local web page you host.
You’ll *see* it in your browser.

### 1) Start a mini web server on port 8080

```bash
# In a dedicated Terminal tab (leave running):
cd ~/iptables-lab
cat > index.html <<'HTML'
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>iptables lab</title></head>
<body style="font-family: system-ui; margin: 2rem;">
  <h1>🎉 Caught by iptables REDIRECT!</h1>
  <p>This page was served from <code>localhost:8080</code>, even though you tried to visit an HTTP site.</p>
  <p>Try opening <strong>http://neverssl.com</strong> or <strong>http://example.com</strong> in your browser.</p>
</body>
</html>
HTML

# Serve it:
python3 -m http.server 8080
```

### 2) Add a REDIRECT rule for your user

> We’ll only affect traffic created by **your login user** so other system services aren’t touched.

```bash
# Replace $USER with your username if needed; $UID expands to your numeric id.
sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -m owner --uid-owner $UID -j REDIRECT --to-ports 8080
```

### 3) Test in the GUI

Open your browser and visit **http://neverssl.com** (intentionally HTTP).  
You should see your **local page** instead of the real site 🎩.

**Turn it off** (so HTTP goes back to normal):

```bash
sudo iptables -t nat -D OUTPUT -p tcp --dport 80 -m owner --uid-owner $UID -j REDIRECT --to-ports 8080
```

> **Why this works:** Packet hits `nat/OUTPUT` (locally generated traffic), matches your UID + TCP dport 80, and is redirected to 8080 on localhost.

---

## 🎯 Exercise 2 — “Only one site works” (curate the web)

Lock your machine so **only Wikipedia** over HTTPS loads; everything else fails in the browser. This is great for focus sessions or demos.

> We’ll use a simple allowlist on the **OUTPUT** chain. We’ll insert rules at the top to take precedence.

### 1) Prep: flush OUTPUT (optional if you want a clean slate for outbound)

```bash
sudo iptables -P OUTPUT ACCEPT   # keep default permissive while editing
sudo iptables -F OUTPUT
```

### 2) Allow essentials first

```bash
# Always allow already-established connections:
sudo iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow local loopback:
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Allow DNS to your resolver (systemd-resolved uses 127.0.0.53)
sudo iptables -A OUTPUT -p udp --dport 53 -d 127.0.0.53 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 53 -d 127.0.0.53 -j ACCEPT
```

### 3) Resolve Wikipedia IPs and allow only those for HTTPS

> IPs can change. We’ll fetch a current list and create targeted allow rules.  
> You can repeat this snippet later if IPs rotate.

```bash
# Build an allowlist for en.wikipedia.org (IPv4)
WIKI_IPS=$(getent ahostsv4 en.wikipedia.org | awk '{print $1}' | sort -u)
for IP in $WIKI_IPS; do
  echo "Allowing HTTPS to $IP"
  sudo iptables -A OUTPUT -p tcp -d "$IP" --dport 443 -j ACCEPT
done
```

### 4) Default-drop the rest of outbound web

```bash
# Drop all other HTTPS/HTTP from your user:
sudo iptables -A OUTPUT -m owner --uid-owner $UID -p tcp --dport 443 -j REJECT --reject-with tcp-reset
sudo iptables -A OUTPUT -m owner --uid-owner $UID -p tcp --dport 80  -j REJECT --reject-with tcp-reset

# As a safety net, you can also drop everything else from your user (optional, stronger lock):
# sudo iptables -A OUTPUT -m owner --uid-owner $UID -j DROP
```

### 5) Test in the GUI

- Go to **https://en.wikipedia.org** → should **work**.
- Try **https://example.com** or **https://news.ycombinator.com** → should **fail immediately** (connection reset).

**Undo this exercise** (remove the added rules in reverse order or flush OUTPUT):  
```bash
sudo iptables -F OUTPUT
sudo iptables -P OUTPUT ACCEPT
```

---

## 📉 Exercise 3 — “Slow-mo ping” (rate-limited ICMP you can *see*)

Use `hashlimit` to **rate-limit ICMP echo requests** so `ping` visibly stutters.

```bash
# Allow ICMP echo-requests but limit to 1/sec with a small burst
sudo iptables -A OUTPUT -p icmp --icmp-type echo-request -m hashlimit \
  --hashlimit 1/second --hashlimit-burst 2 --hashlimit-mode srcip,dstip --hashlimit-name icmp_out \
  -j ACCEPT

# Then drop any extra echo-requests
sudo iptables -A OUTPUT -p icmp --icmp-type echo-request -j DROP
```

**Test:**

```bash
ping -i 0.2 1.1.1.1
# You should see bursts and then "Request timeout" messages.
```

**Cleanup:**

```bash
sudo iptables -D OUTPUT -p icmp --icmp-type echo-request -j DROP
sudo iptables -D OUTPUT -p icmp --icmp-type echo-request -m hashlimit \
  --hashlimit 1/second --hashlimit-burst 2 --hashlimit-mode srcip,dstip --hashlimit-name icmp_out \
  -j ACCEPT
```

---

## 🧲 One-click helpers (toggle scripts)

Save these tiny scripts to quickly enable/disable rules without retyping.

```bash
# Create helpers
cat > ~/iptables-lab/hijack-http-on.sh <<'BASH'
#!/usr/bin/env bash
sudo iptables -t nat -C OUTPUT -p tcp --dport 80 -m owner --uid-owner $UID -j REDIRECT --to-ports 8080 2>/dev/null \
|| sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -m owner --uid-owner $UID -j REDIRECT --to-ports 8080
echo "HTTP hijack ON → redirecting port 80 to localhost:8080 for UID $UID"
BASH

cat > ~/iptables-lab/hijack-http-off.sh <<'BASH'
#!/usr/bin/env bash
sudo iptables -t nat -D OUTPUT -p tcp --dport 80 -m owner --uid-owner $UID -j REDIRECT --to-ports 8080 2>/dev/null || true
echo "HTTP hijack OFF"
BASH

chmod +x ~/iptables-lab/*.sh
echo "Created helper scripts in ~/iptables-lab"
```

Run with:
```bash
~/iptables-lab/hijack-http-on.sh
# ...later...
~/iptables-lab/hijack-http-off.sh
```

---

## 🧼 Full cleanup / restore

When you’re done, either restore your snapshot or wipe rules for this session.

```bash
# Option A: restore previous rules snapshot
sudo iptables-restore < ~/iptables-lab/backup.rules

# Option B: wipe everything to permissive
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -F
sudo iptables -t nat -F
```

---

## 🧠 What you learned

- How `nat/OUTPUT` can **REDIRECT** locally generated packets (great for dev/proxy tricks).
- Building an **allowlist** using `OUTPUT` and targeted destination IPs (and why DNS/IP churn matters).
- Using `hashlimit` to **rate-limit** traffic and watch behavior change live.
- Safe snapshots and quick cleanup with `iptables-save`/`iptables-restore`.

**Next ideas:** Try per-app rules with `-m owner --uid-owner` for a specific service account, or experiment with logging:  
`-j LOG --log-prefix "FW DROP: " --log-level 4` (check with `journalctl -k -f`).

Have fun—and don’t forget to restore when you’re done! 🎈