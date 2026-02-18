
import pickle
import re
import pandas as pd
import streamlit as st


from branca.element import Element
import folium
from streamlit_folium import st_folium

from my_colors import MyColors

def load_data(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data

def draw_folium_maps(row, refresh_key, style):
    m = folium.Map(
        location=[row.long, row.lat],
        zoom_start=16,
        tiles = style,
        dragging=True,
        zoom_control=False,
        scrollWheelZoom=True,
        doubleClickZoom=False,
        attributionControl=False,
        control_scale=True,
    )

    folium.CircleMarker(
        location=[row.long, row.lat],
        radius=10,
        color=MyColors.lines[0],
        fill=True,
        tooltip=folium.Tooltip(
            f"Approaches: {row.approaches}<br>Lane(s): {row.lane_type}<br>Controls: {row.control_type}", 
            # f"Approaches={row.approaches.iloc[0]}<br>Type={row.lane_type.iloc[0]}", 
            style="font-size: 10px;")
    ).add_to(m)

    if row.name2 == 'Place Charles de Gaulle':
        st.markdown("""
        <style>
        iframe {
            border-radius: 50% !important;
            overflow: hidden;
            border: 10px solid #ff0000 !important;
        }
        </style>
        """, unsafe_allow_html=True)    
        st.markdown("<div style='color: red;'>You found it!</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        iframe {
            border-radius: 50% !important;
            overflow: hidden;
            border: 3px solid #1f77b4 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st_folium(m, width='100%', height=450, key=refresh_key)

    # hard coded new lines <br>
    row_names = re.sub(r'\.', '', row.name2)
    # row_names = re.sub(r'<br>$', '', row_names)
    st.markdown(f"<div style='text-align: center; font-weight: 150'>{row_names}</div><br><div style='text-align: center; font-size: 24px; font-weight: bold;'>{row.town_city}</div><div style='text-align: center; font-size: 20px; font-weight: 100;  font-style: italic;'>{row.country}</div>", unsafe_allow_html=True)

def tidy_data(df) -> pd.DataFrame:
    df['name2'] = df['name'].str.replace('\\s/\\s', '<br>', regex=True)
    df['lane_type'] = df['lane_type'].str.replace(', unspecified)', '', regex=False)
    df['lane_type'] = df['lane_type'].str.replace(')', '', regex=False)
    df['lane_type'] = df['lane_type'].str.replace('Multilane (', '', regex=False)
    df['lane_type'] = df['lane_type'].str.replace('2 Lane', 'Two-lane', regex=False)
    return df

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_country_list(df):
    return sorted(df.country.str.strip().drop_duplicates().tolist())

def get_city_list(country, df):
    df_temp = df[df.country == country]
    return sorted(df_temp.town_city.str.strip().drop_duplicates().tolist())

def get_roundabout_list(country, city, n_approaches, df):
    df_temp = df[(df.country == country) & (df.town_city == city) & (df.approaches == n_approaches)]
    return sorted(df_temp.name.str.strip().tolist())

def get_n_approaches_list(country, city, df):
    df_temp = df[(df.country == country) & (df.town_city == city)]
    return sorted(df_temp.approaches.drop_duplicates().tolist())


# Data - Auckland
df = load_data('all.pickle')
df = tidy_data(df)
ncols = 1

st.set_page_config(layout="wide")

load_css()

if "refresh_key" not in st.session_state:
    st.session_state.refresh_key = 0

st.title("Find Roundabouts Near You?")

st.write(f"Data set contains locations of {df.shape[0]} roundabouts around the world")

st.sidebar.header("Filter Options")

style = st.sidebar.selectbox("Choose MAP STYLE", sorted(["OpenStreetMap", 'OpenTopoMap', 'Esri WorldStreetMap', "CartoDB positron"]))

country = st.sidebar.selectbox("Choose COUNTRY", get_country_list(df))

city = st.sidebar.selectbox("Choose CITY/TOWN", get_city_list(country, df))

n_approaches = st.sidebar.selectbox("Choose NUMBER OF APPROACHES", get_n_approaches_list(country, city, df))

roundabout_list = get_roundabout_list(country, city, n_approaches, df)

name = st.sidebar.selectbox(f"Choose ROUNDABOUT ({len(roundabout_list)})", get_roundabout_list(country, city, n_approaches, df))

st.sidebar.write("")

if st.sidebar.button("Refresh Map"):
    st.session_state.refresh_key += 1

row = df[(df.country == country) & (df.town_city == city) & (df.approaches == n_approaches) & (df.name == name)].iloc[0, :]

draw_folium_maps(row, refresh_key=st.session_state.refresh_key, style=style)

