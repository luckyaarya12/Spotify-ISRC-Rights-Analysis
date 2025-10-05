Spotify Music Rights Analysis: Arijit Singh Catalog vs. Unclaimed Works
Project Goal
This project automates the retrieval and cross-referencing of a major artist's music catalog against a large public dataset of unclaimed music publishing rights. The primary objective was to identify any tracks where the ISRC code was present in the unclaimed works dataset.

Methodology & Key Technical Achievements
This analysis was built using Python, leveraging the Spotipy and Pandas libraries for efficiency.

Data Retrieval Scope: The solution successfully retrieved a comprehensive catalog of 980 unique tracks for the artist Arijit Singh.

Efficient Cross-Referencing (O(1) Lookup): The 9.3+ million record TSV file was indexed by the ISRC code to achieve near O(1) time complexity lookups.

Data Integrity Fix (Problem-Solving): A critical .drop_duplicates() operation was implemented prior to indexing to resolve a ValueError caused by duplicate ISRC entries. This ensured the stability and accuracy of the lookup process.

Final Result
The cross-referencing analysis found zero (0) tracks from the analyzed catalog that matched entries in the unclaimed works dataset.

Repository Contents
Project_script.py: The full Python script containing the Spotify API connection, data processing, and analysis logic.

Unclaimed_Music_Rights_Analysis.xlsx: The final report, including the full catalog, match results, and a detailed process notes sheet.

Requirements
Python 3.x

Spotipy

Pandas

Requires a valid Spotify Developer API Client ID and Secret.
