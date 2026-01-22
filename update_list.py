import datetime

# 1. This is your list of AI tools
tools = [
    {"name": "NovaMind AI", "desc": "Turns scattered thoughts into clear action steps."},
    {"name": "AutoTasker Pro", "desc": "Handles repetitive digital tasks across apps."},
    {"name": "WriteFlow AI", "desc": "AI writing assistant for blogs and websites."},
    {"name": "PixelForge AI", "desc": "Creates professional graphics from text prompts."},
    {"name": "CodeBuddy AI", "desc": "Explains and fixes code for beginners."},
    {"name": "SmartFinance AI", "desc": "Analyzes spending habits for smarter budgeting."},
    {"name": "LifeScheduler AI", "desc": "Automatically plans your day based on energy."},
    {"name": "LearnFast AI", "desc": "Creates personalized learning paths for skills."},
    {"name": "VoiceGen AI", "desc": "Converts text into natural, human-sounding speech."},
    {"name": "HomePilot AI", "desc": "Automates smart home devices effortlessly."}
]

# 2. This is the "Shell" of your website (The HTML)
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Tech, Trucks & Motorcycles - AI Tools</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; margin: 0; color: #333; background-color: #f4f4f4; }}
        header {{ background: #222; color: #fff; padding: 20px; text-align: center; }}
        .container {{ max-width: 800px; margin: 20px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .button {{ display: inline-block; background: #e63946; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px; }}
        h2 {{ color: #222; border-bottom: 2px solid #e63946; padding-bottom: 5px; }}
        .tool-box {{ border-left: 5px solid #e63946; padding-left: 15px; margin-bottom: 30px; }}
    </style>
</head>
<body>
<header>
    <h1>🚀 Top 10 AI Tools for 2026</h1>
    <p>Hand-picked for Tech & Ride Enthusiasts</p>
</header>
<div class="container">
    <p><i>Last updated on: {date}</i></p>
    {content}
</div>
</body>
</html>
"""

# 3. This part builds the "Cards" for each tool
content_html = ""
for i, tool in enumerate(tools, 1):
    content_html += f"""
    <div class="tool-box">
        <h2>{i}. {tool['name']}</h2>
        <p>{tool['desc']}</p>
        <a href="#" class="button">Learn More</a>
    </div>
    """

# 4. Save the file as index.html
final_html = html_template.format(date=datetime.datetime.now().strftime("%Y-%m-%d"), content=content_html)

with open("index.html", "w") as f:
    f.write(final_html)

print("Website updated successfully!")
