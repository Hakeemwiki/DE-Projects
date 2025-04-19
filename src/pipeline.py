import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from tmdb_functions import (
    get_api_key,
    fetch_movie_data,
    save_df,
    load_df,
    clean_df,
    kpi_ranking,
    advanced_search,
    franchise_vs_standalone,
    analyze_franchise,
    analyze_directors,
    plot_revenue_vs_budget,
    plot_roi_by_genre,
    plot_popularity_vs_rating,
    plot_yearly_box_office,
    plot_franchise_vs_standalone
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MOVIE_IDS = [0, 299534, 19995, 140607, 299536, 597, 135397,
             420818, 24428, 168259, 99861, 284054, 12445,
             181808, 330457, 351286, 109445, 321612, 260513]
RAW_DATA_PATH = 'raw_movie_data.csv'
CLEANED_DATA_PATH = 'cleaned_movie_data.csv'

def exploratory_analysis(df):
    """
    Performs basic exploratory data analysis, printing summary statistics and missing values.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze
    """
    logging.info("Performing exploratory data analysis...")
    print("Summary Statistics:")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isnull().sum())

def main():
    """
    Main function to execute the movie data analysis pipeline.
    Steps: Fetch data, clean data, perform EDA, calculate KPIs, filter data,
           analyze franchises/directors, and generate visualizations.
    """
    logging.info("Starting movie data analysis pipeline...")
    
    try:
        # Step 1: Fetch movie data
        logging.info("Fetching movie data from TMDB API...")
        raw_data = fetch_movie_data(MOVIE_IDS)
        save_df(raw_data, RAW_DATA_PATH)
        
        # Step 2: Clean the data
        logging.info("Cleaning and preprocessing data...")
        cleaned_data = clean_df(raw_data)
        
        # Additional cleaning steps
        cleaned_data['overview'] = cleaned_data['overview'].replace('No Data', pd.NA)
        cleaned_data['tagline'] = cleaned_data['tagline'].replace('No Data', pd.NA)
        cleaned_data = cleaned_data.drop_duplicates().dropna(subset=['id', 'title'])
        cleaned_data = cleaned_data.dropna(thresh=10)
        if 'status' in cleaned_data:
            cleaned_data = cleaned_data[cleaned_data['status'] == 'Released']
            cleaned_data = cleaned_data.drop(columns=['status'])
        save_df(cleaned_data, CLEANED_DATA_PATH)
        
        # Step 3: Exploratory data analysis
        exploratory_analysis(cleaned_data)
        
        # Step 4: Calculate KPIs
        logging.info("Calculating KPIs...")
        print("\nTop 5 Movies by Revenue:")
        print(kpi_ranking(cleaned_data, 'revenue_millions', n=5)[['title', 'revenue_millions']])
        
        print("\nTop 5 Movies by Budget:")
        print(kpi_ranking(cleaned_data, 'budget_millions', n=5)[['title', 'budget_millions']])
        
        print("\nTop 5 Movies by Profit:")
        print(kpi_ranking(cleaned_data, 'profit', n=5)[['title', 'profit']])
        
        print("\nBottom 5 Movies by Profit:")
        print(kpi_ranking(cleaned_data, 'profit', n=5, top=False)[['title', 'profit']])
        
        print("\nTop 5 Movies by ROI (Budget >= 10M):")
        print(kpi_ranking(cleaned_data, 'roi', n=5, filter_col='budget_millions', filter_val=10)[['title', 'roi']])
        
        print("\nBottom 5 Movies by ROI (Budget >= 10M):")
        print(kpi_ranking(cleaned_data, 'roi', n=5, top=False, filter_col='budget_millions', filter_val=10)[['title', 'roi']])
        
        print("\nMost Voted Movies:")
        print(kpi_ranking(cleaned_data, 'vote_count', n=5)[['title', 'vote_count']])
        
        print("\nHighest Rated Movies (>= 10 votes):")
        print(kpi_ranking(cleaned_data, 'vote_average', n=5, filter_col='vote_count', filter_val=10)[['title', 'vote_average']])
        
        print("\nLowest Rated Movies (>= 10 votes):")
        print(kpi_ranking(cleaned_data, 'vote_average', n=5, top=False, filter_col='vote_count', filter_val=10)[['title', 'vote_average']])
        
        print("\nMost Popular Movies:")
        print(kpi_ranking(cleaned_data, 'popularity', n=5)[['title', 'popularity']])
        
        # Step 5: Advanced filtering
        logging.info("Performing advanced filtering...")
        sci_fi_action_willis = advanced_search(
            cleaned_data,
            genre_keywords='Science Fiction|Action',
            cast_keywords='Bruce Willis',
            sort_by='vote_average',
            ascending=False
        )
        print("\nScience Fiction Action Movies Starring Bruce Willis (Sorted by Rating):")
        print(sci_fi_action_willis[['title', 'genres', 'cast', 'vote_average']])
        
        thurman_tarantino = advanced_search(
            cleaned_data,
            cast_keywords='Uma Thurman',
            director_keywords='Quentin Tarantino',
            sort_by='runtime',
            ascending=True
        )
        print("\nMovies Starring Uma Thurman Directed by Quentin Tarantino (Sorted by Runtime):")
        print(thurman_tarantino[['title', 'cast', 'director', 'runtime']])
        
        # Step 6: Franchise vs. standalone analysis
        logging.info("Comparing franchise vs. standalone movies...")
        franchise_comparison = franchise_vs_standalone(cleaned_data)
        print("\nFranchise vs. Standalone Comparison:")
        print(franchise_comparison)
        
        # Step 7: Franchise analysis
        logging.info("Analyzing franchises...")
        franchise_stats = analyze_franchise(cleaned_data, sort_by='total_revenue_millions', ascending=False)
        print("\nMost Successful Franchises (Sorted by Total Revenue):")
        print(franchise_stats)
        
        # Step 8: Director analysis
        logging.info("Analyzing directors...")
        director_stats = analyze_directors(cleaned_data, sort_by='total_revenue_millions', ascending=False)
        print("\nMost Successful Directors (Sorted by Total Revenue):")
        print(director_stats)
        
        # Step 9: Generate visualizations
        logging.info("Generating visualizations...")
        plot_revenue_vs_budget(cleaned_data)
        plt.savefig('revenue_vs_budget.png')
        plt.close()
        
        plot_roi_by_genre(cleaned_data)
        plt.savefig('roi_by_genre.png')
        plt.close()
        
        plot_popularity_vs_rating(cleaned_data)
        plt.savefig('popularity_vs_rating.png')
        plt.close()
        
        plot_yearly_box_office(cleaned_data)
        plt.savefig('yearly_box_office.png')
        plt.close()
        
        plot_franchise_vs_standalone(cleaned_data)
        plt.savefig('franchise_vs_standalone.png')
        plt.close()
        
        print("\nVisualizations saved as PNG files:")
        print("- revenue_vs_budget.png")
        print("- roi_by_genre.png")
        print("- popularity_vs_rating.png")
        print("- yearly_box_office.png")
        print("- franchise_vs_standalone.png")
        
        logging.info("Movie data analysis pipeline completed successfully.")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()