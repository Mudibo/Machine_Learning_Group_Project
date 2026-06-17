# Raw Data

This directory holds the original, unmodified datasets as downloaded from
their sources. Files are not committed to the repository — each team member
downloads them locally per the instructions in `../README.md`.

## Expected Contents

After downloading and unzipping, this folder should contain:

### From Webis Clickbait Challenge 2017
- `clickbait17-train-170331/`
  - `instances.jsonl` — one tweet per line, with post text, target article
    title, paragraphs, keywords, and timestamps.
  - `truth.jsonl` — one record per tweet, with annotator judgments,
    `truthMean` (continuous 0–1 clickbait score), and `truthClass`
    (binary label).
- `clickbait17-test-170720/`
  - Same structure as the training split.

Join `instances.jsonl` and `truth.jsonl` on the `id` field to produce a
working dataframe.

### From Anand Kaggle Clickbait
- `clickbait_data.csv` (or similarly named) with columns:
  - `headline` — the news headline text
  - `clickbait` — binary label (1 = clickbait, 0 = not clickbait)

## Do Not Modify
Treat everything in this folder as read-only. All cleaning and
transformation outputs belong in `../processed/`.