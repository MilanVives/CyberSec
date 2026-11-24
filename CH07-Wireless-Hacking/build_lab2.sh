#!/bin/bash
# Render the Lab 2 (Campus Wi-Fi Mapping) worksheet to a printable A4 PDF.
# Requires: pandoc and Google Chrome (headless printing).
set -euo pipefail
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

cat > "$tmp/print.css" <<'CSSEOF'
@page { size: A4; margin: 12mm 13mm 12mm 13mm; }
body { font-family: "Helvetica Neue", Helvetica, sans-serif; font-size: 9.5pt;
  line-height: 1.35; color: #111; max-width: none; margin: 0; padding: 0; }
header#title-block-header { display: none; }
h1 { font-size: 17pt; color: #0b3d66; border-bottom: 2.5px solid #0b3d66;
  padding-bottom: 4px; margin: 0 0 8px 0; }
h2 { font-size: 13.5pt; color: #0b3d66; margin-top: 16px;
  border-bottom: 1px solid #9fb6c8; padding-bottom: 2px; break-after: avoid; }
h3 { font-size: 11pt; color: #14507f; margin: 12px 0 4px; break-after: avoid; }
p { margin: 5px 0; }
code { font-family: Menlo, monospace; font-size: 8.5pt; background: #eef1f4;
  padding: 0 3px; border-radius: 2px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 8px; font-size: 9pt;
  break-inside: avoid; table-layout: fixed; }
th { background: #0b3d66; color: #fff; text-align: left; padding: 4px 6px;
  font-weight: 600; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
td { border: 1px solid #8a9aa8; padding: 4px 6px; vertical-align: top; height: 19px; }
blockquote { border: 2px solid #c0392b; background: #fdf0ee; margin: 8px 0;
  padding: 6px 12px; break-inside: avoid; -webkit-print-color-adjust: exact;
  print-color-adjust: exact; }
blockquote p { margin: 4px 0; }
blockquote ~ blockquote { border: 1px solid #e8a33d; background: #fdf7ec; }
blockquote ol { margin: 4px 0; padding-left: 20px; }
hr { border: none; border-top: 1px dashed #9fb6c8; margin: 12px 0; }
h2:last-of-type + ul { list-style: none; padding-left: 4px; }
h2:last-of-type + ul li::before { content: ""; display: inline-block; width: 10px;
  height: 10px; border: 1.5px solid #111; margin-right: 8px; vertical-align: -1px; }
li { margin: 2px 0; }
a { color: #111; text-decoration: none; }
.answer { height: 72px; margin: 4px 0 10px; border: 1px solid #b8c4ce; border-radius: 3px;
  background: repeating-linear-gradient(transparent 0 23px, #d0d8df 23px 24px);
  -webkit-print-color-adjust: exact; print-color-adjust: exact; break-inside: avoid; }
.answer.short { height: 36px; }
CSSEOF

render() {   # render <md-path> <pdf-path> <title>
  pandoc "$1" -f gfm -t html5 -s --metadata title="$3" \
    -c "$tmp/print.css" -o "$tmp/page.html"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$2" "file://$tmp/page.html" 2>/dev/null
  echo "    $2"
}

echo "==> Rendering PDFs"
render Lab2_Campus_WiFi_Mapping.md "$PWD/Lab2_Campus_WiFi_Mapping.pdf" \
  "Lab 2 — Campus Wi-Fi Mapping"

NOTES=../labsolutions/CH07-Wireless-Hacking/Lab2_Teacher_Notes
if [ -f "$NOTES.md" ]; then
  render "$NOTES.md" "$(cd "$(dirname "$NOTES")" && pwd)/$(basename "$NOTES").pdf" \
    "Lab 2 — Teacher Notes"
fi
