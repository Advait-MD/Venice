import spacy
from geopy.geocoders import Nominatim

nlp = spacy.load("en_core_web_sm")  # Load English NLP model
text = "SEATTLE -- The Mariners are still awaiting MRI results on Victor Robles after he crashed into the net when making a remarkable catch on Sunday in San Francisco, but the spark-plug right fielder was."
doc = nlp(text)

# Extract locations
locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
print("Extracted Locations:", locations)

# Initialize geolocator
geolocator = Nominatim(user_agent="geo_finder")

# Fetch latitude and longitude for each location
for loc in locations:
    location = geolocator.geocode(loc)
    if location:
        print(f"Location: {loc}")
        print(f"Latitude: {location.latitude}")
        print(f"Longitude: {location.longitude}")
    else:
        print(f"Location: {loc} - Details not found")