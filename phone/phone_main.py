import phonenumbers
import folium
from myphone import number
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode

# Parse the phone number
pepnumber = phonenumbers.parse(number)
location = geocoder.description_for_number(pepnumber, "en")
print(f"General location from phone number: {location}")

# Get the carrier name
service_pro = phonenumbers.parse(number)
carrier_info = carrier.name_for_number(service_pro, "en")
print(f"Carrier: {carrier_info}")

# OpenCage API key
key = '6c37910b9d7f4867ad59d6db6f3715bd'
geocoder = OpenCageGeocode(key)

# Query using additional details (location, country, etc.)
query = f"{location}, India"  # Adding country to improve accuracy
result = geocoder.geocode(query)
if result and len(result):
    lat = result[0]['geometry']['lat']
    lng = result[0]['geometry']['lng']
    print(f"Coordinates: Latitude: {lat}, Longitude: {lng}")

    # Create a map using Folium
    myMap = folium.Map(location=[lat, lng], zoom_start=15)  # Zoom closer for accuracy
    folium.Marker([lat, lng], popup=location).add_to(myMap)

    # Save the map to an HTML file
    myMap.save("mylocation.html")
else:
    print("Location could not be found.")
