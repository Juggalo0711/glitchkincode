"""Generate the deployed site HTML in `public/`.

This script is designed to run in GitHub Actions (see `.github/workflows/update.yml`).

It uses the YouTube Data API (v3) to search for videos about common “help with AI”
queries, then turns the results into article-style sections with prompt templates.

Configuration:
- Provide `YOUTUBE_API_KEY` via environment variable (recommended: GitHub Actions
  secret `secrets.YOUTUBE_API_KEY`).

Notes:
- YouTube search results include metadata (title/description/channel/thumbnail),
  not full transcripts. The “summary” text here is derived from metadata.
"""

from __future__ import annotations

import datetime
import html
import json
import os
import pathlib
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass


YOUTUBE_SEARCH_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"


@dataclass(frozen=True)
class Video:
    title: str
    description: str
    channel: str
    published_at: str
    video_url: str
    thumbnail_url: str


TOPICS: list[dict[str, object]] = [
    {
        "id": "tools-tutorials",
        "title": "AI Tools & Tutorials",
        "query": "how to use AI tools prompts tutorial",
        "prompt_templates": [
            "You are my AI tutor. Teach me {tool_or_topic} like I'm a beginner. Use a 3-step explanation, then give me 3 practice exercises.",
            "Given my goal: {goal}. Suggest the best AI tool/workflow, then write the exact prompt I should paste. Output in: Steps + Prompt + What good output looks like.",
            "Rewrite this prompt to be clearer and more specific. Keep it under 120 words and add an output format: {my_prompt}",
        ],
        "examples": [
            "Goal: write a resume bullet → Prompt: 'Rewrite these bullets for a senior role. Keep metrics. Output 3 options per bullet.'",
            "Goal: learn React → Prompt: 'Make a 2-week study plan with 5 hours/week. Include daily tasks + a tiny project.'",
        ],
    },
    {
        "id": "video-generators",
        "title": "AI Video Generators & Content Creation",
        "query": "AI video generator tutorial prompts storyboard",
        "prompt_templates": [
            "Create a 6-shot storyboard for a 30s video about {topic}. For each shot: scene description, on-screen text, voiceover, and b-roll suggestions.",
            "Turn this idea into 5 short hooks for TikTok/Shorts. Keep each under 12 words: {idea}",
            "Write a voiceover script (120-160 words) with a strong hook + 3 tips + CTA for {audience} about {topic}.",
        ],
        "examples": [
            "Topic: 'Use AI to write emails faster' → 6-shot storyboard with on-screen tips.",
        ],
    },
    {
        "id": "content-creation",
        "title": "AI Content Creation",
        "query": "ChatGPT content creation workflow prompts blog outline",
        "prompt_templates": [
            "Create a detailed outline for an article about {topic}. Audience: {audience}. Tone: {tone}. Include 6 headings and bullet points under each.",
            "Draft the introduction (120-160 words) using PAS (Problem-Agitate-Solve) for: {topic}.",
            "Rewrite this paragraph to be clearer and more persuasive. Keep meaning the same. Output 2 versions: {paragraph}",
        ],
        "examples": [
            "Audience: small business owners → Topic: 'AI customer support FAQ'",
        ],
    },
    {
        "id": "learning-education",
        "title": "AI Learning & Education",
        "query": "AI study plan tutor prompt templates learning faster",
        "prompt_templates": [
            "Make a study plan for {subject} for 14 days. Each day: concept, explanation, 5-question quiz, and an answer key.",
            "Explain {concept} with 2 analogies, then give me 3 practice problems and check my answers.",
            "I learn best by doing. Give me a mini-project to learn {skill}. Include requirements, milestones, and a rubric.",
        ],
        "examples": [
            "Subject: SQL → 14-day plan with daily practice queries.",
        ],
    },
    {
        "id": "entertainment",
        "title": "AI Generated Entertainment Content",
        "query": "AI generated entertainment story prompt tips",
        "prompt_templates": [
            "Write a short story (900-1200 words) in the style of {style_reference}. Include a twist at the end and 3 memorable characters.",
            "Generate 10 character ideas for a series about {premise}. For each: goal, flaw, secret, and a catchphrase.",
            "Turn this premise into 5 episode summaries (1 paragraph each): {premise}",
        ],
        "examples": [
            "Premise: 'A small town where everyone's AI assistant starts giving contradictory advice.'",
        ],
    },
    {
        "id": "vtubers-avatars",
        "title": "AI VTubers / Avatars",
        "query": "AI vtuber avatar setup prompt voice personality",
        "prompt_templates": [
            "Design a VTuber persona for {niche}. Provide: name ideas, backstory, speaking style, do/don't list, and 10 stream segment ideas.",
            "Write a stream intro script (20-30 seconds) for a VTuber named {name} with vibe {vibe}.",
            "Create a chat moderation policy and 10 auto-reply templates for common questions about {topic}.",
        ],
        "examples": [
            "Niche: 'AI productivity for beginners' → persona + intro script.",
        ],
    },
]


def _compact(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _truncate(text: str, max_len: int = 320) -> str:
    t = _compact(text)
    if len(t) <= max_len:
        return t
    return t[: max_len - 1].rstrip() + "…"


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "glitchkincode-bot/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def fetch_videos(*, api_key: str, query: str, max_results: int = 3) -> list[Video]:
    params = {
        "part": "snippet",
        "type": "video",
        "q": query,
        "maxResults": str(max_results),
        "order": "relevance",
        "safeSearch": "moderate",
        "relevanceLanguage": "en",
        "key": api_key,
    }
    url = f"{YOUTUBE_SEARCH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = _get_json(url)

    if "error" in data:
        message = data.get("error", {}).get("message", "Unknown YouTube API error")
        raise RuntimeError(message)

    out: list[Video] = []
    for item in data.get("items", []):
        vid = (item.get("id") or {}).get("videoId")
        snippet = item.get("snippet") or {}
        if not vid:
            continue

        thumbs = snippet.get("thumbnails") or {}
        thumb_url = (
            (thumbs.get("high") or {}).get("url")
            or (thumbs.get("medium") or {}).get("url")
            or (thumbs.get("default") or {}).get("url")
            or ""
        )

        out.append(
            Video(
                title=_compact(str(snippet.get("title") or "")),
                description=_compact(str(snippet.get("description") or "")),
                channel=_compact(str(snippet.get("channelTitle") or "")),
                published_at=_compact(str(snippet.get("publishedAt") or "")),
                video_url=f"https://www.youtube.com/watch?v={vid}",
                thumbnail_url=_compact(thumb_url),
            )
        )

    return out


def render_topic_section(*, topic: dict[str, object], videos: list[Video]) -> str:
    title = html.escape(str(topic["title"]))
    section_id = html.escape(str(topic["id"]))

    cards: list[str] = []
    for v in videos:
        cards.append(
            "\n".join(
                [
                    '<article class="card">',
                    f"  <h3><a href=\"{html.escape(v.video_url)}\">{html.escape(v.title)}</a></h3>",
                    f"  <p style=\"margin:0 0 10px; color: var(--muted);\">{html.escape(v.channel)} · {html.escape(v.published_at[:10])}</p>",
                    (
                        f"  <img src=\"{html.escape(v.thumbnail_url)}\" alt=\"Thumbnail\" "
                        "style=\"width:100%; border-radius: 10px; border: 1px solid var(--border);\">"
                        if v.thumbnail_url
                        else ""
                    ),
                    f"  <p><strong>Summary:</strong> {html.escape(_truncate(v.description) or 'No description available.')}</p>",
                    "</article>",
                ]
            )
        )

    prompt_templates = topic.get("prompt_templates") or []
    examples = topic.get("examples") or []

    prompts_html = "\n".join(
        [
            "<h4>Prompt templates</h4>",
            "<ul>",
            *[f"  <li><code>{html.escape(str(p))}</code></li>" for p in prompt_templates],
            "</ul>",
        ]
    )

    examples_html = "\n".join(
        [
            "<h4>Examples</h4>",
            "<ul>",
            *[f"  <li>{html.escape(str(e))}</li>" for e in examples],
            "</ul>",
        ]
    )

    return "\n".join(
        [
            f'<section id="{section_id}" class="section">',
            f"  <h2>{title}</h2>",
            '  <div class="section cards">',
            "\n".join(cards) if cards else "<p>No videos found.</p>",
            "  </div>",
            '  <div class="section">',
            prompts_html,
            examples_html,
            "  </div>",
            "</section>",
        ]
    )


def render_page(*, generated_date: str, sections_html: str) -> str:
    # Uses existing site styling from `public/style.css`.
    return """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Glitchkin Code - AI Help Articles</title>
  <link rel=\"stylesheet\" href=\"./style.css\">
</head>
<body>
  <header class=\"hero\">
    <div class=\"logo\">GLITCHKINCODE</div>
    <nav>
      <a href=\"#tools-tutorials\">Tools</a>
      <a href=\"#content-creation\">Content</a>
      <a href=\"#learning-education\">Learning</a>
      <a href=\"#video-generators\">Video</a>
      <a href=\"#vtubers-avatars\">Avatars</a>
    </nav>
  </header>

  <main>
    <section class=\"section\">
      <h1>AI help topics people search for</h1>
      <p>Generated from YouTube search results. Each section includes prompt templates you can copy/paste and adapt.</p>
      <p style=\"color: var(--muted);\"><i>Last updated: {date}</i></p>
      <p><a href=\"./ai-benefits.html\">Read: How to Benefit from AI</a></p>
    </section>

    {sections}
  </main>

  <footer>
    <small>&copy; {year} Glitchkin Code</small>
  </footer>
</body>
</html>
""".format(
        date=html.escape(generated_date),
        year=html.escape(str(datetime.datetime.now().year)),
        sections=sections_html,
    )


def maybe_copy_ai_benefits() -> None:
    """Ensure `public/ai-benefits.html` exists for GitHub Pages.

    The repo currently has `ai-benefits.html` at the root; Pages deploys `public/`.
    """

    root_src = pathlib.Path("ai-benefits.html")
    if not root_src.exists():
        return

    public_dst = pathlib.Path("public") / "ai-benefits.html"
    public_dst.parent.mkdir(parents=True, exist_ok=True)
    public_dst.write_text(root_src.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> None:
    api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Missing YOUTUBE_API_KEY env var. In GitHub Actions, set secrets.YOUTUBE_API_KEY and pass it as env."  # noqa: E501
        )

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    sections: list[str] = []
    for topic in TOPICS:
        query = str(topic["query"])
        videos = fetch_videos(api_key=api_key, query=query, max_results=3)
        sections.append(render_topic_section(topic=topic, videos=videos))

    page = render_page(generated_date=today, sections_html="\n\n".join(sections))

    pathlib.Path("public").mkdir(parents=True, exist_ok=True)
    out_path = pathlib.Path("public") / "index.html"
    out_path.write_text(page, encoding="utf-8")

    maybe_copy_ai_benefits()

    print("public/index.html regenerated successfully.")


if __name__ == "__main__":
    main()

