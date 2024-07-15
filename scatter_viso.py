from pandasql import sqldf
import plotly.graph_objects as go
from scipy.stats import trim_mean

def create_viso(df, mode='Total Score'):
    if mode == 'Total Score':
        voters = 'final_total_points'
    elif mode == 'Jury Score':
        voters = 'final_jury_points'
    elif mode == 'Televote Score':
        voters = 'final_televote_points'

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

    # Calculate trimmed mean points and places for each draw position
    trimmed_mean_score = df.groupby('final_draw_position')[voters].apply(
        lambda x: round(trim_mean(x, proportiontocut=0.1),2)).reset_index()

    # Sort the DataFrames by final_draw_position
    df_sorted = df.sort_values('final_draw_position')
    trimmed_mean_score_sorted = trimmed_mean_score.sort_values('final_draw_position')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted['final_draw_position'],
        y=df_sorted[voters],
        mode='markers',
        marker=dict(
            size=10,
            color='green',
            opacity=0.6,
        ),
        text=[f'Country: {country}<br>Year: {year}<br>Running Position: {draw_position}<br>Final Place: {place}'
              for country, year, draw_position, place in
              zip(df_sorted['country'], df_sorted['year'], df_sorted['final_draw_position'], df_sorted[voters])],
        hoverinfo='text',
        name='Individual Score'
    ))

    fig.add_trace(go.Scatter(
        x=trimmed_mean_score_sorted['final_draw_position'],
        y=trimmed_mean_score_sorted[voters],
        mode='lines+markers',
        marker=dict(
            size=10,
            color='orange',
        ),
        line=dict(
            width=2,
            color='orange',
        ),
        text=[f'Running Position: {draw_position}<br>Trimmed Mean Final Place: {place}'
              for draw_position, place in
              zip(trimmed_mean_score_sorted['final_draw_position'], trimmed_mean_score_sorted[voters])],
        hoverinfo='text',
        name='Trimmed Mean Score'
    ))

    fig.update_layout(
        # title='Final Score by Running Order and Type of Votes',
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
            y=1.1,
            bgcolor='rgba(0,0,0,0)',
            xanchor='center',
            yanchor='middle',
        ),
        plot_bgcolor='rgba(240, 240, 240, 1)'
    )

    return fig