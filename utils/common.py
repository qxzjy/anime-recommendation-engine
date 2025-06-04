from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Optional

import re
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DATA_ANIMES_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/animes_clean.csv")
DATA_PROFILES_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/profiles_clean.csv")
DATA_REVIEWS_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/reviews_clean.csv")
DATA_SYNOPSIS_EMBEDDING_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/synopsis_embedding.json")
DATA_ALS_RECOMMENDATION_URL = ("https://anime-recommendation-engine.s3.eu-west-3.amazonaws.com/data/als_is_favorite_based_reco.csv")

# ANIMES
@st.cache_data
def load_animes(nrows=None):
    data = pd.read_csv(DATA_ANIMES_URL, nrows=nrows)
    data["episodes"] = data["episodes"].astype("Int64")
    data.sort_values("title", axis=0, ascending=True, inplace=True)
    return data

@st.cache_data
def load_anime(df, uid):
    selected_anime = df[df["uid"]==int(uid)]
    if selected_anime.empty:
        return None
    return selected_anime.iloc[0]
##


# PROFILES
@st.cache_data
def load_profiles(nrows=None):
    data = pd.read_csv(DATA_PROFILES_URL, nrows=nrows)
    data.sort_values("profile", axis=0, ascending=True, inplace=True)
    return data

@st.cache_data
def load_profile(df, profile):
    selected_profile = df[df["profile"]==profile]
    return selected_profile.iloc[0]
##


# REVIEWS
@st.cache_data
def load_reviews(nrows=None):
    data = pd.read_csv(DATA_REVIEWS_URL, nrows=nrows)
    return data


# SYNOPSIS EMBEDDING
@st.cache_data
def load_synopsis_embedding(nrows=None):
    data = pd.read_json(DATA_SYNOPSIS_EMBEDDING_URL, nrows=nrows)
    return data

def search_closest_by_uid(given_uid, df, filter):
        given_embedding = df.loc[df['uid'] == int(given_uid), filter].values[0]
        similarities = cosine_similarity([given_embedding], list(df[filter]))[0]
        similarity_df = pd.DataFrame({'uid': df['uid'], 'similarity': similarities})
        closest = similarity_df[similarity_df['uid'] != given_uid].sort_values(by='similarity', ascending=False).head(5)
        return closest
##

# NAN
def write_col(col):
    if col is None or col != col:
        st.write("No information available.")
    else:
        st.write(col)

def display_img(col_image, col_caption):
    if col_image is None or col_image != col_image:
        st.write("No picture to display.")
    else:
        st.image(col_image, caption=col_caption, width=300)
##

# ALS (Collaborative filtering)
@st.cache_data
def load_als_recommendations():
    data = pd.read_csv(DATA_ALS_RECOMMENDATION_URL)
    return data

@st.cache_data
def load_profile_recommendations(df, profile):
    selected_profile = df[df["profile"]==profile]
    if selected_profile.empty :
        return selected_profile
    return selected_profile.iloc[0]



## RECO_05 : input in natural language

# Output format
class OutputSchema(BaseModel):
    positive: str
    negative: str
    title: Optional[str]

# init Model LLM
@st.cache_resource
def init_model_llm():
    # Prompt string 
    sys_prompt="""
    You are a positive and negative element extractor.

    Analyze the user's sentence and extract:
    - what the user wants (positive),
    - what the user explicitly wants to avoid (negative).

    If the user mentions a well-known title (such as an anime, movie, game, etc.) in what they want to avoid, extract it separately.

    Return your response as a JSON object with three fields:
    - positive: a single string summarizing with key-words what the user wants.
    - negative: a single string summarizing with key-words what the user wants to avoid.
    - title: the name of the title the user wants to avoid, if any (e.g., an anime, show, movie); return `null` if none is found.

    {{format_instructions}}
    """

    # Define system prompt
    start_prompt = ChatPromptTemplate.from_messages([
        ("system", sys_prompt),
        ("user", "{text}")
    ])

    # Don't forget your API Key : export MISTRAL_API_KEY=...

    # Let's instanciate a model 
    llm = ChatMistralAI(model="mistral-medium-latest")

    model_llm = start_prompt | llm 

    return model_llm

# init Model MiniLM
@st.cache_data
def init_model_MiniLM():
    # pre-trained model
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Search closest anime by content
def search_closest_by_content(content, df, filter, rows):
    similarities = cosine_similarity([content], list(df[filter]))[0]
    similarity_df = pd.DataFrame({'uid': df['uid'], 'similarity': similarities})
    closest = similarity_df.sort_values(by='similarity', ascending=False).head(rows)
    return closest

# Based on an input anime descrption, search recommended animes from LLM
def search_recommended_animes_from_llm(input_anime_description):
    input_clean = re.sub("[^A-Za-z]+", " ", str(input_anime_description)).lower()

    model_llm = init_model_llm()
    parser = PydanticOutputParser(pydantic_object=OutputSchema)

    # Get the response 
    response = model_llm.invoke({"text": input_clean, "format_instructions": parser.get_format_instructions()})
    input_positive_clean = parser.parse(response.content).positive
    input_negative_clean = parser.parse(response.content).negative
    input_title_clean = parser.parse(response.content).title

    # User wants ...
    if input_positive_clean:
        model = init_model_MiniLM()
        df_MiniLM = load_synopsis_embedding()
        df_animes = load_animes()

        result_df_negative = pd.DataFrame(columns=["uid", "similarity"])
        filter = 'synopsis_embedding'

        # Find all animes that are the closest to the user's preferences
        input_positive_embedding = model.encode(input_positive_clean)
        result_df_positive = pd.DataFrame(search_closest_by_content(input_positive_embedding, df_MiniLM, filter, 20), columns=['uid','similarity'])

         # User don't want ...
        if input_negative_clean:

            # Find all animes that are the closest to what the user wants to avoid
            input_negative_embedding = model.encode(input_negative_clean)
            result_df_negative = pd.DataFrame(search_closest_by_content(input_negative_embedding, df_MiniLM, filter, 20), columns=['uid','similarity'])

        # User don't want a Title ...
        if input_title_clean:
            mask = df_animes["title"].str.lower().apply(lambda title: any(mot in title for mot in input_negative_clean.lower().split()))
            result_df_title_negative = df_animes[mask]
            result_df_negative = pd.concat([result_df_negative, result_df_title_negative], ignore_index=True)   

        # We exclude the anime the user doesn't want from those they do want
        result_df_final = result_df_positive[~result_df_positive['uid'].isin(result_df_negative['uid'])]
        result_df_final = result_df_final.sort_values(by='similarity', ascending=False)

        return result_df_final.head(5)
    
    else:
         raise ValueError("Sorry, your input doesn't allow us to generate any recommendations. Please try rephrasing your request with more details or clarity.")