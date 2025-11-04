# Lab 2 — Steganography (PNG tEXt chunk + appended ZIP)

**Objective:** Discover hidden messages in images using basic stego techniques and command-line tools.  
**Prerequisites:** Kali Linux VM with `exiftool`, `strings`, and `binwalk` (install with `apt install exiftool binwalk`).

## Files provided
- `stego_text_png.png` — PNG image with a `tEXt` chunk containing a hidden flag.
- `stego_appended.jpg` — JPEG image with an appended ZIP file containing `secret.txt`.

## Tasks
1. Inspect PNG metadata for hidden text:
```bash
exiftool stego_text_png.png
# or
strings stego_text_png.png | less
```
Look for a tag or text entry named `flag` or any suspicious textual content.

2. Extract text chunks using `pngcheck` (optional):
```bash
pngcheck -v stego_text_png.png
```

3. For the appended-JPEG method, try `strings` first:
```bash
strings stego_appended.jpg | grep -i FLAG -n
```
You should see the `FLAG{...}` entry.

4. Use `binwalk` to detect embedded archives:
```bash
binwalk stego_appended.jpg
```
You can carve the embedded ZIP out:
```bash
# easiest: let binwalk extract for you
binwalk -e stego_appended.jpg
```

5. Once you extract `secret.txt`, open it:
```bash
cat _stego_appended.jpg.extracted/secret.txt
```
(Exact path depends on `binwalk -e` output.)

## Instructor notes
- Explain difference between embedding in metadata (visible with exiftool) vs. hiding data by appending (requires scanning for embedded file signatures).
- Discuss detection and mitigation strategies.

## Hints for students
- `exiftool` shows PNG text chunks.
- Appending data to images doesn't break rendering in most viewers but can be detected by tools that look for file signatures.
