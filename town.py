# geo_extractor.py

import spacy
from geopy.geocoders import Nominatim

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="geo_locator")

def extract_coordinates(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    coords = []
    for loc in locations:
        try:
            location = geolocator.geocode(loc)
            if location:
                coords.append({
                    "place": loc,
                    "lat": location.latitude,
                    "lon": location.longitude
                })
        except Exception as e:
            continue

    return coords
