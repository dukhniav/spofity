import sys
import os
import json
import spotipy
import pickle
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from typing import Any
import pandas as pd


class Utils:
    def __init__(self) -> None:
        self.username = None
        self.playlist_name = None
        self.export_dir = None
        self.playlist_uri = None
        self.scope = None
        self.cache_dir = None
        self.use_cache = None

    def setup(self):
        # Load env variables
        load_dotenv()

        # Load config
        f = open("config/config.json")
        config = json.load(f)
        f.close()

        # Load config variables
        self.username = os.getenv("SPOTIPY_CLIENT_USERNAME", "")
        self.playlist_name = config['playlist_name']
        self.scope = config['scope']
        self.playlist_uri = config['playlist_uri']
        self.use_cache = config['use_cache']

        # Create local cache directory
        if self.use_cache:
            self.cache_dir = os.getcwd() + '/sp_cache'
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)

        # Create local export directory
        self.export_dir = os.getcwd() + '/export/'
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def get_sp_user_playlists(self, sp: spotipy, username: str) -> dict:
        '''
        Get a dict of current users' playlists
        '''
        playlists = sp.user_playlists(username)
        playlist_ids = {}
        for playlist in playlists['items']:
            playlist_ids[playlist['name']] = playlist['id']

        return playlist_ids

    def get_sp_playlist(self, sp: spotipy) -> Any:
        '''
        Gets playlist by id
        '''
        print('Getting playlist...')

        playlist = None

        if self.use_cache:
            try:
                with open(self.cache_dir + '/playlist.pkl', 'rb') as f:
                    playlist = pickle.load(f)
            except:
                playlist = sp.playlist(playlist_id=self.playlist_uri)
                with open(self.cache_dir + '/playlist.pkl', 'wb') as f:
                    pickle.dump(playlist, f)
        else:
            playlist = sp.playlist(playlist_id=self.playlist_uri)

        return playlist

    def get_sp_track_features(self, sp: spotipy, songs: list) -> dict:
        '''
        Turn playlist into dataframe
        '''
        print('\n\n\n\n --- Transforming playlist')
        empty_track = {'danceability': 0, 'energy': 0, 'key': 0, 'loudness': 0, 'mode': 0, 'speechiness': 0, 'acousticness': 0, 'instrumentalness': 0, 'liveness': 0, 'valence': 0, 'tempo': 0,
                       'type': 'audio_features', 'id': '00000', 'uri': 'spotify:track:0', 'track_href': 'https://api.spotify.com/', 'analysis_url': 'https://api.spotify.com/', 'duration_ms': 0, 'time_signature': 0}

        tracks = {}

        for i in range(0, len(songs)):
            track_id = songs[i]['track']['id']
            track_name = songs[i]['track']['name']
            if track_id != None:  # Removes the local tracks in your playlist if there is any
                audio_features = sp.audio_features(track_id)
                for track in audio_features:
                    feature = None
                    if track is None:
                        feature = empty_track
                    else:
                        feature = track
                    tracks[track_id] = [track_name, feature]

        return tracks

    def transform_playlist_to_dataframe(self, features, names) -> pd.DataFrame:
        playlist_df = pd.DataFrame(features, index=names)
        playlist_df = playlist_df[["id", "acousticness", "danceability", "duration_ms",
                                   "energy", "instrumentalness",  "key", "liveness",
                                   "loudness", "mode", "speechiness", "tempo", "valence"]]
        playlist_df.head()
        return playlist_df

    def export_csv(self, dataframe: pd.DataFrame, filename):
        dataframe.head()
        dataframe.to_csv(self.export_dir + filename)
        # df = pd.DataFrame(list(tracks.items()), columns)
        # df = pd.DataFrame(list(data.items()), columns=['Date', 'DateValue'])

        # features = []
        # for k,v in tracks.items():
        #     audio_features = sp.audio_features(k)
        #     for track in audio_features:

        #         if track is None:
        #             print(track)
        #             features.append()
        #         else:
        #             features.append(track)

        # playlist_df = pd.DataFrame(features, index = track_names)
        # return playlist_df
