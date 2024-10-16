import streamlit as st
import requests
import pandas as pd

API_KEY = '4915f8e461a2b02451d25462e8dbc456'
BASE_URL = 'https://api.themoviedb.org/3'

# Function to get movie ID by title
def get_movie_id_by_title(movie_title):
    url = f'{BASE_URL}/search/movie?api_key={API_KEY}&query={movie_title}'
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            return results[0]['id'], results[0]['title']
        return None, None
    return None, None

# Function to get movie recommendations by movie ID
def get_movie_recommendations(movie_id, num_recommendations=5, min_rating=0, genre_preference=None):
    url = f'{BASE_URL}/movie/{movie_id}/recommendations?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['results']
        filtered_recommendations = [
            movie for movie in data
            if movie['vote_average'] >= min_rating
        ]
        return filtered_recommendations[:num_recommendations]
    return []

# Streamlit interface
st.title('Movie Recommendation System')

# Input fields
movie_title_input = st.text_input("Enter a movie title you enjoyed:")
genre_input = st.selectbox("Do you have a preferred genre?", ('Any', 'Action', 'Comedy', 'Drama', 'Horror', 'Romance'))
rating_input = st.slider("Minimum rating you'd like to see", 0.0, 10.0, 7.0)

if st.button("Get Recommendations"):
    if movie_title_input:
        movie_id, movie_title = get_movie_id_by_title(movie_title_input)
        if movie_id:
            st.write(f"Fetching recommendations for: {movie_title}")
            recommendations = get_movie_recommendations(movie_id, min_rating=rating_input)
            if recommendations:
                for rec in recommendations:
                    st.write(f"- {rec['title']} (Rating: {rec['vote_average']}, Release: {rec['release_date']})")
            else:
                st.write("No recommendations found based on your preferences.")
        else:
            st.write("Movie not found!")
