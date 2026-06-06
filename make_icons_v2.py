#!/usr/bin/env python3
"""
HobbyRAT Portfolio Section Icons v2
High-quality icons with gradients, shadows, glow effects, and detailed artwork.
All based on the HobbyRAT purple theme (#8E3CFF, #C77DFF, #6A2C91).
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import math

GRAPHICS_DIR = "/home/dirdy/portfolio/assets/graphics"
SIZE = 512

# Colors
PURPLE = (142, 60, 255)       # #8E3CFF - primary
PURPLE_LIGHT = (199, 125, 255) # #C77DFF - accent
PURPLE_DARK = (106, 44, 145)   # #6A2C91 - dark
BLACK = (13, 13, 13)           # #0D0D0D
DARK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 65)           # terminal green
GOLD = (255, 215, 0)
RED = (220, 38, 38)
CYAN = (0, 200, 255)

def new_img():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

def gradient_circle(draw, cx, cy, r, color_inner, color_outer):
    """Draw a circle with radial gradient."""
    for i in range(r, 0, -1):
        t = i / r
        r_c = int(color_inner[0] * (1-t) + color_outer[0] * t)
        g_c = int(color_inner[1] * (1-t) + color_outer[1] * t)
        b_c = int(color_inner[2] * (1-t) + color_outer[2] * t)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=(r_c, g_c, b_c, 255))

def glow_ring(draw, cx, cy, r, color, width=3, glow=True):
    """Draw a glowing ring."""
    if glow:
        for i in range(width + 8, width, -1):
            alpha = int(30 * (1 - (i - width) / 8))
            draw.ellipse([cx-r-i, cy-r-i, cx+r+i, cy+r+i], outline=(*color, alpha), width=2)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=width)

def rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    """Draw a rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def save_icon(img, name):
    path = os.path.join(GRAPHICS_DIR, f"section-{name}.png")
    img.save(path, "PNG")
    print(f"[v2] {path}")

# ============================================================
# ABOUT - ID Card with person silhouette
# ============================================================
def make_about():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer glow ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    glow_ring(draw, cx, cy, 200, PURPLE_LIGHT, width=1)
    
    # ID Card
    card_w, card_h = 200, 130
    cx1, cy1 = cx - card_w//2, cy - card_h//2 - 10
    
    # Card shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [cx1+4, cy1+4, cx1+card_w+4, cy1+card_h+4], 12, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Card body with gradient
    for y in range(cy1, cy1 + card_h):
        t = (y - cy1) / card_h
        r_c = int(DARK[0] * (1-t) + PURPLE_DARK[0] * t)
        g_c = int(DARK[1] * (1-t) + PURPLE_DARK[1] * t)
        b_c = int(DARK[2] * (1-t) + PURPLE_DARK[2] * t)
        draw.line([(cx1, y), (cx1 + card_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [cx1, cy1, cx1+card_w, cy1+card_h], 12, fill=None, outline=PURPLE, width=3)
    
    # Photo circle
    photo_cx = cx1 + 45
    photo_cy = cy1 + card_h // 2
    photo_r = 28
    gradient_circle(draw, photo_cx, photo_cy, photo_r, PURPLE, PURPLE_DARK)
    draw.ellipse([photo_cx-26, photo_cy-26, photo_cx+26, photo_cy+26], outline=PURPLE_LIGHT, width=2)
    
    # Person silhouette in photo
    # Head
    draw.ellipse([photo_cx-10, photo_r-18, photo_cx+10, photo_r-2], fill=PURPLE_LIGHT)
    # Body
    draw.ellipse([photo_cx-14, photo_r-2, photo_cx+14, photo_r+20], fill=PURPLE_LIGHT)
    
    # Text lines
    for i in range(3):
        lx = cx1 + 80
        ly = cy1 + 30 + i * 22
        lw = card_w - 90 - (i * 15)
        alpha = 200 - i * 40
        draw.rounded_rectangle([lx, ly, lx+lw, ly+6], radius=3, fill=(*PURPLE_LIGHT, alpha))
    
    # Chip
    chip_x, chip_y = cx1 + card_w - 35, cy1 + card_h - 30
    draw.rounded_rectangle([chip_x, chip_y, chip_x+22, chip_y+16], radius=3, fill=(*GOLD, 200), outline=(*GOLD, 255), width=1)
    
    # Question mark overlay
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    except:
        font = ImageFont.load_default()
    
    # Glow behind question mark
    for offset in range(12, 0, -1):
        alpha = int(15 * (1 - offset/12))
        draw.text((cx, cy - 15), "?", fill=(*PURPLE_LIGHT, alpha), font=font, anchor="mm")
    draw.text((cx, cy - 15), "?", fill=WHITE, font=font, anchor="mm")
    
    save_icon(img, "about")

# ============================================================
# TOOLS - Terminal with code
# ============================================================
def make_tools():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Terminal window
    term_w, term_h = 240, 170
    tx, ty = cx - term_w//2, cy - term_h//2 - 10
    
    # Shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [tx+5, ty+5, tx+term_w+5, ty+term_h+5], 10, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Terminal body
    for y in range(ty, ty + term_h):
        t = (y - ty) / term_h
        r_c = int(BLACK[0] * (1-t) + 30 * t)
        g_c = int(BLACK[1] * (1-t) + 10 * t)
        b_c = int(BLACK[2] * (1-t) + 40 * t)
        draw.line([(tx, y), (tx + term_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [tx, ty, tx+term_w, ty+term_h], 10, fill=None, outline=PURPLE, width=3)
    
    # Title bar
    for y in range(ty, ty + 24):
        t = (y - ty) / 24
        r_c = int(PURPLE_DARK[0] * (1-t) + PURPLE[0] * t)
        g_c = int(PURPLE_DARK[1] * (1-t) + PURPLE[1] * t)
        b_c = int(PURPLE_DARK[2] * (1-t) + PURPLE[2] * t)
        draw.line([(tx, y), (tx + term_w, y)], fill=(r_c, g_c, b_c, 255))
    draw.rounded_rectangle([tx, ty, tx+term_w, ty+24], 10, fill=None)
    draw.rectangle([tx, ty+12, tx+term_w, ty+24], fill=PURPLE)
    
    # Traffic lights
    for i, c in enumerate([(255, 90, 90), (255, 190, 50), (80, 200, 80)]):
        draw.ellipse([tx+10+i*18, ty+6, tx+20+i*18, ty+16], fill=(*c, 255))
    
    # Terminal text
    lines = [
        ("$ nmap -sV target.com", GREEN),
        ("PORT     STATE SERVICE", PURPLE_LIGHT),
        ("22/tcp   open  ssh", WHITE),
        ("80/tcp   open  http", WHITE),
        ("443/tcp  open  https", WHITE),
        ("", WHITE),
        ("[*] Scan complete.", CYAN),
    ]
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    for i, (text, color) in enumerate(lines):
        if text:
            draw.text((tx + 12, ty + 30 + i * 18), text, fill=color, font=font)
    
    # Cursor
    draw.rectangle([tx + 12 + len(lines[-1][0]) * 8, ty + 30 + (len(lines)-1) * 18,
                    tx + 12 + len(lines[-1][0]) * 8 + 10, ty + 30 + (len(lines)-1) * 18 + 14],
                   fill=PURPLE_LIGHT)
    
    save_icon(img, "tools")

# ============================================================
# SERVICES - Shield with bug bounty crosshair
# ============================================================
def make_services():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Shield shape
    shield_w, shield_h = 180, 220
    sx, sy = cx - shield_w//2, cy - shield_h//2 - 10
    
    # Shield points
    shield_points = [
        (cx, sy),  # top
        (cx + shield_w//2, sy + shield_h * 0.15),
        (cx + shield_w//2, sy + shield_h * 0.55),
        (cx, sy + shield_h),  # bottom point
        (cx - shield_w//2, sy + shield_h * 0.55),
        (cx - shield_w//2, sy + shield_h * 0.15),
    ]
    
    # Shield gradient fill
    for y in range(sy, sy + shield_h):
        t = (y - sy) / shield_h
        r_c = int(DARK[0] * (1-t) + PURPLE_DARK[0] * t)
        g_c = int(DARK[1] * (1-t) + PURPLE_DARK[1] * t)
        b_c = int(DARK[2] * (1-t) + PURPLE_DARK[2] * t)
        # Clip to shield shape (approximate with horizontal scan)
        progress = (y - sy) / shield_h
        if progress < 0.15:
            half_w = int(shield_w/2 * progress / 0.15)
        elif progress < 0.55:
            half_w = shield_w // 2
        else:
            half_w = int(shield_w/2 * (1 - (progress - 0.55) / 0.45))
        draw.line([(cx - half_w, y), (cx + half_w, y)], fill=(r_c, g_c, b_c, 255))
    
    draw.polygon(shield_points, outline=PURPLE, width=3)
    
    # Inner shield outline
    inner_points = [
        (cx, sy+15),
        (cx+shield_w//2-15, sy+shield_h*0.18),
        (cx+shield_w//2-15, sy+shield_h*0.52),
        (cx, sy+shield_h-15),
        (cx-shield_w//2+15, sy+shield_h*0.52),
        (cx-shield_w//2+15, sy+shield_h*0.18),
    ]
    draw.polygon(inner_points, outline=(*PURPLE_LIGHT, 120), width=1)
    
    # Crosshair in center
    ch_cx, ch_cy = cx, cy - 5
    ch_r = 35
    
    # Crosshair circle
    draw.ellipse([ch_cx-ch_r, ch_cy-ch_r, ch_cx+ch_r, ch_cy+ch_r], outline=PURPLE_LIGHT, width=2)
    draw.ellipse([ch_cx-ch_r+10, ch_cy-ch_r+10, ch_cx+ch_r-10, ch_cy+ch_r-10], outline=(*PURPLE_LIGHT, 150), width=1)
    
    # Crosshair lines
    draw.line([(ch_cx-ch_r-5, ch_cy), (ch_cx-12, ch_cy)], fill=PURPLE_LIGHT, width=2)
    draw.line([(ch_cx+12, ch_cy), (ch_cx+ch_r+5, ch_cy)], fill=PURPLE_LIGHT, width=2)
    draw.line([(ch_cx, ch_cy-ch_r-5), (ch_cx, ch_cy-12)], fill=PURPLE_LIGHT, width=2)
    draw.line([(ch_cx, ch_cy+12), (ch_cx, ch_cy+ch_r+5)], fill=PURPLE_LIGHT, width=2)
    
    # Center dot
    draw.ellipse([ch_cx-4, ch_cy-4, ch_cx+4, ch_cy+4], fill=PURPLE)
    draw.ellipse([ch_cx-2, ch_cy-2, ch_cx+2, ch_cy+2], fill=WHITE)
    
    # Bug icon near crosshair
    bug_cx, bug_cy = cx + 55, cy + 30
    # Body
    draw.ellipse([bug_cx-10, bug_cy-14, bug_cx+10, bug_cy+14], fill=PURPLE, outline=PURPLE_LIGHT, width=1)
    # Head
    draw.ellipse([bug_cx-7, bug_cy-20, bug_cx+7, bug_cy-8], fill=PURPLE_LIGHT)
    # Legs
    for angle in [-50, -25, 25, 50]:
        rad = math.radians(angle)
        x1 = bug_cx + int(12 * math.cos(rad))
        y1 = bug_cy + int(4 * math.sin(rad))
        x2 = bug_cx + int(20 * math.cos(rad))
        y2 = bug_cy + int(12 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=PURPLE, width=2)
    # Antennae
    draw.line([(bug_cx-4, bug_cy-18), (bug_cx-10, bug_cy-26)], fill=PURPLE_LIGHT, width=1)
    draw.line([(bug_cx+4, bug_cy-18), (bug_cx+10, bug_cy-26)], fill=PURPLE_LIGHT, width=1)
    
    # Dollar sign near bug
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
    draw.text((bug_cx, bug_cy + 25), "$", fill=(*GOLD, 220), font=font, anchor="mm")
    
    save_icon(img, "services")

# ============================================================
# PROJECTS - Code brackets with connection nodes
# ============================================================
def make_projects():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Central code brackets
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Glow behind brackets
    for offset in range(15, 0, -1):
        alpha = int(10 * (1 - offset/15))
        draw.text((cx, cy - 10), "</>", fill=(*PURPLE_LIGHT, alpha), font=font, anchor="mm")
    draw.text((cx, cy - 10), "</>", fill=PURPLE, font=font, anchor="mm")
    
    # Connection nodes around
    nodes = [
        (cx, cy - 120),   # top
        (cx + 110, cy - 60),  # top-right
        (cx + 110, cy + 60),  # bottom-right
        (cx, cy + 120),   # bottom
        (cx - 110, cy + 60),  # bottom-left
        (cx - 110, cy - 60),  # top-left
    ]
    
    # Draw connections
    for i, n in enumerate(nodes):
        next_n = nodes[(i + 1) % len(nodes)]
        draw.line([n, next_n], fill=(*PURPLE_DARK, 150), width=1)
        # Also connect to center
        draw.line([n, (cx, cy)], fill=(*PURPLE_DARK, 80), width=1)
    
    # Draw nodes
    for i, (nx, ny) in enumerate(nodes):
        # Node glow
        for r in range(18, 8, -1):
            alpha = int(20 * (1 - (r-8)/10))
            draw.ellipse([nx-r, ny-r, nx+r, ny+r], fill=(*PURPLE_LIGHT, alpha))
        
        # Node circle
        draw.ellipse([nx-10, ny-10, nx+10, ny+10], fill=DARK, outline=PURPLE, width=2)
        
        # Mini icon inside node
        mini_icons = ["{}", "()", "[]", "<>", "/*", "*/"]
        try:
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
        except:
            small_font = ImageFont.load_default()
        draw.text((nx, ny), mini_icons[i], fill=PURPLE_LIGHT, font=small_font, anchor="mm")
    
    save_icon(img, "projects")

# ============================================================
# HALL OF FAME - Trophy with star and badges
# ============================================================
def make_hall_of_fame():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Trophy cup
    cup_w, cup_h = 120, 140
    tx, ty = cx - cup_w//2, cy - cup_h//2 - 20
    
    # Cup body gradient
    for y in range(ty, ty + cup_h):
        t = (y - ty) / cup_h
        r_c = int(PURPLE_DARK[0] * (1-t) + PURPLE[0] * t)
        g_c = int(PURPLE_DARK[1] * (1-t) + PURPLE[1] * t)
        b_c = int(PURPLE_DARK[2] * (1-t) + PURPLE[2] * t)
        progress = (y - ty) / cup_h
        if progress < 0.1:
            half_w = int(cup_w/2 * progress / 0.1)
        else:
            shrink = min((progress - 0.1) / 0.9, 1.0)
            half_w = int(cup_w/2 * (1 - shrink * 0.3))
        draw.line([(cx - half_w, y), (cx + half_w, y)], fill=(r_c, g_c, b_c, 255))
    
    # Cup outline
    cup_points = [
        (cx - cup_w//2, ty),
        (cx + cup_w//2, ty),
        (cx + cup_w//2 - 10, ty + cup_h),
        (cx - cup_w//2 + 10, ty + cup_h),
    ]
    draw.polygon(cup_points, outline=PURPLE_LIGHT, width=2)
    
    # Cup rim
    draw.rectangle([cx-cup_w//2-5, ty-5, cx+cup_w//2+5, ty+5], fill=PURPLE)
    draw.rectangle([cx-cup_w//2-5, ty-5, cx+cup_w//2+5, ty+5], outline=PURPLE_LIGHT, width=1)
    
    # Handles
    draw.arc([cx-cup_w//2-25, ty+15, cx-cup_w//2+10, ty+cup_h-20], 90, 270, fill=PURPLE_LIGHT, width=3)
    draw.arc([cx+cup_w//2-10, ty+15, cx+cup_w//2+25, ty+cup_h-20], -90, 90, fill=PURPLE_LIGHT, width=3)
    
    # Base
    draw.rectangle([cx-20, ty+cup_h+5, cx+20, ty+cup_h+12], fill=PURPLE_DARK)
    draw.rectangle([cx-35, ty+cup_h+12, cx+35, ty+cup_h+20], fill=PURPLE)
    draw.rectangle([cx-35, ty+cup_h+12, cx+35, ty+cup_h+20], outline=PURPLE_LIGHT, width=1)
    
    # Star on cup
    star_cx, star_cy = cx, ty + cup_h//2
    draw_star(draw, star_cx, star_cy, 22, 10, fill=GOLD, outline=WHITE)
    
    # Sparkles around
    sparkle_positions = [(cx-80, cy-60), (cx+80, cy-40), (cx-60, cy+80), (cx+70, cy+70)]
    for sx, sy in sparkle_positions:
        draw_star(draw, sx, sy, 6, 3, fill=(*PURPLE_LIGHT, 180), outline=None)
    
    save_icon(img, "hall-of-fame")

def draw_star(draw, cx, cy, outer_r, inner_r, fill, outline=None):
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill, outline=outline)

# ============================================================
# REVIEWS - Chat bubble with rating stars
# ============================================================
def make_reviews():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Chat bubble
    bubble_w, bubble_h = 200, 130
    bx, by = cx - bubble_w//2, cy - bubble_h//2 - 20
    
    # Shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [bx+4, by+4, bx+bubble_w+4, by+bubble_h+4], 18, fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Bubble body
    for y in range(by, by + bubble_h):
        t = (y - by) / bubble_h
        r_c = int(DARK[0] * (1-t) + PURPLE_DARK[0] * t)
        g_c = int(DARK[1] * (1-t) + PURPLE_DARK[1] * t)
        b_c = int(DARK[2] * (1-t) + PURPLE_DARK[2] * t)
        draw.line([(bx, y), (bx + bubble_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [bx, by, bx+bubble_w, by+bubble_h], 18, fill=None, outline=PURPLE, width=3)
    
    # Bubble tail
    tail_points = [(cx-12, by+bubble_h), (cx, by+bubble_h+18), (cx+12, by+bubble_h)]
    draw.polygon(tail_points, fill=DARK)
    draw.polygon(tail_points, outline=PURPLE, width=2)
    # Cover the top edge of tail
    draw.line([(cx-12, by+bubble_h), (cx+12, by+bubble_h)], fill=DARK, width=3)
    
    # Stars inside bubble
    star_y = by + 35
    for i in range(5):
        sx = bx + 25 + i * 20
        draw_star(draw, sx, star_y, 7, 3, fill=GOLD, outline=(*GOLD, 200))
    
    # Text lines
    for i in range(2):
        lx = bx + 20
        ly = by + 55 + i * 16
        lw = bubble_w - 40 - (i * 20)
        draw.rounded_rectangle([lx, ly, lx+lw, ly+5], radius=2, fill=(*PURPLE_LIGHT, 120))
    
    # Quote marks
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except:
        font = ImageFont.load_default()
    draw.text((bx + 15, by + 5), """, fill=(*PURPLE_LIGHT, 150), font=font)
    draw.text((bx + bubble_w - 30, by + bubble_h - 35), """, fill=(*PURPLE_LIGHT, 150), font=font)
    
    save_icon(img, "reviews")

# ============================================================
# BLOG - Document with pen and lines
# ============================================================
def make_blog():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Document
    doc_w, doc_h = 160, 200
    dx, dy = cx - doc_w//2, cy - doc_h//2
    
    # Shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [dx+4, dy+4, dx+doc_w+4, dy+doc_h+4], 8, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Document body
    for y in range(dy, dy + doc_h):
        t = (y - dy) / doc_h
        r_c = int(DARK[0] * (1-t) + 30 * t)
        g_c = int(DARK[1] * (1-t) + 20 * t)
        b_c = int(DARK[2] * (1-t) + 40 * t)
        draw.line([(dx, y), (dx + doc_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [dx, dy, dx+doc_w, dy+doc_h], 8, fill=None, outline=PURPLE, width=3)
    
    # Folded corner
    corner_size = 20
    draw.polygon([(dx+doc_w-corner_size, dy), (dx+doc_w, dy+corner_size), (dx+doc_w, dy)],
                 fill=(*PURPLE_DARK, 200))
    draw.line([(dx+doc_w-corner_size, dy), (dx+doc_w, dy+corner_size)], fill=PURPLE_LIGHT, width=1)
    
    # Text lines
    for i in range(6):
        lx = dx + 15
        ly = dy + 20 + i * 18
        lw = doc_w - 30 if i != 3 else doc_w - 60
        alpha = 180 - i * 15
        draw.rounded_rectangle([lx, ly, lx+lw, ly+5], radius=2, fill=(*PURPLE_LIGHT, alpha))
    
    # Pen
    pen_x = dx + doc_w - 8
    pen_y = dy + 15
    # Pen body
    draw.polygon([(pen_x, pen_y), (pen_x+7, pen_y), (pen_x+5, pen_y+55), (pen_x+2, pen_y+55)],
                 fill=PURPLE, outline=PURPLE_LIGHT, width=1)
    # Pen tip
    draw.polygon([(pen_x+2, pen_y+55), (pen_x+5, pen_y+55), pen_x+3.5, pen_y+65],
                 fill=WHITE)
    # Pen cap detail
    draw.rectangle([pen_x-1, pen_y-6, pen_x+8, pen_y], fill=PURPLE_DARK)
    # Pen clip
    draw.line([(pen_x+6, pen_y-6), (pen_x+8, pen_y-6), (pen_x+8, pen_y+10), (pen_x+6, pen_y+10)],
              fill=PURPLE_LIGHT, width=2)
    
    save_icon(img, "blog")

# ============================================================
# CONTACT - Envelope with PGP lock
# ============================================================
def make_contact():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Envelope
    env_w, env_h = 200, 140
    ex, ey = cx - env_w//2, cy - env_h//2
    
    # Shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [ex+4, ey+4, ex+env_w+4, ey+env_h+4], 8, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Envelope body
    for y in range(ey, ey + env_h):
        t = (y - ey) / env_h
        r_c = int(DARK[0] * (1-t) + PURPLE_DARK[0] * t)
        g_c = int(DARK[1] * (1-t) + PURPLE_DARK[1] * t)
        b_c = int(DARK[2] * (1-t) + PURPLE_DARK[2] * t)
        draw.line([(ex, y), (ex + env_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [ex, ey, ex+env_w, ey+env_h], 8, fill=None, outline=PURPLE, width=3)
    
    # Envelope flap
    flap_points = [(ex, ey), (cx, ey + env_h*0.45), (ex+env_w, ey)]
    draw.polygon(flap_points, fill=(*PURPLE, 200), outline=PURPLE_LIGHT, width=1)
    
    # Inner flap line
    draw.line([(ex+10, ey+5), (cx, ey+env_h*0.42), (ex+env_w-10, ey+5)],
              fill=(*PURPLE_LIGHT, 100), width=1)
    
    # Lock icon in center
    lock_cx, lock_cy = cx, cy + 5
    
    # Lock glow
    for r in range(25, 15, -1):
        alpha = int(15 * (1 - (r-15)/10))
        draw.ellipse([lock_cx-r, lock_cy-r, lock_cx+r, lock_cy+r], fill=(*PURPLE_LIGHT, alpha))
    
    # Lock body
    rounded_rect(draw, [lock_cx-14, lock_cy-2, lock_cx+14, lock_cy+18], 4,
                 fill=PURPLE, outline=PURPLE_LIGHT, width=2)
    
    # Lock shackle
    draw.arc([lock_cx-12, lock_cy-22, lock_cx+12, lock_cy+2], 0, 180, fill=PURPLE_LIGHT, width=4)
    
    # Keyhole
    draw.ellipse([lock_cx-3, lock_cy+4, lock_cx+3, lock_cy+10], fill=BLACK)
    draw.rectangle([lock_cx-1, lock_cy+8, lock_cx+1, lock_cy+14], fill=BLACK)
    
    # Key icon next to lock
    key_cx, key_cy = cx + 55, cy + 30
    # Key head (circle)
    draw.ellipse([key_cx-8, key_cy-8, key_cx+8, key_cy+8], fill=(*GOLD, 200), outline=GOLD, width=1)
    draw.ellipse([key_cx-3, key_cy-3, key_cx+3, key_cy+3], fill=BLACK)
    # Key shaft
    draw.rectangle([key_cx+6, key_cy-2, key_cx+22, key_cy+2], fill=(*GOLD, 200))
    # Key teeth
    draw.rectangle([key_cx+16, key_cy+2, key_cx+18, key_cy+6], fill=(*GOLD, 200))
    draw.rectangle([key_cx+20, key_cy+2, key_cx+22, key_cy+5], fill=(*GOLD, 200))
    
    save_icon(img, "contact")

# ============================================================
# SHOP - Shopping bag with security products
# ============================================================
def make_shop():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Shopping bag
    bag_w, bag_h = 160, 190
    bx, by = cx - bag_w//2, cy - bag_h//2 + 10
    
    # Shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [bx+4, by+4, bx+bag_w+4, by+bag_h+4], 8, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Bag body
    for y in range(by, by + bag_h):
        t = (y - by) / bag_h
        r_c = int(DARK[0] * (1-t) + PURPLE_DARK[0] * t)
        g_c = int(DARK[1] * (1-t) + PURPLE_DARK[1] * t)
        b_c = int(DARK[2] * (1-t) + PURPLE_DARK[2] * t)
        draw.line([(bx, y), (bx + bag_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [bx, by, bx+bag_w, by+bag_h], 8, fill=None, outline=PURPLE, width=3)
    
    # Handles
    draw.arc([bx+bag_w*0.2, by-25, bx+bag_w*0.4, by+10], 0, 180, fill=PURPLE_LIGHT, width=3)
    draw.arc([bx+bag_w*0.6, by-25, bx+bag_w*0.8, by+10], 0, 180, fill=PURPLE_LIGHT, width=3)
    
    # Shield icon on bag (security product)
    shield_cx, shield_cy = cx, by + 55
    shield_points = [
        (shield_cx, shield_cy - 25),
        (shield_cx + 25, shield_cy - 15),
        (shield_cx + 25, shield_cy + 10),
        (shield_cx, shield_cy + 30),
        (shield_cx - 25, shield_cy + 10),
        (shield_cx - 25, shield_cy - 15),
    ]
    draw.polygon(shield_points, fill=(*PURPLE, 200), outline=PURPLE_LIGHT, width=2)
    
    # Checkmark in shield
    draw.line([(shield_cx-10, shield_cy), (shield_cx-3, shield_cy+10), (shield_cx+12, shield_cy-8)],
              fill=GREEN, width=3)
    
    # Dollar sign below
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    # Glow behind dollar
    for offset in range(8, 0, -1):
        alpha = int(20 * (1 - offset/8))
        draw.text((cx, by + 120), "$", fill=(*GOLD, alpha), font=font, anchor="mm")
    draw.text((cx, by + 120), "$", fill=GOLD, font=font, anchor="mm")
    
    save_icon(img, "shop")

# ============================================================
# DEMOS - Monitor with play button
# ============================================================
def make_demos():
    img = new_img()
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    
    # Outer ring
    glow_ring(draw, cx, cy, 220, PURPLE, width=3)
    
    # Monitor
    mon_w, mon_h = 220, 150
    mx, my = cx - mon_w//2, cy - mon_h//2 - 15
    
    # Shadow
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, [mx+4, my+4, mx+mon_w+4, my+mon_h+4], 8, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Monitor body
    for y in range(my, my + mon_h):
        t = (y - my) / mon_h
        r_c = int(DARK[0] * (1-t) + 25 * t)
        g_c = int(DARK[1] * (1-t) + 25 * t)
        b_c = int(DARK[2] * (1-t) + 35 * t)
        draw.line([(mx, y), (mx + mon_w, y)], fill=(r_c, g_c, b_c, 255))
    
    rounded_rect(draw, [mx, my, mx+mon_w, my+mon_h], 8, fill=None, outline=PURPLE, width=3)
    
    # Screen content - terminal-like
    screen_margin = 12
    draw.rectangle([mx+screen_margin, my+screen_margin, mx+mon_w-screen_margin, my+mon_h-screen_margin],
                   fill=BLACK)
    
    # Terminal lines on screen
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
    except:
        font = ImageFont.load_default()
    
    screen_lines = [
        ("$ ./demo.sh", GREEN),
        ("[*] Starting capture...", PURPLE_LIGHT),
        ("[+] Recording active", CYAN),
    ]
    for i, (text, color) in enumerate(screen_lines):
        draw.text((mx + screen_margin + 5, my + screen_margin + 5 + i * 14), text, fill=color, font=font)
    
    # Blinking cursor
    draw.rectangle([mx + screen_margin + 5 + len(screen_lines[-1][0])*6,
                    my + screen_margin + 5 + (len(screen_lines)-1)*14,
                    mx + screen_margin + 5 + len(screen_lines[-1][0])*6 + 8,
                    my + screen_margin + 5 + (len(screen_lines)-1)*14 + 10],
                   fill=PURPLE_LIGHT)
    
    # Play button overlay (center of screen)
    play_cx = mx + mon_w//2
    play_cy = my + mon_h//2 + 10
    
    # Play button glow
    for r in range(22, 12, -1):
        alpha = int(20 * (1 - (r-12)/10))
        draw.ellipse([play_cx-r, play_cy-r, play_cx+r, play_cy+r], fill=(*PURPLE_LIGHT, alpha))
    
    # Play button circle
    draw.ellipse([play_cx-14, play_cy-14, play_cx+14, play_cy+14], fill=PURPLE, outline=PURPLE_LIGHT, width=2)
    
    # Play triangle
    p1 = (play_cx - 6, play_cy - 10)
    p2 = (play_cx - 6, play_cy + 10)
    p3 = (play_cx + 10, play_cy)
    draw.polygon([p1, p2, p3], fill=WHITE)
    
    # Monitor stand
    draw.rectangle([cx-15, my+mon_h, cx+15, my+mon_h+12], fill=PURPLE_DARK)
    draw.rectangle([cx-30, my+mon_h+12, cx+30, my+mon_h+18], fill=PURPLE)
    draw.rectangle([cx-30, my+mon_h+12, cx+30, my+mon_h+18], outline=PURPLE_LIGHT, width=1)
    
    save_icon(img, "demos")

# ============================================================
# Generate all
# ============================================================
print("=" * 60)
print("Generating Section Icons v2")
print("=" * 60)

make_about()
make_tools()
make_services()
make_projects()
make_hall_of_fame()
make_reviews()
make_blog()
make_contact()
make_shop()
make_demos()

print()
print("=" * 60)
print("ALL DONE!")
print("=" * 60)
