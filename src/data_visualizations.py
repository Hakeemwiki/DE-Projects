# src/visualize_data.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_revenue_vs_budget(df):
    """Visualize Revenue vs. Budget Trends using a scatter plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df['budget_musd'], df['revenue_musd'], alpha=0.5)
    plt.title("Revenue vs. Budget Trends")
    plt.xlabel("Budget (Millions USD)")
    plt.ylabel("Revenue (Millions USD)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_roi_by_genre(df):
    """Visualize Mean ROI by Genre using a bar chart."""
    # Ensure genres is a string
    df['genres'] = df['genres'].astype(str)
    
    # Split genres (since they’re separated by '|') and explode into rows
    df_genres = df.assign(genres=df['genres'].str.split('|')).explode('genres')
    
    # Calculate mean ROI per genre
    roi_by_genre = df_genres.groupby('genres')['roi'].mean().sort_values(ascending=False)
    
    # Plotting
    plt.figure(figsize=(12, 6))
    roi_by_genre.plot(kind='bar', color='skyblue')
    plt.title("Mean ROI by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Mean ROI (Revenue / Budget)")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()
    plt.show()
    plt.close()

def plot_popularity_vs_rating(df):
    """Visualize Popularity vs. Rating using a scatter plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df['popularity'], df['vote_average'], alpha=0.5)
    plt.title("Popularity vs. Rating")
    plt.xlabel("Popularity")
    plt.ylabel("Rating (Vote Average)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    plt.close()

def plot_yearly_box_office(df):
    """Visualize Yearly Trends in Box Office Performance using a line plot."""
    # Extract year from release_date
    df['year'] = pd.to_datetime(df['release_date']).dt.year
    
    # Group by year and calculate total revenue
    yearly_revenue = df.groupby('year')['revenue_musd'].sum()
    
    plt.figure(figsize=(12, 6))
    yearly_revenue.plot(kind='line', marker='o')
    plt.title("Yearly Trends in Box Office Performance")
    plt.xlabel("Year")
    plt.ylabel("Total Revenue (Millions USD)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    plt.close()

def plot_franchise_vs_standalone(df):
    """Visualize Comparison of Franchise vs. Standalone Success using a bar plot."""
    # Separate franchise and standalone
    franchise = df[df['belongs_to_collection'].notna()]
    standalone = df[df['belongs_to_collection'].isna()]
    
    # Calculate metrics
    metrics = {
        'Mean Revenue': franchise['revenue_musd'].mean(),
        'Mean Budget': franchise['budget_musd'].mean(),
        'Mean Rating': franchise['vote_average'].mean()
    }
    standalone_metrics = {
        'Mean Revenue': standalone['revenue_musd'].mean(),
        'Mean Budget': standalone['budget_musd'].mean(),
        'Mean Rating': standalone['vote_average'].mean()
    }
    
    # Prepare data for plotting
    comparison_df = pd.DataFrame({
        'Franchise': metrics,
        'Standalone': standalone_metrics
    })
    
    # Plot
    plt.figure(figsize=(10, 6))
    comparison_df.plot(kind='bar')
    plt.title("Franchise vs. Standalone Success")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.xticks(rotation=0)
    plt.legend(title="Movie Type")
    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    # Load cleaned data
    cleaned_data_path = "/Users/hakeemwikireh/Desktop/tmdb_movie_analysis/data/processed/cleaned_movie_data.csv"
    data = pd.read_csv(cleaned_data_path)

    # Add KPI columns (needed for ROI)
    from analysis import add_kpi_columns
    data = add_kpi_columns(data)

    # Generate visualizations
    plot_revenue_vs_budget(data)
    plot_roi_by_genre(data)
    plot_popularity_vs_rating(data)
    plot_yearly_box_office(data)
    plot_franchise_vs_standalone(data)