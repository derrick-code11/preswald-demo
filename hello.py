from preswald import connect, get_df, text, table, slider, selectbox, plotly, image, matplotlib
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Initialize connection and load the Books dataset
connect()
df = get_df("books")

# Data cleaning
df["pages"] = (
    pd.to_numeric(df["pages"], errors="coerce")
      .fillna(0)
      .astype(int)
)
# Extract a clean integer year from published_date
df["year"] = (
    pd.to_datetime(df["published_date"], errors="coerce")
      .dt.year
      .fillna(0)
      .astype(int)
)

# Dashboard title & overview
text("# 📚 Literary Compass 🧭")
text("""
Welcome! This interactive dashboard shows key insights from the Books dataset sourced from Kaggle through the Google books API.
Use the controls below to filter by page-count and language, then explore trends
in publication year, genre breakdowns, language distributions, and ratings over time.
""")

# High-level summary
text(f"""
**Dataset summary**  
- **Total books:** {len(df)}  
- **Genres covered:** {df['genre'].nunique()}  
- **Languages represented:** {df['language'].dropna().nunique()}  
- **Publication span:** up to {df['year'].max()}
""")
text("")

# Filters
text("## 🔧 Filters")
min_pages = slider(
    label="Minimum Pages",
    min_val=0,
    max_val=int(df["pages"].max()),
    default=100,
    size=0.7
)
lang = selectbox(
    label="Language",
    options=["All"] + sorted(df["language"].dropna().unique().tolist()),
    default="All",
    size=0.3
)
text("")

# Filtered Data Table
text("## 🗂️ Filtered Books Table")
text("Below is your current selection of books matching the filters.")
filtered = df[df["pages"] >= min_pages]
if lang != "All":
    filtered = filtered[filtered["language"] == lang]
table(filtered, title="Filtered Books")
text("")

# Scatter: Year vs. Pages
text("## 📈 Publication Year vs. Page Count")
text("This scatter plot shows how book lengths have trended over time.")
fig = px.scatter(
    filtered,
    x="year",
    y="pages",
    color="language",
    hover_data=["title", "author"]
)
plotly(fig)
text("")

# Bar: Books per Genre
text("## 🏷️ Books per Genre")
text("See which genres dominate in your selection.")
genre_counts = (
    filtered["genre"]
      .value_counts()
      .reset_index(name="count")
      .rename(columns={"index": "genre"})
)
fig_bar = px.bar(
    genre_counts,
    x="genre",
    y="count",
    labels={"genre":"Genre", "count":"Number of Books"}
)
plotly(fig_bar, size=0.5)
text("")

# Histogram: Page-count Distribution
text("## 📊 Distribution of Book Lengths")
text("A histogram of page counts helps identify whether most books are short, long, or in-between.")
fig_hist = px.histogram(
    filtered,
    x="pages",
    nbins=20
)
plotly(fig_hist, size=0.5)
text("")

# Bar: Language Distribution
text("## 🌐 Language Distribution")
text("How many books are available in each language?")
lang_counts = (
    filtered["language"]
      .value_counts()
      .reset_index(name="count")
      .rename(columns={"index": "language"})
)
fig_lang = px.bar(
    lang_counts,
    x="language",
    y="count",
    labels={"language":"Language", "count":"Number of Books"}
)
plotly(fig_lang, size=0.5)
text("")

# Cover Preview
text("## 🖼️ Book Cover Preview")
text("Select a book to view its cover image.")
if not filtered.empty:
    selected_title = selectbox(
        label="Select a Book",
        options=filtered["title"].tolist()
    )
    book = df[df["title"] == selected_title].iloc[0]
    image(book["thumbnail"], caption=selected_title)
