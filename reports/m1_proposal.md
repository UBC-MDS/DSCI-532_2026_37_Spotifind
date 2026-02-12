# Spotifind Dashboard Proposal

## Section 1: Motivation and Purpose

**Our role:** Data science students building a tool for music industry professionals  
**Target audience:** DJs, playlist curators, and music enthusiasts

Finding the right songs on Spotify is tough. When you're making a playlist for a specific vibe like an intense workout mix or a relaxing study session, you can't just search by genre. Genre labels like "Pop" or "Rock" don't tell you if a song is energetic, danceable, or has a happy mood. Right now, people spend hours manually clicking through playlists trying to find tracks that match what they're looking for.

To solve this problem, we're building Spotifind, a dashboard that lets users search for music using Spotify's audio features instead of just genres. Users can filter songs by things like energy level, danceability, tempo, and mood (called "valence" in the data). For example, a DJ building a workout playlist can filter for high-energy songs above 140 BPM, while someone making a chill playlist can look for acoustic tracks with low energy. Our dashboard turns these technical audio measurements into easy-to-use filters and visualizations, making it way faster to discover the perfect tracks.

## Section 2: Description of the Data

We're using the TidyTuesday Spotify Songs dataset, which has **32,833 songs** across **23 columns**. The data comes from Spotify's API and includes detailed audio features for each track.

The most important variables for music discovery are:

- **Energy** (0-1) and **Tempo** (BPM): Let users find high-intensity workout tracks or low-key background music
- **Danceability** (0-1): Helps DJs identify tracks suitable for dance floors
- **Valence** (0-1): Enables mood-based filtering (happy vs sad songs)
- **Acousticness** (0-1): Distinguishes electronic vs acoustic sounds

These features let users make really specific searches. A DJ could filter for "energy > 0.8 AND tempo > 140 BPM" to find high-intensity tracks, or someone making a sad playlist could look for "valence < 0.4 AND acousticness > 0.6" to find mellow acoustic songs. By combining these different audio features, users can discover songs that match exactly what they're looking for instead of just browsing by genre.

## Section 3: Research Questions & Usage Scenarios

## Section 4: Exploratory Data Analysis

## Section 5: App Sketch & Description
