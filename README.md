# CS25: Transformers United — Study Notes

**📖 Read the notes online → [starkaritra.github.io/cs25-notes](https://starkaritra.github.io/cs25-notes/)**

Self-contained, teach-yourself HTML notes for **all 50 talks** of Stanford's
[CS25: Transformers United](https://web.stanford.edu/class/cs25/) (seminar versions V1–V6).
Each note is a single HTML file you can read in a browser or print to PDF — no build step, no server.

---

## What this is

CS25 is Stanford's seminar series where researchers present the ideas behind modern
Transformer models — from the original attention mechanism through today's frontier
agents. These notes turn each ~1-hour talk into a written, self-paced lesson so you can
learn the material without watching every video end-to-end.

Every note is designed to be **understood, not just skimmed**. Each one includes:

- **Prerequisite refresher** — the background you need, recapped up front.
- **Worked numeric example** — the core idea run through with real numbers.
- **End-to-end trace** — how data flows through the method, step by step.
- **Check-yourself questions** — test your understanding as you go.
- **Glossary + references** — every term defined once in plain words; links to sources.

Math is rendered with **MathJax**, diagrams with **Mermaid**, on a dark "notebook"
page with light "paper" diagram cards ([Atkinson Hyperlegible](https://www.brailleinstitute.org/freefont/)
body + Caveat handwritten headings for readability).

## The 50 notes, in 10 batches

The [hub page](https://starkaritra.github.io/cs25-notes/) organizes all notes with
previous/next navigation:

| Batch | Theme | CS25 version |
|------:|-------|--------------|
| 1 | Foundations | V1 |
| 2 | Architecture & Interpretability | V1 |
| 3 | Ideas, Alignment & Agents | V2 |
| 4 | Reasoning, Science & Embodied Agents | V2 → V3 |
| 5 | Assistants, Translation & Retrieval | V3 |
| 6 | The 2024 Frontier | V4 |
| 7 | Multimodal, Data & the Scaling Mind | V4 → V5 |
| 8 | Reasoning, Interpretability & Generation | V5 |
| 9 | Video, World Models & Efficient Scale | V5 → V6 |
| 10 | Frontier, Agents & Systems | V6 (finale) |

## Repository layout

```
notes/            The website. index.html is the hub; NN-slug.html are the 50 notes.
  index.html      Landing hub — 10 batch sections, 50 cards, prev/next wired.
  *.html          One self-contained note per talk (styles + scripts inlined).
  .nojekyll       Tells GitHub Pages to serve the raw HTML (no Jekyll processing).
transcripts/      Raw source transcripts the notes were written from.
theme.py          Shared theme/style injected into each note at build time.
validate.js       Puppeteer render-check: opens each note in headless Edge,
                  fails on any JS / MathJax / Mermaid error.
.github/workflows/deploy.yml   Publishes notes/ to GitHub Pages on every push to main.
```

## Read locally

The notes are plain files — just open the hub in any browser:

```powershell
# from the repo root
start notes\index.html      # Windows
# open notes/index.html     # macOS
# xdg-open notes/index.html # Linux
```

To save a note as PDF, open it and use your browser's **Print → Save as PDF**.

## Validate the notes render (optional, for contributors)

`validate.js` uses Puppeteer to open each note in headless Edge and fail on any
render error. It is a **local-only dev tool** — it is not required to read the notes
and is not part of the Pages deploy.

```powershell
npm install
node validate.js notes\*.html
```

## How it's published

Pushing to `main` triggers `.github/workflows/deploy.yml`, which uploads the `notes/`
folder as the site root and deploys it to GitHub Pages — no framework, no build.
The site source (**Settings → Pages → Source = GitHub Actions**) must be enabled once
for the first deploy to succeed.

## License & attribution

These are personal learning notes summarizing publicly available CS25 talks. All
credit for the underlying research and lectures belongs to the original speakers and
to Stanford's CS25 course. See the [official course site](https://web.stanford.edu/class/cs25/)
for the source talks.
