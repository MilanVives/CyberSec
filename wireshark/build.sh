#!/bin/bash
# Rebuild the Chapter 1 Wireshark lab: reference capture, PDFs, Toledo ZIP.
# Requires: python3, pandoc, weasyprint, tshark.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Regenerating reference capture"
python3 make_reference_capture.py chapter1_reference.pcap

echo "==> Verifying checksums"
bad=$(tshark -r chapter1_reference.pcap \
  -o ip.check_checksum:TRUE -o tcp.check_checksum:TRUE \
  -o udp.check_checksum:TRUE \
  -Y 'ip.checksum.status=="Bad" || tcp.checksum.status=="Bad" || udp.checksum.status=="Bad" || icmp.checksum.status=="Bad"' \
  2>/dev/null | wc -l | tr -d ' ')
[ "$bad" = "0" ] || { echo "FAIL: $bad frames with bad checksums"; exit 1; }

echo "==> Verifying all three required protocols are present"
for proto in icmp dns http; do
  n=$(tshark -r chapter1_reference.pcap -Y "$proto" 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" -gt 0 ] || { echo "FAIL: no $proto packets"; exit 1; }
  printf "    %-5s %2s packets\n" "$proto" "$n"
done

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/lab.css" <<'CSSEOF'
@page { size: A4; margin: 18mm 16mm 20mm 16mm;
  @bottom-center { content: counter(page) " / " counter(pages);
    font-family: "Helvetica Neue", sans-serif; font-size: 8pt; color: #666; } }
body { font-family: "Helvetica Neue", Helvetica, "Apple Color Emoji", sans-serif;
  font-size: 10pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 19pt; color: #0b3d66; border-bottom: 2.5px solid #0b3d66;
  padding-bottom: 5px; margin-top: 0; }
h2 { font-size: 14pt; color: #0b3d66; margin-top: 20px;
  border-bottom: 1px solid #c8d6e0; padding-bottom: 3px; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #14507f; margin-top: 14px; page-break-after: avoid; }
h4 { font-size: 10.5pt; color: #333; page-break-after: avoid; }
code { font-family: Menlo, monospace; font-size: 8.5pt;
  background: #f2f4f6; padding: 1px 3px; border-radius: 2px; }
pre { font-family: Menlo, monospace; font-size: 8pt; background: #f7f8fa;
  border: 1px solid #dde3e8; border-left: 3px solid #0b3d66; border-radius: 3px;
  padding: 7px 9px; line-height: 1.35; white-space: pre-wrap;
  overflow-wrap: break-word; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8pt; }
table { border-collapse: collapse; width: 100%; margin: 9px 0; font-size: 8.5pt;
  page-break-inside: avoid; }
th { background: #0b3d66; color: #fff; text-align: left; padding: 5px 7px; font-weight: 600; }
td { border: 1px solid #d5dde4; padding: 4px 7px; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fb; }
blockquote { border-left: 3px solid #e8a33d; background: #fdf7ec; margin: 9px 0;
  padding: 7px 11px; page-break-inside: avoid; }
blockquote p { margin: 3px 0; }
a { color: #14507f; text-decoration: none; word-break: break-all; }
hr { border: none; border-top: 1px solid #d5dde4; margin: 16px 0; }
li { margin: 2px 0; }
#TOC { background: #f7f9fb; border: 1px solid #dde3e8; border-radius: 4px;
  padding: 9px 15px; page-break-after: always; }
#TOC ul { list-style: none; padding-left: 14px; margin: 3px 0; }
#TOC > ul { padding-left: 0; }
#TOC a { color: #1a1a1a; }
CSSEOF

render() {   # render <basename> <title> <subtitle>
  pandoc "$1.md" -f gfm -t html5 -s --toc --toc-depth=2 \
    --metadata title="$2" --metadata subtitle="$3" -o "$tmp/$1.html" 2>/dev/null
  weasyprint -s "$tmp/lab.css" "$tmp/$1.html" "$1.pdf" 2>/dev/null
  echo "    $1.pdf"
}

echo "==> Rendering PDFs"
render Lab1_Wireshark_Traffic_Analysis \
  "Lab 1 — Packet Capture and Protocol Analysis with Wireshark" \
  "Cybersecurity Architecture (ACS) · Chapter 1"
render Lab1_Instructor_Solution \
  "Lab 1 — Instructor Solution and Marking Guide" \
  "Cybersecurity Architecture (ACS) · Chapter 1 · Not for student distribution"

echo "==> Building Toledo student bundle"
mkdir -p dist
stage="$tmp/Chapter1_Wireshark_Lab"
mkdir -p "$stage"
cp Lab1_Wireshark_Traffic_Analysis.pdf \
   Lab1_Wireshark_Traffic_Analysis.md \
   chapter1_reference.pcap "$stage/"
cat > "$stage/READ_ME_FIRST.txt" <<'TXTEOF'
Cybersecurity Architecture (ACS) - Chapter 1
Lab 1: Packet Capture and Protocol Analysis with Wireshark

CONTENTS
  Lab1_Wireshark_Traffic_Analysis.pdf   The lab assignment - start here
  Lab1_Wireshark_Traffic_Analysis.md    Same content in Markdown
  chapter1_reference.pcap               Fallback capture, if you cannot capture live

DURATION       90 minutes
SUBMIT         lastname_firstname_chapter1.zip  (see "Deliverables" in the PDF)

BEFORE YOU START
  Capture only on your own machine, on traffic you generate yourself.
  Do not capture on the school network or any shared/public Wi-Fi.
  Intercepting other people's communications without consent is a criminal
  offence in Belgium (Art. 314bis Sw.) and under the EU ePrivacy Directive.

  When the lab asks you to submit a login over plain HTTP, use the dummy
  password given in the instructions. Never use a real password.

THE REFERENCE CAPTURE
  chapter1_reference.pcap is a synthetic file built for this lab - no real
  person's traffic is in it. Every display filter in the assignment works on
  it unchanged. If you use it instead of capturing live, say so in your
  report; it costs you only the "Capture setup" part of the grade.

  Open it with:  wireshark chapter1_reference.pcap

Milan Dima - milan.dima@vives.be - CC BY 4.0
TXTEOF
rm -f dist/Chapter1_Wireshark_Lab_Toledo.zip
( cd "$tmp" && zip -qr "Chapter1_Wireshark_Lab_Toledo.zip" "Chapter1_Wireshark_Lab" -x '.*' '__MACOSX/*' )
mv "$tmp/Chapter1_Wireshark_Lab_Toledo.zip" dist/

echo "==> Done"
ls -la dist/Chapter1_Wireshark_Lab_Toledo.zip
