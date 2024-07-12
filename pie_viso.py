from pandasql import sqldf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go

def create_viso(dfs, selected_years):
    scores = dfs['song_data']

    query = """
        SELECT
            year,
            country,
            language,
            style,
            key,
            BPM,
            energy,
            danceability,
            happiness,
            loudness,
            acousticness,
            instrumentalness,
            liveness,
            speechiness,
            qualified_10,
            final_place,
            final_total_points
        FROM scores
    """

    song_data = sqldf(query, locals())


    cont_cols_arr = ['BPM', 'energy', 'danceability', 'happiness', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    num_bins = 5

    song_data_temp = song_data.copy()
    binned_columns = []
    for col in cont_cols_arr:
        # Ensure the column is numeric, coercing errors to NaN
        song_data_temp[col] = pd.to_numeric(song_data_temp[col], errors='coerce')
        # Drop NaN values to avoid issues with binning
        song_data_temp = song_data_temp.dropna(subset=[col])
        # Create bins and convert intervals to strings
        bin_col_name = f'{col}_bin'
        song_data_temp[bin_col_name] = pd.cut(song_data_temp[col], bins=num_bins).apply(lambda x: f"{x.left} - {x.right}")
        binned_columns.append(bin_col_name)

    new_df = song_data_temp[binned_columns].copy()
    new_df.columns = cont_cols_arr

    new_df['Genre'] = song_data_temp['style']
    new_df['final_total_points'] = song_data_temp['final_total_points']

    def create_pie_data(df, column_name):
        pie_data = df[column_name].value_counts().reset_index()
        pie_data.columns = [column_name, 'count']
        if column_name in cont_cols_arr:
            pie_data['sort_key'] = pie_data[column_name].apply(lambda x: float(x.split(' - ')[0]))
            pie_data = pie_data.sort_values(by='sort_key', ascending=False).drop(columns='sort_key')
        return pie_data, column_name

    # Initial column to display
    initial_column = 'Genre'
    pie_data, column_name = create_pie_data(new_df, initial_column)

    # Create the initial donut chart
    fig = go.Figure()

    # Inner donut chart
    fig.add_trace(go.Pie(
        labels=pie_data[column_name],
        values=pie_data['count'],
        hoverinfo='label+percent',
        textinfo='value',
        name=initial_column,
        hole=0.4,
        domain={'x': [0.3, 0.7], 'y': [0.3, 0.7]}  # Adjust domain to create margin between inner and outer ring
    ))

    # Outer donut chart for total points
    outer_data = new_df.groupby(initial_column)['final_total_points'].sum().reset_index()

    # If the initial column is a range, sort by the range
    if initial_column in cont_cols_arr:
        outer_data = outer_data.sort_values(by=initial_column, key=lambda x: x.str.split(' - ').str[0].astype(float), ascending=True)

    fig.add_trace(go.Pie(
        labels=outer_data[initial_column],
        values=outer_data['final_total_points'],
        hoverinfo='label+percent',
        textinfo='value',
        name='Total Points',
        hole=0.7,
        domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}  # Adjust domain to create margin between inner and outer ring
    ))

    # Function to update pie chart data and sort the legend
    def update_pie_chart_data(df, column_name):
        pie_data, column_name = create_pie_data(df, column_name)
        return pie_data, column_name

    # Function to update the outer donut chart for total points
    def update_outer_pie_chart_data(df, column_name):
        outer_data = df.groupby(column_name)['final_total_points'].sum().reset_index()
        if column_name in cont_cols_arr:
            outer_data = outer_data.sort_values(by=column_name, key=lambda x: x.str.split(' - ').str[0].astype(float), ascending=True)
        return outer_data

    # Update layout with dropdowns for column
    fig.update_layout(
        title=f'Distribution of {initial_column}',
        width=1000,  # Set the width of the figure
        height=500,  # Set the height of the figure
        updatemenus=[
            dict(
                buttons=[dict(
                    args=[{
                        "values": [update_pie_chart_data(new_df, col)[0]['count']],
                        "labels": [update_pie_chart_data(new_df, col)[0][update_pie_chart_data(new_df, col)[1]]],
                        "values2": [update_outer_pie_chart_data(new_df, col)['final_total_points']],
                        "labels2": [update_outer_pie_chart_data(new_df, col)[col]]},
                        {"title": f"Distribution of {col}"}],
                    label=f"{col}",
                    method="update"
                ) for col in new_df.columns if col not in ['final_total_points']],  # Include all columns except 'final_total_points'
                direction="down",
                showactive=True
            )
        ]
    )

    return fig