# Lab 2 — Steganography: Instructor Solutions & Variations

## Provided files (original)
- `stego_text_png.png` — contains a PNG tEXt chunk with key `flag`.
- `stego_appended.jpg` — JPEG image with a ZIP appended containing `secret.txt`.
- `stego_lsb.png` — LSB-steganography image (new variation).

## Instructor solution (step-by-step)
### PNG text chunk
1. Use `exiftool`:
```bash
exiftool stego_text_png.png
```
**Expected snippet:**
```
Flag                            : FLAG{png_text_chunk_hidden_message}
Comment                         : This is a normal image.
```
Alternative quick method:
```bash
strings stego_text_png.png | grep -i FLAG
```
You should see the `FLAG{png_text_chunk_hidden_message}` string.

### Appended ZIP in JPEG
1. Try `strings` first:
```bash
strings stego_appended.jpg | grep -i FLAG -n
```
You should see the `FLAG{zip_appended_stego}` text in the output.

2. Use `binwalk` to detect embedded ZIP:
```bash
binwalk stego_appended.jpg
```
Run extraction:
```bash
binwalk -e stego_appended.jpg
# Look in the extracted folder for secret.txt
cat _stego_appended.jpg.extracted/secret.txt
# Expected: Hidden flag inside zip: FLAG{zip_appended_stego}
```

### LSB image (new variation)
To extract an LSB hidden message from `stego_lsb.png` using a small Python snippet:
```python
from PIL import Image
img = Image.open('stego_lsb.png')
pixels = img.load()
w,h = img.size
bits = []
for y in range(h):
    for x in range(w):
        r,g,b = pixels[x,y]
        bits.append(b & 1)
# Convert bits to bytes until null terminator
byts = []
for i in range(0, len(bits), 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | bits[i+j]
    if byte == 0:
        break
    byts.append(byte)
print(bytes(byts).decode('utf-8'))
```
**Expected output:** `LSB_FLAG{hidden_in_lsb}`

## Variations (increasing difficulty)
1. **Encrypted ZIP** — append an AES-encrypted zip (password required) so students must discover the zip and then perform a dictionary or brute-force attack on the zip password with `fcrackzip` or `john` (via zip2john).
2. **Obfuscated metadata** — place the flag across multiple PNG text chunks or rename chunk keys to non-obvious names to teach thorough metadata inspection.
3. **LSB with noise** — scatter bits across channels and pixel locations (use a seed) so students must find the embedding pattern or the PRNG seed.
4. **Use stegsolve/stegseek/OpenStego** — provide students tools to try different stego techniques (color plane, palette, LSB).
5. **Network stego** — hide data inside a PCAP file payload and teach students to look for anomalies and file signatures inside capture data.

## Additional instructor artifacts included
- `stego_lsb.png` — an image with message embedded in blue-channel LSBs.
- `stego_text_png.png` and `stego_appended.jpg` (from original lab).

---
Instructor tip: For stronger assessment, give each student a unique image with the flag encoded using a different PRNG seed or different embedding technique and require a short lab report describing the detection method and commands used.
