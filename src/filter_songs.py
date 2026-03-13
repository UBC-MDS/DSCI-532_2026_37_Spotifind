import pandas as pd

def filter_songs(df: pd.DataFrame, danceability = (0.0, 1.0), energy = (0.0, 1.0), valence = (0.0, 1.0),
    acousticness  = (0.0, 1.0), tempo = (0, 250), duration_s = (0, 600), popularity = (0, 100), genre = "All") -> pd.DataFrame:
    
    """
    Filter the Spotify songs data set by audio features, track properties, and genres.

    All parameter have contraint range of values that user can input (or slider control).
    Choosing genre = "All" means display songs from all genres at default.

    Examples
    --------
    >>> import pandas as pd
    >>> example_df = {[
                       {"danceability": 0.9, "energy": 0.8, "valence": 0.5,
                       "acousticness": 0.1, "tempo": 120, "duration_s": 250,
                       "track_popularity": 80, "playlist_genre": "pop"},

                       {"danceability": 0.2, "energy": 0.5, "valence": 0.2,
                       "acousticness": 0.1, "tempo": 100, "duration_s": 300,
                       "track_popularity": 80, "playlist_genre": "edm"}
                       ]}

    >>> df = pd.DataFrame([example_df])
    >>> len(filter_songs(df, genre="pop"))
    1
    >>> len(filter_songs(df, energy < 0.2))
    0
    """
    data = df[
        (df["danceability"].between(*danceability)) &
        (df["energy"].between(*energy)) &
        (df["valence"].between(*valence)) &
        (df["acousticness"].between(*acousticness)) &
        (df["tempo"].between(*tempo)) &
        (df["duration_s"].between(*duration_s)) &
        (df["track_popularity"].between(*popularity))
    ]
    if genre != "All":
        data = data[data["playlist_genre"] == genre]
    return data