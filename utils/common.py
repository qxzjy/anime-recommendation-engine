import streamlit as st
import pandas as pd

DATA_ANIMES_URL = ("data/animes_clean.csv")
DATA_PROFILES_URL = ("data/profiles_clean.csv")


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

