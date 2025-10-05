# Spotify Music Rights Analysis: Arijit Singh Catalog vs. Unclaimed Works

## Project Goal
This project automates the retrieval and cross-referencing of a major artist's music catalog against a large public dataset of unclaimed music publishing rights. The primary objective was to identify any tracks where the ISRC code was present in the unclaimed works dataset.

## Methodology & Key Technical Achievements
This analysis was built using Python, leveraging the `Spotipy` and `Pandas` libraries for efficiency.

* **Data Retrieval Scope:** The solution successfully retrieved a comprehensive catalog of 980 unique tracks for the artist Arijit Singh.
* **Efficient Cross-Referencing (O(1) Lookup):** The 9.3+ million record TSV file was indexed by the ISRC code for high performance.
* **Data Integrity Fix (Problem-Solving):** A critical **`.drop_duplicates()`** operation was implemented to ensure a stable index by resolving a `ValueError` caused by duplicate ISRC entries in the raw data.

## Final Result
The cross-referencing analysis found **zero (0) tracks** from the analyzed catalog that matched entries in the unclaimed works dataset.
