import ast
import streamlit as st
import pandas as pd

st.set_page_config(page_title="USERS", page_icon="🥷")

st.markdown("## 🎥 User-Based Anime Recommendations")

st.write(
    """Discover anime recommendations tailored to your viewing history and preferences.  
We analyze your liked animes and compare them with other users favorites to suggest titles you might enjoy."""
)

DATA_PROFILES_URL = ("data/profiles_clean.csv")
DATA_URL = ("data/profiles_clean.csv")



@st.cache_data
def load_animes(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data["dateRep"] = pd.to_datetime(data["dateRep"], format="%d/%m/%Y")
    data = data.sort_values("dateRep")
    return data

df = load_data()

selected_user_profile = st.selectbox("Choose user",
    df["profile"],
    index=None,
    placeholder="Select a user ...")


if selected_user_profile != None :
    selected_anime = load_user(selected_user_profile)
    st.write("You selected :", selected_anime["profile"])

    favorites_anime = ast.literal_eval(selected_anime["favorites_anime"])
    st.write("His favorite animes :")

    for fav in favorites_anime:
        st.write(fav)
