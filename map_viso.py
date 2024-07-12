from libs.pandasql import sqldf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go

def create_viso(dfs, selected_year, group, selected_country):
    country_coor = {
        "Andorra": (42.546245, 1.601554),
        "United Arab Emirates": (23.424076, 53.847818),
        "Afghanistan": (33.93911, 67.709953),
        "Antigua and Barbuda": (17.060816, -61.796428),
        "Anguilla": (18.220554, -63.068615),
        "Albania": (41.153332, 20.168331),
        "Armenia": (40.069099, 45.038189),
        "Netherlands Antilles": (12.226079, -69.060087),
        "Angola": (-11.202692, 17.873887),
        "Antarctica": (-75.250973, -0.071389),
        "Argentina": (-38.416097, -63.616672),
        "American Samoa": (-14.270972, -170.132217),
        "Austria": (47.516231, 14.550072),
        "Australia": (-25.274398, 133.775136),
        "Aruba": (12.52111, -69.968338),
        "Azerbaijan": (40.143105, 47.576927),
        "Bosnia and Herzegovina": (43.915886, 17.679076),
        "Barbados": (13.193887, -59.543198),
        "Bangladesh": (23.684994, 90.356331),
        "Belgium": (50.503887, 4.469936),
        "Burkina Faso": (12.238333, -1.561593),
        "Bulgaria": (42.733883, 25.48583),
        "Bahrain": (25.930414, 50.637772),
        "Burundi": (-3.373056, 29.918886),
        "Benin": (9.30769, 2.315834),
        "Bermuda": (32.321384, -64.75737),
        "Brunei": (4.535277, 114.727669),
        "Bolivia": (-16.290154, -63.588653),
        "Brazil": (-14.235004, -51.92528),
        "Bahamas": (25.03428, -77.39628),
        "Bhutan": (27.514162, 90.433601),
        "Bouvet Island": (-54.423199, 3.413194),
        "Botswana": (-22.328474, 24.684866),
        "Belarus": (53.709807, 27.953389),
        "Belize": (17.189877, -88.49765),
        "Canada": (56.130366, -106.346771),
        "Cocos [Keeling] Islands": (-12.164165, 96.870956),
        "Congo [DRC]": (-4.038333, 21.758664),
        "Central African Republic": (6.611111, 20.939444),
        "Congo [Republic]": (-0.228021, 15.827659),
        "Switzerland": (46.818188, 8.227512),
        "Côte d'Ivoire": (7.539989, -5.54708),
        "Cook Islands": (-21.236736, -159.777671),
        "Chile": (-35.675147, -71.542969),
        "Cameroon": (7.369722, 12.354722),
        "China": (35.86166, 104.195397),
        "Colombia": (4.570868, -74.297333),
        "Costa Rica": (9.748917, -83.753428),
        "Cuba": (21.521757, -77.781167),
        "Cape Verde": (16.002082, -24.013197),
        "Christmas Island": (-10.447525, 105.690449),
        "Cyprus": (35.126413, 33.429859),
        "Czech Republic": (49.817492, 15.472962),
        "Germany": (51.165691, 10.451526),
        "Djibouti": (11.825138, 42.590275),
        "Denmark": (56.26392, 9.501785),
        "Dominica": (15.414999, -61.370976),
        "Dominican Republic": (18.735693, -70.162651),
        "Algeria": (28.033886, 1.659626),
        "Ecuador": (-1.831239, -78.183406),
        "Estonia": (58.595272, 25.013607),
        "Egypt": (26.820553, 30.802498),
        "Western Sahara": (24.215527, -12.885834),
        "Eritrea": (15.179384, 39.782334),
        "Spain": (40.463667, -3.74922),
        "Ethiopia": (9.145, 40.489673),
        "Finland": (61.92411, 25.748151),
        "Fiji": (-16.578193, 179.414413),
        "Falkland Islands [Islas Malvinas]": (-51.796253, -59.523613),
        "Micronesia": (7.425554, 150.550812),
        "Faroe Islands": (61.892635, -6.911806),
        "France": (46.227638, 2.213749),
        "Gabon": (-0.803689, 11.609444),
        "United Kingdom": (55.378051, -3.435973),
        "Grenada": (12.262776, -61.604171),
        "Georgia": (42.315407, 43.356892),
        "French Guiana": (3.933889, -53.125782),
        "Guernsey": (49.465691, -2.585278),
        "Ghana": (7.946527, -1.023194),
        "Gibraltar": (36.137741, -5.345374),
        "Greenland": (71.706936, -42.604303),
        "Gambia": (13.443182, -15.310139),
        "Guinea": (9.945587, -9.696645),
        "Guadeloupe": (16.995971, -62.067641),
        "Equatorial Guinea": (1.650801, 10.267895),
        "Greece": (39.074208, 21.824312),
        "South Georgia and the South Sandwich Islands": (-54.429579, -36.587909),
        "Guatemala": (15.783471, -90.230759),
        "Guam": (13.444304, 144.793731),
        "Guinea-Bissau": (11.803749, -15.180413),
        "Guyana": (4.860416, -58.93018),
        "Gaza Strip": (31.354676, 34.308825),
        "Hong Kong": (22.396428, 114.109497),
        "Heard Island and McDonald Islands": (-53.08181, 73.504158),
        "Honduras": (15.199999, -86.241905),
        "Croatia": (45.1, 15.2),
        "Haiti": (18.971187, -72.285215),
        "Hungary": (47.162494, 19.503304),
        "Indonesia": (-0.789275, 113.921327),
        "Ireland": (53.41291, -8.24389),
        "Israel": (31.046051, 34.851612),
        "Isle of Man": (54.236107, -4.548056),
        "India": (20.593684, 78.96288),
        "British Indian Ocean Territory": (-6.343194, 71.876519),
        "Iraq": (33.223191, 43.679291),
        "Iran": (32.427908, 53.688046),
        "Iceland": (64.963051, -19.020835),
        "Italy": (41.87194, 12.56738),
        "Jersey": (49.214439, -2.13125),
        "Jamaica": (18.109581, -77.297508),
        "Jordan": (30.585164, 36.238414),
        "Japan": (36.204824, 138.252924),
        "Kenya": (-0.023559, 37.906193),
        "Kyrgyzstan": (41.20438, 74.766098),
        "Cambodia": (12.565679, 104.990963),
        "Kiribati": (-3.370417, -168.734039),
        "Comoros": (-11.875001, 43.872219),
        "Saint Kitts and Nevis": (17.357822, -62.782998),
        "North Korea": (40.339852, 127.510093),
        "South Korea": (35.907757, 127.766922),
        "Kuwait": (29.31166, 47.481766),
        "Cayman Islands": (19.3133, -81.2546),
        "Kazakhstan": (48.019573, 66.923684),
        "Laos": (19.85627, 102.495496),
        "Lebanon": (33.854721, 35.862285),
        "Saint Lucia": (13.909444, -60.978893),
        "Liechtenstein": (47.166, 9.555373),
        "Sri Lanka": (7.873054, 80.771797),
        "Liberia": (6.428055, -9.429499),
        "Lesotho": (-29.609988, 28.233608),
        "Lithuania": (55.169438, 23.881275),
        "Luxembourg": (49.815273, 6.129583),
        "Latvia": (56.879635, 24.603189),
        "Libya": (26.3351, 17.228331),
        "Morocco": (31.791702, -7.09262),
        "Monaco": (43.750298, 7.412841),
        "Moldova": (47.411631, 28.369885),
        "Montenegro": (42.708678, 19.37439),
        "Madagascar": (-18.766947, 46.869107),
        "Marshall Islands": (7.131474, 171.184478),
        "Macedonia [FYROM]": (41.608635, 21.745275),
        "Mali": (17.570692, -3.996166),
        "Myanmar [Burma]": (21.913965, 95.956223),
        "Mongolia": (46.862496, 103.846656),
        "Macau": (22.198745, 113.543873),
        "Northern Mariana Islands": (17.33083, 145.38469),
        "Martinique": (14.641528, -61.024174),
        "Mauritania": (21.00789, -10.940835),
        "Montserrat": (16.742498, -62.187366),
        "Malta": (35.937496, 14.375416),
        "Mauritius": (-20.348404, 57.552152),
        "Maldives": (3.202778, 73.22068),
        "Malawi": (-13.254308, 34.301525),
        "Mexico": (23.634501, -102.552784),
        "Malaysia": (4.210484, 101.975766),
        "Mozambique": (-18.665695, 35.529562),
        "Namibia": (-22.95764, 18.49041),
        "New Caledonia": (-20.904305, 165.618042),
        "Niger": (17.607789, 8.081666),
        "Norfolk Island": (-29.040835, 167.954712),
        "Nigeria": (9.081999, 8.675277),
        "Nicaragua": (12.865416, -85.207229),
        "Netherlands": (52.132633, 5.291266),
        "Norway": (60.472024, 8.468946),
        "Nepal": (28.394857, 84.124008),
        "Nauru": (-0.522778, 166.931503),
        "Niue": (-19.054445, -169.867233),
        "New Zealand": (-40.900557, 174.885971),
        "Oman": (21.512583, 55.923255),
        "Panama": (8.537981, -80.782127),
        "Peru": (-9.189967, -75.015152),
        "French Polynesia": (-17.679742, -149.406843),
        "Papua New Guinea": (-6.314993, 143.95555),
        "Philippines": (12.879721, 121.774017),
        "Pakistan": (30.375321, 69.345116),
        "Poland": (51.919438, 19.145136),
        "Saint Pierre and Miquelon": (46.941936, -56.27111),
        "Pitcairn Islands": (-24.703615, -127.439308),
        "Puerto Rico": (18.220833, -66.590149),
        "Palestinian Territories": (31.952162, 35.233154),
        "Portugal": (39.399872, -8.224454),
        "Palau": (7.51498, 134.58252),
        "Paraguay": (-23.442503, -58.443832),
        "Qatar": (25.354826, 51.183884),
        "Réunion": (-21.115141, 55.536384),
        "Romania": (45.943161, 24.96676),
        "Serbia": (44.016521, 21.005859),
        "Russia": (61.52401, 105.318756),
        "Rwanda": (-1.940278, 29.873888),
        "Saudi Arabia": (23.885942, 45.079162),
        "Solomon Islands": (-9.64571, 160.156194),
        "Seychelles": (-4.679574, 55.491977),
        "Sudan": (12.862807, 30.217636),
        "Sweden": (60.128161, 18.643501),
        "Singapore": (1.352083, 103.819836),
        "Saint Helena": (-24.143474, -10.030696),
        "Slovenia": (46.151241, 14.995463),
        "Svalbard and Jan Mayen": (77.553604, 23.670272),
        "Slovakia": (48.669026, 19.699024),
        "Sierra Leone": (8.460555, -11.779889),
        "San Marino": (43.94236, 12.457777),
        "Senegal": (14.497401, -14.452362),
        "Somalia": (5.152149, 46.199616),
        "Suriname": (3.919305, -56.027783),
        "São Tomé and Príncipe": (0.18636, 6.613081),
        "El Salvador": (13.794185, -88.89653),
        "Syria": (34.802075, 38.996815),
        "Swaziland": (-26.522503, 31.465866),
        "Turks and Caicos Islands": (21.694025, -71.797928),
        "Chad": (15.454166, 18.732207),
        "French Southern Territories": (-49.280366, 69.348557),
        "Togo": (8.619543, 0.824782),
        "Thailand": (15.870032, 100.992541),
        "Tajikistan": (38.861034, 71.276093),
        "Tokelau": (-9.20046, -171.8484),
        "Timor-Leste": (-8.874217, 125.727539),
        "Turkmenistan": (38.969719, 59.556278),
        "Tunisia": (33.886917, 9.537499),
        "Tonga": (-21.178986, -175.198242),
        "Turkey": (38.963745, 35.243322),
        "Trinidad and Tobago": (10.691803, -61.222503),
        "Tuvalu": (-7.109535, 179.194),
        "Taiwan": (23.69781, 120.960515),
        "Tanzania": (-6.369028, 34.888822),
        "Ukraine": (48.379433, 31.16558),
        "Uganda": (1.373333, 32.290275),
        "U.S. Minor Outlying Islands": (19.282319, 166.647047),
        "United States": (37.09024, -95.712891),
        "Uruguay": (-32.522779, -55.765835),
        "Uzbekistan": (41.377491, 64.585262),
        "Vatican City": (41.902916, 12.453389),
        "Saint Vincent and the Grenadines": (12.984305, -61.287228),
        "Venezuela": (6.42375, -66.58973),
        "British Virgin Islands": (18.420695, -64.639968),
        "U.S. Virgin Islands": (18.335765, -64.896335),
        "Vietnam": (14.058324, 108.277199),
        "Vanuatu": (-15.376706, 166.959158),
        "Wallis and Futuna": (-13.768752, -177.156097),
        "Samoa": (-13.759029, -172.104629),
        "Yemen": (15.552727, 48.516388),
        "Mayotte": (-12.8275, 45.166244),
        "South Africa": (-30.559482, 22.937506),
        "Zambia": (-13.133897, 27.849332),
        "Zimbabwe": (-19.015438, 29.154857),
        "North Macedonia": (41.724182, 21.774216)
    }

    data = [(country, coords[0], coords[1]) for country, coords in country_coor.items()]

    # turn country_coor into df
    coords_df = pd.DataFrame(data, columns=['country', 'lat', 'lon'])
    scores = dfs['song_data']
    scores = scores[scores['year']==selected_year]


    query = """
        SELECT
            country,
            final_total_points as 'Total Points'
        FROM scores
        WHERE qualified_10 = '1'
        GROUP BY country
        """
    scores = sqldf(query, locals())

    # merge with coords
    query = """
        SELECT
            a.country,
            a.'Total Points',
            c.lat,
            c.lon
        FROM scores as a
        LEFT JOIN coords_df as c ON c.country=a.country
    """
    scores_with_coords = sqldf(query, locals())
    country_types = {
        'Nordic': ['Denmark', 'Finland', 'Iceland', 'Norway', 'Sweden'],
        'Slavic': ['Belarus', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czech Republic',
                   'Montenegro', 'North Macedonia', 'Poland', 'Russia', 'Serbia', 'Slovakia',
                   'Slovenia', 'Ukraine'],
        'Baltic': ['Estonia', 'Latvia', 'Lithuania'],
        'Mediterranean': ['Albania', 'Cyprus', 'Greece', 'Italy', 'Malta', 'Portugal', 'Spain'],
        'Western': ['Austria', 'Belgium', 'France', 'Germany', 'Ireland', 'Netherlands',
                    'Switzerland', 'United Kingdom'],
        'Eastern': ['Armenia', 'Azerbaijan', 'Georgia', 'Moldova'],
        'Other': ['Australia', 'Israel']
    }

    area_data = [(country, type_) for type_, countries in country_types.items() for country in countries]
    area_df = pd.DataFrame(area_data, columns=['country', 'type'])


    # add area to avg_scores_with_coords
    query = """
        SELECT
            a.country,
            a.'Total Points',
            a.lat,
            a.lon,
            ad.type
        FROM scores_with_coords as a
        LEFT JOIN area_df as ad ON a.country=ad.country
    """
    scores_and_area = sqldf(query, locals())
    eco_classes = pd.read_excel(r'Data\OGHIST.xlsx', sheet_name=2, skiprows=5)
    filtered_eco_classes = eco_classes[eco_classes['Data for calendar year :'].isin(scores['country'])][
        ['Data for calendar year :', 2016, 2017, 2018, 2019, 2021, 2022, 2023]]
    eco_classes = pd.melt(filtered_eco_classes, id_vars=['Data for calendar year :'],
                          var_name='Year', value_name='Economic Class')

    # Rename the columns for clarity
    eco_classes.columns = ['Country', 'Year', 'Economic Class']
    most_frequent_eco_class = eco_classes.groupby('Country')['Economic Class'].agg(lambda x: x.mode()[0])

    # Reset index to convert the result back into a DataFrame
    most_frequent_eco_class = most_frequent_eco_class.reset_index()

    query = """
        SELECT
            sa.country,
            sa.'Total Points',
            sa.lat,
            sa.lon,
            sa.type as Region,
            ec.'Economic Class' as 'Economy Level'
        FROM scores_and_area as sa
        LEFT JOIN most_frequent_eco_class as ec ON ec.Country=sa.country
    """
    scored_area_and_eco = sqldf(query, locals())

    economy_mapping = {
        'L': 'Low income',
        'LM': 'Lower middle income',
        'UM': 'Upper middle income',
        'H': 'High income',
        None: 'No information'  # Handle None values
    }
    economy_mapping = {
        'L': 'Low income',
        'LM': 'Lower middle income',
        'UM': 'Upper middle income',
        'H': 'High income',
        None: 'No information'  # Handle None values
    }

    # Map the values in the 'economy_level' column using the mapping dictionary
    scored_area_and_eco['Economy Level'] = scored_area_and_eco['Economy Level'].map(economy_mapping)

    data = {
        "Country": [
            "Albania", "Andorra", "Armenia", "Australia", "Austria", "Azerbaijan",
            "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
            "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia",
            "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Israel", "Italy",
            "Latvia", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco",
            "Montenegro", "Morocco", "Netherlands", "North Macedonia", "Norway",
            "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia",
            "Serbia and Montenegro", "Slovakia", "Slovenia", "Spain", "Sweden",
            "Switzerland", "Turkey", "Ukraine", "United Kingdom", "Yugoslavia"
        ],
        "Debut year": [
            2004, 2004, 2006, 2015, 1957, 2008, 2004, 1956, 1993, 2005, 1993, 1981,
            2007, 1957, 1994, 1961, 1956, 2007, 1956, 1974, 1994, 1986, 1965, 1973,
            1956, 2000, 1994, 1956, 1971, 2005, 1959, 2007, 1980, 1956, 1998, 1960,
            1994, 1964, 1994, 1994, 2008, 2007, 2004, 1994, 1993, 1961, 1958, 1956,
            1975, 2003, 1957, 1961
        ]
    }

    # Creating the DataFrame
    debut_df = pd.DataFrame(data)

    # Define a function to categorize debut years
    def categorize_year(year):
        if 1950 <= year <= 1969:
            return "1950s-1960s"
        elif 1970 <= year <= 1989:
            return "1970s-1980s"
        elif 1990 <= year <= 2009:
            return "1990s-2000s"
        elif 2010 <= year <= 2029:
            return "2010s-2020s"
        else:
            return "Unknown"

    # Apply the categorization function to create a new column
    debut_df["Debut Years"] = debut_df["Debut year"].apply(categorize_year)

    query = """
        SELECT
            sa.country,
            sa.'Total Points',
            sa.lat,
            sa.lon,
            sa.Region,
            sa.'Economy Level',
            d.'Debut Years' as 'Eurovision Debut Year'
        FROM scored_area_and_eco as sa
        LEFT JOIN debut_df as d ON d.Country=sa.country
    """
    final_df = sqldf(query, locals())

    # Initialize the scaler
    scaler = MinMaxScaler()

    # Fit and transform the points column
    final_df['score_scaled'] = scaler.fit_transform(final_df[['Total Points']])

    final_df['lat'] = final_df['lat'].astype(float)
    final_df['lon'] = final_df['lon'].astype(float)
    # Calculate the average score for each country
    if group != 'No Groups':
        score_df = final_df.groupby(['country', group])[['Total Points','score_scaled']].mean().reset_index()
        score_df.columns = ['country', group, 'Total Points', 'score_scaled']
        if group == 'Economy Level':
            symbols = {
                'High income': 'circle',
                'Upper middle income': 'square',
                'Lower middle income': 'diamond',
                'Low income': 'star',
                'No information': 'cross'
            }
            colors = {
                'High income': 'green',
                'Upper middle income': 'gray',
                'Lower middle income': 'red',
                'Low income': 'white',
                'No information': 'Cyan'
            }
        elif group == 'Region':
            symbols = {
                'Nordic': "circle",
                'Slavic': 'square',
                'Baltic': 'diamond',
                'Mediterranean': 'cross',
                'Western': 'hexagram',
                'Eastern': 'triangle-down',
                'Other': 'star'
            }

            colors = {
                'Nordic': "green",
                'Slavic': 'Cyan',
                'Baltic': 'red',
                'Mediterranean': 'gray',
                'Western': 'Lime',
                'Eastern': 'White',
                'Other': 'pink'
            }
        elif 'Eurovision Debut Year':
            symbols = {
                '1950s-1960s': 'circle',
                '1970s-1980s': 'square',
                '1990s-2000s': 'diamond',
                '2010s-2020s': 'star'
            }
            # colors = {
            #     '1950s-1960s': 'green',
            #     '1970s-1980s': 'Cyan',
            #     '1990s-2000s': 'red',
            #     '2010s-2020s': 'white'
            # }
            colors = {
                '1950s-1960s': 'white',
                '1970s-1980s': 'white',
                '1990s-2000s': 'white',
                '2010s-2020s': 'white'
            }
        else:
            symbols ={}
            colors = {}

        # Create choropleth map
        map_viso = px.choropleth(
            score_df,
            locations='country',
            locationmode='country names',
            color='score_scaled',
            hover_name='country',
            hover_data={'score_scaled': False, group: False},
            custom_data=['country', 'Total Points', group],
            color_continuous_scale='plasma',  # Single color scale
            labels={'Total Points': 'Total Points', group: 'Group'},
            width=1800,
            height=550,
        )


        hover_template = (
                '<b>Country:</b> %{customdata[0]}<br>' +
                '<b>Average Score:</b> %{customdata[1]:.2f}<br>' +
                '<b>Group:</b> %{customdata[2]}<br>'
        )
        map_viso.update_traces(hovertemplate=hover_template)
        for chosen_type, symbol in symbols.items():
            subset = score_df[score_df[group] == chosen_type]
            lon_values = subset.apply(lambda row: final_df[final_df['country'] == row['country']]['lon'].values[0], axis=1)
            lat_values = subset.apply(lambda row: final_df[final_df['country'] == row['country']]['lat'].values[0], axis=1)
            points = subset['Total Points']
            text_values = (
                    '<b>Country: </b> ' + subset['country'].astype(str) + '<br>' +
                    '<b>Total Points: </b> ' + points.astype(str) + '<br>' +
                    '<b>Group:</b>'+chosen_type+'<br>'
            )

            trace = go.Scattergeo(
                lon=lon_values,
                lat=lat_values,
                text=text_values,
                hoverinfo='text',  # Show custom hoverinfo
                hovertemplate='%{text}',
                marker=dict(
                    symbol=symbol,
                    size=10,
                    color=colors[chosen_type],  # Set color based on economy level
                    line=dict(width=1, color='black')
                ),
                name=chosen_type,
                showlegend=True
            )

            map_viso.add_trace(trace)
        # Update layout to position legends

        map_viso.update_layout(
            legend=dict(
                x=1,
                y=0.97,
                traceorder='normal',
                title=dict(text='Group'),
                itemsizing='constant'
            ),
            coloraxis_colorbar=dict(
                title='Average Score (scaled)',
                x=1,
                y=0.3,
                len=0.5,  # Adjust the length (relative to the plot height)
            )
        )
    else:
        score_df = final_df.groupby(['country'])[['Total Points', 'score_scaled']].mean().reset_index()
        score_df.columns = ['country', 'Total Points', 'score_scaled']
        map_viso = px.choropleth(
            score_df,
            locations='country',
            locationmode='country names',
            color='score_scaled',
            hover_name='country',
            hover_data={'score_scaled': False},
            custom_data=['country', 'Total Points'],
            color_continuous_scale='plasma',  # Single color scale
            # title='Choropleth Map of Average Scores by Country',
            labels={'Total Points': 'Total Points'},
            width=1800,
            height=550,
        )
        hover_template = (
                '<b>Country:</b> %{customdata[0]}<br>' +
                '<b>Average Score:</b> %{customdata[1]:.2f}<br>'
        )
        map_viso.update_traces(hovertemplate=hover_template)
        map_viso.update_layout(
            coloraxis_colorbar=dict(
                title='Average Score (scaled)',
                x=1,
                y=0.5,
                len=1,  # Adjust the length (relative to the plot height)
            )
        )
    map_viso.update_layout(template='plotly_dark+presentation')
    # Update geos and display the chart
    map_viso.update_geos(projection_type="natural earth")

    if selected_country != 'All Countries':
        map_viso.update_geos(
            center = {"lat": country_coor[selected_country][0], "lon": country_coor[selected_country][1]},
            projection_scale=5
        )

    return map_viso
