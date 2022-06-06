import authentication as auth
import pitchfork_reviews as pf
import random
from tqdm import tqdm


class FeatureCollector:

    def __init__(self):
        self.pitchfork_csv = pf.PitchforkReviews("pitchfork.csv")
        self.sp = auth.authenticate_spotify()
        self.artist_names = self.pitchfork_csv.get_artist_names()
        self.album_names = self.pitchfork_csv.get_album_names()
        self.final_dict = {
            "index": list(),
            "danceability": list(),
            "energy": list(),
            "key": list(),
            "loudness": list(),
            "mode": list(),
            "speechiness": list(),
            "acousticness": list(),
            "instrumentalness": list(),
            "liveness": list(),
            "valence": list(),
            "tempo": list(),
            "duration_ms": list(),
            "popularity": list()
        }

    def get_album_uri(self, artist, album):
        results = self.sp.search(f"{artist} {album}")
        if len(results['tracks']['items']) < 2:
            return -1
        return results['tracks']['items'][1]['album']['uri']

    def get_album_tracks(self, a_uri):
        return self.sp.album_tracks(a_uri)

    def get_album(self, a_uri):
        return self.sp.album(a_uri)

    def aggregate_audio_features(self, album_tracks):
        num_tracks = len(album_tracks['items'])
        aggregate_features = [0] * 12
        for track in album_tracks['items']:
            try:
                features = list(self.sp.audio_features(track['uri'])[0].values())
                numerical_features = list(features[i] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16])
                for i in range(len(numerical_features)):
                    aggregate_features[i] = aggregate_features[i] + (numerical_features[i] / num_tracks)
            except AttributeError:
                print(f"Track has no available features -- \n{track}")
        return aggregate_features

    def gather_features(self):

        # print(len(self.artist_names))
        # rand_indexes = random.choices(range(len(self.artist_names)), k=1000)

        # self.pitchfork_csv.df = self.pitchfork_csv.df.iloc[rand_indexes]
        self.pitchfork_csv.df = self.pitchfork_csv.df[:1000]

        for i in tqdm(range(len(self.artist_names))[:1000]):
            album_uri = self.get_album_uri(self.artist_names[i], self.album_names[i])
            if album_uri != -1:
                album_tracks = self.get_album_tracks(album_uri)
                new_features = self.aggregate_audio_features(album_tracks)
                self.final_dict['index'].append(i)
                self.final_dict['danceability'].append(round(new_features[0], 3))
                self.final_dict['energy'].append(round(new_features[1], 3))
                self.final_dict['key'].append(round(new_features[2], 3))
                self.final_dict['loudness'].append(round(new_features[3], 3))
                self.final_dict['mode'].append(round(new_features[4], 3))
                self.final_dict['speechiness'].append(round(new_features[5], 3))
                self.final_dict['acousticness'].append(round(new_features[6], 3))
                self.final_dict['instrumentalness'].append(round(new_features[7], 3))
                self.final_dict['liveness'].append(round(new_features[8], 3))
                self.final_dict['valence'].append(round(new_features[9], 3))
                self.final_dict['tempo'].append(round(new_features[10], 3))
                self.final_dict['duration_ms'].append(round(new_features[11], 3))
                self.final_dict['popularity'].append(self.get_album(album_uri)['popularity'])
            else:
                self.pitchfork_csv.drop_row(i)
        print(self.final_dict)
        self.pitchfork_csv.combine_dicts(self.final_dict)
        self.pitchfork_csv.write_csv()


fc = FeatureCollector()
fc.gather_features()
