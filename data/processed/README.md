# Processed Data

Cleaned outputs from Sprint 1. Files here are derived from `../raw/` by running `notebooks/sprint1_data_cleaning.ipynb` — regenerate locally rather than committing.

## `f1_modern_cleaned.csv`

A driver-race level table for modern-era F1 (2000–2024): ~9,600 rows, 479 races, 126 drivers, 38 constructors.

### Schema

| Column | Type | Description |
|---|---|---|
| `resultId`, `raceId`, `driverId`, `constructorId` | int | Foreign keys from Ergast. |
| `year`, `round`, `date` | int / int / datetime | Race timing. |
| `race_name`, `circuit_name`, `circuit_country` | str | Race and circuit details. |
| `driver_name`, `driver_nationality` | str | Driver details. |
| `constructor_name`, `constructor_nationality` | str | Team details. |
| `grid` | float | Starting position. |
| `qualifying_position` | float | Position after qualifying. May be null. |
| `position` | float | Finishing position. Null for DNFs. |
| `positionOrder` | int | Finishing order including DNFs. **Recommended target.** |
| `points`, `laps` | float | Championship points and laps completed. |
| `status` | str | Finish status (e.g., "Finished", "Engine", "Collision"). |
| `finished` | bool | True if the driver was classified as a finisher. |

### Notes for Sprint 2

- **Target:** use `positionOrder` (always populated). Use `position` only if restricting to finishers, or `finished` if modelling DNFs separately.
- **Missing qualifying:** some rows have null `qualifying_position`. Open decision — impute, drop, or fall back to `grid`.
- **High-cardinality categoricals:** 126 drivers and 38 constructors. One-hot encoding may not be ideal; consider target encoding or aggregate features.
- **`\N` handling:** raw CSVs use `\N` for missing values. The cleaning notebook handles this — preserve the convention if reloading raw data.

See `reports/sprint1/sprint1_report.md` for full Sprint 1 findings.