import ast
import streamlit as st

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

from utils.common import df_profiles, load_profile, df_animes, load_anime, display_img

st.markdown("## 🎥 User-Based Anime Recommendations")

st.write(
    """Discover anime recommendations tailored to your viewing history and preferences.  
We analyze your liked animes and compare them with other users favorites to suggest titles you might enjoy."""
)

# SelectBox
selected_user_profile = st.selectbox("Choose user",
    df_profiles["profile"],
    index=None,
    placeholder="Select a user ...")

# Anime selected
if selected_user_profile != None :
    selected_profile= load_profile(selected_user_profile)

    # Favorite anims
    with st.expander("Favorite anims"):
        favorites_anime = ast.literal_eval(selected_profile["favorites_anime"])

        if favorites_anime:
            for i in range(0, len(favorites_anime), 3):
                cols = st.columns(3)
                for col, fav in zip(cols, favorites_anime[i:i+3]):
                    anime = load_anime(fav)
                    if anime is not None:
                        with col:
                            display_img(anime["img_url"], anime["title"])
        else:
            st.write("No favorite anime to display.")

    # RECO_02
    with st.expander("Anime recommendations based on what users who liked the same things as me"):
            st.write("TADAAAAAM")
