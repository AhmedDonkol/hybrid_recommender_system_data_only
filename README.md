# Hybrid Recommender System: Data-Only Repository

This repository contains the dataset artifacts used for the hybrid recommender system experiments and manuscript.

Repository URL:

`https://github.com/AhmedDonkol/hybrid_recommender_system_data_only`

## Scope

This is a data-only repository. It includes:
- third-party source files from LastFM-2K HetRec 2011,
- converted tabular files used by the project schema,
- processed matrices/arrays used by recommender training and inference.

## Data Inventory

| File | Type | Role |
|---|---|---|
| `data/hetrec2011-lastfm-2k.zip` | Raw archive | Original LastFM-2K HetRec package |
| `data/artists.dat` | Raw table | Artist metadata from HetRec |
| `data/tags.dat` | Raw table | Tag dictionary |
| `data/user_artists.dat` | Raw table | User-artist listening counts |
| `data/user_taggedartists.dat` | Raw table | User tagging events |
| `data/user_taggedartists-timestamps.dat` | Raw table | Tagging timestamps |
| `data/user_friends.dat` | Raw table | User friendship links |
| `data/readme.txt` | Raw doc | Dataset README distributed with HetRec |
| `data/Music Info.csv` | Derived table | Item metadata/features in project schema |
| `data/User Listening History.csv` | Derived table | User-item interaction table in project schema |
| `data/cleaned_data.csv` | Derived table | Cleaned metadata for downstream modeling |
| `data/collab_filtered_data.csv` | Derived table | Item table aligned to collaborative track IDs |
| `data/interaction_matrix.npz` | Derived sparse matrix | Track-by-user interaction matrix |
| `data/track_ids.npy` | Derived array | Track ID index mapping for matrix rows |
| `data/transformed_data.npz` | Derived sparse matrix | Content feature matrix after preprocessing |

## Processing Lineage

Processing lineage is documented in detail in:

- [DATA_PROVENANCE.md](DATA_PROVENANCE.md)

## License and Usage

This repository includes third-party data from LastFM-2K HetRec 2011.

- The HetRec README states the data are available for non-commercial use.
- For commercial usage, follow the original dataset terms and contact instructions in `data/readme.txt`.
- This repository provides redistributed artifacts for research/reproducibility use.

## Integrity

File checksums are provided in:

- [CHECKSUMS.sha256](CHECKSUMS.sha256)
