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

## Dataset Used

### Formula 1 World Championship (1950–2024)
- **Source (Kaggle):** https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
- **Original source:** Ergast Motor Racing Developer API (http://ergast.com/mrd/), a long-standing open dataset maintained for the F1 community.
- **Content:** A normalised relational dataset spanning every Formula 1 season from 1950 to 2024, covering races, results, drivers, constructors, qualifying sessions, lap times, pit stops, sprint races, status codes and circuits.
- **Files used in this project (subset of the full dump):**
  - `races.csv` — race metadata (season, round, circuit, date)
  - `results.csv` — race results per driver (finishing position, points, status)
  - `qualifying.csv` — qualifying session results
  - `drivers.csv` — driver reference data
  - `constructors.csv` — team reference data
  - `circuits.csv` — circuit reference data
  - `status.csv` — finish status codes (finished, retired, disqualified, etc.)
- **Approximate scale:** ~25,000 driver-race entries across ~1,100 races, ~860 drivers, and ~210 constructors.
- **Target variable:** finishing position (`positionOrder` in `results.csv`). May be modelled as ordinal classification (top 3, points-scoring, finished) or regression depending on Sprint 2 decisions.

## How to Obtain the Data
The raw CSV files are not committed to this repository (see `.gitignore`). Each team member should download the dataset from the Kaggle link above and place the unzipped CSV files into `data/raw/`.

## Schema and Data Dictionary
See `data/raw/README.md` for expected file contents and column descriptions, and `data/processed/README.md` (produced in Sprint 1) for cleaned dataset schemas.