# Symbolic music classification framework

### Structure of this repository

- `config.py` stores all the constants (for example, filenames)
- `preprocess.py` creates two `json` files - first with pairs (`track_id`, `path to midi file`), and second with pairs (`track_id`, `tag`)
- `msd.py` has a class for convenient interaction with MSD dataset

### Plan

1. Install all dependencies: `pip install -r requirements.txt`
2. Configure `config.py` file
3. Preprocess data: `python preprocess.py`