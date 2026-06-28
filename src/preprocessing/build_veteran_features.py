"""Build veteran-only training matrix with leakage-safe engineered features."""

import os

import pandas as pd

VETERAN_DRIVER_IDS = {
    "verstappen",
    "hamilton",
    "leclerc",
    "norris",
    "russell",
    "sainz",
    "perez",
    "bottas",
    "alonso",
    "stroll",
    "ocon",
    "gasly",
    "albon",
    "hulkenberg",
}

DRIVER_ID_ALIASES = {
    "max_verstappen": "verstappen",
}

MECHANICAL_DNF_KEYWORDS = (
    "engine",
    "gearbox",
    "hydraul",
    "power unit",
    "transmission",
    "clutch",
    "driveshaft",
    "electrical",
    "battery",
    "ers",
    "turbo",
    "brake",
    "suspension",
    "cooling",
    "water leak",
    "fuel",
    "oil leak",
    "exhaust",
    "throttle",
)

CIRCUIT_TYPE_MAP = {
    "silverstone": "Power/High-Speed",
    "monza": "Power/High-Speed",
    "spa": "Power/High-Speed",
    "red_bull_ring": "Power/High-Speed",
    "monaco": "High-Downforce",
    "hungaroring": "High-Downforce",
    "marina_bay": "High-Downforce",
    "suzuka": "Balanced/Technical",
    "catalunya": "Balanced/Technical",
    "circuit_americas": "Balanced/Technical",
    "jeddah": "Street Circuit",
    "baku": "Street Circuit",
    "miami": "Street Circuit",
}

CIRCUIT_TYPE_CODE = {
    "Power/High-Speed": 0,
    "High-Downforce": 1,
    "Balanced/Technical": 2,
    "Street Circuit": 3,
}

REQUIRED_COLUMNS = {
    "race_id",
    "season",
    "round",
    "circuit_id",
    "driver_id",
    "constructor_id",
    "finish_position",
    "points",
    "status_str",
    "grid_position",
    "quali_position",
    "is_wet",
    "track_temp",
}


def _validate_columns(df):
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns in canonical input: {missing}")


def _safe_numeric_cast(df):
    casted = df.copy()
    for column in [
        "season",
        "round",
        "finish_position",
        "points",
        "grid_position",
        "quali_position",
        "is_wet",
        "track_temp",
    ]:
        casted[column] = pd.to_numeric(casted[column], errors="coerce")
    return casted


def _add_mechanical_dnf_flag(df):
    status_text = df["status_str"].astype("string").str.lower()
    pattern = "|".join(MECHANICAL_DNF_KEYWORDS)
    flagged = df.copy()
    flagged["constructor_mechanical_dnf"] = status_text.str.contains(pattern, regex=True, na=False).astype(int)
    return flagged


def build_veteran_training_matrix(input_csv_path, output_csv_path):
    """Create processed veteran training matrix from canonical raw dataset."""
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Canonical input file not found: {input_csv_path}")

    df = pd.read_csv(input_csv_path)
    if "is_wet" not in df.columns:
        df["is_wet"] = 0
    if "track_temp" not in df.columns:
        df["track_temp"] = 25.0

    _validate_columns(df)
    df = _safe_numeric_cast(df)

    df["driver_id"] = df["driver_id"].astype("string").str.lower().str.strip()
    df["driver_id"] = df["driver_id"].replace(DRIVER_ID_ALIASES)
    df["constructor_id"] = df["constructor_id"].astype("string").str.lower().str.strip()
    df["circuit_id"] = df["circuit_id"].astype("string").str.lower().str.strip()

    df["is_wet"] = df["is_wet"].fillna(0).astype(int)
    df["track_temp"] = df["track_temp"].fillna(25.0).astype(float)
    df["circuit_type"] = df["circuit_id"].map(CIRCUIT_TYPE_MAP).fillna("Balanced/Technical")
    df["circuit_type_code"] = df["circuit_type"].map(CIRCUIT_TYPE_CODE).fillna(2).astype(int)

    circuit_dummies = pd.get_dummies(df["circuit_type"], prefix="circuit_type", dtype=int)
    df = pd.concat([df, circuit_dummies], axis=1)

    veteran_df = df[df["driver_id"].isin(VETERAN_DRIVER_IDS)].copy()
    veteran_df = veteran_df.sort_values(["season", "round", "race_id", "driver_id"]).reset_index(drop=True)

    veteran_df["driver_form_3races"] = (
        veteran_df.sort_values(["driver_id", "season", "round", "race_id"])
        .groupby("driver_id")["finish_position"]
        .transform(lambda s: s.shift(1).rolling(window=3, min_periods=1).mean())
    )

    veteran_df["circuit_historical_avg"] = (
        veteran_df.sort_values(["driver_id", "circuit_id", "season", "round", "race_id"])
        .groupby(["driver_id", "circuit_id"])["finish_position"]
        .transform(lambda s: s.shift(1).expanding(min_periods=1).mean())
    )

    veteran_df["constructor_points_current"] = (
        veteran_df.sort_values(["season", "constructor_id", "round", "race_id", "driver_id"])
        .groupby(["season", "constructor_id"])["points"]
        .transform(lambda s: s.shift(1).cumsum().fillna(0.0))
    )

    veteran_df = _add_mechanical_dnf_flag(veteran_df)
    veteran_df["constructor_dnf_rate_10races"] = (
        veteran_df.sort_values(["constructor_id", "season", "round", "race_id", "driver_id"])
        .groupby("constructor_id")["constructor_mechanical_dnf"]
        .transform(lambda s: s.shift(1).rolling(window=10, min_periods=3).mean())
    )

    veteran_df = veteran_df.drop_duplicates(subset=["race_id", "driver_id"], keep="last")
    veteran_df = veteran_df.sort_values(["season", "round", "race_id", "driver_id"]).reset_index(drop=True)

    output_dir = os.path.dirname(output_csv_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    veteran_df.to_csv(output_csv_path, index=False)
    return veteran_df


if __name__ == "__main__":
    input_path = os.environ.get("CANONICAL_INPUT_CSV_PATH", "data/raw/f1_canonical_master.csv")
    output_path = os.environ.get("VETERAN_OUTPUT_CSV_PATH", "data/processed/veteran_training_matrix.csv")

    default_is_wet = int(os.environ.get("SIM_DEFAULT_IS_WET", "0"))
    default_track_temp = float(os.environ.get("SIM_DEFAULT_TRACK_TEMP", "25.0"))

    output_df = build_veteran_training_matrix(input_csv_path=input_path, output_csv_path=output_path)
    output_df["is_wet"] = output_df["is_wet"].fillna(default_is_wet).astype(int)
    output_df["track_temp"] = output_df["track_temp"].fillna(default_track_temp).astype(float)
    output_df.to_csv(output_path, index=False)
    print("Veteran feature matrix build completed.")
    print(f"Rows in processed output dataframe: {len(output_df)}")
    print(f"Output file: {output_path}")