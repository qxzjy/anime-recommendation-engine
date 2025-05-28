import streamlit as st
from utils.common import df_animes, load_anime, df_synopsis_embedding, search_closest_by_uid

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
        container = st.container(border=True)
        container.write("Anime informations")
        col1, col2 = container.columns(2)
        with col1:
            if selected_anime["img_url"] is None or selected_anime["img_url"] != selected_anime["img_url"]:
                st.write("No picture to display.")
            else:
                st.image(selected_anime["img_url"], caption=selected_anime["title"], use_column_width=False)
        with col2:
            st.write(selected_anime["synopsis"])
            st.write("Episodes : ", selected_anime["episodes"])            

        # RECO_01
        with st.expander("Anime recommendations based on the description"):
            filter = 'synopsis_embedding'
            closest_anime_synopsis = search_closest_by_uid(selected_anime["uid"], df_synopsis_embedding, filter)

            favorites_anime = closest_anime_synopsis['uid'].tolist()

            if favorites_anime:
                for fav in favorites_anime:
                    col1, col2 = st.columns(2)
                    anime = load_anime(fav)                    
                    if anime is not None:
                        with col1:
                            if anime["img_url"] is None or anime["img_url"] != anime["img_url"]:
                                st.write("No picture to display.")
                            else:
                                st.image(anime["img_url"], caption=anime["title"], use_column_width=False)

                        with col2:
                            st.write(anime["synopsis"])
                            st.write("Episodes : ", anime["episodes"])
                    st.divider()  
            else:
                st.write("No favorite anime to display.")