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

### Persona
Alex is a part-time DJ who manages club party playlists. He spends 4-6 hours a week manually sifting through songs on Spotify, but the genre tags are too broad, making it difficult to quickly find high-energy, danceable tracks. He needs a tool that can quickly filter songs by audio characteristics, saving time and improving playlist quality.

### Usage Scenario
Alex is preparing a playlist for his Saturday gym party. He opened Spotfind, selected the "High-Energy Workout Mix" mode, and set the filters: energy > 0.8, danceability > 0.9. The dashboard displayed a scatter plot of matching songs (x-axis: tempo, y-axis: energy, bubble size: danceability). He clicked on the top 10 previews and added them to the playlist. The whole process took only 5 minutes, instead of the usual hours.

### User Stories
When Alex prepares a playlist for his gym morning class on Saturdays, he needs to select the first 15 songs with energy > 0.85 and tempo 135-155 BPM, which allows him to complete the selection within 20 minutes.

When Alex creates a 'Late Night Focused Study' playlist for clients, he needs to filter 10 songs with a valence < 0.3, acoustics > 0.7, and duration < 240 seconds, so that clients receive the perfect study tracks.

When Alex wants to discover new songs for the dance floor, he needs to look at scatter plots of songs with danceability > 0.8 but popularity < 0.2. This way, he can find hidden potential songs that are not yet popular but are suitable for parties, thus improving his reputation.

## Section 4: Exploratory Data Analysis

The summary table is for the second story mentioned above, which can be seen in jupyter notebook.

As shown in the diagram, based on Alex's requirements—valence < 0.3, acoustics > 0.7, and duration < 240 seconds—all matching songs can be easily obtained. Selecting 10 of these satisfies Alex's needs, and he can see all the basic information about the matching songs, greatly saving time compared to manually selecting songs. Later, after we build the actual dashboard, users will only need to use the dashboard and won't need to touch anything related to code.

Link: 
https://github.com/UBC-MDS/DSCI-532_2026_37_Spotifind/blob/hubery/notebooks/analysis.ipynb.ipynb

## Section 5: App Sketch & Description

Here is the sketch: ![Sketch](../img/sketch.png)

The sketch shows the landing page of the app, and there are five main regions of the app: the filter control, the result table, the scatter plot, the top genre table, and finally the song search bar.

- **The filter control**: It is a sidebar that can be opened or hidden from the main page. It contains danceability, tempo, and acoustic sliders as filters. Moreover, there will also be a mood map that controls valence and energy. For example, if you choose a point in the top-right corner, it will filter songs that have the highest energy and valence.

- **The result table**: It shows the song name, artist, album name, and release date. It will display up to four songs on the page and more can be viewed when the table is expanded.

- **The scatter plot**: It will include dropdown menus to choose the X and Y features you want to display on the plot.

- **The top genre table**: It will show the genres that appear most frequently, ranked from most to least according to the filter results.

- **The song search bar**: When you search for any song, it will display all the statistical features of that song. Eight features can be displayed initially, and more can be seen when expanded.



