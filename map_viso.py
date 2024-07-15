from libs.pandasql import sqldf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go
import additional_data as ad

def create_viso(df, selected_year, group, selected_country):

    # turn country_coor into df
    data = [(country, coords[0], coords[1]) for country, coords in ad.country_coor.items()]
    coords_df = pd.DataFrame(data, columns=['country', 'lat', 'lon'])

    scores = df
    # filter by the chosen year
    scores = scores[scores['year']==selected_year]
    scores = scores.dropna(subset=['final_total_points'])
    scores['semi_final'] = scores['semi_final'].replace('-', '0')

    # set categories
    query = """
        SELECT
            country,
            final_total_points as 'Total Points',
            CASE
                WHEN semi_final = '0' THEN 'Top 5/Host'
                WHEN semi_final = '1' THEN '1st Semi Final'
                WHEN semi_final = '2' THEN '2nd Semi Final'
                ELSE semi_final
            END as 'Semi Final'
        FROM scores
        WHERE qualified_10 = '1' OR qualified_10 = '-'
        """
    scores = sqldf(query, locals())
    # merge with coords
    query = """
        SELECT
            a.country,
            a.'Total Points',
            a.'Semi Final',
            c.lat,
            c.lon
        FROM scores as a
        LEFT JOIN coords_df as c ON c.country=a.country
    """
    scores_with_coords = sqldf(query, locals())

    debut_df = pd.DataFrame(ad.euro_debut_years)

    # categorize debut years
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

    debut_df["Debut Years"] = debut_df["Debut year"].apply(categorize_year)

    query = """
        SELECT
            sa.country,
            sa.'Total Points',
            sa.lat,
            sa.lon,
            sa.'Semi Final',
            d.'Debut Years' as 'Eurovision Debut Year'
        FROM scores_with_coords as sa
        LEFT JOIN debut_df as d ON d.Country=sa.country
    """
    final_df = sqldf(query, locals())

    # scale points
    scaler = MinMaxScaler()
    final_df['score_scaled'] = scaler.fit_transform(final_df[['Total Points']])

    final_df['lat'] = final_df['lat'].astype(float)
    final_df['lon'] = final_df['lon'].astype(float)

    # categorize total points
    bins = [0, 50, 150, 250, 350, 450, 550, 650]
    colors = ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#8c2d04']
    bin_labels = [f'{bins[i]} - {bins[i + 1]}' for i in range(len(bins) - 1)]
    color_map = {}
    for bin_label in bin_labels:
        color_map[bin_label] = colors[bin_labels.index(bin_label)]
    final_df['Total Points Range'] = pd.cut(final_df['Total Points'], bins=bins, labels=bin_labels, precision=0, include_lowest=True)
    final_df['Total Points Range'] = pd.Categorical(final_df['Total Points Range'], categories=bin_labels, ordered=True)
    if group != 'No Groups':
        score_df = final_df.groupby(['country', group])[['Total Points','score_scaled']].mean().reset_index()
        score_df.columns = ['country', group, 'Total Points', 'score_scaled']

        # colors and shapes for markers
        if group == 'Eurovision Debut Year':
            symbols = {
                '1950s-1960s': 'circle',
                '1970s-1980s': 'square',
                '1990s-2000s': 'cross',
                '2010s-2020s': 'triangle-up'
            }
            colors = {
                '1950s-1960s': '#4daf4a',
                '1970s-1980s': '#984ea3',
                '1990s-2000s': '#377eb8',
                '2010s-2020s': '#e41a1c'
            }
        elif group == 'Semi Final':
            symbols = {
                'Top 5/Host': 'circle',
                "1st Semi Final": 'square',
                "2nd Semi Final": 'triangle-up'
            }
            colors = {
                'Top 5/Host': '#4daf4a',
                "1st Semi Final": '#984ea3',
                "2nd Semi Final": '#377eb8'
            }
        else:
            symbols ={}
            colors = {}

       # create map plot
        map_viso = px.choropleth(
            final_df,
            locations='country',
            locationmode='country names',
            color='Total Points Range',
            hover_name='country',
            hover_data={'score_scaled': False, group: False},
            custom_data=['country', 'Total Points', group],
            color_discrete_map=color_map,
            labels={'Total Points': 'Total Points'},
            category_orders={'Total Points Range': bin_labels},
            width=1800,
            height=550,
        )

        hover_template = (
                '<b>Country:</b> %{customdata[0]}<br>' +
                '<b>Total Points:</b> %{customdata[1]:.2f}<br>' +
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
                    '<b>Final Score: </b> ' + points.astype(str) + '<br>' +
                    '<b>Group:</b>'+chosen_type+'<br>'
            )

            trace = go.Scattergeo(
                lon=lon_values,
                lat=lat_values,
                text=text_values,
                hoverinfo='text',
                hovertemplate='%{text}',
                marker=dict(
                    symbol=symbol,
                    size=10,
                    color=colors[chosen_type],
                    line=dict(width=2, color='black')
                ),
                name=chosen_type,
                showlegend=True
            )

            map_viso.add_trace(trace)

        map_viso.update_layout(
            legend=dict(
                x=1,
                y=0.97,
                traceorder='normal',
                title=f'Final Score & {group}',
                itemsizing='constant'
            )
        )
    else:
        map_viso = px.choropleth(
            final_df,
            locations='country',
            locationmode='country names',
            color='Total Points Range',
            hover_name='country',
            hover_data={'score_scaled': False},
            custom_data=['country', 'Total Points'],
            color_discrete_map = color_map,
            labels={'Total Points': 'Total Points'},
            category_orders={'Total Points Range': bin_labels},
            width=1800,
            height=550,
        )
        hover_template = (
                '<b>Country:</b> %{customdata[0]}<br>' +
                '<b>Final Score:</b> %{customdata[1]:.2f}<br>'
        )
        map_viso.update_traces(hovertemplate=hover_template)
        map_viso.update_layout(
            coloraxis_colorbar=dict(
                title='Final Score',
                x=1,
                y=0.5,
                len=1,
            ),
        )
    map_viso.update_layout(template='plotly_white')
    map_viso.update_geos(projection_type="natural earth")

    if selected_country != 'All Countries':
        map_viso.update_geos(
            center = {"lat": ad.country_coor[selected_country][0], "lon": ad.country_coor[selected_country][1]},
            projection_scale=5
        )

    return map_viso
