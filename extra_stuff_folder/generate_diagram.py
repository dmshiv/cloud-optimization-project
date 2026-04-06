from PIL import Image, ImageDraw, ImageFont
import os

# ─── Canvas setup ───
W, H = 1600, 950
img = Image.new('RGB', (W, H), '#0d1117')
draw = ImageDraw.Draw(img)

# ─── Fonts (use default, scale up) ───
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    font_stage = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    font_desc  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except:
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf", 30)
        font_stage = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf", 15)
        font_desc  = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 12)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 11)
    except:
        font_title = ImageFont.load_default()
        font_stage = font_label = font_desc = font_small = font_title

# ─── Colors ───
C_BG       = '#0d1117'
C_BORDER   = '#30363d'
C_TEXT     = '#e6edf3'
C_DIM      = '#8b949e'
C_ORANGE   = '#ff9900'
C_GREEN    = '#3ecf8e'
C_RED      = '#ff4444'
C_BLUE     = '#58a6ff'
C_PURPLE   = '#a855f7'
C_PINK     = '#da3b8a'

# ─── Helper: draw rounded rect ───
def rounded_rect(x, y, w, h, r, fill, outline=None):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill, outline=outline, width=2)

# ─── Helper: draw a node (icon box + label + desc) ───
def draw_node(cx, cy, emoji, label, desc, color, glow=False):
    bx, by, bw, bh = cx-42, cy-42, 84, 84
    if glow:
        for g in range(3, 0, -1):
            rounded_rect(bx-g*3, by-g*3, bw+g*6, bh+g*6, 18, None, outline=color)
    rounded_rect(bx, by, bw, bh, 16, color, outline='#ffffff30')
    # emoji text centered
    draw.text((cx, cy), emoji, fill='white', font=font_title, anchor='mm')
    # label below
    draw.text((cx, cy+58), label, fill=C_TEXT, font=font_label, anchor='mt')
    # desc below label
    draw.text((cx, cy+78), desc, fill=C_DIM, font=font_desc, anchor='mt')

# ─── Helper: arrow with animated-style dots ───
def draw_arrow(x1, y1, x2, y2, color, dashed=False, dots=True):
    if dashed:
        dash_len = 10
        dx = x2 - x1
        dy = y2 - y1
        dist = (dx**2 + dy**2) ** 0.5
        num_dashes = int(dist / (dash_len * 2))
        for i in range(num_dashes):
            t1 = (i * 2 * dash_len) / dist
            t2 = ((i * 2 + 1) * dash_len) / dist
            if t2 > 1: t2 = 1
            sx = x1 + dx * t1
            sy = y1 + dy * t1
            ex = x1 + dx * t2
            ey = y1 + dy * t2
            draw.line([(sx, sy), (ex, ey)], fill=color, width=2)
    else:
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

    # arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arr_len = 12
    lx = x2 - arr_len * math.cos(angle - 0.4)
    ly = y2 - arr_len * math.sin(angle - 0.4)
    rx = x2 - arr_len * math.cos(angle + 0.4)
    ry = y2 - arr_len * math.sin(angle + 0.4)
    draw.polygon([(x2, y2), (lx, ly), (rx, ry)], fill=color)

    # glowing dots along path
    if dots:
        num_dots = 3
        for i in range(num_dots):
            t = (i + 0.5) / num_dots
            dx2 = x1 + (x2 - x1) * t
            dy2 = y1 + (y2 - y1) * t
            r = 5
            for g in range(3, 0, -1):
                glow_color = color + '40'
                draw.ellipse([dx2-r-g*2, dy2-r-g*2, dx2+r+g*2, dy2+r+g*2], fill=glow_color)
            draw.ellipse([dx2-r, dy2-r, dx2+r, dy2+r], fill=color)

# ─── Helper: draw vertical transition arrow ───
def draw_vertical_arrow(x, y1, y2, color):
    draw_arrow(x, y1, x, y2, color, dashed=True, dots=True)


# ═══════════════════════════════════════════════════════════
# DRAW THE DIAGRAM
# ═══════════════════════════════════════════════════════════

# ── Title ──
draw.text((W//2, 35), "AWS Cloud Optimization Project — Architecture", fill=C_BLUE, font=font_title, anchor='mt')
draw.text((W//2, 72), "boto3 script flow: Create → Delete → Detect idle snapshots → Clean up", fill=C_DIM, font=font_desc, anchor='mt')

# ── AWS Cloud boundary ──
rounded_rect(180, 95, 1350, 780, 20, None, outline=C_BORDER)
draw.text((210, 83), "  ☁  AWS Cloud — eu-central-1 (Frankfurt)  ", fill=C_DIM, font=font_small)
# fill the background behind the label
rounded_rect(200, 78, 320, 20, 4, C_BG)
draw.text((210, 80), "☁  AWS Cloud — eu-central-1 (Frankfurt)", fill=C_DIM, font=font_small)

# ── Row Y positions ──
ROW1 = 220   # Stage 1
ROW2 = 470   # Stage 2
ROW3 = 720   # Stage 3

# ── Column X positions ──
COL0 = 100    # User
COL1 = 310    # boto3
COL2 = 560    # EC2
COL3 = 830    # EBS Volume
COL4 = 1100   # Snapshot
COL5 = 1370   # Result / Status

# ═══════════════════════════════════════════════════════════
# STAGE 1 — CREATE
# ═══════════════════════════════════════════════════════════

# Stage label
rounded_rect(220, ROW1-55, 200, 30, 14, '#ff990025', outline=C_ORANGE)
draw.text((320, ROW1-40), "STAGE 1 — CREATE", fill=C_ORANGE, font=font_stage, anchor='mm')

# Nodes
draw_node(COL0, ROW1, "👨", "You (DevOps)", "runs the script", '#6e7681')
draw_node(COL1, ROW1, "🐍", "boto3", "run_instances()", '#1a73e8', glow=True)
draw_node(COL2, ROW1, "🖥", "EC2 Instance", "t2.micro launched", C_ORANGE)
draw_node(COL3, ROW1, "💾", "EBS Volume", "8 GB root disk", '#1a9f5c')
draw_node(COL4, ROW1, "📸", "Snapshot", "backup created", '#7c3aed')
draw_node(COL5, ROW1, "✔", "Stage 1 Done", "all resources up", '#1a9f5c')

# Arrows
draw_arrow(COL0+42, ROW1, COL1-50, ROW1, C_ORANGE)
draw_arrow(COL1+42, ROW1, COL2-50, ROW1, C_ORANGE)
draw_arrow(COL2+42, ROW1, COL3-50, ROW1, C_GREEN)
draw_arrow(COL3+42, ROW1, COL4-50, ROW1, C_PURPLE)
draw_arrow(COL4+42, ROW1, COL5-50, ROW1, C_GREEN, dots=False)

# ═══════════════════════════════════════════════════════════
# STAGE 2 — DELETE
# ═══════════════════════════════════════════════════════════

rounded_rect(220, ROW2-55, 200, 30, 14, '#ff444425', outline=C_RED)
draw.text((320, ROW2-40), "STAGE 2 — DELETE", fill=C_RED, font=font_stage, anchor='mm')

draw_node(COL1, ROW2, "🐍", "boto3", "terminate_instances()", '#1a73e8')
draw_node(COL2, ROW2, "💥", "EC2 Terminated", "instance gone", '#cc0000')
draw_node(COL3, ROW2, "💥", "Volume Deleted", "auto-deleted", '#cc0000')
draw_node(COL4, ROW2, "📸", "Snapshot ALIVE", "still costs $$$!", '#7c3aed', glow=True)
draw_node(COL5, ROW2, "⚠", "Problem!", "idle snap = waste", C_ORANGE)

draw_arrow(COL1+42, ROW2, COL2-50, ROW2, C_RED)
draw_arrow(COL2+42, ROW2, COL3-50, ROW2, C_RED)
draw_arrow(COL3+42, ROW2, COL4-50, ROW2, C_PURPLE, dashed=True)
draw_arrow(COL4+42, ROW2, COL5-50, ROW2, C_ORANGE, dots=False)

# Vertical transition arrows
draw_vertical_arrow(COL1, ROW1+90, ROW2-55, C_BLUE)

# ═══════════════════════════════════════════════════════════
# STAGE 3 — OPTIMIZE
# ═══════════════════════════════════════════════════════════

rounded_rect(220, ROW3-55, 220, 30, 14, '#58a6ff25', outline=C_BLUE)
draw.text((330, ROW3-40), "STAGE 3 — OPTIMIZE", fill=C_BLUE, font=font_stage, anchor='mm')

draw_node(COL1, ROW3, "🐍", "boto3", "describe_snapshots()", '#1a73e8')
draw_node(COL2, ROW3, "🔍", "Cross-Check", "volume exists?", '#1f6feb')
draw_node(COL3, ROW3, "🛡", "AMI Safety", "skip if AMI-backed", '#b02a6f')
draw_node(COL4, ROW3, "🧹", "Delete Snap", "delete_snapshot()", '#7c3aed')
draw_node(COL5, ROW3, "💰", "Cost Saved!", "$0.05/GB/month", '#1a9f5c', glow=True)

draw_arrow(COL1+42, ROW3, COL2-50, ROW3, C_BLUE)
draw_arrow(COL2+42, ROW3, COL3-50, ROW3, C_PINK)
draw_arrow(COL3+42, ROW3, COL4-50, ROW3, C_PURPLE)
draw_arrow(COL4+42, ROW3, COL5-50, ROW3, C_GREEN)

draw_vertical_arrow(COL1, ROW2+90, ROW3-55, C_BLUE)

# ═══════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════

ly = H - 30
items = [
    (C_ORANGE, "Create (EC2 + Volume)"),
    (C_GREEN,  "Snapshot / Success"),
    (C_RED,    "Delete / Terminate"),
    (C_PURPLE, "Snapshot survives"),
    (C_BLUE,   "Scan & Optimize"),
    (C_PINK,   "AMI Safety Check"),
]
lx = 200
for color, text in items:
    draw.ellipse([lx, ly-5, lx+10, ly+5], fill=color)
    draw.text((lx+18, ly), text, fill=C_DIM, font=font_small, anchor='lm')
    lx += 220

# ── Save ──
out = os.path.join(os.path.dirname(__file__), 'architecture.png')
img.save(out, 'PNG', quality=95)
print(f"Saved: {out}")
print(f"Size: {img.size[0]}x{img.size[1]}")
