import random

# --- CONFIGURATION (Your Money Info) ---
# Replace 'glitchkin-20' with your actual Amazon Associate ID
AMAZON_TAG = "glitchkin-20" 

# --- REFINED SEARCH BRAIN ---
SEARCH_KEYWORDS = [
    {"query": "hall effect joystick install", "title": "Permanent Stick Drift Fix", "desc": "Fix your 2026 controllers with magnetic sticks that never drift."},
    {"query": "AI wearable battery replacement", "title": "Revive Your AI Wearables", "desc": "Don't toss your smart pin or glasses; swap the battery instead."},
    {"query": "laptop thermal paste 2026", "title": "Stop AI Laptop Overheating", "desc": "High-power AI tasks make laptops hot. Here is the cooling fix."},
    {"query": "OLED screen flickering repair", "title": "Fix Screen Flickering", "desc": "A quick guide to stopping glitches on the latest 2026 displays."}
]

# --- ROBOT LOGIC ---
current_trend = random.choice(SEARCH_KEYWORDS)

# Mapping real, high-quality tutorial IDs
VIDEO_MAP = {
    "hall effect joystick install": "4pS6DshU8_E",
    "AI wearable battery replacement": "8dLgzEAmVTE",
    "laptop thermal paste 2026": "POfX9A_7f1A",
    "OLED screen flickering repair": "fT_p6Xz9qK0"
}

video_id = VIDEO_MAP.get(current_trend["query"])

# AUTOMATED AFFILIATE LINK BUILDER
# This creates a search link on Amazon that includes your money-making Tag
money_link = f"https://www.amazon.com/s?k={current_trend['query'].replace(' ', '+')}&tag={AMAZON_TAG}"

new_card = f"""
        <div class="card">
            <div class="video-box"><iframe src="https://www.youtube.com/embed/{video_id}"></iframe></div>
            <div class="content">
                <h3>{current_trend['title']}</h3>
                <p>{current_trend['desc']}</p>
                <a href="{money_link}" class="btn">Shop Repair Parts</a>
            </div>
        </div>
"""

# --- UPDATE THE WEBSITE ---
with open("index.html", "r") as f:
    html = f.read()

if '' in html:
    # This adds the newest video to the TOP of the list
    updated_html = html.replace('', '\n' + new_card)
    with open("index.html", "w") as f:
        f.write(updated_html)
