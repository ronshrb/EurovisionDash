from libs.pandasql import sqldf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import additional_data as ad

def create_viso(df, selected_year, selected_country, colorblind_mode=False):

    # turn country_coor into df
    data = [(country, coords[0], coords[1]) for country, coords in ad.country_coor.items()]
    coords_df = pd.DataFrame(data, columns=['country', 'lat', 'lon'])

    scores = df
    query = """
            SELECT *
            FROM scores
            WHERE qualified_10 = '1' OR qualified_10 = '-'
        """
    scores = sqldf(query, locals())
    # merge with coords and find average score
    query = """
        SELECT
            a.country,
            a.'final_total_points'/count(*) as 'Average Total Points',
            c.lat,
            c.lon
        FROM scores as a
        LEFT JOIN coords_df as c ON c.country=a.country
        group by a.country
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
            sa.'Average Total Points',
            sa.lat,
            sa.lon,
            d.'Debut Years' as 'Eurovision Debut Year'
        FROM scores_with_coords as sa
        LEFT JOIN debut_df as d ON d.Country=sa.country
    """
    final_df = sqldf(query, locals())

    final_df['lat'] = final_df['lat'].astype(float)
    final_df['lon'] = final_df['lon'].astype(float)
    final_df['Average Total Points'] = round(final_df['Average Total Points'],2)

    # categorize total points
    bins = [0, 50, 150, 250, 350, 450, 550, 650]

    # Define colors based on colorblind_mode
    if colorblind_mode:
        colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
    else:
        colors = ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#8c2d04']

    bin_labels = [f'{bins[i]} - {bins[i + 1]}' for i in range(len(bins) - 1)]
    color_map = {bin_label: colors[i] for i, bin_label in enumerate(bin_labels)}

    final_df['Average Total Points Range'] = pd.cut(final_df['Average Total Points'], bins=bins, labels=bin_labels, precision=0, include_lowest=True)
    final_df['Average Total Points Range'] = pd.Categorical(final_df['Average Total Points Range'], categories=bin_labels, ordered=True)

    symbols = {
        '1950s-1960s': 'circle',
        '1970s-1980s': 'square',
        '1990s-2000s': 'cross',
        '2010s-2020s': 'triangle-up'
    }
    if colorblind_mode:
        colors = {
            '1950s-1960s': '#CC79A7',
            '1970s-1980s': '#D55E00',
            '1990s-2000s': '#009E73',
            '2010s-2020s': '#F0E442'
        }
    else:
        colors = {
            '1950s-1960s': '#4daf4a',
            '1970s-1980s': '#984ea3',
            '1990s-2000s': '#377eb8',
            '2010s-2020s': '#e41a1c'
        }

        # create map plot
    map_viso = px.choropleth(
            final_df,
            locations='country',
            locationmode='country names',
            color='Average Total Points Range',
            hover_name='country',
            hover_data={'Average Total Points': False, 'Eurovision Debut Year': False},
            custom_data=['country', 'Average Total Points', 'Eurovision Debut Year'],
            color_discrete_map=color_map,
            labels={'Average Total Points': 'Average Total Points'},
            category_orders={'Average Total Points Range': bin_labels},
            width=1800,
            height=700,
        )

    hover_template = (
            '<b>Country:</b> %{customdata[0]}<br>' +
            '<b>Average Total Score:</b> %{customdata[1]:.2f}<br>' +
            '<b>Group:</b> %{customdata[2]}<br>'
        )
    map_viso.update_traces(hovertemplate=hover_template)

    for chosen_type, symbol in symbols.items():
            subset = final_df[final_df['Eurovision Debut Year'] == chosen_type]
            lon_values = subset.apply(lambda row: final_df[final_df['country'] == row['country']]['lon'].values[0], axis=1)
            lat_values = subset.apply(lambda row: final_df[final_df['country'] == row['country']]['lat'].values[0], axis=1)
            points = subset['Average Total Points']
            text_values = (
                '<b>Country: </b> ' + subset['country'].astype(str) + '<br>' +
                '<b>Average Total Score: </b> ' + round(points.astype(str),2) + '<br>' +
                '<b>Group:</b>' + chosen_type + '<br>'
            )

            trace = go.Scattergeo(
                lon=lon_values,
                lat=lat_values,
                text=text_values,
                hoverinfo='text',
                hovertemplate='%{text}',
                marker=dict(
                    symbol=symbol,
                    size=7,
                    color=colors[chosen_type],
                    line=dict(width=1, color='black')
                ),
                name=chosen_type,
                showlegend=True
            )
            map_viso.add_trace(trace)
    map_viso.update_layout(
        legend=dict(
            x=1.02,
            y=0.85,
            traceorder='normal',
            title=dict(text=f'Final Score & Debut Year',
                       font=dict(
                           size=18)
                       ),
            itemsizing='constant',
            font=dict(
                size=15
            ),
        )
    )

    map_viso.update_layout(template='plotly_white')
    map_viso.update_geos(projection_type="natural earth")

    if selected_country != 'All Countries':
        map_viso.update_geos(
            center={"lat": ad.country_coor[selected_country][0], "lon": ad.country_coor[selected_country][1]},
            projection_scale=5
        )

    return map_viso

