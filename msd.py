import zipfile
import config
import simplejson as json


class MSD:
    def __init__(self):
        print("\n===== Initializing MSD dataset =====")

        self.zip_train_file = zipfile.ZipFile(config.lastfm_train_file, "r")
        self.zip_test_file =  zipfile.ZipFile(config.lastfm_test_file,  "r")

        self.json_train_files = [f for f in self.zip_train_file.namelist() if f.endswith(".json")]
        self.json_test_files =  [f for f in self.zip_test_file.namelist()  if f.endswith(".json")]

    def __len__(self):
        return len(self.json_train_files) + len(self.json_test_files)

    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError("Index out of range")

        if idx < len(self.json_train_files):
            json_path = self.json_train_files[idx]
            with self.zip_train_file.open(json_path, "r") as f:
                return json.load(f)
        else:
            json_path = self.json_test_files[idx - len(self.json_train_files)]
            with self.zip_test_file.open(json_path, "r") as f:
                return json.load(f)

    def close(self):
        self.zip_train_file.close()
        self.zip_test_file.close()

    def __del__(self):
        self.close()

    def items(self):
        return [(composition["track_id"], composition["tags"]) for composition in self]
