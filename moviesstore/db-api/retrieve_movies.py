import requests
import os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# TMDb API Configuration
API_KEY = "61759505be57e7942838e2db9f22286b"
API_URL = "https://api.themoviedb.org/3/discover/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

FOLDER_NAME = "movie_posters"
os.makedirs(FOLDER_NAME, exist_ok=True)

def rating_to_price(vote_average):
    """
    Converts a TMDb movie rating (0-10 scale) into a price estimate.
    """
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

# Fetch movies
params = {
    "api_key": API_KEY,
    "language": "en-US",
    "sort_by": "popularity.desc",
    "page": 1
}
response = requests.get(API_URL, params=params)
movies = response.json().get("results", [])[:15]  # Get first 5 movies

# Process movies
for movie in movies:
    title = movie["title"]
    description = movie["overview"]
    poster_path = movie.get("poster_path")
    rating = movie.get("vote_average", 0)  # Default to 0 if missing
    price = rating_to_price(rating)

    print(f"{title}\n{price:.2f}\n{description}\n\n")

    # Download and save poster if available
    if poster_path:
        image_url = f"{IMAGE_BASE_URL}{poster_path}"
        image_data = requests.get(image_url).content
        file_path = os.path.join(FOLDER_NAME, f"{title.replace(' ', '_')}.jpg")

        with open(file_path, "wb") as f:
            f.write(image_data)

        print(f"Saved poster: {file_path}")

print("Download complete!")
