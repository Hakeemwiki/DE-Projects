# TMDB Movie Data Analysis

This project provides a comprehensive analysis of movie data sourced from [The Movie Database (TMDB) API](https://www.themoviedb.org/documentation/api). It includes Python scripts and a Jupyter Notebook to fetch, clean, analyze, and visualize movie data, focusing on key performance indicators (KPIs), franchise vs. standalone comparisons, director performance, and more. The project is modular, well-documented, and designed for reproducibility and extensibility.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage](#usage)
  - [Running the Jupyter Notebook](#running-the-jupyter-notebook)
  - [Using the Python Module](#using-the-python-module)
- [Data Source](#data-source)
- [Key Components](#key-components)
  - [Data Fetching](#data-fetching)
  - [Data Cleaning](#data-cleaning)
  - [Analysis Functions](#analysis-functions)
  - [Visualizations](#visualizations)
- [Example Outputs](#example-outputs)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Project Overview
The TMDB Movie Data Analysis project is designed to:
- Fetch movie metadata (e.g., budget, revenue, genres, cast, crew) from the TMDB API for a predefined list of movie IDs.
- Clean and preprocess the data to ensure consistency and usability.
- Perform advanced analyses, including KPI rankings, franchise vs. standalone comparisons, and director performance evaluations.
- Generate insightful visualizations to explore trends such as revenue vs. budget, ROI by genre, and yearly box office performance.

The project is implemented in Python, leveraging libraries like `pandas`, `requests`, `matplotlib`, and `logging`. It is structured to be modular, with reusable functions in `tmdb_functions.py` and an interactive analysis workflow in `TMDB_analysis(Modular).ipynb`.

## Features
- **Data Fetching**: Retrieve movie details and credits from the TMDB API with retry logic for robust handling of network issues.
- **Data Cleaning**: Standardize and preprocess complex data (e.g., nested JSON, stringified lists) into a clean, analysis-ready DataFrame.
- **KPI Analysis**: Rank movies by metrics like revenue, ROI, or popularity, with optional filtering.
- **Advanced Search**: Filter movies by genres, cast, or directors, with customizable sorting.
- **Franchise vs. Standalone Analysis**: Compare financial and popularity metrics between franchise and standalone films.
- **Director Analysis**: Evaluate directors based on total movies directed, revenue, and average ratings.
- **Visualizations**: Generate plots for revenue vs. budget, ROI by genre, popularity vs. rating, yearly box office trends, and franchise vs. standalone comparisons.
- **Modular Design**: Reusable functions in a separate Python module for easy integration into other projects.
- **Logging**: Comprehensive logging for debugging and monitoring data fetching and saving processes.

## Repository Structure
```plaintext
TMDB-Movie-Analysis/
├── tmdb_functions.py         # Python module with data fetching, cleaning, and analysis functions
├── TMDB_analysis(Modular).ipynb  # Jupyter Notebook for interactive analysis and visualization
├── raw_movie_data_new.csv    # Raw data fetched from TMDB API (generated)
├── cleaned_movie_data.csv    # Cleaned and processed data (generated)
├── visualizations/           # Directory for saved visualization PNG files
│   ├── revenue_vs_budget.png
│   ├── roi_by_genre.png
│   ├── popularity_vs_rating.png
│   ├── yearly_box_office.png
│   └── franchise_vs_standalone.png
├── README.md                 # Project documentation (this file)
└── requirements.txt          # Python dependencies
```

## Installation

### Prerequisites
- **Python**: Version 3.8 or higher
- **TMDB API Key**: Obtain a free API key from [TMDB](https://www.themoviedb.org/documentation/api).
- **Git**: For cloning the repository.
- **Jupyter Notebook**: For running the interactive analysis.

Required Python libraries (listed in `requirements.txt`):
- `requests`
- `pandas`
- `matplotlib`
- `urllib3`

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/TMDB-Movie-Analysis.git
   cd TMDB-Movie-Analysis
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the TMDB API Key**:
   - Create an environment variable named `api_key` with your TMDB API key.
     - On Linux/Mac:
       ```bash
       export api_key='your-api-key-here'
       ```
     - On Windows (Command Prompt):
       ```bash
       set api_key=your-api-key-here
       ```
     - Alternatively, add the API key to a `.env` file (requires `python-dotenv`) or modify `tmdb_functions.py` to hardcode the key (not recommended).

5. **Verify Setup**:
   Ensure the TMDB API key is accessible by running:
   ```python
   from tmdb_functions import get_api_key
   print(get_api_key())
   ```

## Usage

### Running the Jupyter Notebook
1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
2. Open `TMDB_analysis(Modular).ipynb` in the browser.
3. Run the cells sequentially to:
   - Fetch raw movie data.
   - Clean and preprocess the data.
   - Perform analyses (e.g., KPI rankings, franchise comparisons).
   - Generate and save visualizations.

### Using the Python Module
The `tmdb_functions.py` module can be imported into other Python scripts or projects. Example usage:
```python
from tmdb_functions import fetch_movie_data, clean_df, kpi_ranking, plot_revenue_vs_budget

# Fetch data for specific movie IDs
movie_ids = [299534, 19995, 140607]  # Example IDs
raw_data = fetch_movie_data(movie_ids)

# Clean the data
cleaned_data = clean_df(raw_data)

# Rank top 5 movies by revenue
top_revenue = kpi_ranking(cleaned_data, metric='revenue_millions', n=5)
print(top_revenue[['title', 'revenue_millions']])

# Generate a revenue vs. budget plot
plot_revenue_vs_budget(cleaned_data)
```

## Data Source
The project uses the [TMDB API](https://www.themoviedb.org/documentation/api) to fetch movie metadata, including:
- Movie details (title, budget, revenue, genres, release date, etc.).
- Credits (cast and crew information).
The API requires an API key, which must be set as an environment variable (`api_key`).

## Key Components

### Data Fetching
- **Function**: `fetch_movie_data(ids)`
- **Description**: Retrieves movie details and credits for a list of TMDB movie IDs. Includes retry logic for handling API timeouts or errors.
- **Output**: A `pandas` DataFrame with raw JSON data.
- **Features**:
  - Handles HTTP errors (e.g., 429, 500) with retries.
  - Logs warnings for failed fetches.
  - Appends credits (cast and crew) to movie data.

### Data Cleaning
- **Function**: `clean_df(df)`
- **Description**: Processes raw TMDB data into a clean, analysis-ready DataFrame.
- **Features**:
  - Drops irrelevant columns (e.g., `adult`, `homepage`).
  - Processes nested JSON (genres, production companies, credits).
  - Converts data types (e.g., numeric, datetime).
  - Computes financial metrics (budget/revenue in millions, profit, ROI).
  - Standardizes genre and country values (e.g., sorts `US|UK` to `United States of America|United Kingdom`).
  - Extracts cast size, crew size, and director names from credits.

### Analysis Functions
- **KPI Ranking** (`kpi_ranking`): Ranks movies by any metric (e.g., revenue, ROI) with optional filtering.
- **Advanced Search** (`advanced_search`): Filters movies by genres, cast, or directors, with sorting options.
- **Franchise vs. Standalone** (`franchise_vs_standalone`): Compares mean revenue, ROI, budget, popularity, and ratings between franchise and standalone films.
- **Franchise Analysis** (`analyze_franchise`): Aggregates metrics (e.g., total movies, budget, revenue) by franchise.
- **Director Analysis** (`analyze_directors`): Evaluates directors by total movies directed, revenue, and ratings.

### Visualizations
- **Revenue vs. Budget** (`plot_revenue_vs_budget`): Scatter plot showing the relationship between budget and revenue.
- **ROI by Genre** (`plot_roi_by_genre`): Bar chart of mean ROI per genre.
- **Popularity vs. Rating** (`plot_popularity_vs_rating`): Scatter plot comparing popularity and vote average.
- **Yearly Box Office** (`plot_yearly_box_office`): Line plot of total revenue by release year.
- **Franchise vs. Standalone** (`plot_franchise_vs_standalone`): Bar plot comparing key metrics.

## Example Outputs
- **Cleaned Data Sample** (`cleaned_movie_data.csv`):
  ```csv
  id,title,tagline,release_date,genres,belongs_to_collection,...
  299534,Avengers: Endgame,Avenge the fallen.,2019-04-24,Action|Adventure|Science Fiction,The Avengers Collection,...
  19995,Avatar,Enter the world of Pandora.,2009-12-15,Action|Adventure|Fantasy|Science Fiction,Avatar Collection,...
  ```
- **Visualization**: `revenue_vs_budget.png` (scatter plot of budget vs. revenue).
- **Analysis Output**: Top 5 movies by ROI:
  ```plaintext
  title                      roi
  Jurassic World: Fallen Kingdom  6.948
  Beauty and the Beast       5.036
  Incredibles 2              4.133
  Avengers: Endgame          3.937
  Avatar                     3.708
  ```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the API.
- Python libraries: `pandas`, `requests`, `matplotlib`, `urllib3`.
- The open-source community for inspiration and resources.

## Contact
For questions or feedback, please contact:
- **Your Name**: [your.email@example.com](mailto:your.email@example.com)
- **GitHub**: [your-username](https://github.com/your-username)

---

This README follows best practices for open-source project documentation, providing clear instructions, comprehensive details, and a professional structure. Update the placeholders (e.g., `your-username`, `your.email@example.com`) with your actual details before uploading to GitHub.