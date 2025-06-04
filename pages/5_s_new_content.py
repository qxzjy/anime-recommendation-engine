import streamlit as st

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

from utils.common import load_profiles, load_animes, load_synopsis_embedding

st.markdown("##  Diffusion list for new content")

st.write(
    """ List of diffusions for new content, based on the synopsis and targeting profiles who have favorited similar content. """
)


# Load data
df_animes = load_animes()
df_profiles = load_profiles()
df_synopsis_embedding = load_synopsis_embedding()


# Form
with st.form("anime_input_form"):
    input_anime_description = st.text_area("Summit the new content synopsis to generate the diffusions list !")
    submitted = st.form_submit_button("Find")