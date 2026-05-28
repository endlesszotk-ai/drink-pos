"""
Pure-Python sprite sheet slicer (no external dependencies).
Usage: python tools/slice_sprites.py
"""
import struct
import zlib
from pathlib import Path

# ── Pure-Python PNG decoder ───────────────────────────────────────────────────

def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def read_png_rgba(path: str):
    """Return (width, height, pixels) where pixels[y][x] = (R,G,B,A)."""
    data = Path(path).read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', "Not a PNG"

    pos = 8
    w = h = bit_depth = color_type = 0
    idat = []
    palette = []

    while pos < len(data):
        length = struct.unpack('>I', data[pos:pos+4])[0]
        ctype  = data[pos+4:pos+8]
        cdata  = data[pos+8:pos+8+length]
        pos   += 12 + length

        if ctype == b'IHDR':
            w, h = struct.unpack('>II', cdata[:8])
            bit_depth, color_type = cdata[8], cdata[9]
        elif ctype == b'PLTE':
            palette = [(cdata[i*3], cdata[i*3+1], cdata[i*3+2]) for i in range(len(cdata)//3)]
        elif ctype == b'tRNS':
            # add alpha to palette
            for i, a in enumerate(cdata):
                if i < len(palette):
                    palette[i] = (*palette[i], a)
        elif ctype == b'IDAT':
            idat.append(cdata)
        elif ctype == b'IEND':
            break

    # Determine channels & bytes per pixel
    ch_map = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
    channels = ch_map[color_type]
    bpp = channels * (bit_depth // 8)
    stride = w * bpp

    raw = zlib.decompress(b''.join(idat))

    # Defilter scanlines
    rows = []
    prev = bytearray(stride)
    for y in range(h):
        off = y * (stride + 1)
        filt = raw[off]
        row  = bytearray(raw[off+1 : off+1+stride])

        if filt == 1:
            for i in range(bpp, len(row)):
                row[i] = (row[i] + row[i-bpp]) & 0xFF
        elif filt == 2:
            for i in range(len(row)):
                row[i] = (row[i] + prev[i]) & 0xFF
        elif filt == 3:
            for i in range(len(row)):
                a = row[i-bpp] if i >= bpp else 0
                row[i] = (row[i] + (a + prev[i]) // 2) & 0xFF
        elif filt == 4:
            for i in range(len(row)):
                a = row[i-bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i-bpp] if i >= bpp else 0
                row[i] = (row[i] + _paeth(a, b, c)) & 0xFF

        prev = row

        # Convert to RGBA tuples
        line = []
        for x in range(w):
            b0 = x * bpp
            if color_type == 6:
                if bit_depth == 16:
                    r = (row[b0]<<8|row[b0+1])>>8
                    g = (row[b0+2]<<8|row[b0+3])>>8
                    bv= (row[b0+4]<<8|row[b0+5])>>8
                    a = (row[b0+6]<<8|row[b0+7])>>8
                else:
                    r,g,bv,a = row[b0],row[b0+1],row[b0+2],row[b0+3]
            elif color_type == 2:
                r,g,bv = row[b0],row[b0+1],row[b0+2]; a=255
            elif color_type == 0:
                g = row[b0]; r,bv,a = g,g,255
            elif color_type == 3:
                idx = row[b0]
                entry = palette[idx] if idx < len(palette) else (0,0,0,255)
                r,g,bv = entry[0],entry[1],entry[2]
                a = entry[3] if len(entry)>3 else 255
            else:
                r=g=bv=row[b0]; a=255
            line.append((r, g, bv, a))
        rows.append(line)

    return w, h, rows


def write_png_rgba(path: str, pixels, width: int, height: int):
    """Write RGBA pixel list-of-lists to PNG."""
    def chunk(t, d):
        crc = zlib.crc32(t + d) & 0xFFFFFFFF
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', crc)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    raw = bytearray()
    for row in pixels:
        raw.append(0)  # filter None
        for r, g, b, a in row:
            raw.extend((r, g, b, a))

    out  = b'\x89PNG\r\n\x1a\n'
    out += chunk(b'IHDR', ihdr)
    out += chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    out += chunk(b'IEND', b'')
    Path(path).write_bytes(out)


# ── Sprite detection ──────────────────────────────────────────────────────────

def find_sprite_boxes(pixels, w, h, alpha_thresh=12):
    """
    Find bounding boxes of all distinct sprites.
    Auto-detects transparent vs. solid-background sheets.
    Returns list of (x1, y1, x2, y2) sorted top-left → bottom-right.
    """
    # Sample corners: if real alpha exists, use it; otherwise use color distance from bg
    corner_alphas = [pixels[0][0][3], pixels[0][w-1][3],
                     pixels[h-1][0][3], pixels[h-1][w-1][3]]
    use_alpha = any(a < 200 for a in corner_alphas)

    if use_alpha:
        occ = [[pixels[y][x][3] > alpha_thresh for x in range(w)] for y in range(h)]
    else:
        # Solid background: sample corners/edges for bg colour
        edge = ([pixels[0][x] for x in range(0, w, max(1, w//20))] +
                [pixels[h-1][x] for x in range(0, w, max(1, w//20))] +
                [pixels[y][0] for y in range(0, h, max(1, h//20))] +
                [pixels[y][w-1] for y in range(0, h, max(1, h//20))])
        bg_r = sum(p[0] for p in edge) // len(edge)
        bg_g = sum(p[1] for p in edge) // len(edge)
        bg_b = sum(p[2] for p in edge) // len(edge)
        THRESH = 25  # distance from bg colour → foreground

        def is_fg(r, g, b):
            dist = ((r-bg_r)**2 + (g-bg_g)**2 + (b-bg_b)**2) ** 0.5
            return dist > THRESH

        occ = [[is_fg(*pixels[y][x][:3]) for x in range(w)] for y in range(h)]

    # --- Step 1: find all non-empty horizontal bands ---
    # Project onto Y axis: which rows have content?
    row_has = [any(occ[y]) for y in range(h)]
    # Group into bands separated by empty rows
    bands = []  # list of (y_start, y_end)
    in_band = False
    for y, has in enumerate(row_has):
        if has and not in_band:
            band_start = y; in_band = True
        elif not has and in_band:
            bands.append((band_start, y - 1)); in_band = False
    if in_band:
        bands.append((band_start, h - 1))

    # --- Step 2: within each band, find column groups ---
    boxes = []
    for y1, y2 in bands:
        col_has = [any(occ[y][x] for y in range(y1, y2+1)) for x in range(w)]
        in_sprite = False
        for x, has in enumerate(col_has):
            if has and not in_sprite:
                sx = x; in_sprite = True
            elif not has and in_sprite:
                # Compute tight y bounds for this column slice
                ys = [y for y in range(y1, y2+1) if any(occ[y][xx] for xx in range(sx, x))]
                if ys:
                    boxes.append((sx, min(ys), x-1, max(ys)))
                in_sprite = False
        if in_sprite:
            ys = [y for y in range(y1, y2+1) if any(occ[y][xx] for xx in range(sx, w))]
            if ys:
                boxes.append((sx, min(ys), w-1, max(ys)))

    return boxes


# ── Pose name mapping ─────────────────────────────────────────────────────────
# Sprite sheet rows (visual inspection):
#   Row 1 (y≈60–250):  5 walking / upright poses
#   Row 2 (y≈276–485): 5 sitting poses
#   Row 3 (y≈506–714): 3 crouching poses
#   Row 4 (y≈738–879): 5 lying-down poses
#   Row 5 (y≈916–1068): 5 sleeping poses

MIN_W, MIN_H = 40, 40   # ignore noise pixels smaller than this

POSE_NAMES = [
    # Row 1 – walking / upright (5)
    "walk",
    "walk2",
    "walk3",
    "stand",
    "idle_front",
    # Row 2 – sitting (5)
    "idle_sleepy",
    "sit_yawn",
    "peek",
    "sit_alert",
    "sit_side",
    # Row 3 – crouching (3)
    "crouch_yawn",
    "curl_sleep",
    "crouch",
    # Row 4 – lying down (5)
    "sleep_side",
    "sleep_stretch",
    "sleep_long_left",
    "sleep_low_left",
    "sleep_low_right",
    # Row 5 – fully sleeping / rolling (5)
    "surprised",
    "sleep_flat",
    "sleep_roll",
    "sleep_back",
    "sleep_curl2",
]


def main():
    ROOT = Path(__file__).resolve().parent.parent
    sheet_path = ROOT / "assets" / "poopee_sprite_sheet_new.png"
    out_dir    = ROOT / "assets" / "sprites"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading {sheet_path} …")
    w, h, pixels = read_png_rgba(str(sheet_path))
    print(f"  Size: {w}×{h}")

    print("Finding sprites …")
    all_boxes = find_sprite_boxes(pixels, w, h)
    # Filter out noise (tiny boxes)
    boxes = [(x1,y1,x2,y2) for x1,y1,x2,y2 in all_boxes
             if (x2-x1+1) >= MIN_W and (y2-y1+1) >= MIN_H]
    print(f"  Found {len(all_boxes)} regions → {len(boxes)} real sprites after filtering")
    for i, (x1,y1,x2,y2) in enumerate(boxes):
        print(f"  [{i:02d}] ({x1},{y1}) → ({x2},{y2})  size {x2-x1+1}×{y2-y1+1}")

    PAD = 4
    saved = []
    for i, (x1, y1, x2, y2) in enumerate(boxes):
        name = POSE_NAMES[i] if i < len(POSE_NAMES) else f"extra_{i:02d}"

        bx1 = max(0, x1 - PAD)
        by1 = max(0, y1 - PAD)
        bx2 = min(w - 1, x2 + PAD)
        by2 = min(h - 1, y2 + PAD)
        sw, sh = bx2 - bx1 + 1, by2 - by1 + 1

        crop = [pixels[y][bx1:bx2+1] for y in range(by1, by2+1)]
        out_path = out_dir / f"{name}.png"
        write_png_rgba(str(out_path), crop, sw, sh)
        saved.append((name, sw, sh))
        print(f"  Saved {out_path.name}  ({sw}×{sh})")

    print(f"\nDone — saved {len(saved)} sprites to {out_dir}")

    import shutil
    shutil.copy(str(sheet_path), str(ROOT / "assets" / "poopee_sprite_sheet.png"))
    print("Updated poopee_sprite_sheet.png")


if __name__ == "__main__":
    main()
