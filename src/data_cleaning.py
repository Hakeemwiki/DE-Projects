# # import pandas as pd
# # import ast

# # data = pd.read_csv('data/raw/raw_movie_data.csv')

# # data.drop(columns=['adult', 'imdb_id', 'original_title', 'video', 'homepage'], inplace=True)

# # data.shape
# # print(f"Total number of rows: {data.shape[0]}. Total number of columns: {data.shape[1]}")

# # # columns = ['belongs_to_collection', 'genres', 'production_countries','production_companies', 'spoken_languages'] 
    
# # # def clean_data_point_list(col):
# # #     if isinstance(col, list):
# # #         names = []
# # #         for item in col:
# # #             names.append(item['name'])
# # #         return '|'.join(names)
    

# # # def clean_data_point_dict(data):
# # #     if pd.notna and isinstance(data, dict):
# # #         return data.get('name')
# # #     return None

# # def clean_data_point_list(col):
# #     try:
# #         if isinstance(col, str):
# #             col = ast.literal_eval(col)
# #         if isinstance(col, list):
# #             names = [item['name'] for item in col if isinstance(item, dict) and 'name' in item]
# #             return '|'.join(names)
# #     except:
# #         return None
# #     return None

# # def clean_data_point_dict(data):
# #     try:
# #         if isinstance(data, str):
# #             data = ast.literal_eval(data)
# #         return data.get('name') if isinstance(data, dict) else None
# #     except:
# #         return None



# # #List columns
# # data['genres'] = data['genres'].apply(clean_data_point_list)
# # data['production_countries'] = data['production_countries'].apply(clean_data_point_list)
# # data['production_companies'] = data['production_companies'].apply(clean_data_point_list)
# # data['spoken_languages'] = data['spoken_languages'].apply(clean_data_point_list)

# # #Dictionary columns
# # data['belongs_to_collection'] = data['belongs_to_collection'].apply(clean_data_point_dict)

# # print(data['belongs_to_collection'])

# import pandas as pd
# import numpy as np

# def extract_credits_info(df):
#     """Extract cast, crew, and director info from 'credits' column (nested JSON)."""
#     def get_director(crew_list):
#         if isinstance(crew_list, list):
#             for member in crew_list:
#                 if member.get('job') == 'Director':
#                     return member.get('name')
#         return np.nan

#     def get_cast_names(cast_list):
#         if isinstance(cast_list, list):
#             return '|'.join([member.get('name') for member in cast_list[:5]])
#         return np.nan

#     df['cast'] = df['credits'].apply(lambda x: get_cast_names(x['cast']) if isinstance(x, dict) else np.nan)
#     df['cast_size'] = df['credits'].apply(lambda x: len(x['cast']) if isinstance(x, dict) and 'cast' in x else 0)
#     df['crew_size'] = df['credits'].apply(lambda x: len(x['crew']) if isinstance(x, dict) and 'crew' in x else 0)
#     df['director'] = df['credits'].apply(lambda x: get_director(x['crew']) if isinstance(x, dict) else np.nan)
#     return df

# def clean_movie_data(df):
#     """Clean and preprocess the movie DataFrame."""
#     # Extract credits
#     df = extract_credits_info(df)

#     # Parse genres and belongs_to_collection
#     df['genres'] = df['genres'].apply(
#         lambda x: '|'.join([g['name'] for g in x]) if isinstance(x, list) else np.nan
#     )
#     df['belongs_to_collection'] = df['belongs_to_collection'].apply(
#         lambda x: x['name'] if isinstance(x, dict) else np.nan
#     )

#     # Convert budget and revenue to millions
#     df['budget_musd'] = df['budget'] / 1e6
#     df['revenue_musd'] = df['revenue'] / 1e6

#     # Drop unnecessary columns
#     columns_to_drop = ['adult', 'backdrop_path', 'homepage', 'imdb_id', 'original_title', 
#                        'video', 'credits', 'budget', 'revenue']
#     df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

#     # Replace 0s with NaN and handle missing data
#     for col in ['budget_musd', 'revenue_musd']:
#         df[col] = df[col].replace(0, np.nan)
#     df = df.dropna(thresh=10).drop_duplicates(subset=['id', 'title'])

#     return df

# data = pd.read_csv("/Users/hakeemwikireh/Desktop/tmdb_movie_analysis/notebooks/raw_movie_data.csv")
# cleaned_data = clean_movie_data(data)
# cleaned_data.to_csv("/Users/hakeemwikireh/Desktop/tmdb_movie_analysis/data/processed/cleaned_movie_data.csv", index=False)
# print("Cleaned data saved to '../data/cleaned_movie_data.csv'")
