import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Spotify Music Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    # Changed path from "../data/" to "data/" for Streamlit Cloud compatibility
    try:
        df = pd.read_csv("data/spotify_tracks.csv")
    except FileNotFoundError:
        # Fallback for local development if your structure differs
        df = pd.read_csv("../data/spotify_tracks.csv")
    
    df = df.drop_duplicates()
    df = df[(df["popularity"] >= 0) & (df["popularity"] <= 100)]

    top_genres = df["track_genre"].value_counts().nlargest(10).index
    df = df[df["track_genre"].isin(top_genres)]

    return df


df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

genre = st.sidebar.multiselect(
    "Select Genre(s)",
    options=df["track_genre"].unique(),
    default=df["track_genre"].unique()
)

popularity_range = st.sidebar.slider(
    "Select Popularity Range",
    min_value=0,
    max_value=100,
    value=(0, 100)
)

filtered_df = df[
    (df["track_genre"].isin(genre)) &
    (df["popularity"].between(popularity_range[0], popularity_range[1]))
]

# -----------------------------
# Title
# -----------------------------
st.title("🎧 Spotify Music Analytics Dashboard")
st.markdown(
    "This interactive dashboard explores Spotify song characteristics, "
    "genres, and popularity using audio features."
)

# -----------------------------
# Row 1: Popularity distribution & Average popularity by genre
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        filtered_df,
        x="popularity",
        nbins=30,
        title="Distribution of Song Popularity"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    genre_pop = (
        filtered_df
        .groupby("track_genre", as_index=False)["popularity"]
        .mean()
        .sort_values("popularity", ascending=False)
    )
    fig2 = px.bar(
        genre_pop,
        x="track_genre",
        y="popularity",
        title="Average Popularity by Genre"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Row 2: Danceability vs popularity & Energy vs popularity
# -----------------------------
col3, col4 = st.columns(2)

with col3:
    fig3 = px.scatter(
        filtered_df,
        x="danceability",
        y="popularity",
        title="Danceability vs Popularity",
        hover_data=["track_name", "artists"]
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(
        filtered_df,
        x="energy",
        y="popularity",
        title="Energy vs Popularity",
        hover_data=["track_name", "artists"]
    )
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Row 3: Average audio features by genre
# -----------------------------
features = ["danceability", "energy", "valence"]
genre_features = (
    filtered_df
    .groupby("track_genre")[features]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    genre_features,
    x="track_genre",
    y=features,
    barmode="group",
    title="Average Audio Features by Genre"
)
st.plotly_chart(fig5, use_container_width=True)
