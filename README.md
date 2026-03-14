# B Tecnologia GitHub Pages

Static GitHub Pages source for the public B Tecnologia landing at `https://brunoluizmendes.github.io/`.

## Local build

```bash
python3 site_builder/build_site.py
python3 -m http.server 8000 --directory dist
```

## Structure

- `site_builder/content.py`: site copy, project catalog, and bilingual content
- `site_builder/build_site.py`: static site generator that outputs `dist/`
- `.github/workflows/pages.yml`: GitHub Pages deployment workflow
