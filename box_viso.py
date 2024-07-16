import plotly.graph_objects as go
import pandas as pd
from pandasql import sqldf
def create_viso(df, colorblind_mode=False):
    # create a new column that says if a country is a host or not
    query = """
            SELECT
                country,
                final_total_points as 'Total Points',
                CASE
                    WHEN host_10 = '1' THEN 'Host'
                    ELSE semi_final
                END as 'Semi Final'
            FROM df
            WHERE qualified_10 = '1' OR qualified_10 = '-'
            """
    df = sqldf(query, locals())
    # fill the semi final column with the correct values
    query = """
        SELECT
            country,
            df.'Total Points',
            CASE
                WHEN df.'Semi Final' = '-' THEN 'Top 5'
                WHEN df.'Semi Final' = '1' THEN '1st Semi Final'
                WHEN df.'Semi Final' = '2' THEN '2nd Semi Final'
                ELSE df.'Semi Final'
            END as 'Semi Final'
        FROM df
        """
    df = sqldf(query, locals())

    if colorblind_mode:
        colors = ['#E69F00', '#56B4E9', '#009E73', '#0072B2']
    else:
        colors = ['#e78ac3', '#66c2a5', '#fc8d62', '#8da0cb']

    # the box plot
    fig = go.Figure()

    for i, semi_final in enumerate(df['Semi Final'].unique()):
        filtered_df = df[df['Semi Final'] == semi_final]
        fig.add_trace(go.Box(
            y=filtered_df['Total Points'],
            name=semi_final,
            marker=dict(color=colors[i % len(colors)])
        ))

    fig.update_layout(
        xaxis_title='Semi Final',
        yaxis_title='Total Points',
        xaxis=dict(
            tickmode='linear',
            tickangle=0,
            tickfont=dict(size=13),
            titlefont=dict(size=18),
        ),
        yaxis=dict(
            rangemode='tozero',
            titlefont=dict(size=18)
        ),
        showlegend=False,
        width=800,
        height=600,
        plot_bgcolor='rgba(240, 240, 240, 1)'
    )

    return fig