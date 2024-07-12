import streamlit as st
import plotly.express as px
import pandas as pd

# Filter by year
selected_year = st.sidebar.selectbox('Select Year:', options=[''] + sorted(df['Year'].unique().tolist()))

# Filter by country
selected_country = st.sidebar.selectbox('Select Country:', options=[''] + sorted(df['Country'].unique().tolist()))

# Search box for song
# selected_song_term = st.sidebar.text_input('Search for a song:', '')

# Filter data based on selections
filtered_df = df.copy()
if selected_year:
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
if selected_country:
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]


st.sidebar.write("Song Information:")

if not filtered_df.empty:
    selected_song = st.sidebar.selectbox('Select a song to view details:', options=filtered_df['Song'].unique())
    if selected_song:
        st.sidebar.write(f"**Information about {selected_song}:**")
        st.sidebar.write(song_info[selected_song])
else:
    st.sidebar.write("No songs match your search criteria.")