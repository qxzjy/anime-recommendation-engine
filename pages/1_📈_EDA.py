import streamlit as st
import pandas as pd
import plotly.express as px
import ast

from utils.common import df_animes, df_profiles, df_reviews

st.set_page_config(page_title="Anime Recommendation Engine 🏯", layout="wide")

st.markdown("# EDA")

st.markdown("""
Welcome to the EDA section!

Here, we will seek to analyze the data gathered through scraping on the platform dedicated to japanese animation MyAnimeList (myanimelist.net)
This data has been collected in january of 2020, and includes tables for :
- anime (more than 16k entries)
- user profiles (more than 47k entries)
- reviews (more than 130k entries)
            
The dataset we are using is available on Kaggle : https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews

Here, we explore the anime dataset to better understand its structure, trends, and key insights.  
You will find visualizations and statistics about:

- Most common anime genres
- The top 10 best rated animes, and their average scores
- The age and gender repartition of the user base for the platform
- The amount of reviews by anime (data for the top 10 best rated entries)

These insights help guide the recommendation system and ensure data quality.
""")

st.subheader("1) Anime-based analysis")

st.markdown("First, let's get the most represented genres")

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

st.markdown("Let's find out the average score of the 10 best ranked animes")

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

st.subheader("2) User-based analysis")


age_graph = px.histogram(df_profiles,
                         x='age',
                         color='gender',
                         labels={'count': 'Count', 'age': 'Age'},
                         title='Age and gender distribution that users declared for themselves (sample of 22k)',
                         color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                         template='plotly_dark')

st.plotly_chart(age_graph, use_container_width=True)

st.markdown("""Observations :
It appears some users have voluntarily declared an age that is unrepresentative of their real age (some users are aged 0, some older than 90).
According to the Wikipedia article on MyAnimeList, the website exists since 2004. Which means that users simply entering the current day's date as their birthday when joining can be up to 15 years old by the point the data has been collected.
So we have to be aware of the potential inaccuracy of the data around its edges.

However, given the population watching anime tends to be fairly young, it is safe to assume that the median and mean of the age remain representative of the reality.
""")
            
st.subheader("3) Review-based analysis")


top10_anime_uid = rank['uid'].tolist()
reviews_for_top10 = df_reviews[df_reviews['anime_uid'].isin(top10_anime_uid)]
reviews_for_top10 = pd.merge(reviews_for_top10, df_animes, left_on='anime_uid', right_on='uid')

reviews_for_top10 = reviews_for_top10[reviews_for_top10['ranked'] <= 10]

columns_to_keep = ['uid_x', 'profile',	'anime_uid', 'text','score_x', 'scores', 'link_x', 'title', 'ranked', 'score_y', 'popularity', 'members']
reviews_for_top10 = reviews_for_top10[columns_to_keep]

reviews_top10 = px.bar(reviews_for_top10,
                       x='title',
                    
                       labels={'count': 'Amount of reviews', 'title': 'Title'},
                        title='Amount of reviews on the top 10 best ranked animes (excluding top 3 entry for which data is missing)',
                        text='ranked',
                        height= 600,
                        color_discrete_sequence=px.colors.qualitative.Alphabet,
                        template='ggplot2'
                       )
st.plotly_chart(reviews_top10, use_container_width=True)


st.markdown("""
Observation : Bias in some of the models due to missing data in reviews.
            
Here, we see that among the top 10 best rated entries, one is missing. the 3rd ranked entry, Hunter X Hunter (2011), does not appear on the graph due to its reviews' data not being collected through the scraping process that permitted the dataset's construction.

This means that models relying on reviews for recommendations will exclude the animes that saw their reviews not being collected, which includes some recommendation-worthy titles such as HxH. 

Beside, we have to take into account the release date of the titles. For example, the most recent entry in this top 10 is top 5 "Shingeki no Kyojin Season 3 Part 2" ("Attack on Titan"), which finished airing july 2019, less than 6 months before the collection of the data (january the 5th 2020). This means that some entries have had less time to accumulate reviews, and this can possibly weight in the recommendation models based on them.           
""")