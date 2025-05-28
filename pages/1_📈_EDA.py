import streamlit as st
import pandas as pd
import plotly.express as px
import ast

from utils.common import df_animes

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

st.markdown("# EDA")

st.markdown("""
Welcome to the EDA section!  
Here, we explore the anime dataset to better understand its structure, trends, and key insights.  
You will find visualizations and statistics about:

- Most common anime genres
- ....

These insights help guide the recommendation system and ensure data quality.
""")

df_animes['genre'] = df_animes['genre'].apply(ast.literal_eval)
df_exploded = df_animes.explode('genre')
genre_count = pd.DataFrame(df_exploded['genre'].value_counts().reset_index(name='count').head(10))

count = px.bar(genre_count,
               x='genre',
               y='count', 
               labels={'genre': 'Genre', 'count': 'Count'},
               text='count',
               title="10 most represented genres",
               template="plotly_dark", 
               color_discrete_sequence=px.colors.qualitative.G10)

st.plotly_chart(count, use_container_width=True)

st.subheader("Let's find out the average score of the 10 best ranked animes")

rank = df_animes.sort_values(by='ranked').head(10)

top_rank = px.bar(rank,
                        x='title',
                        y='score',
                        labels={'title': 'Title', 'score': 'Score'},
                        text='ranked',
                        title='Top ranked animes and their average score',
                        template="plotly_dark", 
                        color_discrete_sequence=px.colors.qualitative.G10)
top_rank.update_yaxes(range=[8.9,9.4])

st.plotly_chart(top_rank, use_container_width=True)

