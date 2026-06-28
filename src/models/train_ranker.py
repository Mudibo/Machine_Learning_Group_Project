"""Train and explain XGBRanker and LGBMRanker for F1 veteran rankings."""

from __future__ import annotations

import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from lightgbm import LGBMRanker
from sklearn.metrics import ndcg_score
from xgboost import XGBRanker

INPUT_PATH = "data/processed/veteran_training_matrix.csv"

XGB_MODEL_PATH = "models/f1_xgb_ranker.pkl"
LGB_MODEL_PATH = "models/f1_lgb_ranker.pkl"

XGB_SHAP_PATH = "outputs/reports/xgb_shap_summary.png"
LGB_SHAP_PATH = "outputs/reports/lgb_shap_summary.png"

FEATURE_COLUMNS = [
    "grid_position",
    "quali_position",
    "driver_form_3races",
    "circuit_historical_avg",
    "constructor_points_current",
    "constructor_dnf_rate_10races",
    "circuit_type_code",
    "is_wet",
    "track_temp",
]
TARGET_COLUMN = "finish_position"
RELEVANCE_COLUMN = "relevance_score"
MODEL_TARGET_COLUMN = "model_relevance_score"


def _ensure_dirs(*paths: str) -> None:
    for path in paths:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)


def _validate_columns(df: pd.DataFrame) -> None:
    required = set(FEATURE_COLUMNS + [TARGET_COLUMN, "season", "race_id", "driver_id"])
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns for training: {missing}")


def _prepare_training_frame(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training matrix not found at {path}")

    df = pd.read_csv(path)
    _validate_columns(df)

    for column in FEATURE_COLUMNS + [TARGET_COLUMN, "season"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN]).copy()
    df[RELEVANCE_COLUMN] = 15 - df[TARGET_COLUMN]
    # LightGBM lambdarank requires non-negative labels.
    df[MODEL_TARGET_COLUMN] = df[RELEVANCE_COLUMN].clip(lower=0)

    # Required by spec: ensure race groups are contiguous by race_id.
    df = df.sort_values("race_id").reset_index(drop=True)
    return df


def _split_train_validation(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[(df["season"] >= 2022) & (df["season"] <= 2025)].copy()
    valid_df = df[df["season"] == 2026].copy()

    if train_df.empty:
        raise ValueError("No training rows found for seasons 2022-2025.")
    if valid_df.empty:
        raise ValueError(
            "No validation rows found for season 2026. "
            "Ingest 2026 completed rounds, rebuild veteran matrix, and rerun training."
        )

    train_df = train_df.sort_values("race_id").reset_index(drop=True)
    valid_df = valid_df.sort_values("race_id").reset_index(drop=True)
    return train_df, valid_df


def _group_sizes(df: pd.DataFrame) -> list[int]:
    return df.groupby("race_id", sort=False).size().astype(int).tolist()


def _compute_grouped_ndcg(valid_df: pd.DataFrame, pred_scores: np.ndarray) -> float:
    scored = valid_df.copy()
    scored["pred_score"] = pred_scores
    ndcgs: list[float] = []

    for _, race_df in scored.groupby("race_id", sort=False):
        y_true = race_df[MODEL_TARGET_COLUMN].to_numpy(dtype=float)
        y_pred = race_df["pred_score"].to_numpy(dtype=float)
        ndcgs.append(float(ndcg_score([y_true], [y_pred], k=len(race_df))))

    return float(np.mean(ndcgs))


def _compute_grouped_mrr(valid_df: pd.DataFrame, pred_scores: np.ndarray) -> float:
    scored = valid_df.copy()
    scored["pred_score"] = pred_scores
    reciprocal_ranks: list[float] = []

    for _, race_df in scored.groupby("race_id", sort=False):
        predicted = race_df.sort_values("pred_score", ascending=False).reset_index(drop=True)
        winner_index = predicted.index[predicted[RELEVANCE_COLUMN] == 14]
        if len(winner_index) == 0:
            reciprocal_ranks.append(0.0)
        else:
            reciprocal_ranks.append(1.0 / float(winner_index[0] + 1))

    return float(np.mean(reciprocal_ranks))


def _save_shap_summary(model, x_valid: pd.DataFrame, output_path: str, model_name: str) -> None:
    _ensure_dirs(output_path)

    if model_name == "xgb":
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(x_valid)
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, x_valid, show=False)
    else:
        try:
            explainer = shap.TreeExplainer(model, feature_perturbation="interventional")
            shap_values = explainer.shap_values(x_valid)
            plt.figure(figsize=(10, 6))
            shap.summary_plot(shap_values, x_valid, show=False)
        except Exception:
            explainer = shap.Explainer(model.predict, x_valid)
            explanation = explainer(x_valid)
            plt.figure(figsize=(10, 6))
            shap.plots.beeswarm(explanation, max_display=len(FEATURE_COLUMNS), show=False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def train_rankers(input_path: str = INPUT_PATH) -> dict[str, float]:
    df = _prepare_training_frame(input_path)
    train_df, valid_df = _split_train_validation(df)

    x_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[MODEL_TARGET_COLUMN]
    x_valid = valid_df[FEATURE_COLUMNS]
    y_valid = valid_df[MODEL_TARGET_COLUMN]

    train_group = _group_sizes(train_df)
    valid_group = _group_sizes(valid_df)

    xgb_model = XGBRanker(
        objective="rank:pairwise",
        n_estimators=100,
        learning_rate=0.05,
        random_state=42,
    )
    lgb_model = LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        n_estimators=100,
        learning_rate=0.05,
        random_state=42,
    )

    xgb_model.fit(
        x_train,
        y_train,
        group=train_group,
        eval_set=[(x_valid, y_valid)],
        eval_group=[valid_group],
        verbose=False,
    )
    lgb_model.fit(
        x_train,
        y_train,
        group=train_group,
        eval_set=[(x_valid, y_valid)],
        eval_group=[valid_group],
    )

    xgb_pred = xgb_model.predict(x_valid)
    lgb_pred = lgb_model.predict(x_valid)

    xgb_ndcg = _compute_grouped_ndcg(valid_df, xgb_pred)
    lgb_ndcg = _compute_grouped_ndcg(valid_df, lgb_pred)

    xgb_mrr = _compute_grouped_mrr(valid_df, xgb_pred)
    lgb_mrr = _compute_grouped_mrr(valid_df, lgb_pred)

    _save_shap_summary(xgb_model, x_valid, XGB_SHAP_PATH, model_name="xgb")
    _save_shap_summary(lgb_model, x_valid, LGB_SHAP_PATH, model_name="lgb")

    _ensure_dirs(XGB_MODEL_PATH, LGB_MODEL_PATH)
    with open(XGB_MODEL_PATH, "wb") as file_obj:
        pickle.dump(
            {
                "model": xgb_model,
                "features": FEATURE_COLUMNS,
                "target": RELEVANCE_COLUMN,
                "model_target": MODEL_TARGET_COLUMN,
            },
            file_obj,
        )

    with open(LGB_MODEL_PATH, "wb") as file_obj:
        pickle.dump(
            {
                "model": lgb_model,
                "features": FEATURE_COLUMNS,
                "target": RELEVANCE_COLUMN,
                "model_target": MODEL_TARGET_COLUMN,
            },
            file_obj,
        )

    print("Training completed for both rankers with relevance_score = 15 - finish_position.")
    print(f"Train rows (2022-2025): {len(train_df)}")
    print(f"Validation rows (2026): {len(valid_df)}")
    print("Validation Metrics (2026):")
    print(f"XGBRanker NDCG: {xgb_ndcg:.6f} | MRR: {xgb_mrr:.6f}")
    print(f"LGBMRanker NDCG: {lgb_ndcg:.6f} | MRR: {lgb_mrr:.6f}")
    print(f"XGB model saved to: {XGB_MODEL_PATH}")
    print(f"LGB model saved to: {LGB_MODEL_PATH}")
    print(f"XGB SHAP summary saved to: {XGB_SHAP_PATH}")
    print(f"LGB SHAP summary saved to: {LGB_SHAP_PATH}")

    return {
        "xgb_ndcg": xgb_ndcg,
        "xgb_mrr": xgb_mrr,
        "lgb_ndcg": lgb_ndcg,
        "lgb_mrr": lgb_mrr,
    }


if __name__ == "__main__":
    custom_input_path = os.environ.get("VETERAN_MATRIX_INPUT_PATH", INPUT_PATH)
    train_rankers(input_path=custom_input_path)