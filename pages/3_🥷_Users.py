import ast
import streamlit as st
from utils.common import df_profiles, load_profile, df_animes, load_anime

st.set_page_config(page_title="USERS", page_icon="🥷")

st.markdown("## 🎥 User-Based Anime Recommendations")

st.write(
    """Discover anime recommendations tailored to your viewing history and preferences.  
We analyze your liked animes and compare them with other users favorites to suggest titles you might enjoy."""
)

selected_user_profile = st.selectbox("Choose user",
    df_profiles["profile"],
    index=None,
    placeholder="Select a user ...")


if selected_user_profile != None :
    selected_profile= load_profile(selected_user_profile)
    st.write("You selected :", selected_profile["profile"])

    favorites_anime = ast.literal_eval(selected_profile["favorites_anime"])
    st.write("His favorite animes :")

    for fav in favorites_anime:
        st.write(fav)
        anime = load_anime(fav)
        st.image(anime["img_url"], caption=anime["title"], use_column_width=False)
