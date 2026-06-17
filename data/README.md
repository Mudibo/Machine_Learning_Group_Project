# Data Directory

## Purpose
This folder stores all project datasets and derived data artifacts.

## Structure
- `raw/`: Original source datasets as collected.
- `processed/`: Cleaned and transformed datasets ready for modeling.

## Guidelines
- Do not modify files in `raw/` manually after acquisition.
- Store preprocessing outputs in `processed/` with clear naming and version notes.
- Document dataset provenance and assumptions in Sprint 1 artifacts.

## Datasets Used

### Primary: Webis Clickbait Challenge 2017 (Webis-Clickbait-17)
- **Source:** Zenodo record 5530410 — https://zenodo.org/records/5530410
- **Original project page:** https://webis.de/data/webis-clickbait-17.html
- **Files used:**
  - `clickbait17-train-170331.zip` (147.8 MB) — training split
  - `clickbait17-test-170720.zip` (934.7 MB) — test split
- **Files ignored:** the five `archives-*` zips (~100 GB total) contain full
  web archives of linked articles and are not needed for this project.
- **Content:** ~38,000 Twitter posts from 27 US news outlets, each annotated
  on a 4-point clickbait-strength scale (0.0, 0.33, 0.66, 1.0) by five human
  annotators. Provides both a continuous score (`truthMean`) and a binary
  label (`truthClass`).

### Secondary: Anand Clickbait Headlines (Kaggle)
- **Source:** https://www.kaggle.com/datasets/amananandrai/clickbait-dataset
- **Content:** ~32,000 news headlines with binary clickbait labels.
  Clickbait sources include BuzzFeed, Upworthy, ViralNova; non-clickbait
  sources include NYT, The Guardian, WikiNews.
- **Role in project:** secondary corroboration of findings from the primary
  dataset; used to check whether linguistic patterns generalise across
  headline-style and tweet-style text.

## How to Obtain the Data
The raw zip files are not committed to this repository (see `.gitignore`).
Each team member must download them locally into `data/raw/` from the
sources listed above before running any notebooks.

## Schema and Data Dictionary
See `data/raw/README.md` for raw file schemas and `data/processed/README.md`
(produced in Sprint 1) for cleaned dataset schemas.