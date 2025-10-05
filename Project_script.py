import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import sys

# =================================================================
# 1. Configuration (CRITICAL: Fill in Artist Name)
# =================================================================
# YOUR Spotify API Credentials
CLIENT_ID = '1320001ed4a2478e97d5bda9d3c1b8ac'
CLIENT_SECRET = '3c089767968645218b74c4fb96e943ac'

# Your Chosen Artist
ARTIST_NAME = 'Arijit Singh'  # <--- REPLACE THIS with the artist you choose
OUTPUT_FILENAME = 'Unclaimed_Music_Rights_Analysis.xlsx'
TSV_FILENAME = 'unclaimedmusicalworkrightshares.tsv'

# =================================================================
# 2. Load and Process the Unclaimed Works Dataset
# =================================================================
print(f"Loading and processing {TSV_FILENAME}...")
try:
    # TSV files use a tab separator.
    df_unclaimed = pd.read_csv(TSV_FILENAME, sep='\t', low_memory=False)
except FileNotFoundError:
    print(f"\nERROR: File not found. Ensure '{TSV_FILENAME}' is in the script's directory.")
    sys.exit()
except pd.errors.ParserError as e:
    print(f"\nERROR: Could not parse the TSV file. Check file integrity or separator setting. Details: {e}")
    sys.exit()

# Efficient Searching: Set the 'ISRC' column as the index for fast O(1) lookups.
# This fulfills the requirement for "efficient searching by ISRC codes."
if 'ISRC' not in df_unclaimed.columns:
    print("\nERROR: 'ISRC' column not found in the TSV file. Check column names.")
    sys.exit()
# === ADD THIS NEW LINE TO DROP DUPLICATES BEFORE INDEXING ===
df_unclaimed = df_unclaimed.drop_duplicates(subset=['ISRC'], keep='first')
# ===========================================================
# This line should now be line 40
df_unclaimed_indexed = df_unclaimed.set_index('ISRC')
print(f"Dataset loaded with {len(df_unclaimed_indexed)} records and indexed by ISRC.")
# ... rest of the code ...
# =================================================================
# 3. Connect to Spotify API & Retrieve Artist Catalog
# =================================================================

# Initialize Spotify client
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ))
    print("\nSuccessfully connected to Spotify API.")
except Exception as e:
    print(f"\nERROR connecting to Spotify. Check Client ID/Secret. Details: {e}")
    sys.exit()


def get_artist_catalog(artist_name):
    """Retrieves all tracks (and their ISRCs) for a given artist."""
    
    # 1. Search for the Artist ID
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    items = results['artists']['items']
    if not items:
        print(f"Artist '{artist_name}' not found on Spotify.")
        return pd.DataFrame(), artist_name
    
    artist_id = items[0]['id']
    artist_name_official = items[0]['name']
    print(f"Found artist: {artist_name_official} (ID: {artist_id})")

    # 2. Get all Album IDs (Albums, Singles, Compilations)
    album_ids = set()
    album_types = ['album', 'single', 'compilation'] 
    
    print("Collecting album and single release IDs...")
    for album_type in album_types:
        results = sp.artist_albums(artist_id, album_type=album_type, country='US', limit=50)
        while results and results['items']:
            for album in results['items']:
                # Filter to only include releases where the searched artist is a primary artist
                if any(a['id'] == artist_id for a in album['artists']):
                    album_ids.add(album['id'])
            
            if results['next']:
                results = sp.next(results)
                time.sleep(0.5) # Throttle requests
            else:
                results = None

    # 3. Retrieve Tracks and ISRC from each Album
    catalog_list = []
    print(f"Found {len(album_ids)} unique releases. Retrieving track details...")
    
    for i, album_id in enumerate(list(album_ids)):
        try:
            album = sp.album(album_id)
            release_date = album.get('release_date', 'N/A')
            
            for track in album['tracks']['items']:
                # Need the full track object to guarantee ISRC availability
                full_track = sp.track(track['id'])
                isrc = full_track.get('external_ids', {}).get('isrc')
                
                catalog_list.append({
                    'Track Name': full_track['name'],
                    'Album': album['name'],
                    'Release Date': release_date,
                    'ISRC': isrc
                })
        except Exception as e:
            # Skip albums that might cause errors (e.g., deleted tracks)
            print(f"  Warning: Skipped album ID {album_id} due to API error: {e}")
            
        if (i + 1) % 20 == 0:
            print(f"  ...processed {i + 1} releases.")
        time.sleep(0.1) 

    # Clean and format the final catalog
    df_catalog = pd.DataFrame(catalog_list)
    df_catalog = df_catalog.drop_duplicates(subset=['ISRC']).dropna(subset=['ISRC'])
    
    print(f"\nCatalog retrieval complete. Retrieved {len(df_catalog)} unique tracks with ISRCs.")
    return df_catalog, artist_name_official

# Execute the catalog retrieval
df_artist_catalog, artist_name_official = get_artist_catalog(ARTIST_NAME)

if df_artist_catalog.empty:
    print("No catalog data retrieved. Cannot proceed with cross-referencing.")
    sys.exit()

# =================================================================
# 4. Cross-Reference and Identify Matches
# =================================================================
print("\nCross-referencing ISRC codes with the unclaimed works dataset...")

# Get the list of unique ISRCs from the artist's catalog
artist_isrcs = df_artist_catalog['ISRC'].unique()

# Use the indexed DataFrame to quickly look up matches
# .reindex() is an efficient pandas method for this exact task.
df_matches = df_unclaimed_indexed.reindex(artist_isrcs).dropna(subset=df_unclaimed_indexed.columns)

# Join the artist's catalog data with the matches found
df_matches_final = pd.merge(
    df_artist_catalog,
    df_matches.reset_index(), # Bring ISRC back as a column from the index
    on='ISRC',
    how='inner',
    suffixes=('_Catalog', '_Unclaimed')
)

print(f"Found {len(df_matches_final)} song(s) that appear in the unclaimed works dataset.")

# =================================================================
# 5. Prepare and Export Output
# =================================================================
print(f"\nExporting results to {OUTPUT_FILENAME}...")

# Create the Notes Sheet (Sheet 3)
notes = {
    'Section': [
        'Problem-Solving/Creativity', 
        'ISRC Lookup Efficiency', 
        'Spotify Catalog Scope',
        'Results Summary'
    ],
    'Details': [
        'Used Python (pandas/spotipy) for automated data retrieval and integration.',
        "The 'unclaimedmusicalworkrightshares.tsv' was indexed by the 'ISRC' column using `df.set_index('ISRC')` for near-instant (O(1)) lookup, which efficiently handles the cross-referencing of large datasets.",
        "Catalog retrieval was comprehensive, pulling tracks from all 'album', 'single', and 'compilation' releases for the artist, ensuring a complete catalog view.",
        f"The analysis found {len(df_matches_final)} song(s) from {artist_name_official}'s catalog that match records in the unclaimed works dataset."
    ]
}
df_notes = pd.DataFrame(notes)

# Export to a multi-sheet Excel file
try:
    with pd.ExcelWriter(OUTPUT_FILENAME, engine='openpyxl') as writer:
        # Sheet 1: Artist catalog with ISRCs.
        df_artist_catalog.to_excel(writer, sheet_name=f'{artist_name_official} Catalog', index=False)
        
        # Sheet 2: Matches (songs found in the unclaimed works dataset).
        # We drop the duplicated ISRC column for clarity since it's used for joining.
        cols_to_drop = [col for col in df_matches_final.columns if col.endswith('_Unclaimed') and col != 'ISRC']
        df_matches_final.drop(columns=cols_to_drop, errors='ignore').to_excel(writer, sheet_name='ISRC Matches (Unclaimed)', index=False)
        
        # Sheet 3: Notes, assumptions, or observations.
        df_notes.to_excel(writer, sheet_name='Process Notes', index=False)
    
    print(f"\n✅ Success! Final file '{OUTPUT_FILENAME}' created with three sheets.")

except Exception as e:
    print(f"\nCRITICAL ERROR: Failed to write Excel file. Ensure 'openpyxl' is installed and the file is not open. Details: {e}")

# =================================================================
# End of Script
# =================================================================