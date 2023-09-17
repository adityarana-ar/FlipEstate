import streamlit as st
import requests
import random
import pandas as pd
import locale  # Import the locale module
import re
from PIL import Image, ImageDraw
from io import BytesIO



# Streamlit app title and page layout
st.set_page_config(page_title="*FlipEstate*", layout="centered")
col5,col6,col7 = st.columns(3)
with col6:
    st.title("FlipEstate")

data = pd.read_csv('predicted_prices_final.csv')

# User input for address with autocomplete
randomIndex = random.randint(0, len(data))
random_address = data.at[randomIndex, 'address']

# Function to convert address to coordinates using the Google Geocoding API
def get_coordinates_from_address(address):
    # Google Maps Geocoding API Key (replace with your own key)
    geocoding_api_key = "AIzaSyDeUhGLYtdSyzjss6hPN-og9x04tL9mLVY"

    # Define the Geocoding API URL
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={geocoding_api_key}"

    # Send a GET request to the Geocoding API
    response = requests.get(geocoding_url)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None

# Function to display the Street View image
def display_street_view(lat, lon):
    # Google Maps API Key (replace with your own key)
    api_key = "AIzaSyDeUhGLYtdSyzjss6hPN-og9x04tL9mLVY"

    # Define the Street View API URL
    street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lon}&key={api_key}"

    # Send a GET request to the API
    response = requests.get(street_view_url)

    if response.status_code == 200:
        # Display the Street View image
        rounded_image_html = f"""
        <div style="border-radius: 15px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
            <img src="data:image/png;base64,{response.content}" alt="Google Street View" style="width: 100%; height: auto;">
        </div>
        """
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)
        # Display the rounded Street View image
        st.image(round_corners(image,50), use_column_width=True)
        
    else:
        st.error("Error fetching Street View image. Please check your address and API Key.")


# Function to round the corners of a PIL image
def round_corners(pil_image, corner_radius):
    circle = Image.new('L', (corner_radius * 2, corner_radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, corner_radius * 2, corner_radius * 2), fill=255)
    alpha = Image.new('L', pil_image.size, 255)
    w, h = pil_image.size
    alpha.paste(circle.crop((0, 0, corner_radius, corner_radius)), (0, 0))
    alpha.paste(circle.crop((0, corner_radius, corner_radius, corner_radius * 2)), (0, h - corner_radius))
    alpha.paste(circle.crop((corner_radius, 0, corner_radius * 2, corner_radius)), (w - corner_radius, 0))
    alpha.paste(circle.crop((corner_radius, corner_radius, corner_radius * 2, corner_radius * 2)), (w - corner_radius, h - corner_radius))
    pil_image.putalpha(alpha)
    return pil_image

def showProperty(index):
    
    random_address = data.at[randomIndex, 'address']
    # Convert the entered address to coordinates
    coordinates = get_coordinates_from_address(random_address)

    if coordinates:
        lat, lon = coordinates
        display_street_view(lat, lon)
        left_column, middle_column, right_column = st.columns(3)
        with middle_column:
            st.write("Predicted Price:", format_currency(data.at[randomIndex, "predicted_price"]))
            st.write("Bed:",data.at[randomIndex, "bedroom_number"])
        with left_column:
            st.write("Flip Potential:", format_currency(data.at[randomIndex, "predicted_price"] - data.at[randomIndex, "price"]))
            st.write("Bathrooms:",data.at[randomIndex, "bathroom_number"])
        with right_column:
            st.write("Current Price:", format_currency(data.at[randomIndex, "price"]))
            st.write("SQFT:",data.at[randomIndex, "living_space"])

    else:
        st.error("Invalid address or unable to retrieve coordinates.")


   # Function to format a number as a currency string
# Function to format a number as a currency string using regex
def format_currency(number):
    formatted = re.sub(r'(?<=\d)(?=(\d{3})+(?!\d))', ',', str(number))  # Add commas for thousands separators
    return f"${formatted}"  # Add the dollar sign

saved_properties = []
    

col1,col2 = st.columns(2)

# Display the Street View image when the user clicks a button
if col1.button("Save Property"):
    saved_properties.append(randomIndex)
    # User input for address with autocomplete
    randomIndex = random.randint(0, len(data))
    showProperty(randomIndex)
    
    
 # Display the Street View image when the user clicks a button
if col2.button("Show Property"):
    randomIndex = random.randint(0, len(data))
    showProperty(randomIndex)




# from streamlit_option_menu import option_menu

# with st.sidebar:
#     selected = option_menu("Main Menu", ["Home", 'Settings',"My Properties"], 
#         icons=['house', 'gear'], menu_icon="cast", default_index=1)
#     if selected == "My Properties":
#         if len(saved_properties) == 0:
#             st.error("You have no properties saved.")
#         else:
#             for i, property_index in enumerate(saved_properties):
#                 if st.button(f"Property {i + 1}", key=f"property_button_{i}"):
#                     showProperty(property_index)
        

#if button("Show My Properties", o):


