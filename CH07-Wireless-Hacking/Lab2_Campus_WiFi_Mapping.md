# Lab 2 — Mapping Wi-Fi From the Air: Campus and Neighbourhood Survey

**Book:** CEH All-in-One, Chapter 7 — *Wireless Network Hacking* · **Duration:** 60 min
**Team:** 3 students, ideally one **Android** phone (or a Windows laptop, see Part 0) · **Hand in:** this worksheet, filled in

Every Wi-Fi access point announces itself several times per second with a **beacon**:
its name (SSID), its hardware address (BSSID), its channel and the security it uses.
Anyone nearby can receive these beacons without connecting to anything. Attackers start
here (the *Wi-Fi discovery* and *footprinting* phases from the book).
Today, you do the same thing as a defender would. You **only listen**.

**Team members:** ______________________ · ______________________ · ______________________

---

## ⚠ Rules: read before you start, then sign

> **You only listen. You never connect, log in or try anything.**
>
> 1. **Connect only to the school networks** you already use (VIVES-Guest, eduroam,
>    Campusroam) with your own account. Never connect to any other network,
>    **not even an open one without a password**. Connecting to a network you have
>    no permission to use is unauthorised access to a computer system
>    (Belgian Criminal Code, **art. 550bis**): a criminal offence, even "just to check".
> 2. **Do not try passwords, do not use WPS buttons or PINs, do not send anything** to
>    a network. Do not install any other tools than the ones on this sheet.
> 3. **Do not capture traffic.** Intercepting other people's communications is a
>    criminal offence (**art. 314bis**). Beacons are fine; data is not.
> 4. **Respect privacy.** SSIDs such as "Familie Peeters" or "Lisa's iPhone" are personal
>    data (GDPR). **Never write down a house number or a network name that contains a person's
>    name.** Write street names and counts only. Don't take photos of houses.
> 5. **Do not upload** anything to WiGLE or any other website. **Delete** your log at
>    the end of the lab (see Part 4).
> 6. **Outside the campus:** stay on the public pavement, stay together as a team, mind
>    the traffic, and don't stop in front of anyone's house or window.
>    If a resident asks what you are doing, explain politely; it is a school assignment.
>    Be back on time.
>
> Breaking these rules means you fail the lab, and it can mean more than that.

We have read and will follow these rules (all three sign):

______________________ · ______________________ · ______________________

---

## Part 0 — Set up your phone (5 min)

On the Android phone(s) of your team:

1. Install **WiGLE WiFi Wardriving** from the Play Store (free). Backup app:
   **WiFiAnalyzer** (open source). iPhones cannot do this, so share an Android phone.
2. **Do not sign in** to WiGLE and **never press Upload**.
3. Allow location access (Android needs it for Wi-Fi scanning) and turn **Wi-Fi on**.
4. Turn off **Wi-Fi scan throttling**, or Android will only scan 4 times every 2 minutes
   and you'll miss most access points:
   - Settings › About phone › tap **Build number** 7 times (Samsung: About phone ›
     Software information) to enable *Developer options*.
   - Settings › System › Developer options › **Wi-Fi scan throttling** → **off**.
5. Start scanning in WiGLE (the play/scan button). Networks appear in the list.

> **No Android phone in your team? Use a Windows laptop.** Open a terminal and run
> `netsh wlan show networks mode=bssid`. For every network you get the SSID, the
> **Authentication** (Open / WPA2-Personal / WPA2-Enterprise / WPA3-Personal …), and per
> BSSID the signal (%), band and channel. Run it again at each stop during the walk.
> Signal is shown in % instead of dBm: above 70 % is good, below 40 % is weak.
> **iPhone only:** the *AirPort Utility* app has a Wi-Fi scanner (enable it in Settings ›
> AirPort Utility) that shows BSSIDs, channels and signal, but **not** the security
> type, so it only helps for Part 1.2–1.4.

### How to read the security of a network

WiGLE shows a "capabilities" string next to each network. Learn this table:

| You see | Meaning | Strength |
|---|---|---|
| `[ESS]` and nothing else | **Open**: no encryption at all | ✗ none |
| `[WEP]` | WEP: cracked in minutes (see Lab 1) | ✗ broken |
| `[WPA-PSK-TKIP]` | Original WPA with TKIP | ✗ weak, outdated |
| `[WPA2-PSK-CCMP]` | WPA2-Personal: one shared password (typical at home) | ✓ OK if the password is strong |
| `[RSN-SAE-CCMP]` or `SAE` | **WPA3-Personal** | ✓✓ good |
| `[WPA2-EAP-CCMP]` or `EAP` | **Enterprise** (802.1X): a personal login per user | ✓✓ good, if set up correctly |
| `[WPS]` added to any of these | WPS is enabled: an extra, often weak, way in | ⚠ risk |

---

## Part 1 — The campus network (20 min)

The campus has only **3 SSIDs** but **hundreds of access points**. Your job: find out how
this network is built and protected, using beacons only.

### 1.1 Security per SSID

Stand in one spot on campus and look up each school SSID.

| SSID | Capabilities string (copy it) | Open / Personal (PSK) / Enterprise (EAP)? | WPA2 or WPA3? | WPS? |
|---|---|---|---|---|
| VIVES-Guest | | | | |
| eduroam | | | | |
| Campusroam | | | | |

**Q1.** Are all three SSIDs protected in the same way? With **Enterprise** (802.1X), the
access point doesn't check your password itself: it passes your login to a central
**RADIUS** server. Why is that better for a school than one shared Wi-Fi password? Why does
a school still need a *separate* SSID for guests?

<div class="answer"></div>

**Q2.** With a shared password (or no password), everyone on the network can decrypt each
other's Wi-Fi traffic. With Enterprise, every user gets their **own encryption key**. Explain
why, and what that means for traffic that is *not* protected by HTTPS.

<div class="answer"></div>

### 1.2 How many access points can you see?

Every access point broadcasts each SSID under its **own BSSID** (MAC address), and those
BSSIDs are usually almost identical, e.g. `a8:46:9d:12:34:50`, `…:51`, `…:52`.
**BSSIDs that differ only in the last character are almost certainly one physical
access point.**

From one spot (your classroom), fill in:

| | Count |
|---|---|
| Number of BSSIDs you see for eduroam | |
| Number of BSSIDs for all 3 SSIDs together | |
| Your estimate of the number of **physical access points** you hear from here | |

**Q3.** The first 3 bytes of a MAC address (the OUI) identify the manufacturer. Look one
BSSID up (WiGLE often shows the vendor; otherwise search "MAC vendor lookup").
Which vendor makes the campus access points? ___________________________

### 1.3 Bands and channels

| Band | Number of campus BSSIDs you see | Channels used |
|---|---|---|
| 2.4 GHz (channels 1–13) | | |
| 5 GHz (channels 36–165) | | |
| 6 GHz (if any) | | |

**Q4.** On 2.4 GHz only channels **1, 6 and 11** don't overlap. Does the campus stick to
those? Why does it matter that neighbouring access points use different channels?

<div class="answer short"></div>

### 1.4 Coverage: where is the signal good or bad?

Signal strength is in dBm: closer to 0 is stronger.
**−30 to −60** excellent · **−60 to −70** good · **−70 to −80** weak · **below −80** unusable.

Walk to 5 places and note the **strongest** eduroam signal you see there.

| Location (e.g. classroom, corridor, stairwell, cafeteria, entrance) | Strongest signal (dBm) | Good / weak? |
|---|---|---|
| | | |
| | | |
| | | |
| | | |
| | | |

**Q5.** Where would you add an access point? Why is a weak signal not only a comfort
problem, but also a security problem? (Hint: what does a phone do when a stronger
access point with the same name shows up?)

<div class="answer"></div>

### 1.5 Check your own eduroam settings

Anyone can create an access point called **"eduroam"** (a *rogue access point* or
*evil twin*). If your phone does not check the server's certificate, it may send your
VIVES login to that fake access point.

On **your own** phone: Settings › Wi-Fi › eduroam › (edit / advanced) and look at the
**CA certificate** and **domain** fields.

| Team member | CA certificate setting | Domain filled in? | Safe? (yes/no) |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

**"Don't validate"** or an empty domain = **not safe**. Fix it with the official
**geteduroam** app, or ask the ICT helpdesk.

---

## Part 2 — The neighbourhood: hunt for the poorest encryption (20 min)

Walk the route your teacher gives you **around** the campus, past houses and shops, with
WiGLE scanning. Remember the rules: **listen only, write no names or house numbers.**

### 2.1 Tally sheet

Each time you find a **new** (non-school) network, put a stroke in the right row.
Tip: at the end, use WiGLE's list instead of counting live.

| Security | Tally | Total |
|---|---|---|
| Open `[ESS]` | | |
| WEP | | |
| WPA (TKIP) | | |
| WPA2-Personal (PSK) | | |
| WPA3 (SAE) | | |
| Enterprise (EAP) | | |
| **…of all these: with `[WPS]`** | | |
| **…of all these: default name** (e.g. `telenet-…`, `Proximus-Home-…`, `TP-Link_…`) | | |
| **Total networks** | | |

> Note: many "open" networks near houses are **public hotspots** shared by an internet provider
> (e.g. *Telenet Wi-Free*, *Proximus Public Wi-Fi*). They don't count as "an insecure home
> network". Count them separately here: ________

### 2.2 Your weakest find

| | Your answer |
|---|---|
| Weakest security you found (copy the capabilities string) | |
| Street (**no** house number, **no** network name) | |
| Signal strength (dBm) | |

### 2.3 Scoring

| Find | Points |
|---|---|
| Each WEP network | 5 |
| Each WPA-TKIP network | 3 |
| Each network with WPS | 1 |
| Each network with a default ISP/vendor name | 1 |
| Each WPA3 network (the good guys) | 2 |
| Complete Part 1 tables | 10 |
| **Team score** | |

---

## Part 3 — Analysis and debrief (10 min)

**Q6.** What percentage of the neighbourhood networks you found is open + WEP + WPA-TKIP
together? What percentage uses WPA3?

<div class="answer short"></div>

**Q7.** Why is a **default SSID** (e.g. `telenet-1A2B3C`) useful information for an
attacker, even if the password is strong? (Think: router model, known default passwords,
known vulnerabilities, firmware.)

<div class="answer"></div>

**Q8.** A neighbour uses `[WPA2-PSK-CCMP][WPS]`. Give two concrete pieces of advice for
this person.

<div class="answer"></div>

**Q9.** Compare **eduroam** (Enterprise, a personal login) with a **home network**
(one shared password). Give one advantage of each for the network owner.

<div class="answer"></div>

**Q10.** You collected all this without connecting to anything. What can an attacker
learn this way (passive reconnaissance), and what is the one thing a network owner can
do to reveal less?

<div class="answer"></div>

---

## Part 4 — Clean up (before you leave)

- Stop scanning in WiGLE.
- Delete the log: WiGLE › Database › clear / delete the database (or uninstall the app).
- Nothing was uploaded.
- Turn **Wi-Fi scan throttling** back **on** if you want (it saves battery).
- Worksheet handed in.
