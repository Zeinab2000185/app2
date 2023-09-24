import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
df = pd.read_csv('InOut.csv')
df = df.replace('', 0)

# Title and Sidebar
st.title("Lebanon Immigration Data")
st.sidebar.title("Interactive Options")

# Add search bar to filter the first visual (Bar Chart) by country
if st.sidebar.checkbox("Filter by Country"):
    search_country = st.sidebar.text_input("Enter a country name:")
else:
    search_country = None

# Add search bar to filter visuals by type
visual_type = st.sidebar.selectbox("Select Visual Type", ["Bar Chart", "Choropleth Map", "Scatter Plot", "Sunburst Chart"])

# Filter data based on selected visual type
if visual_type == "Bar Chart":
    st.subheader("Influx of Nationalities into Lebanon (Excluding Arabs)")
    values2 = ["Arabs"]
    df_filtered = df.loc[~df['Group'].isin(values2)]
elif visual_type == "Choropleth Map":
    st.subheader("Influx of Nationalities into Lebanon by Year (Including Arabs, Excluding Lebanon and Syria)")
    values3 = ["Lebanon", "Syria"]
    df_filtered = df.loc[~df['Country'].isin(values3)]
elif visual_type == "Scatter Plot":
    st.subheader("Influx and Outflux of Nationalities into Lebanon (Including Arabs, Excluding Lebanon and Syria)")
    values3 = ["Lebanon", "Syria"]
    df_filtered = df.loc[~df['Country'].isin(values3)]
elif visual_type == "Sunburst Chart":
    st.subheader("Snapshot of Influx into Lebanon in 2018 (Excluding Lebanon and Syria)")
    values3 = ["Lebanon", "Syria"]
    df_filtered = df.loc[~df['Country'].isin(values3)]

# Apply the country filter for the first visual (Bar Chart)
if search_country and visual_type == "Bar Chart":
    df_filtered = df_filtered[df_filtered['Country'].str.contains(search_country, case=False)]

# Create interactive visuals based on selected type
if visual_type == "Bar Chart":
    fig = px.bar(df_filtered, x="Group", y="In", color="Group",
                 animation_frame="Year", animation_group="Country")
    st.plotly_chart(fig)
elif visual_type == "Choropleth Map":
    fig = px.choropleth(df_filtered, locations='iso_alpha', color="In", hover_name='Country',
                        animation_frame='Year', color_continuous_scale=px.colors.sequential.Plasma,
                        projection='natural earth')
    st.plotly_chart(fig)
elif visual_type == "Scatter Plot":
    fig = px.scatter(df_filtered, x="In", y="Out", animation_frame="Year", animation_group="Country",
                     size="In", color="Country", hover_name="Country",
                     log_x=True, range_x=[10000, 300000], range_y=[10000, 300000])
    st.plotly_chart(fig)
elif visual_type == "Sunburst Chart":
    df7 = df_filtered.query("Year == 2018")
    fig = px.sunburst(df7, path=['Group', 'Country'], values='In',
                      color='Group', hover_data=['iso_alpha'])
    st.plotly_chart(fig)
