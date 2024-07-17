
st.set_page_config(
    page_title="Eurovision Dashboard",
    page_icon = 'icon.png',
    layout="wide",
    initial_sidebar_state="expanded")

# set logo
col1, col2, col3 = st.columns([1.1,2.4,1])
with col2:
    image_path = 'logo2.png'

    st.image(image_path, caption='', use_column_width=False)

# set df for search
url_list = [{'Song Name': song, 'URL': details['url']} for song, details in ad.urls.items()]
urls_df = pd.DataFrame(url_list)
song_data = pd.read_csv('Data/song_data.csv', encoding='latin1')
df = song_data.copy()
df= df[['year', 'country', 'artist_name', 'song_name', 'style', 'final_place','language']]

query = """
    SELECT
        d.year,
        d.country,
        d.artist_name,
        d.song_name,
        d.style,
        d.final_place,
        d.language,
        u.URL
    FROM df as d
    LEFT JOIN urls_df as u ON u.'Song Name'=d.song_name
"""
search_df = sqldf(query, locals())


# Colorblind Mode
if 'colorblind_mode' not in st.session_state:
    st.session_state.colorblind_mode = False
def toggle_colorblind_mode():
    st.session_state.colorblind_mode = not st.session_state.colorblind_mode

if st.session_state.colorblind_mode:
    text = 'Colorblind Mode Active'
else:
    text = 'Colorblind Mode Disabled'

col1, col2, col3, col4 = st.columns([1,1,1,0.6])
with col4:
    st.markdown("")
    st.markdown("")
    st.button(text, on_click=toggle_colorblind_mode)
# main filter for years
years = [2009, 2010, 2011, 2012, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023]
with col1:
    selected_years = st.select_slider(
        'Global filter by range of years:',
        options=years,
        value=(2009, 2023)
    )
song_data = song_data[song_data['year'].between(selected_years[0], selected_years[1])]
song_data = song_data[song_data['year'] != 2013]

# songs search engine
st.sidebar.title("Search for a Song")
selected_year = st.sidebar.selectbox('Select Year:', options=[''] + sorted(df['year'].unique().tolist()))
selected_country = st.sidebar.selectbox('Select Country:', options=[''] + sorted(df['country'].unique().tolist()))
filtered_df = search_df.copy()

if selected_year:
    filtered_df = search_df[search_df['year'] == selected_year]
if selected_country:
    filtered_df = search_df[search_df['country'] == selected_country]

if not filtered_df.empty:
    selected_song = st.sidebar.selectbox('Select a song to view details:', options=filtered_df['song_name'].unique())
    if selected_song:
        artist= filtered_df[filtered_df['song_name']==selected_song]['artist_name'].values[0]
        country = filtered_df[filtered_df['song_name'] == selected_song]['country'].values[0]
        st.sidebar.write(f"**Information about {selected_song} by {artist} from {country}:**")
        st.sidebar.write(
            f"Year: {filtered_df[filtered_df['song_name'] == selected_song]['year'].values[0]}")
        st.sidebar.write(
            f"Style: {filtered_df[filtered_df['song_name'] == selected_song]['style'].values[0]}")
        final_place = filtered_df[filtered_df['song_name'] == selected_song]['final_place'].values[0]
        if np.isnan(final_place):
            final_place = 'Has not participated in the final'
        else:
            final_place = int(final_place)
        st.sidebar.write(
            f"Final Place: {final_place}")

        video_url = filtered_df[filtered_df['song_name'] == selected_song]['URL'].values[0]
        if video_url:
            st.sidebar.video(video_url)
        else:
            st.sidebar.write("No video available for this song.")
else:
    st.sidebar.write("No songs match your search criteria.")

# visualizations
st.markdown("#### Average Score by Country and Eurovision Debut Year")
st.markdown("Shows average total points for each country and their eurovision debut year")
dataset_options = ['No Groups', 'Eurovision Debut Year', 'Semi Final']
selected_years_for_map = [year for year in range(*selected_years)]
selected_years_for_map.append(selected_years[-1])  # add the last year
if (2019 in selected_years_for_map) and (2021 in selected_years_for_map):
        selected_years_for_map.remove(2020)
if (2012 in selected_years_for_map) and (2014 in selected_years_for_map):
        selected_years_for_map.remove(2013)

selected_countries = song_data[(song_data['qualified_10'] == '1') | (song_data['qualified_10'] == '-')][
            'country'].unique()
selected_countries = np.insert(selected_countries, 0, 'All Countries')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    selected_country = st.selectbox('Select country:', selected_countries)


map_viso = mv2.create_viso(song_data, selected_year, selected_country,
                               colorblind_mode=st.session_state.colorblind_mode)
st.plotly_chart(map_viso, use_container_width=True)


col1, col2 = st.columns([0.9,1.1])
with col2:
        st.markdown("#### Final Score by Semi Final/Host/Top 5")
        st.markdown("Shows statics of total points by the way the country qualified for the final")
with col1:
    st.markdown("#### Songs (Inner) & Average Scores (Outer) by Feature")
    st.markdown("Shows which features are the most used and what effect they have on the final score")


col1, col2, col3, col4 = st.columns([1,0.7,1,1])

with col1:
    feature = ["style","BPM","energy","danceability","happiness"]
    selected_feature = st.selectbox('Select Feature:', feature)

pie_viso = pv.create_viso(song_data,selected_feature,colorblind_mode=st.session_state.colorblind_mode)
col1, col2 = st.columns([0.9,1.1])
with col1:
    st.plotly_chart(pie_viso, use_container_width=True)
with col2:
    bars_viso = bv.create_viso(song_data, colorblind_mode=st.session_state.colorblind_mode)
    st.plotly_chart(bars_viso, use_container_width=True)


st.markdown("#### Scores by Running Order & Voting Type")
st.markdown("Shows if the running order affects the score given to a country")
col1, col2, col3, col4 = st.columns([1,0.7,1,1])
with col1:
    modes = ['Total Score', 'Jury VS Televote']
    selected_mode = st.selectbox('Select Voting Group:', modes)
scatter_viso = sv.create_viso(song_data, selected_mode,colorblind_mode=st.session_state.colorblind_mode)
st.plotly_chart(scatter_viso, use_container_width=True)
