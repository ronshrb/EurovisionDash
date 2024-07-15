from libs.pandasql import sqldf
import plotly.graph_objects as go
from scipy.stats import trim_mean

def create_viso(df, mode='Total Score', colorblind_mode=False):

    scores = df
    query = """
        SELECT
            year,
            country,
            final_draw_position,
            final_place,
            final_total_points,
            final_jury_points,
            final_televote_points
        FROM scores
        WHERE qualified_10 = '1' OR direct_qualifier_10='1' AND final_draw_position != '27'
    """
    score_post = sqldf(query, locals())
    score_post = score_post.dropna()
    df = score_post
    df['final_draw_position'] = df['final_draw_position'].astype(int)

    if mode == 'Total Score':
        # Calculate trimmed mean points and places for each draw position
        trimmed_mean_score = df.groupby('final_draw_position')['final_total_points'].apply(
            lambda x: round(trim_mean(x, proportiontocut=0.1), 2)).reset_index()

        # Sort the DataFrames by final_draw_position
        df_sorted = df.sort_values('final_draw_position')
        trimmed_mean_score_sorted = trimmed_mean_score.sort_values('final_draw_position')

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_sorted['final_draw_position'],
            y=df_sorted['final_total_points'],
            mode='markers',
            marker=dict(
                size=10,
                color='#5aae61' if not colorblind_mode else '#E69F00',
                opacity=0.6,
            ),
            text=[f'Country: {country}<br>Year: {year}<br>Running Position: {draw_position}<br>Final Place: {place}'
                  for country, year, draw_position, place in
                  zip(df_sorted['country'], df_sorted['year'], df_sorted['final_draw_position'],
                      df_sorted['final_total_points'])],
            hoverinfo='text',
            name='Individual Total Score'
        ))

        fig.add_trace(go.Scatter(
            x=trimmed_mean_score_sorted['final_draw_position'],
            y=trimmed_mean_score_sorted['final_total_points'],
            mode='lines+markers',
            marker=dict(
                size=10,
                color='#1b7837' if not colorblind_mode else '#56B4E9',
            ),
            line=dict(
                width=2,
                color='#1b7837' if not colorblind_mode else '#56B4E9',
            ),
            text=[f'Running Position: {draw_position}<br>Trimmed Mean Final Place: {place}'
                  for draw_position, place in
                  zip(trimmed_mean_score_sorted['final_draw_position'],
                      trimmed_mean_score_sorted['final_total_points'])],
            hoverinfo='text',
            name='Trimmed Mean Total Score'
        ))
    else:
        # Calculate trimmed mean points and places for each draw position
        trimmed_mean_score = df.groupby('final_draw_position')['final_televote_points'].apply(
            lambda x: round(trim_mean(x, proportiontocut=0.1), 2)).reset_index()

        # Sort the DataFrames by final_draw_position
        df_sorted = df.sort_values('final_draw_position')
        trimmed_mean_score_sorted = trimmed_mean_score.sort_values('final_draw_position')

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_sorted['final_draw_position'],
            y=df_sorted['final_televote_points'],
            mode='markers',
            marker=dict(
                size=10,
                color='#fdae61' if not colorblind_mode else '#E69F00',
                opacity=0.6,
            ),
            text=[f'Country: {country}<br>Year: {year}<br>Running Position: {draw_position}<br>Final Place: {place}<br> Type: Televote'
                  for country, year, draw_position, place in
                  zip(df_sorted['country'], df_sorted['year'], df_sorted['final_draw_position'], df_sorted['final_televote_points'])],
            hoverinfo='text',
            name='Individual Televote Score'
        ))

        fig.add_trace(go.Scatter(
            x=df_sorted['final_draw_position'],
            y=df_sorted['final_jury_points'],
            mode='markers',
            marker=dict(
                size=10,
                color='#7570b3' if not colorblind_mode else '#009E73',
                opacity=0.6,
            ),
            text=[f'Country: {country}<br>Year: {year}<br>Running Position: {draw_position}<br>Final Place: {place}<br> Type: Jury'
                  for country, year, draw_position, place in
                  zip(df_sorted['country'], df_sorted['year'], df_sorted['final_draw_position'], df_sorted['final_televote_points'])],
            hoverinfo='text',
            name='Individual Jury Score'
        ))

        fig.add_trace(go.Scatter(
            x=trimmed_mean_score_sorted['final_draw_position'],
            y=trimmed_mean_score_sorted['final_televote_points'],
            mode='lines+markers',
            marker=dict(
                size=10,
                color='#e66101' if not colorblind_mode else '#0072B2',
            ),
            line=dict(
                width=2,
                color='#e66101' if not colorblind_mode else '#0072B2',
            ),
            text=[f'Running Position: {draw_position}<br>Trimmed Mean Final Place: {place}<br> Type: Televote'
                  for draw_position, place in
                  zip(trimmed_mean_score_sorted['final_draw_position'],
                      trimmed_mean_score_sorted['final_televote_points'])],
            hoverinfo='text',
            name='Trimmed Mean Televote Score'
        ))

        trimmed_mean_score = df.groupby('final_draw_position')['final_jury_points'].apply(
            lambda x: round(trim_mean(x, proportiontocut=0.1), 2)).reset_index()

        trimmed_mean_score_sorted = trimmed_mean_score.sort_values('final_draw_position')
        fig.add_trace(go.Scatter(
            x=trimmed_mean_score_sorted['final_draw_position'],
            y=trimmed_mean_score_sorted['final_jury_points'],
            mode='lines+markers',
            marker=dict(
                size=10,
                color='#762a83' if not colorblind_mode else '#CC79A7',
            ),
            line=dict(
                width=2,
                color='#762a83' if not colorblind_mode else '#CC79A7',
            ),
            text=[f'Running Position: {draw_position}<br>Trimmed Mean Final Place: {place}<br> Type: Jury'
                  for draw_position, place in
                  zip(trimmed_mean_score_sorted['final_draw_position'], trimmed_mean_score_sorted['final_jury_points'])],
            hoverinfo='text',
            name='Trimmed Mean Jury Score'
        ))

    fig.update_layout(
        xaxis_title='Running Order',
        yaxis_title='Total Score',
        xaxis=dict(
            tickmode='linear',
            tickangle=0,
            tick0=0,
            dtick=1,
            range=[0.5, 26.5],
            titlefont=dict(
                size=20
            )
        ),
        yaxis=dict(
            rangemode='tozero',
            titlefont=dict(
                size=20
            ),
        ),
        showlegend=True,
        width=600,
        height=500,
        legend=dict(
            font=dict(
                size=15
            ),
            x=0.8,
            y=1.2,
            bgcolor='rgba(0,0,0,0)',
            xanchor='center',
            yanchor='middle',
        ),
        plot_bgcolor='rgba(240, 240, 240, 1)'
    )

    return fig

