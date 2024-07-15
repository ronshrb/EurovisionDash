
import pandas as pd
import plotly.graph_objects as go

def create_viso(df, feature='style'):
    scores = df

    grouped_data = scores.groupby(feature).agg({
        'final_total_points': ['mean', 'count']
    }).reset_index()

    grouped_data.columns = [feature, 'Average Score', 'Number of Songs']

    # Calculate standard deviation per group
    std_dev = scores.groupby(feature)['final_total_points'].std().reset_index()
    std_dev.columns = [feature, 'Std Dev']

    # Merge standard deviation back to grouped data
    grouped_data = pd.merge(grouped_data, std_dev, on=feature, how='left')

    # Calculate normalized score
    grouped_data['Normalized Score'] = grouped_data['Average Score'] / grouped_data['Std Dev'].replace(0, pd.NA)

    # Replace NaN values with 0 (if desired)
    grouped_data['Normalized Score'] = grouped_data['Normalized Score'].fillna(0)
    grouped_data['Normalized Score'] = grouped_data['Normalized Score'].round(2)
    grouped_data['Average Score'] = grouped_data['Average Score'].round(2)

    if feature != 'style':
        grouped_data = grouped_data[(grouped_data[feature] != '-') & (grouped_data[feature].notna())]
        grouped_data[feature] = grouped_data[feature].astype(float)
        bins = pd.cut(grouped_data[feature], bins=6, precision=0)  # Adjust number of bins and precision as needed
        labels = bins.astype(str)
        grouped_data[feature] = labels

    grouped_data_sorted = grouped_data.sort_values(by=['Average Score'])
    fig = go.Figure()
    # Inner donut chart
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f']
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
        hoverinfo='percent+value',
        textinfo='percent+label',
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
        height=500,
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
