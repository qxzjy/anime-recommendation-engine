import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

DATA_ANIMES_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/animes_clean.csv")
DATA_PROFILES_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/profiles_clean.csv")
DATA_SYNOPSIS_EMBEDDING_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/synopsis_embedding.json")


# ANIMES
@st.cache_data
def load_animes(nrows=None):
    data = pd.read_csv(DATA_ANIMES_URL, nrows=nrows)
    data.sort_values("title", axis=0, ascending=True, inplace=True)
    return data

df_animes = load_animes()

@st.cache_data
def load_anime(uid):
    selected_anime = df_animes[df_animes["uid"]==int(uid)]
    if selected_anime.empty:
        return None
    return selected_anime.iloc[0]
##


# PROFILES
@st.cache_data
def load_profiles(nrows=None):
    data = pd.read_csv(DATA_PROFILES_URL, nrows=nrows)
    data.sort_values("profile", axis=0, ascending=True, inplace=True)
    return data

df_profiles = load_profiles()

@st.cache_data
def load_profile(profile):
    selected_profile = df_profiles[df_profiles["profile"]==profile]
    return selected_profile.iloc[0]
##


# SYNOPSIS EMBEDDING
@st.cache_data
def load_synopsis_embedding(nrows=None):
    data = pd.read_json(DATA_SYNOPSIS_EMBEDDING_URL, nrows=nrows)
    return data

df_synopsis_embedding = load_synopsis_embedding()

def search_closest_by_uid(given_uid, df, filter):
        given_embedding = df.loc[df['uid'] == int(given_uid), filter].values[0]
        similarities = cosine_similarity([given_embedding], list(df[filter]))[0]
        similarity_df = pd.DataFrame({'uid': df['uid'], 'similarity': similarities})
        closest = similarity_df[similarity_df['uid'] != given_uid].sort_values(by='similarity', ascending=False).head(5)
        return closest
##

# NAN
def write_col(col):
    if col is None or col != col:
        st.write("No information available.")
    else:
        st.write(col)

def display_img(col_image, col_caption):
    if col_image is None or col_image != col_image:
        st.write("No picture to display.")
    else:
        st.image(col_image, caption=col_caption, use_column_width=False)
##