import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import warnings
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from scipy.sparse import csr_matrix, hstack
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn import decomposition
from sklearn.ensemble._forest import RandomForestRegressor, RandomForestClassifier
import os
import json
import pickle
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
import sys

from utils import Utils

from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

# https://medium.com/geekculture/spotifys-song-recommendation-ai-wasnt-good-enough-so-i-made-an-ai-better-than-it-38b8528f14bd


def main():
    utils = Utils()
    utils.setup()

    # authenticate
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=utils.scope))

    playlist = utils.get_sp_playlist(sp)

    tracks = playlist["tracks"]
    songs = tracks['items']

    track_features_dict = utils.get_sp_track_features(sp, songs)

    track_features = []
    track_ids = []
    track_names = []

    for k, v in track_features_dict.items():
        track_ids.append(k)
        track_names.append(v[0])
        track_features.append(v[1])

    playlist_df = utils.transform_playlist_to_dataframe(
        track_features, track_names)

    # Export playlist to add ranking
    utils.export_csv(playlist_df, 'Spotify_Dataset.csv')

    # Manually add ratings for now
    playlist_df['ratings'] = [9, 8, 10, 7, 8, 8, 8, 6, 8, 8, 6, 8, 8, 9, 7, 8, 9, 7, 7, 6, 9, 6, 9, 6, 8, 8, 7, 8, 9, 5, 6, 7, 9, 7, 6, 8, 8, 8, 6, 7, 8, 5, 6, 7, 8, 7,
                              6, 9, 7, 8, 8, 7, 7, 6, 8, 7, 8, 7, 8, 6, 8, 5, 6, 5, 8, 6, 8, 6, 7, 4, 9, 8, 7, 6, 7, 9, 8, 6, 4, 6, 7, 8, 7, 7, 8, 8, 4, 8, 8, 8, 7, 7, 7, 5, 7, 8, 7, 10, 8, 6]
    playlist_df.head()


if __name__ == '__main__':
    main()
