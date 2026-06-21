# Raw Data

This directory holds the original, unmodified dataset as downloaded from its source. Files are not committed to the repository — each team member downloads them locally per the instructions in `../README.md`.

## Expected Contents

After downloading and unzipping the Kaggle archive, this folder should contain the following CSVs (the Kaggle dump includes more files than listed; only the ones below are used in this project):

### `races.csv`
Race-level metadata.
- `raceId` — primary key
- `year` — season
- `round` — race number within the season
- `circuitId` — foreign key to `circuits.csv`
- `name` — Grand Prix name
- `date` — race date

### `results.csv`
Per-driver, per-race results. This is the central table.
- `resultId` — primary key
- `raceId` — foreign key to `races.csv`
- `driverId` — foreign key to `drivers.csv`
- `constructorId` — foreign key to `constructors.csv`
- `grid` — starting grid position
- `position` — finishing position (null if did not finish)
- `positionOrder` — finishing order including DNFs (always populated)
- `points` — championship points earned
- `laps` — laps completed
- `statusId` — foreign key to `status.csv`

### `qualifying.csv`
Qualifying session results.
- `qualifyId`, `raceId`, `driverId`, `constructorId`
- `position` — qualifying position
- `q1`, `q2`, `q3` — fastest lap times in each qualifying segment

### `drivers.csv`, `constructors.csv`, `circuits.csv`, `status.csv`
Reference tables — names, codes, nationalities, locations, and status descriptions.

## Working Dataset
The Sprint 1 cleaned output will join `results` with `races`, `qualifying`, `drivers`, `constructors`, and `circuits` on the appropriate keys, producing a single driver-race-level table for modelling. Details will be documented in `../processed/README.md` once produced.

## Do Not Modify
Treat everything in this folder as read-only. All cleaning and transformation outputs belong in `../processed/`.