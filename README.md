# Project Title: Explainable Detection of Attention-Capture Techniques in Social Media Text

A Machine Learning semester project investigating whether machine learning models can detect attention-capture techniques in social media text and identify the linguistic features responsible for those decisions.

## Problem Statement

Social media platforms increasingly rely on linguistic techniques such as curiosity gaps, emotional triggers, urgency cues, and sensational wording to capture user attention. While these techniques are effective at driving engagement, they often operate invisibly to users. Existing detection systems typically focus on classifying content as clickbait or non-clickbait without explaining the linguistic signals that influenced the prediction. This project investigates whether machine learning can detect attention-capture language in social media text and identify the specific features responsible for its decisions, thereby improving transparency and digital media literacy.

## Research Question

Can an explainable machine learning model reliably detect attention-capture techniques in social media text, and which linguistic features most strongly influence its predictions?

## Datasets

This project uses two secondary-source datasets. See `data/README.md` for full details on sources, schemas, and how to obtain them.

- **Webis Clickbait Challenge 2017** (primary) — ~38,000 Twitter posts from US news outlets, with continuous and binary clickbait labels from five human annotators per post.
- **Anand Kaggle Clickbait Headlines** (secondary) — ~32,000 news headlines with binary clickbait labels, used for cross-domain corroboration.

## Team and Sprint Structure

The project runs across three one-week sprints (15 June – 3 July 2026).

| Sprint | Dates | Focus | Lead |
|---|---|---|---|
| 1 | 15–19 June | Dataset Acquisition, EDA & Data Cleaning | Sharon |
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
├── notebooks/        # Jupyter notebooks for EDA, modeling, and evaluation
├── presentation/     # Final presentation slides and supporting materials
├── reports/          # Sprint reports, EDA reports, and final write-up
├── src/              # Reusable Python modules and utility scripts
├── .gitignore
├── README.md
└── requirements.txt  # Python dependencies for the project
```