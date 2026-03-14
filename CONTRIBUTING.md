# Contributing to Spotifind

Thank you for your interest in contributing to Spotifind! We appreciate your help in making this project better.

## How Can I Contribute?

There are many ways to contribute, including:

- Reporting bugs or issues
- Suggesting new features or improvements
- Submitting code via pull requests
- Improving documentation
- Helping with testing and reviewing

## General contributing guide

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

5. Create a new branch for your feature or bug fix.

6.  Run the app locally with:
``` bash
shiny run src/app.py # → http://127.0.0.1:8000
```

7. Submit a pull request with a clear description of your changes

## Code Style and Guidelines

- Follow existing code style and formatting.
- Write clear, concise commit messages.
- Document new functions and modules.

## Reporting Issues

If you encounter bugs or want to request features, please open an issue on GitHub with detailed information.

## Code of Conduct

By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md), which outlines expected behavior within this community.

## Need Help?

If you have any questions, feel free to reach out to open an issue for assistance.

Or you can contact the contributor, the emails is here:

Rahiq Raees: rahiqraees10@gmail.com

Nguyen Nguyen: nguyenuyennguyen03@gmail.com

LI SHUHANG: lshfan123456@gmail.com

Jose Davila: jose.dmyt@gmail.com

Thank you for helping make Spotifind great!

---

## M3 Retrospective

**What worked:**
- Slack communication was consistent and responsive throughout the milestone — the team stayed aligned on progress and blockers.

**What didn't:**
- Work distribution was unbalanced, with some members carrying a heavier load than others.
- Several PRs were merged without a proper review, which goes against our agreed workflow and makes it harder to catch bugs early.

## M4 Collaboration Norms

For M4, the team is committing to the following norms:

- **Balanced contributions**: work is explicitly divided so each member owns at least one feature or fix end-to-end.
- **No unreviewed merges**: every PR must receive at least one approving review from a teammate before merging.
- **Early completion**: aim to have all work merged by Saturday, March 14, ahead of the Tuesday deadline, to allow time for final testing and the release.
- **Issue tracking**: every task is tracked as a GitHub Issue and closed via the resolving PR.