# OpenVAS (GVM) — Scanning from the Command Line with `gvm-cli`

`gvm-cli` sends **GMP** (Greenbone Management Protocol) XML commands to `gvmd` —
exactly what the web interface does behind the scenes. Everything you can click in
the GUI, you can script here.

> **Prerequisite:** GVM installed, `sudo gvm-check-setup` reports *installation is
> OK*, and the feed is fully loaded. See
> [OpenVAS_Installation_and_Troubleshooting.md](OpenVAS_Installation_and_Troubleshooting.md).

---

## 1. Set up a `gmp` helper

Three things trip everybody up with `gvm-cli`:

1. it **refuses to run as root** (`sudo gvm-cli` fails on purpose),
2. the socket `/run/gvmd/gvmd.sock` belongs to the `_gvm` user, so your normal
   user gets *Permission denied*,
3. every command must be **authenticated** with a GVM username and password.

So we always run it as `_gvm` and always pass credentials. Wrap that in a function:

```bash
sudo apt install -y gvm-tools                      # provides gvm-cli
read -rsp 'GVM admin password: ' GVM_PASS; echo    # not echoed, not in history

gmp() {
  sudo -u _gvm gvm-cli --gmp-username admin --gmp-password "$GVM_PASS" \
    socket --xml "$1"
}

# list "id  name" for any GMP get_* command
gmp_list() {
  gmp "$1" | python3 -c 'import sys, xml.etree.ElementTree as ET
for e in ET.fromstring(sys.stdin.read()).findall("./*[@id]"):
    if e.get("id"): print(e.get("id"), " ", e.findtext("name"))'
}

gmp '<get_version/>'   # test: should print <get_version_response status="200" ...>
```

> These functions live only in the current terminal. Open a new terminal → paste
> them again.

## 2. Look up the IDs you need

Everything in GMP is referenced by UUID:

```bash
gmp_list '<get_configs/>'        # scan configs
gmp_list '<get_port_lists/>'     # port lists
gmp_list '<get_scanners/>'       # scanners
gmp_list '<get_report_formats/>' # report formats
```

The ones used below are fixed in every Greenbone installation:

| Object | Name | ID |
|---|---|---|
| Scan config | Full and fast | `daba56c8-73ec-11df-a475-002264764cea` |
| Port list | All IANA assigned TCP | `33d0cd82-57c6-11e1-8ed1-406186ea4fc5` |
| Scanner | OpenVAS Default | `08b69003-5fc2-4037-a479-93b440211c73` |
| Report format | TXT | `a3810a62-1f62-11e1-9219-406186ea4fc5` |
| Report format | PDF | `c402cc3e-b531-11e1-9163-406186ea4fc5` |
| Report format | CSV Results | `c1645568-627a-11e3-a660-406186ea4fc5` |
| Report format | XML | `a994b278-1f62-11e1-96ac-406186ea4fc5` |

If `get_configs` returns nothing, the feed is still importing — wait.

## 3. Create a target

```bash
HOST=linux.vives.live

TARGET_ID=$(gmp "<create_target>
    <name>$HOST</name>
    <hosts>$HOST</hosts>
    <port_list id='33d0cd82-57c6-11e1-8ed1-406186ea4fc5'/>
    <alive_tests>Consider Alive</alive_tests>
  </create_target>" | grep -oP ' id="\K[^"]+')
echo "TARGET_ID=$TARGET_ID"
```

- A **port list is mandatory** — without it gvmd rejects the target.
- **`Consider Alive`** skips the ping check. Many internet hosts drop ICMP, and with
  the default alive test OpenVAS would mark them dead and report nothing.

## 4. Create and start a task

```bash
TASK_ID=$(gmp "<create_task>
    <name>Scan-$HOST</name>
    <config id='daba56c8-73ec-11df-a475-002264764cea'/>
    <target id='$TARGET_ID'/>
    <scanner id='08b69003-5fc2-4037-a479-93b440211c73'/>
  </create_task>" | grep -oP ' id="\K[^"]+')
echo "TASK_ID=$TASK_ID"

REPORT_ID=$(gmp "<start_task task_id='$TASK_ID'/>" | grep -oP '<report_id>\K[^<]+')
echo "REPORT_ID=$REPORT_ID"
```

`start_task` returns the ID of the report that this run will fill — keep it.

## 5. Follow progress

```bash
gmp "<get_tasks task_id='$TASK_ID'/>" | grep -oP '<status>\K[^<]+|<progress>\K[^<]+'
```

Prints e.g. `Running` / `42`. Re-run every few minutes until the status is **`Done`**.

All tasks at once:

```bash
gmp_list '<get_tasks/>'
gmp '<get_tasks/>' | grep -oP '<name>Scan-[^<]+|<status>\K[^<]+'
```

## 6. Export the report

Except for XML, gvmd returns the report **base64-encoded inside the XML response**.
This helper decodes it:

```bash
# gmp_report <report-id> <format-id> <output-file>
gmp_report() {
  gmp "<get_reports report_id='$1' format_id='$2' details='1'
         ignore_pagination='1' filter='apply_overrides=0 min_qod=70 rows=-1'/>" |
  python3 -c 'import sys, base64, xml.etree.ElementTree as ET
r = ET.fromstring(sys.stdin.read()).find("report")
data = (r.text or "") + "".join(c.tail or "" for c in r)
sys.stdout.buffer.write(base64.b64decode(data))' > "$3"
  echo "wrote $3"
}

gmp_report "$REPORT_ID" a3810a62-1f62-11e1-9219-406186ea4fc5 "report_$HOST.txt"
gmp_report "$REPORT_ID" c402cc3e-b531-11e1-9163-406186ea4fc5 "report_$HOST.pdf"
gmp_report "$REPORT_ID" c1645568-627a-11e3-a660-406186ea4fc5 "results_$HOST.csv"
```

Raw XML needs no decoding:

```bash
gmp "<get_reports report_id='$REPORT_ID' details='1' ignore_pagination='1'
       filter='rows=-1'/>" > "report_$HOST.xml"
```

An empty PDF means LaTeX is missing — see the troubleshooting table.

## 7. Several hosts in one go

```bash
declare -A TASKS
for HOST in linux.vives.live vault.vives.live; do
  TARGET_ID=$(gmp "<create_target><name>$HOST</name><hosts>$HOST</hosts>
      <port_list id='33d0cd82-57c6-11e1-8ed1-406186ea4fc5'/>
      <alive_tests>Consider Alive</alive_tests></create_target>" | grep -oP ' id="\K[^"]+')
  TASK_ID=$(gmp "<create_task><name>Scan-$HOST</name>
      <config id='daba56c8-73ec-11df-a475-002264764cea'/><target id='$TARGET_ID'/>
      <scanner id='08b69003-5fc2-4037-a479-93b440211c73'/></create_task>" | grep -oP ' id="\K[^"]+')
  TASKS[$HOST]=$(gmp "<start_task task_id='$TASK_ID'/>" | grep -oP '<report_id>\K[^<]+')
  echo "$HOST  task=$TASK_ID  report=${TASKS[$HOST]}"
done

# later, when all are Done:
for HOST in "${!TASKS[@]}"; do
  gmp_report "${TASKS[$HOST]}" a3810a62-1f62-11e1-9219-406186ea4fc5 "report_$HOST.txt"
done
```

## 8. Housekeeping

```bash
gmp "<stop_task task_id='$TASK_ID'/>"
gmp "<delete_task task_id='$TASK_ID' ultimate='1'/>"
gmp "<delete_target target_id='$TARGET_ID' ultimate='1'/>"
```

(Delete the task before the target — a target that is still in use can't be deleted.)

---

## Safety reminder

Only scan hosts you have **explicit, written authorization** to test. Unauthorized
scanning can be a criminal offence (in Belgium: Art. 550bis Sw.).
