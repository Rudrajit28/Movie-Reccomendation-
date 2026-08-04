import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="CineBro — Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (premium dark cinema theme)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 0%, #1b1033 0%, #0b0b16 45%, #08080f 100%);
    color: #f1f1f6;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Hide default streamlit chrome for a cleaner premium feel */
#MainMenu, footer { visibility: hidden; }

/* ===== Header ===== */
.app-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    background: linear-gradient(90deg, #ff5f6d, #ffc371 45%, #7f5aff 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.1rem;
    letter-spacing: -0.5px;
}
.app-subtitle {
    color: #a3a3b8;
    font-size: 1rem;
    margin-bottom: 1.2rem;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14101f 0%, #0b0b16 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    color: #f1f1f6;
    font-weight: 600;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] .stButton button:hover {
    border-color: #7f5aff;
    background: rgba(127,90,255,0.15);
    transform: translateY(-1px);
}

/* ===== Inputs ===== */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #f1f1f6 !important;
}
.stTextInput input:focus {
    border-color: #7f5aff !important;
    box-shadow: 0 0 0 2px rgba(127,90,255,0.25) !important;
}

/* ===== Section headings ===== */
.section-heading {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    margin: 1.6rem 0 0.9rem 0;
    color: #f1f1f6;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-heading .bar {
    width: 5px;
    height: 22px;
    border-radius: 4px;
    background: linear-gradient(180deg, #ff5f6d, #7f5aff);
    display: inline-block;
}

/* ===== Movie Card ===== */
.movie-card-wrap {
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.07);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    padding-bottom: 8px;
    margin-bottom: 6px;
}
.movie-card-wrap:hover {
    transform: translateY(-6px) scale(1.015);
    box-shadow: 0 14px 30px rgba(127,90,255,0.25), 0 4px 10px rgba(0,0,0,0.4);
    border-color: rgba(127,90,255,0.5);
}
.poster-frame {
    position: relative;
    width: 100%;
    aspect-ratio: 2/3;
    overflow: hidden;
    background: #1a1a26;
}
.poster-frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
.no-poster {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #55556b;
    font-size: 2rem;
}
.movie-title {
    font-size: 0.88rem;
    font-weight: 600;
    line-height: 1.2rem;
    height: 2.4rem;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0.55rem 0.7rem 0 0.7rem;
    color: #f1f1f6;
}
.small-muted { color:#8b8ba3; font-size: 0.85rem; }

/* Buttons inside cards */
div[data-testid="column"] .stButton button {
    width: 100%;
    border-radius: 0 0 10px 10px;
    background: rgba(127,90,255,0.12);
    border: 1px solid rgba(127,90,255,0.3);
    color: #d9d1ff;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 0.3rem 0;
    margin-top: 6px;
    transition: all 0.2s ease;
}
div[data-testid="column"] .stButton button:hover {
    background: linear-gradient(90deg, #ff5f6d, #7f5aff);
    color: white;
    border-color: transparent;
}

/* ===== Details card ===== */
.card {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px;
    background: linear-gradient(145deg, rgba(255,255,255,0.045), rgba(255,255,255,0.01));
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(127,90,255,0.15);
    border: 1px solid rgba(127,90,255,0.35);
    color: #d9d1ff;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 2px 4px 2px 0;
}
.detail-label {
    color: #8b8ba3;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
    margin-top: 0.8rem;
}
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Divider spacing tighter */
[data-testid="stDivider"] { margin: 0.6rem 0; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                st.markdown("<div class='movie-card-wrap'>", unsafe_allow_html=True)

                if poster:
                    st.markdown(
                        f"<div class='poster-frame'><img src='{poster}' /></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div class='poster-frame'><div class='no-poster'>🎬</div></div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )

                if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (clean)
# =============================
with st.sidebar:
    st.markdown("## 🎬 CineBro")
    st.markdown("<div class='small-muted'>Your personal movie guide</div>", unsafe_allow_html=True)
    st.markdown("---")

    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### 🏠 Home Feed")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.markdown("<div class='app-title'>🎬 CineBro</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='app-subtitle'>Type a keyword → get instant suggestions & matches → open a movie → discover similar picks</div>",
    unsafe_allow_html=True,
)
st.divider()

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "🔍 Search by movie title",
        placeholder="Type: avenger, batman, love...",
        label_visibility="collapsed",
    )

    st.divider()

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown(
                    "<div class='section-heading'><span class='bar'></span>Results</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    st.markdown(
        f"<div class='section-heading'><span class='bar'></span>🏠 {home_category.replace('_',' ').title()}</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    a, b = st.columns([3, 1])
    with a:
        st.markdown(
            "<div class='section-heading'><span class='bar'></span>📄 Movie Details</div>",
            unsafe_allow_html=True,
        )
    with b:
        if st.button("← Back to Home"):
            goto_home()

    # Details (your FastAPI safe route)
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.4], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], width="stretch")
        else:
            st.write("🖼️ No poster")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"## {data.get('title','')}")
        release = data.get("release_date") or "-"
        genres = data.get("genres", [])

        st.markdown(f"<div class='detail-label'>Release date</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>{release}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='detail-label'>Genres</div>", unsafe_allow_html=True)
        if genres:
            badges = "".join([f"<span class='badge'>{g['name']}</span>" for g in genres])
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.markdown("<div class='small-muted'>-</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"<div class='detail-label'>Overview</div>", unsafe_allow_html=True)
        st.write(data.get("overview") or "No overview available.")
        st.markdown("</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown(
            "<div class='section-heading'><span class='bar'></span>Backdrop</div>",
            unsafe_allow_html=True,
        )
        st.image(data["backdrop_url"], width="stretch")

    st.divider()
    st.markdown(
        "<div class='section-heading'><span class='bar'></span>✅ Recommendations</div>",
        unsafe_allow_html=True,
    )

    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown(
                "<div class='section-heading'><span class='bar'></span>🔎 Similar Movies (TF-IDF)</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown(
                "<div class='section-heading'><span class='bar'></span>🎭 More Like This (Genre)</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")


#to run--- streamlit run app.py 
