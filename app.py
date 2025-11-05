import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Player Stats Visualization", layout="wide")

st.title("⚽ Player Performance Dashboard")

df = pd.read_csv('african_football_legends.csv', encoding='latin-1')
df_data = pd.DataFrame(df)

df_data.columns = (
    df_data.columns
    .str.strip()                     # remove leading/trailing spaces
    .str.lower()                     # convert to lowercase
    .str.replace(' ', '_')           # replace spaces with underscores
    .str.replace(r'[^\w\s]', '', regex=True)  # remove punctuation
)

print(df_data.columns)

# Calculate medians
median_goals = df_data['goals__penalty_kicks'].median()
median_assists = df_data['assists'].median()

# Create hover text
hover_text = [
    f"<b>{row['player']}</b><br>" +
    f"Goals: {row['goals__penalty_kicks']}<br>" +
    f"Assists: {row['assists']}<br>" +
    f"90-min Games: {row['number_of_90s_minimum_4']}<br>" +
    f"Position: {row['position']}<br>" +
    f"Best Season: {row['best_year_in_top_5_euro_league']}"
    for _, row in df_data.iterrows()
]

# Create the scatter plot
fig = go.Figure()

# Add scatter plot
fig.add_trace(go.Scatter(
    x=df_data['goals__penalty_kicks'],
    y=df_data['assists'],
    mode='markers',
    marker=dict(
        size=df_data['number_of_90s_minimum_4'],
        sizemode='diameter',
        sizeref=max(df_data['number_of_90s_minimum_4']) / 40,  # Adjust size scaling
        sizemin=5,
        color=df_data['number_of_90s_minimum_4'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            orientation='h',           # Horizontal orientation
            yanchor='top',
            y=-0.2,                    # Below the chart
            xanchor='center',
            x=0.5,                     # Centered
            title='Number of 90-min Games in best season',
            thickness=15,
            len=0.5                    # Width of colorbar
        ),
        line=dict(width=1, color='white')
    ),
    text=hover_text,
    hovertemplate='%{text}<extra></extra>',
    name='Players'
))

# Add median lines
fig.add_hline(y=median_assists, line_dash="dash", line_color="red", 
              annotation_text=f"Median Assists: {median_assists}",
              annotation_position="right")

fig.add_vline(x=median_goals, line_dash="dash", line_color="blue",
              annotation_text=f"Median Goals: {median_goals}",
              annotation_position="top")

# Update layout
fig.update_layout(
    title="Player Performance: Goals vs Assists",
    xaxis_title="Goals (excluding penalties)",
    yaxis_title="Assists",
    height=600,
    hovermode='closest',
    plot_bgcolor='rgba(240,240,240,0.5)',
    xaxis=dict(gridcolor='white'),
    yaxis=dict(gridcolor='white')
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Display summary statistics
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Players", len(df_data))
with col2:
    st.metric("Avg Goals", f"{df_data['goals__penalty_kicks'].mean():.1f}")
with col3:
    st.metric("Avg Assists", f"{df_data['assists'].mean():.1f}")

# Display data table
with st.expander("View Raw Data"):
    st.dataframe(df_data, use_container_width=True)