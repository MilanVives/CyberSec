# Lab — Web Vulnerability Scanning with Nikto (Docker)

**Book:** CEH All-in-One, Chapter 6 — *Web-Based Hacking: Servers and Applications*
**Level:** 🟢 Beginner · **Duration:** ~45–60 min · **Hardware:** none
**Runs on:** Windows, macOS, or Linux — **only Docker is required** (no Kali, no VM).

In this lab you run a real web-vulnerability scanner (**Nikto**) against a
deliberately insecure web app (**DVWA**). Both the scanner and the target run as
Docker containers on your own laptop, so there is nothing to install besides
Docker and nothing illegal about it — you own both machines.

---

## Learning objectives

By the end you can:

- Start a vulnerable web target and a scanner using Docker.
- Run a Nikto scan and save a readable HTML report.
- Explain three findings Nikto reports and recommend a fix for each.

---

## Requirements

| | |
|---|---|
| Software | [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker Engine (Linux) |
| RAM / disk | ~2 GB free, ~2 GB disk |
| Internet | Needed once, to download the two images |

Check Docker works (you should see "Hello from Docker!"):

```bash
docker run --rm hello-world
```

> On **Windows**, run the commands below in **PowerShell** or **Windows Terminal**.
> They are identical to macOS/Linux. Docker Desktop must be running (whale icon).

---

## Part 1 — Start the target (DVWA)

We put both containers on one private Docker network so the scanner can reach the
target by name.

```bash
docker network create weblab
docker run -d --name dvwa --network weblab -p 8081:80 vulnerables/web-dvwa
```

- `-d` runs it in the background.
- `-p 8081:80` also exposes it to **your browser** at <http://localhost:8081>.

> 🍏 On Apple Silicon (M1/M2/M3) Docker may warn the image is `linux/amd64`.
> That is fine — it runs under emulation.

Give it ~20 seconds, then open <http://localhost:8081> in your browser. You should
see the DVWA login page. (You do **not** need to log in for this lab — Nikto scans
the server itself.)

If you *want* to click around: press **Create / Reset Database**, then log in with
`admin` / `password`.

---

## Part 2 — Run the Nikto scan

Nikto also runs from Docker, so you never install it. It checks a web server for
thousands of known issues: dangerous files, outdated software, missing security
headers, and risky configuration.

> A full scan checks ~6500 items and can take a few minutes. To keep it short in
> class, add `-maxtime 90s` to either command below to stop it after 90 seconds —
> you still get plenty of findings.

### 2a. A quick scan to the screen

```bash
docker run --rm --network weblab frapsoft/nikto -h http://dvwa
```

`-h http://dvwa` is the target: `dvwa` is the container name on the `weblab`
network. Watch the results scroll — each line starting with `+` is a finding.

### 2b. Save a report you can submit

```bash
docker run --rm --network weblab -v "${PWD}:/out" frapsoft/nikto \
  -h http://dvwa -o /out/nikto_report.html -Format html
```

- `-v "${PWD}:/out"` shares your **current folder** with the container so the report
  lands next to you as `nikto_report.html`.
- On Windows PowerShell `${PWD}` works; in the old `cmd.exe` use `%cd%` instead.

Open `nikto_report.html` in your browser and keep it for your submission.

---

## Part 3 — Read the results

Find these in your report and note what each means:

| Look for | What it tells you |
|---|---|
| `Server:` banner (e.g. Apache/…, PHP/…) | Software + version → attacker can look up known CVEs |
| Missing `X-Frame-Options` header | Page can be framed → clickjacking risk |
| Missing `X-Content-Type-Options` header | Browser may MIME-sniff → content-type attacks |
| Cookie without `HttpOnly` flag | Session cookie readable by JavaScript → theft via XSS |
| `/config`, `/.git`, `/setup.php`, `README` etc. | Exposed files/directories that leak information |

> **Why so many findings?** DVWA is *built* to be insecure. On a real target you
> would expect far fewer — and every one would matter.

---

## Deliverable (Core)

Submit a short report (½–1 page) containing:

1. The saved `nikto_report.html` (or a screenshot of the scan output).
2. **Three** findings from your scan, and for **each**: what the risk is and one
   concrete fix (e.g. *"add the `X-Frame-Options: DENY` header in Apache config"*).
3. One sentence: what is Nikto good at, and what can it **not** tell you?

---

## Stretch goals (optional — pick any)

- **Tune the noise.** Re-run with `-Tuning 2` (only "misconfiguration/default files")
  and compare how many findings you get:
  `docker run --rm --network weblab frapsoft/nikto -h http://dvwa -Tuning 2`
- **Second target.** Start OWASP Juice Shop and scan it too, then compare the two
  reports:
  ```bash
  docker run -d --name juice --network weblab -p 3000:3000 bkimminich/juice-shop
  docker run --rm --network weblab frapsoft/nikto -h http://juice:3000
  ```
- **Think like a defender.** Pick your three findings and write the exact config
  line or header that would remove each one.

---

## Cleanup

```bash
docker rm -f dvwa juice 2>/dev/null
docker network rm weblab
```

(Removing the containers is enough; the images stay cached for next time. To free
disk space later: `docker image rm vulnerables/web-dvwa frapsoft/nikto`.)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `docker: command not found` | Install Docker Desktop and make sure it is **running** (whale icon in the tray/menu bar). |
| `port is already allocated` | Something uses 8081. Change `-p 8081:80` to e.g. `-p 8082:80` and use that port in the browser. |
| Nikto says `No web server found` | The target isn't ready yet — wait 20 s and retry, and check both containers are on the **same** `--network weblab`. |
| `http://localhost:8081` won't load | Run `docker ps` — is `dvwa` listed and "Up"? If not: `docker logs dvwa`. |
| Report file not created | Check the `-v "${PWD}:/out"` part; on Windows `cmd.exe` use `-v "%cd%:/out"`. |

---

## Discussion questions

1. Why is a scan result a *starting point*, not proof of a vulnerability? (Think
   "false positives".)
2. What are Nikto's limitations compared to a tool like Burp Suite or OpenVAS?
3. Nikto is "loud" — it makes thousands of requests. Why does that matter on a real
   engagement, and what would the target's logs/IDS see?

---

*Only ever scan systems you own or are explicitly authorised to test. Here, both
containers run on your own machine, so you are in the clear.*
