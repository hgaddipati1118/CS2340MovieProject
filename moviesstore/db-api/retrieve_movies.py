import os
import sys
import django
import requests
from django.core.files.base import ContentFile
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moviesstore.settings")
django.setup()

from movies.models import Movie

API_KEY = os.getenv("API-KEY")
API_URL = "https://api.themoviedb.org/3/discover/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def rating_to_price(vote_average):
    if vote_average >= 8.0:
        return 19.99
    elif vote_average >= 6.0:
        return 14.99
    elif vote_average >= 4.0:
        return 9.99
    elif vote_average >= 2.0:
        return 4.99
    else:
        return 2.99

for page in range(1, 4):
    print(f"Fetching movies from page {page}...")
    
    params = {
        "api_key": API_KEY,
        "language": "en-US",  # Ensure this is set for English
        "sort_by": "popularity.desc",  # Keep the sorting for popularity
        "page": page,
        "include_adult": "false",  # Ensure adult content is excluded
        "region": "US",  # Restrict to US-based content
    }

    response = requests.get(API_URL, params=params)
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page}. Skipping...")
        continue
    
    movies = response.json().get("results", [])

    for movie in movies:
        name = movie["title"]
        description = movie["overview"]
        poster_path = movie.get("poster_path")
        rating = movie.get("vote_average", 0)
        price = rating_to_price(rating)

        if Movie.objects.filter(name=name).exists():
            print(f"Movie '{name}' already exists. Skipping.")
            continue

        image_file = None
        if poster_path:
            image_url = f"{IMAGE_BASE_URL}{poster_path}"
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                image_filename = f"{name.replace(' ', '_')}.jpg"
                image_file = ContentFile(image_response.content, name=image_filename)

        movie_entry = Movie(name=name, price=price, description=description)
        
        if image_file:
            movie_entry.image.save(image_filename, image_file, save=True)

        movie_entry.save()
        print(f"Added to database: {name}")

print("Database update complete!")
