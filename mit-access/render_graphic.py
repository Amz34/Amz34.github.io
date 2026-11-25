import os
from PIL import Image, ImageDraw, ImageFont

def render_linkedin_graphic():
    width = 1080
    height = 1350

    # Create base dark canvas
    img = Image.new("RGBA", (width, height), (11, 15, 25, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_reg_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font_badge = ImageFont.truetype(font_bold_path, 22)
    font_title = ImageFont.truetype(font_bold_path, 46)
    font_sub = ImageFont.truetype(font_reg_path, 26)
    font_card_num = ImageFont.truetype(font_bold_path, 34)
    font_card_lbl = ImageFont.truetype(font_reg_path, 20)
    font_cta_head = ImageFont.truetype(font_bold_path, 28)
    font_cta_sub = ImageFont.truetype(font_bold_path, 24)

    # Background subtle radial/linear glow
    for y in range(height):
        # subtle gradient
        ratio = y / height
        r = int(11 + ratio * 8)
        g = int(15 + ratio * 15)
        b = int(25 + ratio * 28)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Top Header Badge
    badge_text = "AZ CONSULTANTS · SENIOR FORWARD DEPLOYED ENGINEERING"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    bx = (width - bw) // 2
    by = 55
    draw.rounded_rectangle([bx - 18, by - 8, bx + bw + 18, by + bh + 10], radius=16, fill=(13, 148, 136, 45), outline=(13, 148, 136, 255), width=2)
    draw.text((bx, by), badge_text, font=font_badge, fill=(45, 212, 191, 255))

    # Title
    t1 = "MEP & PRIMAVERA P6 CONTROLS MESH"
    bbox_t1 = draw.textbbox((0, 0), t1, font=font_title)
    draw.text(((width - (bbox_t1[2] - bbox_t1[0])) // 2, 120), t1, font=font_title, fill=(248, 250, 252, 255))

    # Subtitle
    sub1 = "Autonomous Variance Detection & DCMA 14-Point Health on Megaprojects"
    bbox_sub = draw.textbbox((0, 0), sub1, font=font_sub)
    draw.text(((width - (bbox_sub[2] - bbox_sub[0])) // 2, 185), sub1, font=font_sub, fill=(148, 163, 184, 255))

    # Metric summary row (3 cards)
    metrics = [
        ("48-Hour", "Predictive Delay Warning"),
        ("100%", "DCMA 14-Point Integrity"),
        ("14 Packages", "Cross-Trade MEP Interfacing")
    ]
    card_w = 300
    card_h = 110
    total_cards_w = 3 * card_w + 2 * 30
    start_x = (width - total_cards_w) // 2
    cards_y = 240

    for i, (m_val, m_lbl) in enumerate(metrics):
        cx = start_x + i * (card_w + 30)
        draw.rounded_rectangle([cx, cards_y, cx + card_w, cards_y + card_h], radius=12, fill=(15, 23, 42, 200), outline=(51, 65, 85, 255), width=2)
        # Value
        v_box = draw.textbbox((0, 0), m_val, font=font_card_num)
        draw.text((cx + (card_w - (v_box[2] - v_box[0])) // 2, cards_y + 18), m_val, font=font_card_num, fill=(45, 212, 191, 255))
        # Label
        l_box = draw.textbbox((0, 0), m_lbl, font=font_card_lbl)
        draw.text((cx + (card_w - (l_box[2] - l_box[0])) // 2, cards_y + 65), m_lbl, font=font_card_lbl, fill=(203, 213, 225, 255))

    # Center Hero Visual (Embed genuine chart)
    chart_path = "/home/ubuntu/agy-argon-home/.gemini/antigravity-cli/scratch/saudi-2tn-projects-intelligence/assets/charts/c17_ai_dash_impact.png"
    if os.path.exists(chart_path):
        chart_img = Image.open(chart_path).convert("RGBA")
        # Target frame size
        frame_w = 960
        frame_h = 580
        frame_x = (width - frame_w) // 2
        frame_y = 385

        # Background card for chart
        draw.rounded_rectangle([frame_x - 6, frame_y - 6, frame_x + frame_w + 6, frame_y + frame_h + 6], radius=16, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=2)

        # Resize chart with high quality
        chart_resized = chart_img.resize((frame_w, frame_h), Image.Resampling.LANCZOS)
        img.paste(chart_resized, (frame_x, frame_y), chart_resized)

    # Bottom High-Converting Privacy & CTA Banner
    banner_y = 995
    banner_h = 295
    banner_x = 60
    banner_w = width - 120

    # Draw gradient container
    draw.rounded_rectangle([banner_x, banner_y, banner_x + banner_w, banner_y + banner_h], radius=20, fill=(15, 23, 42, 240), outline=(13, 148, 136, 255), width=3)

    # Privacy Warning Badge (Amber)
    pw_text = "🔒 PRIVACY NOTICE: DO NOT COMMENT YOUR EMAIL PUBLICLY"
    pw_bbox = draw.textbbox((0, 0), pw_text, font=font_card_lbl)
    pw_w = pw_bbox[2] - pw_bbox[0]
    pw_x = banner_x + (banner_w - pw_w) // 2
    draw.rounded_rectangle([pw_x - 16, banner_y + 25, pw_x + pw_w + 16, banner_y + 60], radius=10, fill=(180, 83, 9, 50), outline=(245, 158, 11, 255), width=1)
    draw.text((pw_x, banner_y + 30), pw_text, font=font_card_lbl, fill=(251, 191, 36, 255))

    # Headline Action
    cta_h1 = "COMMENT 'MIT' BELOW"
    c_box = draw.textbbox((0, 0), cta_h1, font=font_cta_head)
    draw.text((banner_x + (banner_w - (c_box[2] - c_box[0])) // 2, banner_y + 85), cta_h1, font=font_cta_head, fill=(255, 255, 255, 255))

    # Description of what happens
    cta_desc1 = "Our system instantly replies with your private corporate gateway link."
    d1_box = draw.textbbox((0, 0), cta_desc1, font=font_sub)
    draw.text((banner_x + (banner_w - (d1_box[2] - d1_box[0])) // 2, banner_y + 135), cta_desc1, font=font_sub, fill=(203, 213, 225, 255))

    cta_desc2 = "Includes 20-Slide Visual Briefing + Live MkDocs Architectural Models."
    d2_box = draw.textbbox((0, 0), cta_desc2, font=font_sub)
    draw.text((banner_x + (banner_w - (d2_box[2] - d2_box[0])) // 2, banner_y + 175), cta_desc2, font=font_sub, fill=(148, 163, 184, 255))

    # Footer note
    ft_text = "AZ Consultants · amz34.github.io/mit-access · Vision 2030 Portfolio Mesh"
    ft_box = draw.textbbox((0, 0), ft_text, font=font_card_lbl)
    draw.text((banner_x + (banner_w - (ft_box[2] - ft_box[0])) // 2, banner_y + 240), ft_text, font=font_card_lbl, fill=(100, 116, 139, 255))

    # Save output
    output_path = "/home/ubuntu/Amz34.github.io/mit-access/post_graphic.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Generated LinkedIn graphic successfully at {output_path}")

    # Also copy to scratch for artifact viewing
    scratch_copy = "/home/ubuntu/agy-argon-home/.gemini/antigravity-cli/brain/dcdb8121-1c8b-410d-b983-f4000bdcb6ec/post_graphic.png"
    img.save(scratch_copy, "PNG")
    print(f"Saved copy to {scratch_copy}")

if __name__ == "__main__":
    render_linkedin_graphic()
