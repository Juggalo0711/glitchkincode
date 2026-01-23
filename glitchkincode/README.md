# Glitchkincode static site

This repo contains a minimal static site ready to deploy to GitHub Pages.

## Quick start
1) Add your content into `public/index.html`, `public/style.css`, and `public/script.js`.  
2) Drop your logo/images into `public/` (or subfolders) and reference them with relative paths.  
3) Commit and push to the `main` branch. GitHub Actions will build and deploy to Pages automatically.

## Customizing content
- Headline/subhead/buttons are in `public/script.js` (simple JS object) and `public/index.html`.  
- Colors/layout are in `public/style.css`.  
- Replace the `LOGO` div in `public/index.html` with an `<img src="./logo.png" alt="Logo">` once you add your logo file.

## Deployment details
- Workflow file: `.github/workflows/pages.yml`  
- Build step: uploads `./public` directly (no build tools required).  
- Deploy step: `actions/deploy-pages@v4` publishes to GitHub Pages.

## Run locally
Open `public/index.html` in a browser, or serve the folder:
```pwsh
pwsh -c "cd public; python -m http.server 8000"
```
then visit http://localhost:8000.

## Notes
- Keep site sources inside `public/`; only that folder is deployed.  
- If you later add a build step (e.g., Vite), point the upload path in `pages.yml` to the build output directory.
