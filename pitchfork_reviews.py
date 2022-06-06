import csv
import pandas as pd


class PitchforkReviews:

    def __init__(self, filepath):
        rows = []
        with open(filepath, 'r', encoding="utf8") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            for row in csv_reader:
                rows.append(row)

        self.df = pd.DataFrame(rows, columns=headers)
        self.df = self.df.drop(columns=["date", "author", "role", "review", "bnm", "link", "label"])

    def get_artist_names(self):
        return self.df["artist"].to_list()

    def get_album_names(self):
        return self.df["album"].to_list()

    def drop_row(self, index):
        self.df = self.df.drop(index, inplace=False)

    def combine_dicts(self, feature_dict):
        temp_df = pd.DataFrame(feature_dict)
        self.df = self.df.join(temp_df.set_index('index'))

    def write_csv(self):
        self.df.to_csv("pitchfork_audio_features.csv", encoding='utf-8', index=True)
