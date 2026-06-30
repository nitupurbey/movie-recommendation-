# Movie Recommendation System

A movie recommendation web application built using **Streamlit**, **FastAPI**, **TMDB API**, and **TF-IDF Content-Based Filtering**. The application allows users to search for movies, view detailed information, and receive recommendations based on movie content similarity and genres.

---

# Features

* Search movies using the TMDB API
* View detailed movie information
* Display movie posters and backdrops
* Get content-based recommendations using TF-IDF
* Get genre-based recommendations using the TMDB Discover API
* Browse Trending, Popular, Top Rated, Upcoming, and Now Playing movies
* Clean and responsive Streamlit interface

---

# Tech Stack

## Frontend

* Streamlit
* HTML/CSS

## Backend

* FastAPI
* Python

## Machine Learning

* TF-IDF Vectorizer
* Cosine Similarity
* Scikit-learn

## Dataset

* TMDB Movies Dataset
* Pickle files (`df.pkl`, `tfidf.pkl`, `tfidf_matrix.pkl`, `indices.pkl`)

## External API

* TMDB (The Movie Database) API

---

# Project Structure

```text
Movie-Recommender/
│
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── df.pkl
├── tfidf.pkl
├── tfidf_matrix.pkl
├── indices.pkl
├── requirements.txt
├── .env
└── README.md
```

---

# How It Works

## Movie Search

Users enter a movie title in the search box. The application searches the movie using the TMDB API and displays matching results with posters.

## Movie Details

After selecting a movie, the application displays:

* Movie title
* Poster
* Backdrop image
* Release date
* Genres
* Overview

## Content-Based Recommendation

The recommendation system uses a TF-IDF model built on the movie dataset.

The workflow is:

1. Find the selected movie in the local dataset.
2. Convert movie descriptions into TF-IDF vectors.
3. Compute cosine similarity with other movies.
4. Rank movies based on similarity scores.
5. Fetch posters and additional information from TMDB.

## Genre Recommendation

The application uses the selected movie's primary genre to request similar movies from the TMDB Discover API and displays additional recommendations.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommender.git

cd movie-recommender
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file in the project root.

```env
TMDB_API_KEY=YOUR_TMDB_API_KEY
```

You can obtain an API key from https://developer.themoviedb.org/

---

# Running the Project

## Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

## Start the Streamlit Frontend

```bash
streamlit run app.py
```

---



# Recommendation Algorithm

The project uses a **Content-Based Filtering** approach.

The recommendation process consists of:

* Text preprocessing
* TF-IDF vectorization
* Cosine similarity calculation
* Ranking similar movies
* Fetching movie posters and metadata from TMDB

---

# Libraries Used

* Streamlit
* FastAPI
* Pandas
* NumPy
* Scikit-learn
* Python-dotenv
* Pickle

---


# Acknowledgements

This project uses data and images provided by **The Movie Database (TMDB)** through its official API. The recommendation engine is implemented using **Scikit-learn**, while **FastAPI** powers the backend services and **Streamlit** provides the user interface.

---


