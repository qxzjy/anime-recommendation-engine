import streamlit as st

def menu():
    st.sidebar.page_link("pages/1_📈_EDA.py", label="📈 EDA")
    st.sidebar.page_link("pages/2_🎥_Animes.py", label="🎥 Animes")
    st.sidebar.page_link("pages/3_🥷_Users.py", label="🥷 Users")
    st.sidebar.page_link("pages/4_✒️_Describe_your_anime.py", label="Ici animes")
    st.sidebar.page_link("pages/5_💻_Diffusion_list_for_new_content", label="Ici eda")