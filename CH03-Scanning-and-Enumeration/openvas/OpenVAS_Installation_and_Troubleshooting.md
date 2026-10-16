# OpenVAS (Greenbone / GVM) — Installation and Troubleshooting on Kali Linux

> **Do this before the lab.** `gvm-setup` downloads and imports the Greenbone
> Community Feed (100 000+ vulnerability tests, CVE/CERT data). The first run takes
> **30–90 minutes** and the scanner is not usable until the import has finished.

Tested against the Kali `gvm` package **25.04**. If your output differs, run
`sudo gvm-check-setup` — it always tells you the next thing to fix.

---

## 0. Requirements

| | Minimum | Recommended |
|---|---|---|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8 GB |
| Free disk | 20 GB | 40 GB+ |

Give the Kali VM these resources **before** you start. With 2 GB RAM `ospd-openvas`
gets killed while loading the feed and scans hang at 0 %.

---

## 1. Fully update Kali first

Most installation failures come from a half-updated Kali (an old PostgreSQL next to
a new `gvmd`). Update everything, then reboot:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

## 2. Install GVM

```bash
sudo apt update
sudo apt install -y gvm
```

## 3. Check PostgreSQL *before* running setup

`gvmd` is built for **one specific** PostgreSQL major version, and that version
must be the cluster listening on port **5432**.

```bash
cat /usr/share/gvmd/postgresql-version   # version gvmd needs, e.g. 17
pg_lsclusters                            # clusters that exist, and their ports
```

**Good** — the required version is `online` on port 5432:

```
Ver Cluster Port Status Owner    Data directory
17  main    5432 online postgres /var/lib/postgresql/17/main
```

**Problem** — an older cluster holds 5432 and the required one is on 5433:

```
Ver Cluster Port Status Owner    Data directory
16  main    5432 online postgres /var/lib/postgresql/16/main
17  main    5433 online postgres /var/lib/postgresql/17/main
```

Fix (replace `16` / `17` with *your* old / required versions). On a lab VM where
PostgreSQL is used only by GVM this is safe:

```bash
sudo pg_dropcluster --stop 17 main     # remove the new, EMPTY cluster on 5433
sudo pg_upgradecluster 16 main         # migrate the old cluster to 17, on port 5432
sudo pg_dropcluster 16 main            # remove the old cluster
pg_lsclusters                          # 17 must now be online on 5432
```

If there is **no** cluster of the required version at all:
`sudo apt install -y postgresql-17` (your version), then repeat the check.

## 4. Run setup

```bash
sudo gvm-setup
```

At the end it prints the **admin password** — copy it somewhere immediately.

```
[*] User created with password 'b3c1d2e4-....'.
```

Lost it? Set a new one:

```bash
sudo runuser -u _gvm -- gvmd --user=admin --new-password='Choose-A-Password'
```

## 5. Verify

```bash
sudo gvm-check-setup
```

The last line must read **`It seems like your GVM-25.x installation is OK.`**
If not, it prints a `FIX:` line — run that, then check again. See §8 for the
common ones.

## 6. Start / stop

```bash
sudo gvm-start      # opens https://127.0.0.1:9392
sudo gvm-stop
```

Service status, one line each:

```bash
systemctl is-active gvmd ospd-openvas gsad notus-scanner postgresql redis-server@openvas
```

## 7. Wait for the feed to be *loaded* (not just downloaded)

`gvm-setup` downloads the feed, but `gvmd` and `ospd-openvas` then need extra time
to **import** it. Until that is finished:

- the scan config list is empty / **"Full and fast" is missing**,
- new tasks fail with *"Failed to find config"*,
- scans stay at 0 % or end immediately with no results.

Check progress in the web UI under **Administration → Feed Status**: every row must
show **Current**, not *Update in progress*. Or follow the logs:

```bash
sudo tail -f /var/log/gvm/gvmd.log /var/log/gvm/ospd-openvas.log
# wait for lines like "Updating VTs in database ... done" and "Finished loading VTs"
```

Just wait — do **not** restart services or re-run `gvm-setup` while it is loading.

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `gvm-setup`: *The default PostgreSQL version (16) is not 17 that is required by libgvmd* | Old cluster on port 5432 | §3 |
| `gvm-setup`: *No PostgreSQL version uses the port 5432/TCP* | Required cluster missing or on 5433 | §3 |
| `gvm-check-setup`: *No CA certificate file found* | Certificates not generated | `sudo runuser -u _gvm -- gvm-manage-certs -a -f` |
| "Full and fast" missing, *Failed to find config* | Feed not imported yet | §7 — wait |
| Feed status *Too old* / sync never finished | Download interrupted | `sudo greenbone-feed-sync` (all types), then §7 |
| Scan stuck at 0 % / *Interrupted* | `ospd-openvas` still loading VTs, or out of RAM | §7; give the VM ≥ 4 GB; `sudo journalctl -u ospd-openvas -n 50` |
| `https://127.0.0.1:9392` doesn't load | `gsad` not running | `sudo systemctl restart gsad`, then `sudo ss -tlnp \| grep 9392` |
| Login refused | Wrong / lost password | reset command in §4 |
| PDF report empty or PDF format missing | LaTeX not installed | `sudo apt install -y texlive-latex-extra texlive-fonts-recommended`, `sudo systemctl restart gvmd` |
| `gvm-cli`: *This tool must not be run as root user* | `gvm-cli` refuses root by design | Run as `_gvm`: `sudo -u _gvm gvm-cli …` (see CLI guide) |
| `gvm-cli`: *Permission denied* on `/run/gvmd/gvmd.sock` | Your user can't open the socket | Same — run as `_gvm` |

> ⚠️ Old guides use `greenbone-feed-sync --type GVMD_DATA` / `SCAP` / `CERT`
> (uppercase). That syntax belongs to the retired shell scripts and fails on current
> Kali. The current tool uses lowercase types (`--type gvmd-data`, `--type scap`, …)
> or, simplest, no `--type` at all to sync everything.

### Using the web UI from your host machine

`gsad` listens on `127.0.0.1` only. Rather than reconfiguring it, tunnel the port
over SSH from your laptop (Kali needs `sudo systemctl start ssh`):

```bash
ssh -L 9392:127.0.0.1:9392 kali@<kali-vm-ip>
# then browse on your laptop to https://127.0.0.1:9392
```

### Last resort: start clean

If the installation is badly broken, a clean reinstall is usually faster than
repairing it:

```bash
sudo gvm-stop
sudo apt purge -y gvm gvmd openvas-scanner ospd-openvas greenbone-security-assistant
sudo apt autoremove -y
sudo rm -rf /var/lib/gvm /var/lib/openvas /var/lib/notus /var/log/gvm
sudo -u postgres dropdb --if-exists gvmd
```

Then restart at §1.

### Plan B: Greenbone containers

If the Kali packages still won't cooperate, the official Greenbone Community
Containers run the same scanner in Docker. Follow
<https://greenbone.github.io/docs/latest/22.4/container/index.html>. The web UI is
then at `https://127.0.0.1` and the initial login is `admin` / `admin` — change it
immediately with the `gvmd --new-password` command from that page. Everything in
the GUI guide works the same way.
