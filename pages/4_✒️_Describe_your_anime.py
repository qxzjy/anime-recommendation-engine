import streamlit as st

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

from utils.common import search_recommended_animes_from_llm, load_animes, load_anime, write_col, display_img

# Load data
df_animes = load_animes()

st.markdown("## ✒️ Describe an Anime")

# Form
with st.form("anime_input_form"):
    input_anime_description = st.text_area("Tell us what you want — or don’t want — and we’ll recommend the perfect anime !")
    submitted = st.form_submit_button("Find")

    if submitted:
        try:
            recommended_animes = search_recommended_animes_from_llm(input_anime_description)

            recommended_animes_uid = recommended_animes["uid"].tolist()
            
            if recommended_animes_uid:
                st.write("Anime recommandations")

                for reco_uid in recommended_animes_uid:
                    col1, col2 = st.columns(2)
                    anime = load_anime(df_animes, reco_uid)                    
                    if anime is not None:
                        with col1:
                            display_img(anime["img_url"], anime["title"])
                        with col2:
                            write_col(anime["synopsis"])
                            write_col("Episodes : " + str(anime["episodes"]))
                    st.divider()  
            else:
                st.write("No anime to recommend.")

        except ValueError as e:
            st.error(f"Erreur : {e}")         