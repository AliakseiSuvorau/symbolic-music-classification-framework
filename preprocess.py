import simplejson as json
import config
from msd import MSD


def get_mismatched_tracks():
    """
    Deletes tracks that are not trustworthy. It outputs all trustworthy tracks to a json file
    as a list.
    """
    print("\n===== Retrieving mismatched track ids =====")

    track_ids = []
    with open(config.msd_mismatched_pairs_file, encoding="utf-8") as mismatches:
        for line in mismatches:
            # According to http://millionsongdataset.com/sites/default/files/tasteprofile/sid_mismatches.txt
            # each line has the following structure:
            # ERROR: <song_id track_id> title1 != title2
            # We need only track ids
            track_id = line.split(" ")[2][:-1]
            track_ids.append(track_id)

    with open(config.msd_mismatched_track_ids_file, "x", encoding="utf-8") as track_ids_only_file:
        json.dump(track_ids, track_ids_only_file)


def get_track_id_to_midi_filename():
    """
    Creates a json file with pairs (`track_id`, `midi_filename`).

    The path to midi file is relative to root of `lmd_matched.tag.gz` archive.
    """
    print("\n===== Getting track id to midi filename pairs =====")

    # Track ids with corresponding midi filenames
    with open(config.lmd_match_scores_file, encoding="utf-8") as matched_scores_file:
        matched_scores = json.load(matched_scores_file)

    track_id_to_midi_filename = {}
    for track_id, track_data in matched_scores.items():
        if not track_data:
            continue

        midi_filename_with_max_confidence = max(track_data.items(), key=lambda x: float(x[1]))[0]
        directories = list(track_id[2:5])
        directories.append(track_id)
        dir_path = "/".join(directories)
        track_id_to_midi_filename[track_id] = f"{dir_path}/{midi_filename_with_max_confidence}.mid"

    with open(config.track_to_midi_file, "x", encoding="utf-8") as track_to_midi_file:
        json.dump(track_id_to_midi_filename, track_to_midi_file)


def get_most_relevant_tag(target_tags, composition_tags):
    """
    Finds most relevant tags from the list of target tags.
    :param target_tags: A list of strings representing target tags.
    :param composition_tags: A list of pairs (tag, relevance) representing tag data
    for a composition from lastfm dataset.
    :return: The most relevant tag from the list of target tags or None, if there is no.
    """
    # Filtering only tags from target ones
    filtered = [(tag, relevance) for tag, relevance in composition_tags if tag in target_tags]

    if not filtered:
        return None

    return max(filtered, key=lambda x: x[1])[0]


def get_tagged_tracks(target_tags: list):
    """
    Creates a json file with pairs (`track_id`, `tag`).

    It ignores all the tracks that are not trustworthy.
    :param target_tags: A list of strings representing target tags.
    """
    # A list of track ids which one should avoid
    with open(config.msd_mismatched_track_ids_file) as mismatched_track_ids_file:
        mismatched_track_ids = json.load(mismatched_track_ids_file)

    dataset = MSD()

    print("\n===== Retrieving track tags =====")

    tagged_tracks = {}
    for track_id, tags in dataset.items():
        # Checking if the track info is trustworthy
        if track_id in mismatched_track_ids:
            continue

        most_relevant_tag = get_most_relevant_tag(target_tags, tags)

        if most_relevant_tag:
            tagged_tracks[track_id] = most_relevant_tag

    with open(config.tagged_tracks_file, "x", encoding="utf-8") as f:
        json.dump(tagged_tracks, f)


def merge_tags_and_midis():
    """
    Creates a json file of the following structure:

    [
      {
        "track_id": "TRAAA1234567890",
        "tag": "example_tag",
        "midi_path": "A/A/A/TRAAA1234567890/midi_filename.mid"
      },
      ...
    ]
    """
    print("\n===== Merge track ids, tags and midis =====")

    with open(config.tagged_tracks_file, "r", encoding="utf-8") as tagged_tracks_file:
        tagged_tracks = json.load(tagged_tracks_file)

    with open(config.track_to_midi_file, "r", encoding="utf-8") as midi_paths_file:
        midi_paths = json.load(midi_paths_file)

    path_to_tag = []
    for track_id, tag in tagged_tracks.items():
        if track_id not in midi_paths:
            continue

        midi_path = midi_paths[track_id]

        path_to_tag.append({
            "track_id": track_id,
            "genre": tag,
            "midi_path": midi_path
        })

    with open(config.tagged_midis_file, "x", encoding="utf-8") as tagged_midis_file:
        json.dump(path_to_tag, tagged_midis_file)


def main():
    # 1. Get the list of not trustworthy tracks, `sid_mismatched_track_ids.json` by default
    get_mismatched_tracks()

    # 2. Get the list of pairs (track_id: tag), `tagged_tracks.json` by default
    get_tagged_tracks(config.target_labels)

    # 3. Get the list of pairs (track_id: midi_file_path), `track_to_midi.json` by default
    get_track_id_to_midi_filename()

    # 4. Merge lists from steps 2 and 3 to get the list of pairs (path_to_midi, tag), `tagged_midis.json` by default
    merge_tags_and_midis()


if __name__ == '__main__':
    main()
