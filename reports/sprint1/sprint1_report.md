# Sprint 1 Report

## Scope

Pick a dataset, explore it, clean it, and hand a ready-to-use file to Sprint 2.

## Work Completed

- **Dataset chosen:** Formula 1 World Championship 1950–2024 (from Ergast, downloaded via Kaggle). Documented in `data/README.md` and `data/raw/README.md`.
- **Exploration:** `notebooks/sprint1_eda.ipynb` — merged the seven raw tables into one big table (one row per driver per race) and looked at the target and how starting position relates to finishing position.
- **Cleaning:** `notebooks/sprint1_data_cleaning.ipynb` produces `data/processed/f1_modern_cleaned.csv`. Schema in `data/processed/README.md`.
- **Repo docs:** root `README.md` updated with the project title, problem statement, research question and sprint plan.

## Key Findings

- **Size of the cleaned dataset.** About 9,600 driver-race entries in the modern era (2000–2024), covering 479 races, 126 drivers and 38 teams.

- **Where you start predicts where you finish — but only sort of.** The correlation between starting position and finishing position is 0.715. That means qualifying matters a lot, but about half of where a driver ends up depends on other things (driver, team, what happens during the race). That gap is what makes the project worth doing, the model has real room to add value beyond just looking at the grid.

- **DNFs are common.** Around 21% of driver-race entries end in a DNF (the driver doesn't finish; crash, engine failure, etc.). That's too big to ignore, so the model has to handle DNFs somehow.

- **We only used races from 2000 onwards.** F1 has changed a lot over 70+ years; different point systems, smaller fields, less reliable cars. Mixing all eras would confuse a model. Sticking to 2000+ keeps things consistent and still leaves plenty of data.

- **Target column choice:** we use `positionOrder` (always filled in) rather than `position` (empty when a driver DNFs).

## Blockers and Risks

- **Hidden missing-value bug (fixed).** The raw CSVs use the string `\N` for missing values instead of leaving cells empty. Pandas treated `\N` as normal text, so at first every driver looked like they finished every race. Caught it when the "Finished vs DNF" chart only showed one bar. Fixed by telling pandas to read `\N` as missing, and by making sure number columns are actually numbers. **Anyone who reloads the raw data later needs to do the same thing.**

- **Some rows have no qualifying position.** Sprint 2 needs to decide what to do — fill in a guess, drop those rows, or just use the starting grid position instead.

- **Too many drivers and teams to encode the simple way.** 126 drivers and 38 teams. One-hot encoding would explode the column count, so Sprint 2 should consider other encoding methods (target encoding, or driver-level stats like "average finish position").

- **Drivers switch teams over time.** A driver paired with a strong team is different from the same driver in a weak team. Sprint 2 should decide whether to treat the driver–team pair as one combined feature or keep them separate.

## Next Sprint Handoff

**Main thing to use:** `data/processed/f1_modern_cleaned.csv` (~9,600 rows, 2000–2024). Schema is in `data/processed/README.md`.

**Suggested starting point for Cyprian:**
- Predict: `positionOrder`.
- Categorical columns to encode: `constructor_name`, `driver_name`, `circuit_name`, `circuit_country`, `driver_nationality`, `constructor_nationality`.
- Numeric columns available before the race starts: `grid`, `qualifying_position`, `year`, `round`.
- Still to decide: how to fill in missing `qualifying_position`; how to capture things like recent driver form or team standing.

**Notebooks to look at:** `notebooks/sprint1_eda.ipynb` and `notebooks/sprint1_data_cleaning.ipynb`.