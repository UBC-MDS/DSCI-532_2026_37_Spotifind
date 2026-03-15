import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.filter_songs import filter_songs

@pytest.fixture
def example_df():
    song_a = {"danceability": 0.9, "energy": 0.8, "valence": 0.5,
               "acousticness": 0.1, "tempo": 120, "duration_s": 250,
               "track_popularity": 80, "playlist_genre": "pop"}

    song_b = {"danceability": 0.2, "energy": 0.5, "valence": 0.2,
               "acousticness": 0.1, "tempo": 100, "duration_s": 300,
               "track_popularity": 80, "playlist_genre": "edm"}
    
    song_c = {"danceability": 0.5, "energy": 0.6, "valence": 0.4,
               "acousticness": 0.3, "tempo": 90, "duration_s": 200,
               "track_popularity": 40, "playlist_genre": "latin"}

    return pd.DataFrame([song_a, song_b, song_c])

def test_genre_filter(example_df):
    """Test if the genre filter drop box return the correct rows in regard with the genre chosen"""
    result = filter_songs(example_df, genre="pop")
    assert len(result) == 1

def test_slider_control(example_df):
    """Test if the filter function return the correct number of rows after applied filtering with default value"""

    result = filter_songs(example_df, energy = (0.0,0.7))
    assert len(result) == 2
    assert "pop" not in result["playlist_genre"].values

def test_empty_result(example_df):
    """Test extreme filter returns 0 songs without crashing the app."""
    result = filter_songs(example_df, duration_s =(0, 1))
    assert len(result) == 0