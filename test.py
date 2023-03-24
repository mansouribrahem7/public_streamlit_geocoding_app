# Initialize Nominatim geocoder
import geopandas as gpd
import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="my_geocoder")

# Create a Streamlit app
st.title("Geocoding App")

# Ask user for input address
address = st.text_input("Enter an address to geocode:")

# Geocode the address
location = geolocator.geocode(address)
flag=True
# Display the results
if location:
    flag =False
    st.write("Latitude:", location.latitude)
    
    st.write("Longitude:", location.longitude)




    # create a Pandas DataFrame that contains the address I wish to geocode:
    home = gpd.GeoDataFrame([{'address': address}])
    home


    #supply the geocoder class object returns a GeoPandas GeoDataFrame with a geometry that represents the point for each address
    home = gpd.tools.geocode(home['address'], Nominatim, user_agent='Isochrone calculator')
    home

    # Create a folium map centered at the geocoded location
    map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

    length = st.text_input("Enter Distance of buffer:")
    st.write("The Defult value of Buffer 5Km")
    bu=st.button("make buffer")
    if bu:
        if not length:
            length =5000
        length= int(length)
        # we will create our bubble by projecting to the GDA2020 MGA Zone 55 projection (EPSG code 7855) to create the buffer before re-projecting back to the original GCS WGS84 projection
        buffer = home.to_crs(epsg=7855).buffer(length).to_crs(epsg=3857)

    # put buffer on map
        folium.GeoJson(buffer).add_to(map)

        geojson=buffer.to_json()
        file_name ="polygon buffer.geojson"
        st.download_button(label="Download Buffer GeoJSON",data=geojson,file_name=file_name,mime="application/json")


    # put geometry on the same map
    folium.GeoJson(home, tooltip=folium.GeoJsonTooltip(['address'])).add_to(map)

    # Add a marker and popup for the geocoded location
    folium.Marker([location.latitude, location.longitude],popup=address).add_to(map)   
    
    # Display the map
    folium_static(map)

else:
    if address :
        st.write("Location not found.")
    




