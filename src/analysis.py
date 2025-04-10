# # src/analyze_data.py
# import pandas as pd

# def add_kpi_columns(df):
#     """Add KPI columns: profit and ROI."""
#     df['profit_musd'] = df['revenue_musd'] - df['budget_musd']
#     df['roi'] = df['revenue_musd'] / df['budget_musd']
#     return df

# def rank_movies(df, metric, top_n=10, ascending=False, filters=None):
#     """Rank movies based on a metric."""
#     if filters:
#         df = df.query(filters)
#     return df.sort_values(by=metric, ascending=ascending).head(top_n)

# def filter_movies_by_actor_genre(df, actor_name, genre_filters):
#     """Filter movies by actor and genres."""
#     return df[
#         df['genres'].str.contains(genre_filters[0], na=False) &
#         df['genres'].str.contains(genre_filters[1], na=False) &
#         df['cast'].str.contains(actor_name, na=False)
#     ].sort_values(by='vote_average', ascending=False)

# def filter_by_actor_director(df, actor, director):
#     """Filter movies by actor and director."""
#     return df[
#         df['cast'].str.contains(actor, na=False) &
#         df['director'].str.contains(director, na=False)
#     ].sort_values(by='runtime')

# def franchise_vs_standalone(df):
#     """Compare franchise vs standalone movies."""
#     franchise = df[df['belongs_to_collection'].notna()]
#     standalone = df[df['belongs_to_collection'].isna()]

#     summary_stats = {
#         'Group': ['Franchise', 'Standalone'],
#         'Mean Revenue': [
#             franchise['revenue_musd'].mean(),
#             standalone['revenue_musd'].mean()
#         ],
#         'Mean ROI': [
#             franchise['roi'].mean(),
#             standalone['roi'].mean()
#         ],
#         'Mean Budget': [
#             franchise['budget_musd'].mean(),
#             standalone['budget_musd'].mean()
#         ],
#         'Mean Popularity': [
#             franchise['popularity'].mean(),
#             standalone['popularity'].mean()
#         ],
#         'Mean Rating': [
#             franchise['vote_average'].mean(),
#             standalone['vote_average'].mean()
#         ]
#     }

#     return pd.DataFrame(summary_stats)

# def analyze_franchise(df, sort_by=None, ascending=False):
#     """Analyze franchise statistics."""
#     franchise = df[df['belongs_to_collection'].notna()]

#     franchise_stat = franchise.groupby('belongs_to_collection').agg({
#         'id': 'count',
#         'budget_musd': ['sum', 'mean'],
#         'revenue_musd': ['sum', 'mean'],
#         'vote_average': 'mean'
#     })

#     franchise_stat.columns = ['total_movies', 'total_budget_musd', 'budget_mean', 
#                               'total_revenue_musd', 'revenue_mean', 'mean_rating']
    
#     if sort_by:
#         franchise_stat = franchise_stat.sort_values(by=sort_by, ascending=ascending)
#     return franchise_stat

# def analyze_directors(df, sort_by=None, ascending=False):
#     """Analyze directors in franchises."""
#     franchise = df[df['belongs_to_collection'].notna()]

#     franchise_stat = franchise.groupby('director').agg({
#         'id': 'count',
#         'revenue_musd': 'sum',
#         'vote_average': 'mean'
#     })

#     franchise_stat.columns = ['total_movies_directed', 'total_revenue_musd', 'mean_rating']
    
#     if sort_by:
#         franchise_stat = franchise_stat.sort_values(by=sort_by, ascending=ascending)
#     return franchise_stat

# if __name__ == "__main__":
#     # Load cleaned data
#     cleaned_data_path = "/Users/hakeemwikireh/Desktop/tmdb_movie_analysis/data/processed/cleaned_movie_data.csv"
#     data = pd.read_csv(cleaned_data_path)

#     # Add KPI columns
#     data = add_kpi_columns(data)

#     # Example analysis
#     top_movies = rank_movies(data, 'revenue_musd')
#     print("Top 5 movies by revenue:")
#     print(top_movies[['title', 'revenue_musd']])