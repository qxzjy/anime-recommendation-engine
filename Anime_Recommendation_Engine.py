import streamlit as st

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

st.title("Anime Recommendation Engine 🏯")

DATA_URL = ("../data/animes_clean.csv")

st.markdown("""
## Welcome to the Anime Recommendation System!

This app provides personalized anime recommendations using two main approaches:

- **User-based filtering**: Suggestions are based on what you've watched, liked, and commented on, as well as the preferences of similar users.  
- **Content-based filtering**: Recommendations are made by analyzing the content of anime descriptions to find similar titles.  

Enjoy discovering new anime tailored to your tastes!
""")