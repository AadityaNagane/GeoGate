import openrouteservice
from openrouteservice import convert
import folium
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
from streamlit_folium import folium_static

# # Initialize Firebase app with credentials
# cred = credentials.Certificate("D:/SPIT/SEM 4/microproject/miniprojectfrontend/Basic Program/Key.json")
# firebase_admin.initialize_app(cred)

# # Initialize Firestore client
# db = firestore.client()

# Specify collection name and document ID
# collection_name = 'tatya'
# document_id = 'geopoint'

# Reference the document
# doc_ref = db.collection(collection_name).document(document_id)

# # Retrieve longitude and latitude from Firestore
# doc_data = doc_ref.get().to_dict()
# longitude = doc_data.get('longitude')
# latitude = doc_data.get('latitude')

import openrouteservice
from openrouteservice import convert
import folium
from shapely.geometry import Point, Polygon
import streamlit as st

def app():
    # Initialize OpenRouteService client with API key
    client = openrouteservice.Client(key='5b3ce3597851110001cf6248d4f4172ccaa242cab65930185ce46059')

    # Define coordinates for routing
    coords = ((72.84170220982669,19.228556018441456), ( 73.79631472329982,18.63753914054138))
    booth= (
    (19.037095, 73.071661),  # Cord 1
    (19.035766, 73.072364),  # Cord 2
    (19.037095, 73.073871),  # Cord 3
    (19.037808, 73.072816)   # Cord 4
    )
    # Streamlit sidebar input for user's location
    st.sidebar.title("User's Location")
    user_lat = st.sidebar.number_input("Latitude", value=19.123339770515123, step=0.01)
    user_lon = st.sidebar.number_input("Longitude", value=72.83635142888058, step=0.01)
    user_location = (user_lat, user_lon)


    # Get route information
    res = client.directions(coords)
    geometry = res['routes'][0]['geometry']

    # Decode polyline geometry
    decoded = convert.decode_polyline(geometry)

    # Calculate distance and duration
    distance_km = round(res['routes'][0]['summary']['distance'] / 1000, 1)
    duration_min = round(res['routes'][0]['summary']['duration'] / 60, 1)

    # Prepare HTML strings for distance and duration
    distance_txt = "<h4><b>Distance: " + str(distance_km) + " Km</b></h4>"
    duration_txt = "<h4><b>Duration: " + str(duration_min) + " Mins.</b></h4>"

    # Create a folium map
    m = folium.Map(location=[user_lat, user_lon], zoom_start=10, control_scale=True, tiles="cartodbpositron") 

    # Add decoded route to the map with distance and duration popup
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt + duration_txt, max_width=300)).add_to(m)

    # Add markers for start and end points
    folium.Marker(
        location=list(coords[0][::-1]),
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=list(coords[1][::-1]),
        icon=folium.Icon(color="red"),
    )   .add_to(m)

   # Create a Shapely Polygon from the geofence coordinates
    geofence_polygon = Polygon(booth)

    # Add marker for the user's location
    folium.Marker(
    location=[user_lat, user_lon],
    popup='User Location',
    icon=folium.Icon(color='blue')
    ).add_to(m)

    # Highlight the geofence polygon on the map
    folium.Polygon(
    locations=booth,
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.3,
    popup='Geofence Area'
    ).add_to(m)

    # Check if the user's location is within the geofence
    user_point = Point(user_location)
    if geofence_polygon.contains(user_point):
        st.write("The user's location is within the geofence.")
    else:
        st.write("The user's location is outside the geofence.")
    folium.Marker(
        location=(user_lat, user_lon),
        popup="Car's Location",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    # Highlight the route geofence
    folium.Polygon(locations=booth, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)

    # Display the map
    folium_static(m)
