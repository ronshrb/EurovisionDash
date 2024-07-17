
import pandas as pd
import plotly.graph_objects as go
from libs.pandasql import sqldf

def create_viso(df, feature='style', colorblind_mode=False):
    if feature != 'style':
        df = df[(df[feature] != '-') & (df[feature].notna())]
        df[feature] = df[feature].astype(float)
        bins = pd.cut(df[feature], bins=6, precision=0)  # Adjust number of bins and precision as needed
        labels = bins.astype(str)
        df[feature] = labels

    query = f"""
                SELECT
                    {feature},
                    AVG(final_total_points) as 'Average Score',
                    COUNT(*) as 'Number of Songs'
                FROM df
                WHERE qualified_10 = '1' OR qualified_10 = '-'
                GROUP BY {feature}
                """
    grouped_data = sqldf(query, locals())

    grouped_data['Average Score'] = grouped_data['Average Score'].round(2)

    grouped_data_sorted = grouped_data.sort_values(by=['Average Score'])

    # Define colors based on colorblind_mode
    if colorblind_mode:
        colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00']
    else:
        colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f']

    fig = go.Figure()
    # Inner donut chart
    fig.add_trace(go.Pie(
        labels=grouped_data_sorted[feature],
        values=grouped_data_sorted['Number of Songs'],
        sort= False,
        hoverinfo='label+percent+value',
        textinfo='percent',
        textfont_size=15,
        hoverlabel_font_size=15,
        hole=0,
        domain={'x': [0.15, 0.85], 'y': [0.25, 0.75]}  # Add margin between inner and outer ring
    ))
    fig.add_trace(go.Pie(
        labels=grouped_data_sorted[feature],
        values=grouped_data_sorted['Average Score'],
        sort= False,
        hoverinfo='value',
        textinfo='value+label',
        name='Total Points',
        textfont_size=15,
        hoverlabel_font_size=15,
        hole=0.9,
        marker=dict(
            colors=colors
        )
    ))
    fig.update_layout(
        showlegend=False,
        width=600,
        height=600,
        legend=dict(
            font=dict(
                size=15
            ),
            x=0.5,
            y=1.1,
            bgcolor='rgba(0,0,0,0)',
            orientation='h',
            xanchor='center',
            yanchor='middle'
        ),
        plot_bgcolor='rgba(240, 240, 240, 1)'
    )

    return fig
