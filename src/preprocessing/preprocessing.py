"""Preprocessing utilities for the 2022-2026 veteran F1 rank project."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

VETERAN_DRIVERS = (
    "Max Verstappen",
    "Lewis Hamilton",
    "George Russell",
    "Charles Leclerc",
    "Lando Norris",
    "Carlos Sainz",
    "Alexander Albon",
    "Esteban Ocon",
    "Pierre Gasly",
    "Nico Hulkenberg",
    "Fernando Alonso",
    "Lance Stroll",
    "Valtteri Bottas",
    "Sergio Perez",
)

REQUIRED_COLUMNS = {
    "raceId",
    "driverId",
    "constructorId",
    "driver_name",
    "constructor_name",
    "circuit_name",
    "year",
    "round",
    "date",
    "grid",
    "positionOrder",
    "points",
    "status",
}

NUMERIC_COLUMNS = (
    "raceId",
    "driverId",
    "constructorId",
    "year",
    "round",
    "grid",
    "position",
    "positionOrder",
    "points",
)


def _normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim string columns and normalize Ergast missing marker values."""
    normalized = df.replace(r"^\s*\\N\s*$", pd.NA, regex=True).copy()
    for column in [
        "driver_name",
        "constructor_name",
        "circuit_name",
        "status",
    ]:
        if column in normalized.columns:
            normalized[column] = normalized[column].astype("string").str.strip()
    return normalized


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _add_finished_flag(df: pd.DataFrame) -> pd.DataFrame:
    with_finished = df.copy()
    if "position" in with_finished.columns:
        with_finished["finished"] = with_finished["position"].notna()
        return with_finished

    with_finished["finished"] = with_finished["status"].str.contains(
        r"finished|\+\d+\s+lap",
        case=False,
        regex=True,
        na=False,
    )
    return with_finished


def preprocess_data(
    df: pd.DataFrame,
    veteran_drivers: Iterable[str] = VETERAN_DRIVERS,
    min_year: int = 2022,
    max_year: int = 2026,
) -> pd.DataFrame:
    """Clean and filter race-entry data for veteran-only modeling.

    The output preserves one row per race-driver record and is sorted in race
    order for deterministic downstream feature generation.
    """
    _validate_required_columns(df)
    cleaned = _normalize_text_columns(df)

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    veteran_set = {name.strip().lower() for name in veteran_drivers}
    cleaned = cleaned[
        cleaned["driver_name"].str.lower().isin(veteran_set)
        & cleaned["year"].between(min_year, max_year, inclusive="both")
    ].copy()

    cleaned = _add_finished_flag(cleaned)

    cleaned = cleaned.drop_duplicates(subset=["raceId", "driverId"], keep="last")
    cleaned = cleaned.sort_values(["date", "year", "round", "raceId", "driverId"])
    cleaned = cleaned.reset_index(drop=True)

    return cleaned


def validate_race_completeness(df: pd.DataFrame, expected_rows_per_race: int = 14) -> None:
    """Raise if any race has fewer than expected veteran rows."""
    race_counts = df.groupby("raceId", as_index=False).size()
    incomplete = race_counts[race_counts["size"] < expected_rows_per_race]
    if not incomplete.empty:
        preview = incomplete.head(5).to_dict(orient="records")
        raise ValueError(
            "Incomplete race results stream. Aborting pipeline rerun to protect "
            f"database integrity. Sample: {preview}"
        )
