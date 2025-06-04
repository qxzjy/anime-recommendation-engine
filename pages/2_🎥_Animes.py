import streamlit as st

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

from utils.common import load_animes, load_anime, load_synopsis_embedding, search_closest_by_uid, write_col, display_img

st.markdown("## 🎥 Anime Search & Similar Recommendations")

st.write(
    """Search for an anime and discover similar titles based on their descriptions.  
This tool helps you find new animes with themes and storylines that match your interests."""
)

# Load data
df_animes = load_animes()
df_emb = load_synopsis_embedding()

# Create a dictionnary {title to show : id}
animes_dict = {row["title"]: row["uid"] for _, row in df_animes.iterrows()}

# SelectBox
selected_anime_uid = st.selectbox("Choose anime",
    animes_dict,
    index=None,
    placeholder="Select an anime ...")

# Anime selected
if selected_anime_uid != None :

    selected_anime = load_anime(df_animes, animes_dict[selected_anime_uid])

    if selected_anime is not None:

        # Anime informations
        container = st.container(border=True)
        container.write("Anime informations")
        col1, col2 = container.columns(2)
        with col1:
            display_img(selected_anime["img_url"], selected_anime["title"])
        with col2:
            write_col(selected_anime["synopsis"])   
            write_col("Episodes : " + str(selected_anime["episodes"]))

        # RECO_01
        with st.expander("Anime recommendations based on the description"):
            
            if selected_anime["synopsis"] is None or selected_anime["synopsis"] != selected_anime["synopsis"]:
                st.write("No recommendation provided, the synopsis is missing.")
            else:
                closest_anime_synopsis = search_closest_by_uid(selected_anime["uid"], df_emb)
                
                favorites_anime = closest_anime_synopsis['uid'].tolist()

                if favorites_anime:
                    for fav in favorites_anime:
                        col1, col2 = st.columns(2)
                        anime = load_anime(df_animes, fav)                    
                        if anime is not None:
                            with col1:
                                display_img(anime["img_url"], anime["title"])
                            with col2:
                                write_col(anime["synopsis"])
                                write_col("Episodes : " + str(anime["episodes"]))
                        st.divider()  
                else:
                    st.write("No favorite anime to display.")