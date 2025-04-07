import pandas as pd
import ast

data = pd.read_csv('data/raw/raw_movie_data.csv')

data.drop(columns=['adult', 'imdb_id', 'original_title', 'video', 'homepage'], inplace=True)

data.shape
print(f"Total number of rows: {data.shape[0]}. Total number of columns: {data.shape[1]}")

# columns = ['belongs_to_collection', 'genres', 'production_countries','production_companies', 'spoken_languages'] 
    
# def clean_data_point_list(col):
#     if isinstance(col, list):
#         names = []
#         for item in col:
#             names.append(item['name'])
#         return '|'.join(names)
    

# def clean_data_point_dict(data):
#     if pd.notna and isinstance(data, dict):
#         return data.get('name')
#     return None

def clean_data_point_list(col):
    try:
        if isinstance(col, str):
            col = ast.literal_eval(col)
        if isinstance(col, list):
            names = [item['name'] for item in col if isinstance(item, dict) and 'name' in item]
            return '|'.join(names)
    except:
        return None
    return None

def clean_data_point_dict(data):
    try:
        if isinstance(data, str):
            data = ast.literal_eval(data)
        return data.get('name') if isinstance(data, dict) else None
    except:
        return None



#List columns
data['genres'] = data['genres'].apply(clean_data_point_list)
data['production_countries'] = data['production_countries'].apply(clean_data_point_list)
data['production_companies'] = data['production_companies'].apply(clean_data_point_list)
data['spoken_languages'] = data['spoken_languages'].apply(clean_data_point_list)

#Dictionary columns
data['belongs_to_collection'] = data['belongs_to_collection'].apply(clean_data_point_dict)

print(data['belongs_to_collection'])