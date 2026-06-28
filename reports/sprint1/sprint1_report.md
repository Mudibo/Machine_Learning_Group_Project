# Sprint 1 Report (Updated for Veteran-Only 2022-2026 Scope)

## Scope

Establish a production-ready data foundation for:
- Dataset acquisition for a fixed 14-driver veteran cohort.
- EDA and data cleaning for 2022-2026 only.
- Handoff-ready tables for leakage-safe feature engineering in Sprint 2.

## Veteran Cohort Definition

Included drivers (must be active at 2022 regulation reset and still active in 2026):
- Max Verstappen
- Lewis Hamilton
- George Russell
- Charles Leclerc
- Lando Norris
- Carlos Sainz
- Alexander Albon
- Esteban Ocon
- Pierre Gasly
- Nico Hulkenberg
- Fernando Alonso
- Lance Stroll
- Valtteri Bottas
- Sergio Perez

Excluded from this project scope:
- 2026 rookies and low-history drivers (cold-start risk).

## Current Repository Status

What is in order:
- Folder structure is clean and sprint-oriented (`data/`, `notebooks/`, `src/`, `reports/`).
- Source modules for preprocessing and features now exist as reusable code entry points.
- `.gitignore` correctly blocks large local data artifacts in `data/raw/` and `data/processed/`.

What is not yet in order for modeling:
- `data/raw/` currently contains only documentation and no source race files.
- `data/processed/` currently contains only documentation and no veteran modeling table.
- Existing historical docs still refer to broad 1950-2024 coverage and must be considered legacy context.

## Data Readiness Decision

Status: **NOT READY FOR TRAINING**

Reason:
- No local race-result payloads or extracted veteran-level records are present yet.
- Therefore EDA statistics and cleaned outputs cannot yet be validated against physical files in this workspace.

## Engineering Risks and Controls

1. Team-switch distortion:
- Risk: Model conflates driver identity with constructor strength across seasons.
- Control: Use decoupled numerical features; do not train on raw driver/constructor identifiers.

2. API latency and steward-delay ingestion:
- Risk: Pipeline ingests incomplete post-race standings.
- Control: Delay automated ingest trigger by at least 3 hours and enforce hard row-count guards.

3. Rolling-feature leakage:
- Risk: Future race information leaks into historical rows.
- Control: Use strict shift-before-rolling logic for all temporal features.

## Sprint 1 Deliverables (Reframed)

1. Dataset acquisition specification for 2022-2026 race and qualifying streams.
2. Cleaning rules for missing values (`\\N`), typing, duplicate race-driver rows, and veteran filtering.
3. Data quality checks:
- One row per `raceId-driverId`.
- Exactly/at least 14 veteran entries for completed races.
- No nulls in required modeling keys (`raceId`, `driverId`, `constructorId`, `positionOrder`, `grid`).
4. Handoff schema for Sprint 2 feature engineering.

## Handoff to Sprint 2

Sprint 2 should consume a cleaned veteran race-entry table with one row per veteran per race and include:
- `year`, `round`, `date`, `raceId`
- `driverId`, `driver_name`
- `constructorId`, `constructor_name`
- `circuit_name`
- `grid`, `positionOrder`, `points`, `status`, `finished`

Planned derived features for Sprint 2:
- `driver_form_3races`
- `circuit_historical_avg`
- `constructor_points_current`
- `constructor_dnf_rate_10races`
- `grid_position`

## Immediate Next Action

Generate and validate a new processed artifact (for example `data/processed/veteran_race_entries_2022_2026.csv`) before any model training starts.