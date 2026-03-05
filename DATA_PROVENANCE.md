# Data Provenance and Processing

This document describes where each artifact came from and how it was produced.

## Source Dataset

- Dataset: LastFM-2K HetRec 2011
- Official source: https://grouplens.org/datasets/hetrec-2011/
- Local source files in this repo:
  - `artists.dat`
  - `tags.dat`
  - `user_artists.dat`
  - `user_taggedartists.dat`
  - `user_taggedartists-timestamps.dat`
  - `user_friends.dat`
  - `readme.txt`

## Conversion to Project Schema

Outputs:

- `data/Music Info.csv`
- `data/User Listening History.csv`

Key logic:

1. Uses LastFM artist-level records as items (`track_id` in project schema).
2. Aggregates artist tags from user tagging events.
3. Uses median tag year as a year proxy.
4. Generates deterministic synthetic audio features seeded by artist ID.
5. Exports canonical project CSV files used by downstream processing.

## Downstream Processed Files

### Step 1: Cleaning

Input:

- `data/Music Info.csv`

Output:

- `data/cleaned_data.csv`

### Step 2: Content Feature Matrix

Input:

- `data/cleaned_data.csv`

Output:

- `data/transformed_data.npz`

Method summary:

- ColumnTransformer combining frequency/count encoding, one-hot encoding, TF-IDF on tags, and numeric scaling.

### Step 3: Collaborative Artifacts

Inputs:

- `data/User Listening History.csv`
- `data/cleaned_data.csv`

Outputs:

- `data/collab_filtered_data.csv`
- `data/track_ids.npy`
- `data/interaction_matrix.npz`

Method summary:

- Builds a sparse track-by-user interaction matrix from playcounts.
- Saves track ID mapping aligned with matrix row order.

## Notes

- This repository is intentionally data-only.
- Processed files reflect the finalized pipeline outputs used in the reported experiments.
