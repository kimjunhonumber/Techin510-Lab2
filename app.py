import streamlit as st
import pandas as pd
import plotly.express as px  # Import Plotly Express

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Penguins Explorer",
    page_icon="🐧",
    layout="centered",  # Use "wide" for a wider layout
    initial_sidebar_state="auto", 
)

# Title for the app
st.title("🐧 Penguins Explorer")

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/mcnakhaee/palmerpenguins/master/palmerpenguins/data/penguins.csv')

# Safety check to ensure the DataFrame isn't empty
if df.empty:
    st.error("Data could not be loaded. Please check the data source.")
else:
    # Slider for selecting bill length range
    min_bill_length, max_bill_length = st.slider(
        "Bill Length (mm)",
        float(df["bill_length_mm"].min()),  # Convert to float for safety
        float(df["bill_length_mm"].max()),
        (float(df["bill_length_mm"].min()), float(df["bill_length_mm"].max()))  # Default range
    )

    # Select box for choosing species
    species_filter = st.selectbox(
        "Species",
        options=df["species"].unique(),
        index=0  # Default selection
    )

    # Multiselect for choosing islands
    island_filter = st.multiselect(
        "Island",
        options=df["island"].unique(),
        default=df["island"].unique()  # Default to all options selected
    )

    # Filter the DataFrame based on the user's choices
    df_filtered = df[
        (df["bill_length_mm"] >= min_bill_length) & 
        (df["bill_length_mm"] <= max_bill_length) &
        (df["species"] == species_filter)
    ]
    
    if island_filter:
        df_filtered = df_filtered[df_filtered["island"].isin(island_filter)]

    # Display the filtered DataFrame
    st.write(df_filtered)

    # Plotting the distribution of bill lengths in the filtered DataFrame
    fig = px.histogram(
        df_filtered,
        x="bill_length_mm",
        title="Distribution of Bill Lengths",
        labels={"bill_length_mm": "Bill Length (mm)"}
    )
    st.plotly_chart(fig)
    fig2 = px.scatter(
        df,
        x="bill_length_mm",
        y="bill_depth_mm"
    )
    st.plotly_chart(fig2)