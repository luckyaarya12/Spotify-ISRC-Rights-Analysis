# ----------------------------------------------------------------------
# FINAL README.md CONTENT FOR GITHUB (CODE STYLE)
# ----------------------------------------------------------------------

# Spotify-ISRC-Rights-Analysis

## Project_Goal
This project automates the retrieval and cross-referencing of a major artist's music catalog against a large public dataset of unclaimed music publishing rights (`unclaimedmusicalworkrightshares.tsv`). The primary objective was to identify any tracks where the International Standard Recording Code (ISRC) was present in the unclaimed works dataset.

## Methodology_and_Achievements
* **Language**: Python 3.x.
* **Libraries**: `Spotipy` (for Spotify Web API) and `Pandas` (for data processing).
* **Catalog_Scope**: Retrieved a comprehensive catalog of **980 unique tracks** for the artist Arijit Singh.
* **Efficiency**: Achieved near **$\text{O}(1)$ time complexity** lookups by indexing the 9.3+ million record TSV file using the ISRC column.
* **Problem_Solving**: Implemented a critical **`.drop_duplicates()`** operation to resolve a `ValueError` caused by duplicate ISRC labels in the raw data, ensuring a stable index for matching.

## Final_Result
The cross-referencing analysis found **zero (0) tracks** from the analyzed catalog that matched entries in the unclaimed works dataset.

## Repository_Contents
* `Project_script.py`: The complete script containing the API logic and analysis.
* `Unclaimed_Music_Rights_Analysis.xlsx`: The final three-sheet report (Catalog, Matches, Process Notes).

## Requirements
* Python 3.x
* `Spotipy`
* `Pandas`
* Valid Spotify Developer API Client ID and Secret.

# ----------------------------------------------------------------------
