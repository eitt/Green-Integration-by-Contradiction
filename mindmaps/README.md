# Interactive chapter maps

Edit Markdown files in this folder. Each heading becomes a branch in an interactive Markmap.

## Local build

From repository root:

```bash
npm install
npm run build:maps
```

Open `docs/index.html` or any generated map in a browser.

On Windows, double-click `actualizar_mapa.bat` in the repository root. It builds the local HTML, opens the index, and asks whether to commit and push the changes.

## GitHub Pages

The workflow in `.github/workflows/publish-mindmaps.yml` rebuilds the maps whenever files in `mindmaps/` or the generator change, then publishes `docs/` to GitHub Pages. Enable GitHub Pages with **GitHub Actions** as the source in repository settings.

Generated HTML files are committed to `docs/` so the site also works as a standalone static artefact in a normal checkout.
