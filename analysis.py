import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# Load the dataset
df = pd.read_csv("tmdb_movies_data.csv")

# Count complete and incomplete rows
complete_rows = df.dropna().shape[0]
incomplete_rows = df.shape[0] - complete_rows

# Null value summary
null_counts = df.isnull().sum()
null_summary = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": null_counts,
    "Missing %": (null_counts / len(df) * 100).round(2)
}).sort_values(by="Missing Values", ascending=False)

# Add profit column
df['profit'] = df['revenue'] - df['budget']

# Genre counts (Top 10)
genre_counts = df['genres'].value_counts().head(10)

# Top 5 profitable movies
top_profit = df[['original_title', 'budget', 'revenue', 'profit']].sort_values(by='profit', ascending=False).head(5)

# High-revenue movies with missing taglines
missing_taglines = df[df['tagline'].isnull() & (df['revenue'] > 1e8)][['original_title', 'revenue']]

# Zero budget and revenue counts
zero_budget = df[df['budget'] == 0].shape[0]
zero_revenue = df[df['revenue'] == 0].shape[0]

# Top 5 most profitable directors
top_directors = df.groupby('director')['profit'].sum().sort_values(ascending=False).head(5)

# Extract release year and get top 5 most productive years
df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
top_years = df['release_year'].value_counts().head(5)

# Correlation: runtime vs revenue
runtime_corr = df[['runtime', 'revenue']].corr()

# Correlation: popularity vs revenue
popularity_corr = df[['popularity', 'revenue']].corr()

# Split genres and count individual genres
genres_split = df['genres'].dropna().str.split('|')
flat_genres = [genre.strip() for sublist in genres_split for genre in sublist]
genre_counts_split = Counter(flat_genres)

# Word cloud of movie overviews
overview_text = " ".join(df['overview'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(overview_text)

# === VISUALIZATIONS ===
# Missing data heatmap
missing_data_fig = plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("Heatmap of Missing Data")
plt.tight_layout()
missing_data_fig.savefig("missing_data_heatmap.png")

# Genre bar chart
genre_fig = plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="crest")
plt.title("Top 10 Most Common Genre Combos")
plt.xlabel("Count")
plt.ylabel("Genres")
plt.tight_layout()
genre_fig.savefig("top_genres.png")

# Top profit movies chart
profit_fig = plt.figure(figsize=(10, 6))
sns.barplot(x='profit', y='original_title', data=top_profit, palette="rocket")
plt.title("Top 5 Most Profitable Movies")
plt.xlabel("Profit")
plt.ylabel("Movie Title")
plt.tight_layout()
profit_fig.savefig("top_profit_movies.png")

# Runtime vs revenue scatterplot
scatter_fig = plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='runtime', y='revenue')
plt.title("Runtime vs Revenue")
plt.xlabel("Runtime (minutes)")
plt.ylabel("Revenue")
plt.tight_layout()
scatter_fig.savefig("runtime_vs_revenue.png")

# Word cloud image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Common Words in Movie Overviews")
plt.tight_layout()
plt.savefig("overview_wordcloud.png")

# === WRITE TO TEXT FILE ===
with open("analysis_output.txt", "w", encoding="utf-8") as f:
    f.write(f"Total rows: {df.shape[0]}\n")
    f.write(f"Total columns: {df.shape[1]}\n")
    f.write(f"Complete rows: {complete_rows}\n")
    f.write(f"Incomplete rows: {incomplete_rows}\n\n")

    f.write("Top 10 Columns with Missing Values:\n")
    f.write(null_summary.head(10).to_string())
    f.write("\n\nTop 10 Most Common Genre Combos:\n")
    f.write(df['genres'].value_counts().head(10).to_string())
    f.write("\n\nAverage Budget and Revenue:\n")
    f.write(df[['budget', 'revenue']].mean().to_string())
    f.write("\n\nTop 5 Most Profitable Movies:\n")
    f.write(top_profit.to_string())
    f.write("\n\nHigh Revenue Movies Without Taglines:\n")
    f.write(missing_taglines.to_string())
    f.write(f"\n\nMovies with 0 budget: {zero_budget}")
    f.write(f"\nMovies with 0 revenue: {zero_revenue}")

    f.write("\n\nTop 5 Most Profitable Directors:\n")
    f.write(top_directors.to_string())

    f.write("\n\nTop 5 Most Productive Release Years:\n")
    f.write(top_years.to_string())

    f.write("\n\nCorrelation: Runtime vs Revenue:\n")
    f.write(runtime_corr.to_string())

    f.write("\n\nCorrelation: Popularity vs Revenue:\n")
    f.write(popularity_corr.to_string())

    f.write("\n\nMost Common Individual Genres (split):\n")
    for genre, count in genre_counts_split.most_common(10):
        f.write(f"{genre}: {count}\n")

# === Terminal Summary ===
print("\n===== Summary Statistics =====")
print(df[['budget', 'revenue', 'profit']].describe())

print("\n===== Median Values =====")
print("Median Budget:", df['budget'].median())
print("Median Revenue:", df['revenue'].median())
print("Median Profit:", df['profit'].median())

print("\n===== Top Insights =====")
print("Top 5 Most Profitable Directors:\n", top_directors)
print("\nTop 5 Most Productive Years:\n", top_years)
print("\nCorrelation Between Runtime and Revenue:\n", runtime_corr)
print("\nCorrelation Between Popularity and Revenue:\n", popularity_corr)

print("\nTop 10 Most Common Individual Genres:")
for genre, count in genre_counts_split.most_common(10):
    print(f"{genre}: {count}")

# === Show all plots ===
plt.show()
