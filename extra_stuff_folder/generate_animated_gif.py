from PIL import Image, ImageDraw, ImageFont
import math, os

# ─── Config ───
W, H = 1600, 950
FRAMES = 40
DURATION = 80  # ms per frame

# ─── Fonts ───
def load_fonts():
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/google-noto/NotoSans-Bold.ttf",
    ]
    paths2 = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
        "/usr/share/fonts/google-noto/NotoSans-Regular.ttf",
    ]
    bold = reg = None
    for p in paths:
        if os.path.exists(p):
            bold = p; break
    for p in paths2:
        if os.path.exists(p):
            reg = p; break
    if bold and reg:
        return {
            'title': ImageFont.truetype(bold, 30),
            'stage': ImageFont.truetype(bold, 18),
            'label': ImageFont.truetype(bold, 15),
            'desc':  ImageFont.truetype(reg, 12),
            'small': ImageFont.truetype(reg, 11),
        }
    f = ImageFont.load_default()
    return {'title': f, 'stage': f, 'label': f, 'desc': f, 'small': f}

fonts = load_fonts()

# ─── Colors ───
C_BG     = '#0d1117'
C_BORDER = '#30363d'
C_TEXT   = '#e6edf3'
C_DIM    = '#8b949e'
C_ORANGE = '#ff9900'
C_GREEN  = '#3ecf8e'
C_RED    = '#ff4444'
C_BLUE   = '#58a6ff'
C_PURPLE = '#a855f7'
C_PINK   = '#da3b8a'

# ─── Row / Column positions ───
ROW1, ROW2, ROW3 = 220, 470, 720
COL0, COL1, COL2, COL3, COL4, COL5 = 100, 310, 560, 830, 1100, 1370

# ─── Arrow paths (start_x, start_y, end_x, end_y, color) ───
ARROWS = [
    # Stage 1
    (COL0+42, ROW1, COL1-50, ROW1, C_ORANGE),
    (COL1+42, ROW1, COL2-50, ROW1, C_ORANGE),
    (COL2+42, ROW1, COL3-50, ROW1, C_GREEN),
    (COL3+42, ROW1, COL4-50, ROW1, C_PURPLE),
    (COL4+42, ROW1, COL5-50, ROW1, C_GREEN),
    # Vertical 1→2
    (COL1, ROW1+90, COL1, ROW2-55, C_BLUE),
    # Stage 2
    (COL1+42, ROW2, COL2-50, ROW2, C_RED),
    (COL2+42, ROW2, COL3-50, ROW2, C_RED),
    (COL3+42, ROW2, COL4-50, ROW2, C_PURPLE),
    (COL4+42, ROW2, COL5-50, ROW2, C_ORANGE),
    # Vertical 2→3
    (COL1, ROW2+90, COL1, ROW3-55, C_BLUE),
    # Stage 3
    (COL1+42, ROW3, COL2-50, ROW3, C_BLUE),
    (COL2+42, ROW3, COL3-50, ROW3, C_PINK),
    (COL3+42, ROW3, COL4-50, ROW3, C_PURPLE),
    (COL4+42, ROW3, COL5-50, ROW3, C_GREEN),
]

# ─── Drawing helpers ───
def rounded_rect(draw, x, y, w, h, r, fill=None, outline=None):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill, outline=outline, width=2)

def draw_arrowhead(draw, x1, y1, x2, y2, color):
    angle = math.atan2(y2 - y1, x2 - x1)
    L = 12
    lx = x2 - L * math.cos(angle - 0.4)
    ly = y2 - L * math.sin(angle - 0.4)
    rx = x2 - L * math.cos(angle + 0.4)
    ry = y2 - L * math.sin(angle + 0.4)
    draw.polygon([(x2, y2), (lx, ly), (rx, ry)], fill=color)

def draw_node(draw, cx, cy, char, label, desc, color, glow=False):
    bx, by, bw, bh = cx-42, cy-42, 84, 84
    if glow:
        for g in range(3, 0, -1):
            rounded_rect(draw, bx-g*3, by-g*3, bw+g*6, bh+g*6, 18, outline=color)
    rounded_rect(draw, bx, by, bw, bh, 16, fill=color, outline='#ffffff30')
    draw.text((cx, cy), char, fill='white', font=fonts['title'], anchor='mm')
    draw.text((cx, cy+58), label, fill=C_TEXT, font=fonts['label'], anchor='mt')
    draw.text((cx, cy+78), desc, fill=C_DIM, font=fonts['desc'], anchor='mt')

def draw_static_arrow(draw, x1, y1, x2, y2, color, dashed=False):
    if dashed:
        dx, dy = x2-x1, y2-y1
        dist = math.hypot(dx, dy)
        n = int(dist / 20)
        for i in range(n):
            t1 = (i*20)/dist
            t2 = min(((i*20)+10)/dist, 1.0)
            draw.line([(x1+dx*t1, y1+dy*t1), (x1+dx*t2, y1+dy*t2)], fill=color, width=2)
    else:
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    draw_arrowhead(draw, x1, y1, x2, y2, color)

def draw_packet(draw, x, y, color, radius=7):
    """Draw a glowing dot at position."""
    for g in range(4, 0, -1):
        r2 = radius + g*3
        alpha_hex = format(int(255 * 0.15 * g), '02x')
        glow_col = color + alpha_hex if len(color) == 7 else color
        draw.ellipse([x-r2, y-r2, x+r2, y+r2], fill=glow_col)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    # bright center
    draw.ellipse([x-2, y-2, x+2, y+2], fill='#ffffff')


def draw_background(draw):
    """Draw all static elements: title, boundary, nodes, arrows, legend."""

    # Title
    draw.text((W//2, 35), "AWS Cloud Optimization Project", fill=C_BLUE, font=fonts['title'], anchor='mt')
    draw.text((W//2, 72), "boto3 flow: Create EC2 → Delete EC2 → Detect idle snapshots → Clean up & save $$$",
              fill=C_DIM, font=fonts['desc'], anchor='mt')

    # AWS boundary
    rounded_rect(draw, 180, 95, 1350, 780, 20, outline=C_BORDER)
    rounded_rect(draw, 200, 78, 340, 20, 4, fill=C_BG)
    draw.text((210, 80), "☁  AWS Cloud — eu-central-1 (Frankfurt)", fill=C_DIM, font=fonts['small'])

    # ── Stage labels ──
    rounded_rect(draw, 220, ROW1-55, 200, 30, 14, fill='#ff990025', outline=C_ORANGE)
    draw.text((320, ROW1-40), "STAGE 1 — CREATE", fill=C_ORANGE, font=fonts['stage'], anchor='mm')

    rounded_rect(draw, 220, ROW2-55, 200, 30, 14, fill='#ff444425', outline=C_RED)
    draw.text((320, ROW2-40), "STAGE 2 — DELETE", fill=C_RED, font=fonts['stage'], anchor='mm')

    rounded_rect(draw, 220, ROW3-55, 220, 30, 14, fill='#58a6ff25', outline=C_BLUE)
    draw.text((330, ROW3-40), "STAGE 3 — OPTIMIZE", fill=C_BLUE, font=fonts['stage'], anchor='mm')

    # ── Stage 1 nodes ──
    draw_node(draw, COL0, ROW1, "👨", "You (DevOps)", "runs the script", '#6e7681')
    draw_node(draw, COL1, ROW1, "🐍", "boto3", "run_instances()", '#1a73e8', glow=True)
    draw_node(draw, COL2, ROW1, "🖥", "EC2 Instance", "t2.micro launched", C_ORANGE)
    draw_node(draw, COL3, ROW1, "💾", "EBS Volume", "8 GB root disk", '#1a9f5c')
    draw_node(draw, COL4, ROW1, "📸", "Snapshot", "backup created", '#7c3aed')
    draw_node(draw, COL5, ROW1, "✔", "Stage 1 Done", "all resources up", '#1a9f5c')

    # ── Stage 2 nodes ──
    draw_node(draw, COL1, ROW2, "🐍", "boto3", "terminate_instances()", '#1a73e8')
    draw_node(draw, COL2, ROW2, "💥", "EC2 Terminated", "instance gone", '#cc0000')
    draw_node(draw, COL3, ROW2, "💥", "Volume Deleted", "auto-deleted", '#cc0000')
    draw_node(draw, COL4, ROW2, "📸", "Snap ALIVE!", "still costs $$$", '#7c3aed', glow=True)
    draw_node(draw, COL5, ROW2, "⚠", "Problem!", "idle snap = waste", C_ORANGE)

    # ── Stage 3 nodes ──
    draw_node(draw, COL1, ROW3, "🐍", "boto3", "describe_snapshots()", '#1a73e8')
    draw_node(draw, COL2, ROW3, "🔍", "Cross-Check", "volume exists?", '#1f6feb')
    draw_node(draw, COL3, ROW3, "🛡", "AMI Safety", "skip if AMI-backed", '#b02a6f')
    draw_node(draw, COL4, ROW3, "🧹", "Delete Snap", "delete_snapshot()", '#7c3aed')
    draw_node(draw, COL5, ROW3, "💰", "Cost Saved!", "$0.05/GB/month", '#1a9f5c', glow=True)

    # ── Arrows ──
    for (x1, y1, x2, y2, color) in ARROWS:
        is_vert = (x1 == x2)
        draw_static_arrow(draw, x1, y1, x2, y2, color, dashed=is_vert)

    # ── Legend ──
    ly = H - 30
    items = [
        (C_ORANGE, "Create (EC2+Volume)"),
        (C_GREEN,  "Snapshot / Success"),
        (C_RED,    "Delete / Terminate"),
        (C_PURPLE, "Snapshot survives"),
        (C_BLUE,   "Scan & Optimize"),
        (C_PINK,   "AMI Safety Check"),
    ]
    lx = 200
    for color, text in items:
        draw.ellipse([lx, ly-5, lx+10, ly+5], fill=color)
        draw.text((lx+18, ly), text, fill=C_DIM, font=fonts['small'], anchor='lm')
        lx += 220


# ═══════════════════════════════════════════════════════════
# GENERATE FRAMES
# ═══════════════════════════════════════════════════════════

print("Generating animated GIF ...")
frames = []

for frame_idx in range(FRAMES):
    t = frame_idx / FRAMES  # 0.0 → ~1.0

    img = Image.new('RGB', (W, H), C_BG)
    draw = ImageDraw.Draw(img)

    # Draw all static elements
    draw_background(draw)

    # Draw animated packets on each arrow
    for (x1, y1, x2, y2, color) in ARROWS:
        # Each arrow gets 2 packets, staggered
        for offset in [0.0, 0.5]:
            pos = (t + offset) % 1.0
            px = x1 + (x2 - x1) * pos
            py = y1 + (y2 - y1) * pos
            draw_packet(draw, px, py, color, radius=6)

    # Quantize to reduce GIF size (256 colors)
    img_q = img.quantize(colors=200, method=Image.Quantize.MEDIANCUT)
    frames.append(img_q)

    if (frame_idx + 1) % 10 == 0:
        print(f"  Frame {frame_idx+1}/{FRAMES}")

# ── Save animated GIF ──
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'architecture_animated.gif')
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,  # infinite loop
    optimize=True,
)

file_size = os.path.getsize(out_path) / (1024 * 1024)
print(f"\nSaved: {out_path}")
print(f"Size : {file_size:.1f} MB | {W}x{H} | {FRAMES} frames | {DURATION}ms/frame")
