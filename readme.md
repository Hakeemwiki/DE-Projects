# TMDB Movie Analysis

This project is a comprehensive analysis of movie data sourced from The Movie Database (TMDB). It explores various aspects of movie trends, including profitability, popularity, runtime, budget, and more. The goal is to derive actionable insights that can assist in understanding what makes a movie successful.

## Project Structure

- `TMDB_Movie_analysis.ipynb`: Jupyter Notebook containing the full data analysis workflow — from data cleaning to visualization and interpretation.
- The dataset used in this analysis is found in my data folder. Make sure this file is present in the working directory.
- `README.md`: Project documentation (you’re reading it!).

## Key Questions Addressed

- What is the most profitable movie in the dataset?
- Which movie genres are most common?
- Do movies with higher budgets tend to be more profitable?
- How does the runtime of a movie affect its popularity or profitability?
- Which actors and directors appear most frequently?

## Techniques Used

- Data Wrangling with Pandas
- Exploratory Data Analysis (EDA)
- Data Visualization using Matplotlib and Seaborn
- Statistical Aggregation and Grouping

## Data Cleaning

The dataset required several preprocessing steps, including:
- Removing duplicates
- Handling missing or zero values in budget and revenue
- Splitting multi-value columns like genres and cast
- Converting datatypes for easier analysis

## Highlights of the Analysis

- **Most Profitable Movie**: "Avatar"
- **Most Common Genre**: Drama
- **Top Actor**: Tom Cruise (based on frequency)
- **Top Director**: Steven Spielberg
- **Correlation**: A moderate correlation between budget and revenue, indicating some predictive power.

## Requirements

Install the required packages using:

```bash
pip install pandas matplotlib numpy
```

Make sure you have Jupyter Notebook or JupyterLab installed to run the `.ipynb` file.

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/TMDB_Movie_Analysis.git
   cd TMDB_Movie_Analysis
   ```

2. Launch the notebook:
   ```bash
   jupyter notebook TMDB_Movie_analysis.ipynb
   ```

3. Explore and run the cells to see the analysis and visualizations.

## Dataset Source

The dataset used in this project is from [TMDB API](https://api.themoviedb.org/3/movie/).



