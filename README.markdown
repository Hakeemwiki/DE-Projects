# TMDB Movie Data Analysis with PySpark

This project provides a robust analysis of movie data sourced from The Movie Database (TMDB) API, leveraging the power of Apache Spark through PySpark for distributed data processing. It includes a Python script to fetch, clean, analyze, and visualize movie data, focusing on key performance indicators (KPIs), advanced search queries, franchise vs. standalone comparisons, director performance, and insightful visualizations. The project is designed to be modular, well-documented, and optimized for scalability and reproducibility.

## Table of Contents

- Project Overview
- Features
- Repository Structure
- Thought Process
- Installation
  - Prerequisites
  - Setup Instructions
- Usage
  - Running the Script
- Data Source
- Key Components
  - Data Fetching
  - Data Cleaning
  - Analysis Functions
  - Visualizations
- Example Outputs
- Contributing
- Acknowledgements
- Contact

## Project Overview

The TMDB Movie Data Analysis with PySpark project aims to:

- Fetch movie metadata (e.g., budget, revenue, genres, cast, crew) from the TMDB API for a predefined list of movie IDs using HTTP requests with retry logic.
- Clean and preprocess the data using PySpark to handle large datasets efficiently, ensuring consistency and usability.
- Perform advanced analyses, including KPI rankings, advanced search queries, franchise vs. standalone comparisons, and director performance evaluations.
- Generate visualizations to explore trends such as revenue vs. budget, ROI by genre, yearly box office performance, and more, displaying them interactively.

The project is implemented in Python using PySpark for distributed data processing, alongside libraries like `requests`, `matplotlib`, and `pandas` for specific tasks. The script is structured to be modular, with reusable functions in `functions.py`, making it easy to extend or integrate into larger workflows.

## Features

- **Data Fetching**: Retrieve movie details and credits from the TMDB API with retry logic for robust network handling.
- **Distributed Data Processing**: Utilize PySpark to process and analyze movie data efficiently, suitable for large datasets.
- **Data Cleaning**: Standardize and preprocess complex data (e.g., nested JSON, arrays) into a clean, analysis-ready Spark DataFrame.
- **KPI Analysis**: Rank movies by metrics like revenue, ROI, or popularity, with optional filtering (e.g., minimum budget or vote count).
- **Advanced Search**: Filter movies by genres, cast, or directors, with customizable sorting (e.g., by rating or runtime).
- **Franchise vs. Standalone Analysis**: Compare financial and popularity metrics between franchise and standalone films.
- **Director Analysis**: Evaluate directors based on total movies directed, revenue, and average ratings within franchises.
- **Visualizations**: Generate plots for revenue vs. budget, ROI by genre, popularity vs. rating, yearly box office trends, and franchise vs. standalone comparisons, displayed interactively.
- **Modular Design**: Reusable functions in `functions.py` for easy integration into other projects.
- **Logging**: Comprehensive logging for debugging and monitoring data fetching and processing.

## Repository Structure

```plaintext
DE-PROJECTS/
├── data/                             # Directory for data files
│   └── cleaned_movie_data.csv        # Cleaned and processed data (generated)
├── notebooks/                        # Directory for Jupyter Notebooks (currently empty)
│   └── __pycache__/                  # Python cache directory (auto-generated)
├── src/                              # Directory for source code
│   ├── __pycache__/                  # Python cache directory (auto-generated)
│   └── functions.py                  # Main script with data fetching, cleaning, analysis, and visualization functions
├── .env                              # Environment file for storing API keys (not tracked in git)
├── .gitignore                        # Git ignore file for excluding unnecessary files
└── README.md                         # Project documentation (this file)
```

**Note**: The `functions.py` script displays visualizations interactively using `plt.show()`. If you prefer to save them as PNG files (e.g., `revenue_vs_budget.png`), you’ll need to update the visualization functions to include `plt.savefig()` calls before `plt.show()` or `plt.close()`.

## Thought Process

This project was developed as an assignment to analyze movie data, and my goal was to create a scalable, efficient solution using PySpark to handle potentially large datasets while maintaining a modular and reusable codebase. I chose PySpark because it allows for distributed data processing, which is ideal for handling large volumes of movie data that might come from the TMDB API in a real-world scenario. A critical step in this project was building a well-defined schema for the PySpark DataFrame, which I implemented in the `build_schema` function. This was essential because the TMDB API returns complex, nested JSON data with varying structures (e.g., arrays for genres, credits with cast and crew). Defining a schema ensured that the data was correctly typed and structured from the start, preventing issues like type mismatches (e.g., treating numbers as strings) and optimizing performance by avoiding schema inference at runtime. It also made the data more predictable for downstream analysis, such as filtering by genres or calculating financial metrics, which was a core requirement of the assignment. Beyond the schema, I structured the script into distinct sections—data fetching, cleaning, analysis, and visualization—to ensure clarity and maintainability. For example, I implemented retry logic in the data fetching phase to handle API rate limits and network issues, and I used PySpark’s powerful DataFrame API to clean and transform nested JSON data into a structured format. The analysis functions, like `kpi_ranking` and `advanced_search`, were designed to be flexible, allowing users to filter and sort data based on various criteria. Finally, I added visualizations to provide intuitive insights into the data, displaying them interactively to facilitate exploration during analysis. This approach balances performance, flexibility, and usability, making the project a strong foundation for deeper movie data analysis.

## Installation

### Prerequisites

- **Python**: Version 3.8 or higher.
- **Apache Spark**: Ensure Spark is installed and configured (PySpark requires a Spark installation).
- **TMDB API Key**: Obtain a free API key from TMDB.
- **Git**: For cloning the repository.

Required Python libraries (create a `requirements.txt` if not present):

- `pyspark`
- `requests`
- `pandas`
- `matplotlib`
- `urllib3`
- `python-dotenv`

### Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/DE-PROJECTS.git
   cd DE-PROJECTS
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   If a `requirements.txt` file exists:

   ```bash
   pip install -r requirements.txt
   ```

   If not, manually install the required libraries:

   ```bash
   pip install pyspark requests pandas matplotlib urllib3 python-dotenv
   ```

4. **Set Up Apache Spark**:

   - Download and install Apache Spark from [spark.apache.org](https://spark.apache.org/downloads.html).
   - Set the `SPARK_HOME` environment variable to the Spark installation directory.
   - Add Spark’s `bin` directory to your `PATH`.
   - Verify Spark installation:

     ```bash
     pyspark --version
     ```

5. **Set Up the TMDB API Key**:

   - Store your TMDB API key in the `.env` file:

     ```plaintext
     api_key=your-api-key-here
     ```

   - Alternatively, set it as an environment variable:
     - On Linux/Mac:

       ```bash
       export api_key='your-api-key-here'
       ```
     - On Windows (Command Prompt):

       ```bash
       set api_key=your-api-key-here
       ```

6. **Verify Setup**:

   Ensure the TMDB API key is accessible and Spark is configured by running a simple test:

   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(os.getenv('api_key'))  # Should print your API key
   from pyspark.sql import SparkSession
   spark = SparkSession.builder.appName("Test").getOrCreate()
   print(spark.version)  # Should print the Spark version
   spark.stop()
   ```

## Usage

### Running the Script

1. Navigate to the `src/` directory:

   ```bash
   cd src
   ```

2. Run the `functions.py` script:

   ```bash
   python functions.py
   ```

3. The script will:
   - Fetch movie data for the predefined list of movie IDs from the TMDB API.
   - Clean and preprocess the data using PySpark.
   - Perform analyses, including KPI rankings, search queries, franchise vs. standalone comparisons, and director performance.
   - Generate visualizations, which will be displayed interactively using `plt.show()`.

**Note**: The script uses a predefined list of movie IDs. To analyze different movies, modify the `movie_ids` list in the `if __name__ == "__main__":` block of `functions.py`. Visualizations are displayed interactively; to save them as files, add `plt.savefig()` calls in the visualization functions.

## Data Source

The project uses the TMDB API to fetch movie metadata, including:

- Movie details (title, budget, revenue, genres, release date, etc.).
- Credits (cast and crew information).

The API requires an API key, which must be set in the `.env` file or as an environment variable (`api_key`).

## Key Components

### Data Fetching

- **Function**: `fetch_movie_data(movie_ids, schema)`
- **Description**: Retrieves movie details and credits for a list of TMDB movie IDs using a configured HTTP session with retry logic.
- **Output**: A PySpark DataFrame with raw JSON data structured according to the defined schema.
- **Features**:
  - Handles HTTP errors (e.g., 429, 500) with retries.
  - Logs warnings for failed fetches.
  - Processes nested fields (e.g., genres, credits) into structured formats.

### Data Cleaning

- **Function**: `clean_movie_data(df)`
- **Description**: Processes raw TMDB data into a clean, analysis-ready PySpark DataFrame.
- **Features**:
  - Extracts collection names from `belongs_to_collection`.
  - Converts array fields (genres, production companies) into pipe-separated strings.
  - Processes credits to extract cast names, cast size, director names, and crew size.
  - Handles missing or invalid data (e.g., replaces 0 with NULL for budget, revenue, runtime).
  - Computes financial metrics (budget/revenue in millions, profit, ROI).
  - Standardizes genre and country values for consistency.

### Analysis Functions

- **KPI Ranking** (`kpi_ranking`): Ranks movies by any metric (e.g., revenue, ROI) with optional filtering.
- **Advanced Search** (`advanced_search`): Filters movies by genres, cast, or directors, with customizable sorting.
- **Franchise vs. Standalone** (`franchise_vs_standalone`): Compares mean revenue, ROI, budget, popularity, and ratings between franchise and standalone films.
- **Franchise Analysis** (`analyze_franchise`): Aggregates metrics (e.g., total movies, budget, revenue) by franchise.
- **Director Analysis** (`analyze_directors`): Evaluates directors of franchise movies by total movies directed, revenue, and ratings.

### Visualizations

- **Revenue vs. Budget** (`plot_revenue_vs_budget`): Scatter plot showing the relationship between budget and revenue.
- **ROI by Genre** (`plot_roi_by_genre`): Bar chart of mean ROI per genre.
- **Popularity vs. Rating** (`plot_popularity_vs_rating`): Scatter plot comparing popularity and vote average.
- **Yearly Box Office** (`plot_yearly_box_office`): Line plot of total revenue by release year.
- **Franchise vs. Standalone** (`plot_franchise_vs_standalone`): Bar plot comparing key metrics.

**Note**: Visualizations are displayed interactively using `plt.show()`. To save them as PNG files, update the visualization functions by adding `plt.savefig()` before `plt.show()` or `plt.close()`, as shown below:

```python
plt.savefig('revenue_vs_budget.png')
plt.show()
plt.close()
```

## Example Outputs

- **Analysis Output**: Top 5 movies by revenue (example):

  ```plaintext
  Top 5 Movies by Revenue:
  +--------------------+-----------------+----------------+
  |title               |revenue_millions |budget_millions |
  +--------------------+-----------------+----------------+
  |Avengers: Endgame   |2797.800564      |356.0          |
  |Avatar              |2787.965087      |237.0          |
  |Star Wars: The Force Awakens |2068.223624  |245.0          |
  |Avengers: Infinity War |2048.359754   |321.0          |
  |Titanic             |1845.034188      |200.0          |
  +--------------------+-----------------+----------------+
  ```

- **Visualization**: Visualizations like the revenue vs. budget scatter plot are displayed interactively. To save them, modify the visualization functions to include `plt.savefig()` calls.

- **Franchise vs. Standalone Comparison** (example):

  ```plaintext
  Franchise vs Standalone Comparison:
  +----------+-------------+---------+-------------+-----------------+------------+------------+
  |Group     |Mean_Revenue |Mean_ROI |Mean_Budget  |Mean_Popularity  |Mean_Rating |Movie_Count |
  +----------+-------------+---------+-------------+-----------------+------------+------------+
  |Franchise |1975.342234  |6.948    |285.714286   |135.123456       |7.5         |12          |
  |Standalone|845.123456   |3.456    |150.000000   |75.987654        |6.8         |6           |
  +----------+-------------+---------+-------------+-----------------+------------+------------+
  ```


## Contact

For questions or feedback, please contact:

- **Your Name**: hakeemwikireh@gmail.com
- **GitHub**: Hakeemwiki

---