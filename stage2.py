import requests
import spacy
from geopy.geocoders import Nominatim
import time

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize geocoder
geolocator = Nominatim(user_agent="news_location_extractor")

# Your NewsAPI key
API_KEY = '123apispce'

# Function to extract coordinates
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
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
                # To avoid hitting rate limits
                time.sleep(1)
        except Exception as e:
            print(f"Error geocoding {loc}: {e}")
            continue

    return coords

# Fetch news from NewsAPI
def fetch_news():
    url = f"https://content.guardianapis.com/search?section=football&api-key={API_KEY}"
    
    response = requests.get(url)
    print("Response Status Code:", response.status_code)  # Debugging: Print status code

    if response.status_code != 200:
        print("Error: Failed to fetch news. Check API key or endpoint.")
        return

    data = response.json()

    # Check if the response contains the expected data
    if "response" not in data or data["response"].get("status") != "ok":
        print("Unexpected response format:", data)
        return

    articles = data["response"].get("results", [])
    for article in articles[:5]:
        webTitle = article.get("webTitle", "No Title")
        webUrl = article.get("webUrl", "#")

        print("\n📰 Title:", webTitle)
        print("🔗 URL:", webUrl)

    if webTitle:
            coordinates = extract_coordinates(webTitle)
            if coordinates:
                print("📍 Locations:")
                for loc in coordinates:
                    print(f"   - {loc['place']}: Lat = {loc['latitude']}, Lon = {loc['longitude']}")
            else:
                print("📍 No recognizable locations found.")
        


# Run the function
if __name__ == "__main__":
    
    fetch_news()
