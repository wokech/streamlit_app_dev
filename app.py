import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Player Performance Dashboard", layout="wide")

st.title("⚽ Player Performance Dashboard") 

# Load data
df = pd.read_csv('african_football_legends.csv', encoding='latin-1')
df_data = pd.DataFrame(df)

# Clean column names
df_data.columns = (
    df_data.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace(r'[^\w\s]', '', regex=True)
)

# Required columns check (optional best practice)
required_cols = ['player', 'goals__penalty_kicks', 'assists', 'era', 
                 'number_of_90s_minimum_4', 'position', 'best_year_in_top_5_euro_league']
missing = [c for c in required_cols if c not in df_data.columns]
if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# Summary statistics (rounded assist median to 3 decimals)
median_goals = df_data['goals__penalty_kicks'].median()
median_assists = round(df_data['assists'].median(), 3)

# Color map for eras
era_color_map = {
    'Nineties': '#E4572E',   # warm red-orange
    'Twenty-Noughts': '#4C78A8',   # cool blue
    'Twenty-Tens': '#72B7B2',   # teal
    'Twenty-Twenties': '#F2A541',  # amber
}

# Maximum values for scaling
max_size = df_data['number_of_90s_minimum_4'].max()

fig = go.Figure()

# Add scatter traces grouped by era (color legend)
for era, group in df_data.groupby('era'):
    fig.add_trace(go.Scatter(
        x=group['goals__penalty_kicks'],
        y=group['assists'],
        mode='markers',
        name=f"Era: {era.capitalize()}",
        marker=dict(
            size=group['number_of_90s_minimum_4'],
            sizemode='diameter',
            sizeref=max_size / 40,
            sizemin=6,
            color=era_color_map.get(era, "#888888"),
            line=dict(width=1, color='white')
        ),
        text=[
            f"<b>{row['player']}</b><br>"
            f"Goals: {row['goals__penalty_kicks']}<br>"
            f"Assists: {row['assists']}<br>"
            f"90-Min Matches: {row['number_of_90s_minimum_4']}<br>"
            f"Position: {row['position']}<br>"
            f"Era: {row['era']}<br>"
            f"Best Season: {row['best_year_in_top_5_euro_league']}"
            for _, row in group.iterrows()
        ],
        hovertemplate='%{text}<extra></extra>'
    ))

# ⚽ SIZE LEGEND (3 reference bubbles)
size_reference_levels = [5, 10, 40]  # adjust depending on your data
for size in size_reference_levels:
    fig.add_trace(go.Scatter(
        x=[None], y=[None],  # invisible point off-plot
        mode='markers',
        name=f"{size} games",
        marker=dict(
            size=size,
            sizemode='diameter',
            sizeref=max_size / 40,
            sizemin=5,
            color='lightgray',
            line=dict(width=1, color='gray')
        ),
        showlegend=True
    ))

# Median reference lines
fig.add_hline(y=median_assists, line_dash="dot", line_color="gray",
              annotation_text=f"Median Assists = {median_assists}",
              annotation_position="right", annotation_font_size=12)

fig.add_vline(x=median_goals, line_dash="dot", line_color="gray",
              annotation_text=f"Median Goals = {median_goals}",
              annotation_position="top", annotation_font_size=12)

# Layout styling
fig.update_layout(
    title="<b>Goals vs Assists by Era</b>",
    xaxis_title="Goals (excluding penalties)",
    yaxis_title="Assists",
    height=650,
    legend_title="<b>Legend</b>",
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="white",
    xaxis=dict(gridcolor='white'),
    yaxis=dict(gridcolor='white'),
    hovermode='closest'
)

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