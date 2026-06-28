# Sprint Plan

## Sprint 1 Plan

Goal: Build a reliable veteran-only data foundation (2022-2026).

1. Dataset acquisition
- Owner: Sharon
- Inputs: Jolpica/Ergast race results + qualifying endpoints for 2022-2026.
- Output: Local raw snapshots in `data/raw/` (not committed).
- Definition of done:
	- Raw race and qualifying data saved for all available rounds.
	- Ingestion guard enforced for incomplete race weekends (`<14` veteran rows aborts).

2. EDA and data quality profiling
- Owner: Sharon
- Output: EDA notebook update and summary metrics.
- Checks:
	- Race coverage by season/round.
	- Veteran-only row counts by race.
	- Missingness (`grid`, `positionOrder`, `status`, qualifying fields).
	- Team-switch timeline sanity check.

3. Data cleaning and canonical table
- Owner: Sharon
- Output: `data/processed/veteran_race_entries_2022_2026.csv`.
- Rules:
	- Filter to 14 veteran drivers only.
	- Convert `\\N` to null and enforce numeric types.
	- Deduplicate by `raceId-driverId`.
	- Keep one row per veteran per race with consistent schema.

## Sprint 2 Plan

Goal: Produce leakage-safe decoupled feature matrix for rank prediction.

1. Preprocessing pipeline
- Owner: Cyprian
- Output: Reusable preprocessing module in `src/preprocessing/preprocessing.py`.
- Definition of done:
	- Validates required columns.
	- Applies veteran filter and season bounds (2022-2026).
	- Produces clean, typed dataframe with `finished` flag.

2. Feature engineering pipeline
- Owner: Cyprian
- Output: Reusable feature module in `src/features/feature_engineering.py`.
- Required features:
	- `driver_form_3races` (EWM, shifted)
	- `circuit_historical_avg` (driver-circuit expanding mean, shifted)
	- `constructor_points_current` (shifted cumulative points)
	- `constructor_dnf_rate_10races` (shifted rolling DNF rate)
	- `grid_position` (anchor feature)

3. Leakage and feature-governance checks
- Owner: Cyprian + Sean
- Constraints:
	- No raw categorical identifiers (`driver_id`, `constructor_id`) in model input matrix.
	- All rolling features computed from pre-race history only.
	- No future-season standings usage in historical rows.

4. Baseline readiness for modeling
- Owner: Sean
- Output: Training-ready matrix and baseline experiment specs.
- Baselines:
	- Grid-only baseline.
	- Decoupled-feature baseline.

## Sprint 3 Plan

Goal: Evaluate ranking quality and interpret driver-vs-constructor influence.

1. Evaluation protocol
- Owner: Amy
- Time-aware train/validation splits.
- Ranking-oriented metrics plus error analysis by circuit/team.

2. Explainability
- Owner: Amy + Sean
- SHAP global and local analysis for decoupled features.
- Compare driver-side vs constructor-side contribution magnitudes.

3. Reporting and presentation
- Owner: Amy
- Final report narrative tied to research question.
- Visual story focused on explainability and operational pipeline reliability.

## Risk Register

1. Incomplete post-race API updates
- Mitigation: Delay automation by >=3 hours post-race and enforce row-count guard.

2. Driver identity leakage
- Mitigation: Exclude raw identity columns from model features.

3. Team-switch regime shift
- Mitigation: Decoupled features with separate driver momentum and constructor reliability/performance signals.

4. Sparse or missing qualifying values
- Mitigation: Fallback to `grid_position`; document imputation strategy explicitly.

5. Timeline leakage in rolling features
- Mitigation: Mandatory shift-before-rolling pattern and unit checks on first observed rows.
