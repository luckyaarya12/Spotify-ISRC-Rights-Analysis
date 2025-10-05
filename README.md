Spotify Music Rights Analysis: Arijit Singh Catalog vs. Unclaimed Works
Project Goal
This project automates the retrieval and cross-referencing of a major artist's music catalog against a large public dataset of unclaimed music publishing rights (unclaimedmusicalworkrightshares.tsv). The primary objective was to identify any tracks where the International Standard Recording Code (ISRC) was present in the unclaimed works dataset.
Methodology & Key Technical Achievements
This analysis was built using Python, leveraging the Spotipy and Pandas libraries for efficiency.
Data Retrieval Scope: The solution successfully retrieved a comprehensive catalog of 980 unique tracks for the artist Arijit Singh, covering all album, single, and compilation releases.
Efficient Cross-Referencing: The 9.3 million record TSV file was loaded into a Pandas DataFrame and indexed by the ISRC code to achieve near O(1) time complexity lookups during the cross-reference phase.
Data Integrity Fix (Problem-Solving): A critical .drop_duplicates() operation was implemented prior to indexing to resolve a ValueError caused by duplicate ISRC entries in the raw dataset. This ensured the stability and accuracy of the lookup process.
Final Result
The cross-referencing analysis found zero (0) tracks from the Arijit Singh catalog that matched entries in the unclaimed works dataset.
Repository Contents
Project_script.py: The full Python script containing the Spotify API connection, data processing, and analysis logic.
Unclaimed_Music_Rights_Analysis.xlsx: The final report, including the full catalog, match results, and a detailed process notes sheet.
Requirements
Python 3.x
Spotipy
Pandas
Requires a valid Spotify Developer API Client ID and Secret.
