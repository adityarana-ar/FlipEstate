import streamlit as st
import requests

# Streamlit app title
st.title("Google Maps Street View Viewer")

# User input for address with autocomplete
address = st.text_input("Enter an Address:", key="address")

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
        st.image(response.content, use_column_width=True, caption="Google Street View")
    else:
        st.error("Error fetching Street View image. Please check your address and API Key.")

# Display the Street View image when the user clicks a button
if st.button("Show Street View"):
    # Convert the entered address to coordinates
    coordinates = get_coordinates_from_address(address)

    if coordinates:
        lat, lon = coordinates
        display_street_view(lat, lon)
    else:
        st.error("Invalid address or unable to retrieve coordinates.")


import random

# Define a dictionary of responses
responses = {
    "hello": ["Hi!", "Hello!", "Hey there!"],
    "how are you": ["I'm good, thanks!", "I'm just a chatbot.", "I'm functioning well."],
    "what's your name": ["I'm a chatbot.", "You can call me ChatGPT.", "I don't have a name."],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
}

# Function to get a response from the chatbot
def get_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "I'm not sure how to respond to that."

# Main chat loop
print("Chatbot: Hi there! How can I help you today? (Type 'bye' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'bye':
        print("Chatbot: Goodbye!")
        break
    response = get_response(user_input)
    print(f"Chatbot: {response}")
