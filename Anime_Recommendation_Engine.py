import streamlit as st

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

from utils.common import load_animes, load_profiles, load_reviews, load_synopsis_embedding,  init_model_MiniLM

# Load data
df_animes = load_animes()
df_profiles = load_profiles()
df_reviews = load_reviews()
df_MiniLM = load_synopsis_embedding()
model = init_model_MiniLM()

st.title("Anime Recommendation Engine 🏯")

st.markdown("""
## Welcome to the Anime Recommendation System!

This app provides personalized anime recommendations using two main approaches:

- **User-based filtering**: Suggestions are based on what you've watched, liked, and commented on, as well as the preferences of similar users.  
- **Content-based filtering**: Recommendations are made by analyzing the content of anime descriptions to find similar titles.  

Enjoy discovering new anime tailored to your tastes!
""")

# Side menu
st.sidebar.page_link("pages/1_📈_EDA.py", label="Ici eda")
st.sidebar.page_link("pages/2_🎥_Animes.py", label="Ici animes")