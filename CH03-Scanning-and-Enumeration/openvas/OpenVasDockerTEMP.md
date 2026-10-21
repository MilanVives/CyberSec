# OpenVAS Quick Lab with Docker (beginner)

**Book:** CEH All-in-One, Chapter 3 — *Scanning and Enumeration* (vulnerability scanning)
**Duration:** ~5 min setup + **~20 min waiting** + 30–45 min scanning and analysis
**Level:** entry — no Kali install, no PostgreSQL troubleshooting

This lab is an easy way into vulnerability scanning. It uses the ready-made
[`immauss/openvas`](https://immauss.github.io/openvas/) Docker image, which has the
whole Greenbone/OpenVAS stack in **one container**. You scan a deliberately
vulnerable web app (DVWA) that runs in a second container on your own machine, so
you don't need permission from anyone and you don't need an internet target.

> Want the full experience (installing GVM on Kali, the CLI, scanning the course
> hosts)? See the main [OpenVAS Lab Assignment](OpenVAS_Assignment.md).

## Learning Objectives

- Start a vulnerability scanner with Docker.
- Create a target and a scan task in the Greenbone web interface.
- Read a report: severity, CVSS, QoD (Quality of Detection), solution.

## Requirements

| | Minimum |
|---|---|
| Software | [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker Engine (Linux) |
| RAM | 4 GB free for Docker (Docker Desktop → *Settings → Resources*) |
| Disk | ~10 GB free |

Check that Docker works:

```bash
docker run --rm hello-world
```

---

## Step 1 — Create a lab network and start the target (DVWA)

```bash
docker network create scanlab
docker run -d --name dvwa --network scanlab vulnerables/web-dvwa
```

> 🍏 On Apple Silicon (M1/M2/M3…) Docker may warn that the DVWA image is
> `linux/amd64`. That's fine: it runs under emulation.

## Step 2 — Start OpenVAS

```bash
docker volume create openvas

docker run -d --name openvas --network scanlab \
  --publish 8080:9392 \
  -e PASSWORD="ChangeMe123!" \
  --volume openvas:/data \
  immauss/openvas
```

- `--publish 8080:9392`: the web interface will be on **http://localhost:8080**
- `-e PASSWORD=...`: password for the user `admin` (without it, the password is `admin`)
- `--volume openvas:/data`: keeps the feed and your results when you restart the container

## Step 3 — ⏳ Wait about 20 minutes

> ⚠️ **After starting the container, wait ± 20 minutes before you start scanning.**
> On first start the container downloads and imports the Greenbone vulnerability
> feed (100 000+ tests). The web page may open sooner, but until the import has
> finished you'll see empty lists, missing *Scan Configs*, or scans stuck at 0 %.
> On a slow laptop or network this can take longer.

Follow the progress with:

```bash
docker logs -f openvas
```

(Press `Ctrl+C` to stop following; the container keeps running.) The container is
ready when the log says it is **ready to use** and stops scrolling.

Use the wait well: read Steps 4–6 and the report-reading tips below.

## Step 4 — Log in and check the feed

1. Browse to **http://localhost:8080**.
2. Log in as **admin** with the password from Step 2.
3. Go to **Administration → Feed Status**. Every row should say **Current**. If a
   row says *Update in progress…*, wait some more.
4. Go to **Configuration → Scan Configs** and check that **Full and fast** is listed.

## Step 5 — Find the IP address of the target

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dvwa
```

This prints something like `172.18.0.2`. That is your target.

## Step 6 — Create a target and run a scan

1. **Configuration → Targets → ✚ (New Target)**
   - Name: `DVWA`
   - Hosts: *Manual* → the IP from Step 5
   - Alive Test: **Consider Alive**
   - Save.
2. **Scans → Tasks → ✚ (New Task)**
   - Name: `Scan DVWA`
   - Scan Targets: `DVWA`
   - Scan Config: **Full and fast**
   - Save.
3. Click **▶ (Start)** next to the task. The scan takes about **10–20 minutes**.
   Refresh the page to follow the progress.

## Step 7 — Read the report

When the status says **Done**, click the date in the *Last Report* column, then
open the **Results** tab. For each finding you get:

| Field | Meaning |
|---|---|
| **Severity / CVSS** | How bad it is, from 0.0 to 10.0 (High ≥ 7.0) |
| **QoD** | How sure the scanner is (≥ 70 % is shown by default) |
| **Summary / Insight** | What's wrong |
| **Solution** | How to fix it |
| **References** | CVE numbers and links |

Export the report: the **⬇ (Download)** icon at the top of the report → **PDF** or **TXT**.

---

## Deliverables

One ZIP, `lastname_firstname_openvas_docker.zip`, containing:

1. A screenshot of **Feed Status** with every row **Current**.
2. The exported report (`report_dvwa.pdf` or `report_dvwa.txt`).
3. `findings.md` (max. half a page):
   - how many High / Medium / Low findings the scan found
   - the **top 3** findings: name, CVSS, QoD and the proposed solution, in your own words
   - one sentence: why a scanner can report a vulnerability that isn't really there
     (a *false positive*)

## Clean up

```bash
docker stop openvas dvwa
docker rm openvas dvwa
docker network rm scanlab
docker volume rm openvas      # only if you never want to reuse the feed (saves the 20-min wait next time)
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `port is already allocated` | Port 8080 is in use: change it to `--publish 8081:9392` and browse to `localhost:8081` |
| Page doesn't load | Wait: the container is still starting. Check `docker logs -f openvas` |
| Forgot the password | `docker rm -f openvas` and run Step 2 again (your volume keeps the feed) |
| Scan stuck at 0 % / no *Full and fast* | The feed isn't loaded yet: wait and check *Feed Status* |
| Container stops or restarts | Give Docker more RAM (4 GB minimum) |
| Scan finds 0 results | Did you set **Alive Test = Consider Alive** and use the IP from Step 5? |

> ⚠️ **Legal:** Only scan the DVWA container from this lab, or hosts you have
> written permission to scan. Unauthorized scanning can be a criminal offence
> (in Belgium: Art. 550bis Sw.).
