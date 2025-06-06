import streamlit as st
st.set_page_config(layout="wide")

from utils.common import load_animes, load_profiles, load_reviews, load_hentai_uid,load_synopsis_embedding,  init_model_MiniLM

# Load data
df_animes = load_animes()
df_profiles = load_profiles()
df_reviews = load_reviews()
df_hentai_uid = load_hentai_uid()
df_MiniLM = load_synopsis_embedding()
model = init_model_MiniLM()

pages = [
    st.Page("Anime_Recommendation_Engine.py", title="Anime Recommendation Engine"),
    st.Page("pages/1_📈_EDA.py", title="EDA", icon="📈"),
    st.Page("pages/2_🎥_Animes.py", title="Animes", icon="🎥"),
    st.Page("pages/3_🥷_Users.py", title="Users", icon="🥷"),
    st.Page("pages/4_✒️_Describe_your_anime.py", title="Describe your anime", icon="✒️"),
    st.Page("pages/5_💻_Diffusion_list_for_new_content.py", title="Diffusion list for new content", icon="💻")
]

filter_hentai_on = st.sidebar.toggle("Filter out Hentai", value=True)
st.session_state['hentai_filter_on'] = filter_hentai_on

pg = st.navigation(pages)
pg.run()