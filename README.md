# Symbolic music classification framework

### Structure of this repository

- `config.py` stores all the constants (for example, filenames)
- `preprocess.py` creates two `json` files - first with pairs (`track_id`, `path to midi file`), and second with pairs (`track_id`, `tag`)
- `msd.py` has a class for convenient interaction with MSD dataset
- `dataset_analysis.py` displays a bar plot with data distribution between classes
- `train_val_test_split.py` take only 4 labels (Classical, Electronic, Country and Hip-Hop) from `tagged_tracks.json`,
    splits the list of indexes at a given ration and stores the indexes in `train_ids.json`, `val_ids.json` and `test_ids.json`

### Preprocess

1. Install all dependencies: `pip install -r requirements.txt`
2. Configure `config.py` file
3. Preprocess data: `python preprocess.py`

### Collect data for fine-tuning

`python train_val_test_split.py`
