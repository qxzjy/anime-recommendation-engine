import streamlit as st
import pandas as pd

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

from utils.common import generate_diffusion_list, load_animes, load_profiles
# Load data
df_animes = load_animes()
df_profiles = load_profiles()

st.markdown("## Diffusion list for new content")

st.write(
    """ List of diffusions for new content, based on the synopsis and targeting profiles who have favorited similar content. """
)


# Form
with st.form("anime_input_form"):
    input_anime_description = st.text_area("Summit the new content synopsis to generate the diffusions list !")
    submitted = st.form_submit_button("Find")

    if submitted:
        diffusion_list_df = generate_diffusion_list(input_anime_description)

        st.write("#### Because they loved:")

        uids = {uid for sub in diffusion_list_df['uid'] for uid in sub}
        selected_animes = df_animes[df_animes['uid'].isin(uids)][['title','uid']]

        st.write(selected_animes.reset_index(drop=True))

        st.write(f"#### Profiles found: {diffusion_list_df.shape[0]}    ({round(diffusion_list_df.shape[0]/df_profiles.shape[0],2)}% of all profiles)")
        st.write(diffusion_list_df['profile'])