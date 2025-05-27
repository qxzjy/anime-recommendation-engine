import streamlit as st
from utils.common import load_animes, load_anime

st.set_page_config(page_title="ANIMES", page_icon="🎥")

st.markdown("## 🎥 Anime Search & Similar Recommendations")

st.write(
    """Search for an anime and discover similar titles based on their descriptions.  
This tool helps you find new animes with themes and storylines that match your interests."""
)

df = load_animes()

# Créer un dictionnaire {label à afficher : valeur à retourner}
animes_dict = {row["title"]: row["uid"] for _, row in df.iterrows()}

selected_anime_uid = st.selectbox("Choose anime",
    animes_dict,
    index=None,
    placeholder="Select an anime ...")


if selected_anime_uid != None :
    selected_anime = load_anime(df, animes_dict[selected_anime_uid])
    st.write("You selected:")
    st.image(selected_anime["img_url"], caption=selected_anime["title"], use_column_width=False)


