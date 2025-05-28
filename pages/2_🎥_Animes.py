import streamlit as st
from utils.common import df_animes, load_anime

st.markdown("## 🎥 Anime Search & Similar Recommendations")

st.write(
    """Search for an anime and discover similar titles based on their descriptions.  
This tool helps you find new animes with themes and storylines that match your interests."""
)

# Create a dictionnary {title to show : id}
animes_dict = {row["title"]: row["uid"] for _, row in df_animes.iterrows()}

# SelectBox
selected_anime_uid = st.selectbox("Choose anime",
    animes_dict,
    index=None,
    placeholder="Select an anime ...")

# Anime selected
if selected_anime_uid != None :

    selected_anime = load_anime(animes_dict[selected_anime_uid])

    if selected_anime is not None:

        # Anime informations
        with st.expander("Anime informations"):
            col1, col2 = st.columns(2)
            with col1:
                st.image(selected_anime["img_url"], caption=selected_anime["title"], use_column_width=False)

            with col2:
                st.write(selected_anime["synopsis"])
                st.write("Episodes : ", selected_anime["episodes"])            

        # RECO_01
        with st.expander("Anime recommendations based on the description"):
            st.write("TADAAAAAM")