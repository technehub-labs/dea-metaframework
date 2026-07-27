# GitHub Pages Site

Interactive viewer for the 7×7 ECF matrix.

## Files

| File | What it is |
|------|-----------|
| `index.html` | Single-page viewer |
| `assets/site.css` | Same design system as the Metamodel viewer (MD3-aligned, harmonized palette) |
| `assets/site.js` | Three scenarios (Foundation / Telecom / Digital), interactive cell inspector |

## Deploy

GitHub Pages serves this directory at:
**https://technehub-labs.github.io/dea-metaframework/**

To enable Pages on the repo:
1. Repo → Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main` · Folder: `/pages`

## Adding a scenario

To add a fourth scenario (e.g., "Healthcare"):

1. Open `assets/site.js`
2. Add `buildHealthcareCells()` following the pattern of `buildTelecomCells()` — return an object keyed by `'domainKey.stageKey'`
3. Add it to `SCENARIOS`:
   ```js
   healthcare: {
     name: 'Healthcare',
     description: 'A hospital — patient records, clinical pathways, compliance.',
     cells: buildHealthcareCells(),
   },
   ```
4. Add the button to `index.html`:
   ```html
   <button class="layer-btn" data-scenario="healthcare">Healthcare</button>
   ```

Each cell requires:
- `text`: 1-sentence description of the cell content
- `glyph`: `●` (active), `★` (high-risk handoff), or `·` (empty)
- `actors`: array of actor-id strings (e.g. `['noc', 'sre']`)
- `metamodelEntities`: array of entity-type names from `dea-metamodel` that map to this cell