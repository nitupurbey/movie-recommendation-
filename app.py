
import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =============================
# STYLES
# =============================
st.markdown(
    """
<style>

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.small-muted {
    color:#9ca3af;
    font-size:0.92rem;
}

.movie-title {
    font-size:0.92rem;
    line-height:1.2rem;
    height:2.5rem;
    overflow:hidden;
    font-weight:600;
}

.card {
    border-radius:18px;
    padding:14px;
    background:#161b22;
    border:1px solid rgba(255,255,255,0.06);
}

.stApp {
    background-color:#0E1117;
    color:white;
}

</style>
""",
    unsafe_allow_html=True,
)

# =============================
# SESSION STATE
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

# =============================
# ROUTING
# =============================
def goto_home():
    st.session_state.view = "home"
    st.rerun()

def goto_details(tmdb_id):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = tmdb_id
    st.rerun()

# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get(path, params=None):

    try:
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=30
        )

        if response.status_code >= 400:
            return None

        return response.json()

    except:
        return None

# =============================
# IMAGE GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):

    if not cards:
        st.info("No movies found.")
        return

    rows = (len(cards) + cols - 1) // cols

    idx = 0

    for r in range(rows):

        colset = st.columns(cols)

        for c in range(cols):

            if idx >= len(cards):
                break

            movie = cards[idx]
            idx += 1

            tmdb_id = movie.get("tmdb_id")
            title = movie.get("title", "Untitled")
            poster = movie.get("poster_url")

            with colset[c]:

                st.markdown("<div class='card'>", unsafe_allow_html=True)

                if poster:
                    st.image(
                        poster,
                        width="stretch"
                    )
                else:
                    st.write("🖼️ No Poster")

                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True
                )

                st.write("")

                if st.button(
                    "View Details",
                    key=f"{key_prefix}_{tmdb_id}_{idx}"
                ):
                    goto_details(tmdb_id)

                st.markdown("</div>", unsafe_allow_html=True)

# =============================
# TFIDF TO CARD
# =============================
def tfidf_to_cards(items):

    cards = []

    for item in items:

        tmdb = item.get("tmdb")

        if tmdb:

            cards.append({
                "tmdb_id": tmdb.get("tmdb_id"),
                "title": tmdb.get("title"),
                "poster_url": tmdb.get("poster_url")
            })

    return cards

# =============================
# SIDEBAR
# =============================
with st.sidebar:

    st.title("🎬 Menu")

    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")

    home_category = st.selectbox(
        "Home Feed",
        [
            "trending",
            "popular",
            "top_rated",
            "now_playing",
            "upcoming"
        ]
    )

    grid_cols = st.slider(
        "Grid Columns",
        4,
        8,
        6
    )

# =============================
# HEADER
# =============================
st.title("🎥 Movie Recommendation System")

st.markdown(
    """
<div class='small-muted'>
Search movies • View details • Get recommendations from TF-IDF model
</div>
""",
    unsafe_allow_html=True
)

st.divider()

# =================================================
# HOME PAGE
# =================================================
if st.session_state.view == "home":

    # =============================
    # SEARCH
    # =============================
    query = st.text_input(
        "Search Movie",
        placeholder="Search movies like Avengers, Batman..."
    )

    if query.strip():

        search_data = api_get(
            "/tmdb/search",
            params={"query": query}
        )

        if search_data and "results" in search_data:

            results = search_data["results"]

            cards = []

            for movie in results[:24]:

                poster_path = movie.get("poster_path")

                cards.append({
                    "tmdb_id": movie.get("id"),
                    "title": movie.get("title"),
                    "poster_url": (
                        f"{TMDB_IMG}{poster_path}"
                        if poster_path else None
                    )
                })

            st.markdown("## 🔍 Search Results")

            poster_grid(
                cards,
                cols=grid_cols,
                key_prefix="search"
            )

        st.stop()

    # =============================
    # HOME FEED
    # =============================
    st.markdown(
        f"## 🔥 {home_category.replace('_', ' ').title()}"
    )

    movies = api_get(
        "/home",
        params={
            "category": home_category,
            "limit": 24
        }
    )

    if movies:
        poster_grid(
            movies,
            cols=grid_cols,
            key_prefix="home"
        )

# =================================================
# DETAILS PAGE
# =================================================
elif st.session_state.view == "details":

    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:

        st.warning("No movie selected.")

        if st.button("Back"):
            goto_home()

        st.stop()

    details = api_get(f"/movie/id/{tmdb_id}")

    if not details:

        st.error("Could not load movie details.")
        st.stop()

    # =============================
    # BACK BUTTON
    # =============================
    if st.button("⬅ Back To Home"):
        goto_home()

    # =============================
    # DETAILS LAYOUT
    # =============================
    left, right = st.columns([1, 2])

    with left:

        if details.get("poster_url"):

            st.image(
                details["poster_url"],
                width="stretch"
            )

    with right:

        st.title(details.get("title", ""))

        st.markdown(
            f"📅 Release Date: {details.get('release_date', '-')}"
        )

        genres = details.get("genres", [])

        if genres:

            genre_names = [
                g["name"] for g in genres
            ]

            st.markdown(
                "🎭 Genres: " + ", ".join(genre_names)
            )

        st.markdown("---")

        st.subheader("Overview")

        st.write(
            details.get(
                "overview",
                "No overview available."
            )
        )

    # =============================
    # BACKDROP
    # =============================
    if details.get("backdrop_url"):

        st.markdown("## 🎞 Backdrop")

        st.image(
            details["backdrop_url"],
            width="stretch"
        )

    st.divider()

    # =============================
    # RECOMMENDATIONS
    # =============================
    st.markdown("## 🍿 Recommended Movies")

    movie_title = details.get("title")

    bundle = api_get(
        "/movie/search",
        params={
            "query": movie_title,
            "tfidf_top_n": 12,
            "genre_limit": 12
        }
    )

    if bundle:

        # TFIDF
        st.markdown("### 🔎 Similar Movies")

        tfidf_cards = tfidf_to_cards(
            bundle.get(
                "tfidf_recommendations",
                []
            )
        )

        poster_grid(
            tfidf_cards,
            cols=grid_cols,
            key_prefix="tfidf"
        )

        st.divider()

        # Genre
        st.markdown("### 🎭 Genre Recommendations")

        genre_cards = bundle.get(
            "genre_recommendations",
            []
        )

        poster_grid(
            genre_cards,
            cols=grid_cols,
            key_prefix="genre"
        )

    else:

        st.warning(
            "Recommendations unavailable."
        )

