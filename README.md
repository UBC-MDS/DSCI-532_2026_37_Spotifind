# Spotifind

Spotifind is a dashboard that lets users search for music using Spotify's audio features instead of just genres. Users can filter songs by things like energy level, danceability, tempo, and mood (called "valence" in the data). Especially useful for people who are interested in the technical side of music, such as DJs or sound technicians.

## **Contributors**

Rahiq Raees, Nguyen Nguyen, Shuhang Li, Jose Davila

## Installations

1.  Fork the repository: https://github.com/UBC-MDS/DSCI-532_2026_37_Spotifind.git

2.  Clone the fork locally using:

``` bash
git clone git@github.com:UBC-MDS/DSCI-532_2026_37_Spotifind.git
```
Then please cd into the root of the repo by:
```bash
cd DSCI-532_2026_37_Spotifind
```

3.  Create the virtual environment with:

``` bash
conda env create -f environment.yml
```

4.  Once the environment is created, activate it with:

``` bash
conda activate spotifind
```

5.  Run the app locally with:

``` bash
shiny run src/app.py # → http://127.0.0.1:8000
```

## Dataset Acknowledgement

This project was developed using the following dataset:
- Dataset name: [Spotify Songs](https://github.com/rfordatascience/tidytuesday/blob/main/data/2020/2020-01-21/readme.md)
- License: MIT

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this package.

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

This project is licensed under the MIT License, please see [LICENSE](LICENSE) file for details.

## Citation

If you wish to use this app anywhere, please cite as the following:
Raess, R., Nguyen, N., & Li, S., Davila, J. (2026) Spotifind.

