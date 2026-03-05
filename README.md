# Hybrid Recommender System: Data-Only Repository

This repository contains the complete data package used in the hybrid recommender system experiments, including raw source files and finalized derived artifacts.

Repository URL:

`https://github.com/AhmedDonkol/hybrid_recommender_system_data_only`

## Purpose

The repository is intentionally data-only. It is designed to provide:
- source dataset files,
- standardized tabular artifacts,
- matrix/array artifacts used for recommendation experiments,
- transparent provenance and integrity verification.

## Source Dataset

Primary source:
- LastFM-2K HetRec 2011 (GroupLens): `https://grouplens.org/datasets/hetrec-2011/`

Source files included here:
- `data/hetrec2011-lastfm-2k.zip`
- `data/artists.dat`
- `data/tags.dat`
- `data/user_artists.dat`
- `data/user_taggedartists.dat`
- `data/user_taggedartists-timestamps.dat`
- `data/user_friends.dat`
- `data/readme.txt`

## How the Data Were Generated

The finalized data package was produced in four deterministic stages.

1. Canonical schema construction (artist-level to project item schema):
- LastFM artist IDs are used as `track_id` (item ID in the project schema).
- Artist tags are aggregated from user tagging records.
- Item year is set from the median tagging year (fallback defaults applied where needed).
- Audio-style attributes are generated deterministically from artist IDs (fixed seed strategy), then clipped to realistic ranges.
- Outputs:
  - `data/Music Info.csv`
  - `data/User Listening History.csv`

2. Metadata cleaning and normalization:
- Duplicate/unused fields are removed.
- Missing tags are imputed with `no_tags`.
- Text normalization is applied for consistent matching.
- Output:
  - `data/cleaned_data.csv`

3. Content feature representation:
- Mixed-type feature processing is applied (count/frequency encoding, one-hot encoding, TF-IDF for tags, and numeric scaling).
- Output:
  - `data/transformed_data.npz`

4. Collaborative interaction representation:
- Track IDs are aligned to listening-history support.
- Sparse track-by-user playcount matrix is built.
- Outputs:
  - `data/collab_filtered_data.csv`
  - `data/track_ids.npy`
  - `data/interaction_matrix.npz`

## Data Inventory (Final Artifacts)

| File | Type | Description |
|---|---|---|
| `data/Music Info.csv` | Derived table | Canonical item metadata/features |
| `data/User Listening History.csv` | Derived table | Canonical user-item interactions |
| `data/cleaned_data.csv` | Derived table | Cleaned item metadata table |
| `data/collab_filtered_data.csv` | Derived table | Item table aligned with collaborative matrix indexing |
| `data/track_ids.npy` | Derived array | Row index to track ID mapping |
| `data/interaction_matrix.npz` | Derived sparse matrix | Collaborative interaction matrix |
| `data/transformed_data.npz` | Derived sparse matrix | Content feature matrix |

## Provenance

Detailed lineage is documented in:
- [DATA_PROVENANCE.md](DATA_PROVENANCE.md)

## Integrity Verification

SHA-256 checksums for all files in `data/` are provided in:
- [CHECKSUMS.sha256](CHECKSUMS.sha256)

## License and Usage

This repository includes third-party data from LastFM-2K HetRec 2011.

- According to the included HetRec README (`data/readme.txt`), the dataset is available for non-commercial use.
- For commercial use, follow the original dataset contact and licensing instructions from the source provider.
