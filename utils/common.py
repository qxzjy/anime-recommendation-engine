import streamlit as st
import pandas as pd

DATA_ANIMES_URL = ("data/animes_clean.csv")
DATA_PROFILES_URL = ("data/profiles_clean.csv")


@st.cache_data
def load_animes(nrows=None):
    data = pd.read_csv(DATA_ANIMES_URL, nrows=nrows)
    data.sort_values("title", axis=0, ascending=True, inplace=True)
    return data


@st.cache_data
def load_anime(df, uid):
    selected_anime = df[df["uid"]==uid]
    return selected_anime.iloc[0]


@st.cache_data
def load_profiles(nrows=None):
    data = pd.read_csv(DATA_PROFILES_URL)
    data.sort_values("profile", axis=0, ascending=True, inplace=True)
    return data

@st.cache_data
def load_user(df, profile):
    selected_user = df[df["profile"]==profile]
    return selected_user.iloc[0]