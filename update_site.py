import os
import requests

# 1. Get your Key
API_KEY = os.getenv("YOUTUBE_API_KEY")

# 2. Ask YouTube for a fresh 2026 repair video
query = "tech repair 2026"
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={API_KEY}"
data = requests.get(url).json()

if "items" in data:
    video = data["items"][0]
    v_id = video["id"]["videoId"]
    v_title = video["snippet"]["title"]
    
    # Create the new card
    new_card = f'<div class="card"><h3>{v_title}</h3><iframe src="https://www.youtube.com/embed/{v_id}"></iframe></div>'

    # 3. Read your current website
    with open("index.html", "r") as f:
        content = f.read()

    # 4. Find the "Video Zone" and update it
    start_tag = ""
    end_tag = ""
    
    # This splits your site into: [Top Part] [Old Videos] [Bottom Part]
    parts = content.split(start_tag)
    top_part = parts[0]
    bottom_parts = parts[1].split(end_tag)
    old_videos = bottom_parts[0].strip().split('</div>') # Breaks videos apart
    footer_part = bottom_parts[1]

    # Clean up the list and add our new video to the TOP
    all_videos = [new_card] + [v + '</div>' for v in old_videos if '<iframe' in v]
    
    # KEEP ONLY THE TOP 5 (This removes the duplicates at the bottom!)
    fresh_videos = "\n".join(all_videos[:5])

    # 5. Put the website back together
    new_site = f"{top_part}{start_tag}\n{fresh_videos}\n{end_tag}{footer_part}"
    
    with open("index.html", "w") as f:
        f.write(new_site)
