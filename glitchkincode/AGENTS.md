# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common commands
- Serve locally (from README): `pwsh -c "cd public; python -m http.server 8000"` then open `http://localhost:8000`
- Tests/lint/build: none configured (static site; GitHub Pages deploys `public/` directly)

## High-level architecture
- Static site lives in `public/` (`index.html`, `style.css`, `script.js`). This folder is what GitHub Pages publishes (see `.github/workflows/pages.yml`).
- `update_list.py` generates `public/index.html` by querying the YouTube Data API (v3) for a set of curated “AI help” searches and rendering them into topic sections with prompt templates.
- `.github/workflows/update.yml` runs `update_list.py` using `secrets.YOUTUBE_API_KEY`, then uploads `./public` and deploys to GitHub Pages.
- `config.js` provides runtime configuration for the site (API base, env, repo URL).
- Deployment can happen via `pages.yml` (deploy whatever is currently in `public/`) or via `update.yml` (regenerate from YouTube then deploy).
