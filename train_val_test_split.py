import numpy as np
import simplejson as json
import config


def get_finetune_data():
    """
    Leaves only track ids with labels from config.finetune_labels.
    :return: list of track ids
    """
    with open(config.tagged_midis_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total number of track_ids: {len(data)}")

    target_track_ids = []
    for track_data in data:
        genre = track_data["genre"]
        track_id = track_data["track_id"]

        if genre in config.finetune_labels:
            target_track_ids.append(track_id)

    print(f"Target track ids: {len(target_track_ids)}")

    return target_track_ids


def get_train_val_test_split(track_ids, ratio="0.8:0.1:0.1"):
    """
    Splits track_ids into 3 parts at the given ratio.
    :param track_ids: list of track ids
    :param ratio: sets ratio of train, val and tests sets. Default: 0.8:0.1:0.1
    :return: 3 sets of train, val and test track ids
    """
    train_size, val_size, test_size = ratio.split(":")
    train_size, val_size, test_size = float(train_size), float(val_size), float(test_size)

    train_track_ids, val_track_ids, test_track_ids \
        = np.split(track_ids, [int(train_size * len(track_ids)), int((train_size + val_size) * len(track_ids))])
    print(f"Train size: {len(train_track_ids)}, val size: {len(val_track_ids)}, test size: {len(test_track_ids)}")

    return list(train_track_ids), list(val_track_ids), list(test_track_ids)


def main():
    track_ids = get_finetune_data()

    train, val, test = get_train_val_test_split(track_ids)

    with open(config.train_ids_file, "x", encoding="utf-8") as f:
        json.dump(train, f)

    with open(config.val_ids_file, "x", encoding="utf-8") as f:
        json.dump(val, f)

    with open(config.test_ids_file, "x", encoding="utf-8") as f:
        json.dump(test, f)


if __name__ == "__main__":
    main()
