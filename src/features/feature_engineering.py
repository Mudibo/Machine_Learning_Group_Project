"""Feature engineering utilities for decoupled veteran-rank prediction."""

from __future__ import annotations

from typing import Sequence

import pandas as pd

REQUIRED_COLUMNS = {
    "raceId",
    "driverId",
    "constructorId",
    "circuit_name",
    "date",
    "year",
    "round",
    "grid",
    "positionOrder",
    "points",
    "finished",
}

MODEL_FEATURE_COLUMNS = [
    "driver_form_3races",
    "circuit_historical_avg",
    "constructor_points_current",
    "constructor_dnf_rate_10races",
    "grid_position",
]

LEAKY_IDENTIFIER_COLUMNS = {
    "driverId",
    "constructorId",
    "driver_name",
    "constructor_name",
}


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns for feature generation: {missing}")


def _race_sequence(df: pd.DataFrame) -> pd.DataFrame:
    race_order = (
        df[["raceId", "date", "year", "round"]]
        .drop_duplicates()
        .sort_values(["date", "year", "round", "raceId"])
        .reset_index(drop=True)
    )
    race_order["race_seq"] = range(1, len(race_order) + 1)
    return race_order[["raceId", "race_seq"]]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create leakage-safe decoupled features from preprocessed race entries."""
    _validate_required_columns(df)

    features = df.copy()
    features["date"] = pd.to_datetime(features["date"], errors="coerce")
    features = features.sort_values(["date", "year", "round", "raceId", "driverId"])

    features = features.merge(_race_sequence(features), on="raceId", how="left")
    features["dnf_flag"] = (~features["finished"].astype(bool)).astype(float)

    driver_sorted = features.sort_values(["driverId", "race_seq"])
    features["driver_form_3races"] = (
        driver_sorted.groupby("driverId")["positionOrder"]
        .transform(lambda s: s.shift(1).ewm(alpha=0.6, adjust=False, min_periods=1).mean())
    )

    circuit_sorted = features.sort_values(["driverId", "circuit_name", "race_seq"])
    features["circuit_historical_avg"] = (
        circuit_sorted.groupby(["driverId", "circuit_name"])["positionOrder"]
        .transform(lambda s: s.shift(1).expanding(min_periods=1).mean())
    )

    constructor_sorted = features.sort_values(["constructorId", "race_seq"])
    features["constructor_points_current"] = (
        constructor_sorted.groupby("constructorId")["points"]
        .transform(lambda s: s.shift(1).cumsum())
    )
    features["constructor_dnf_rate_10races"] = (
        constructor_sorted.groupby("constructorId")["dnf_flag"]
        .transform(lambda s: s.shift(1).rolling(window=10, min_periods=3).mean())
    )

    features["grid_position"] = pd.to_numeric(features["grid"], errors="coerce")

    return features


def select_model_matrix(
    df: pd.DataFrame,
    feature_columns: Sequence[str] | None = None,
    target_column: str = "positionOrder",
    drop_na: bool = True,
) -> tuple[pd.DataFrame, pd.Series]:
    """Return model-ready X/y with identifier leakage guardrails."""
    if feature_columns is None:
        feature_columns = MODEL_FEATURE_COLUMNS

    unknown_features = [column for column in feature_columns if column not in df.columns]
    if unknown_features:
        raise ValueError(f"Missing model features: {unknown_features}")
    if target_column not in df.columns:
        raise ValueError(f"Missing target column: {target_column}")

    model_df = df.copy()
    if drop_na:
        model_df = model_df.dropna(subset=list(feature_columns) + [target_column])

    x = model_df.loc[:, list(feature_columns)].copy()
    y = pd.to_numeric(model_df[target_column], errors="coerce")

    leaky_in_matrix = sorted(LEAKY_IDENTIFIER_COLUMNS.intersection(x.columns))
    if leaky_in_matrix:
        raise ValueError(f"Leaky identifier columns detected in feature matrix: {leaky_in_matrix}")

    return x, y
