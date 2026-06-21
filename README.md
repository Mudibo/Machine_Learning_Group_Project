# Project Title: Explainable Prediction of Formula 1 Race Outcomes

A Machine Learning semester project investigating whether machine learning models can predict Formula 1 race finishing positions from pre-race features and identifying which factors most strongly drive those predictions.

## Problem Statement

Formula 1 race outcomes are shaped by a complex interaction of factors including driver skill, team performance, qualifying position, circuit characteristics and historical form. While outcomes are often discussed in terms of single dominant factors ("starting position matters most"), the relative contribution of each factor is rarely quantified transparently. This project investigates whether machine learning models can predict race finishing positions from features available before a race starts and uses SHAP-based explainability to identify which factors most strongly drive those predictions. The aim is not only to model outcomes but to make the model's reasoning visible, turning prediction into an interpretable analysis of what shapes race results.

## Research Question

Can an explainable machine learning model predict Formula 1 race finishing positions from pre-race features and which factors most strongly influence its predictions?

## Dataset

This project uses a single secondary-source dataset. See `data/README.md` for full details on the source, schema and how to obtain it.

- **Formula 1 World Championship (1950–2024)** — a normalised relational dataset originally maintained by the Ergast Motor Racing Developer API, mirrored on Kaggle. Covers every Formula 1 season from 1950 onwards, with race results, qualifying, drivers, constructors and circuits. Approximately 25,000 driver-race entries.

## Team and Sprint Structure

The project runs across three one-week sprints (15 June – 3 July 2026).

| Sprint | Dates | Focus | Lead |
|---|---|---|---|
| 1 | 15–21 June | Dataset Acquisition, EDA & Data Cleaning | Sharon |
| 2 | 22–26 June | Data Preprocessing, Feature Engineering & Model Development | Cyprian, Sean |
| 3 | 29 June – 3 July | Model Evaluation, Visualization & Final Presentation | Amy |

Team members and their ownership areas:

- **Sharon** — Dataset Acquisition, EDA & Data Cleaning
- **Cyprian** — Data Preprocessing & Feature Engineering
- **Sean** — Model Development & Hyperparameter Tuning
- **Amy** — Model Evaluation, Visualization & Final Reporting

## Repository Structure

```
.
├── data/             # Datasets (raw not committed; processed produced during sprints)
│   ├── raw/
│   └── processed/
├── docs/             # Project documentation, sprint plans, workflow guides
├── models/           # Trained model artifacts saved during Sprint 2
├── notebooks/        # Jupyter notebooks for EDA, modeling and evaluation
├── presentation/     # Final presentation slides and supporting materials
├── reports/          # Sprint reports, EDA reports and final write-up
├── src/              # Reusable Python modules and utility scripts
├── .gitignore
├── README.md
└── requirements.txt  # Python dependencies for the project
```