import pandas as pd
import pymongo
import sys

const_path = r'C:\git\cenfotec\Proyectos\Proyecto Final\IMDB Datasets'

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

print("Loading titles data")
titles_raw = pd.read_csv(
    const_path+r"\title.basics.tsv.gz"
    , sep='\t'
    , dtype={'startYear': object}
    , compression='gzip'
)
print("Titles data loaded")
print("Loading Person Data")
person_raw = pd.read_csv(
    const_path+r"\name.basics.tsv.gz"
    , sep='\t'
    , compression='gzip'
)
print("Person data loaded")

print("Cleaning movie data")
movie_titles = titles_raw[titles_raw['titleType'] == 'movie']
movie_titles_df = movie_titles[['tconst', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes']]
movie_titles_df = movie_titles_df.replace(r'\N', 'N/A')
movie_titles_df.columns = ['title_id', 'movie_name', 'is_adult', 'year', 'runtime']
movie_titles_df = movie_titles_df.set_index('title_id')
print("Movie data cleaned")

print("Cleaning movie genre data")
movie_genres = movie_titles[['tconst', 'genres']]
movie_genres.columns = ['title_id', 'genres']
movie_genres["genres"] = movie_genres["genres"].str.split(",")
print("Genre data cleaned")

print("Cleaning person data")
person_df = person_raw.replace(r'\N', 'N/A')
person_df = person_df[person_df['deathYear'] == 'N/A']
person_data_df = person_df[['nconst', 'primaryName', 'birthYear']]
person_data_df.columns = ['person_id', 'name', 'birth_year']
person_data_df.set_index('person_id')
print("Person data cleaned")

print("Cleaning person profession data")
person_profession = person_df[['nconst', 'primaryProfession']]
person_profession.columns = ['person_id', 'profession']
person_profession["profession"] = person_profession["profession"].str.split(",")
print("Person profession data cleaned")

print("Cleaning person known titles data")
person_known_titles = person_df[['nconst', 'knownForTitles']]
person_known_titles.columns = ['person_id', 'titles']
person_known_titles["titles"] = person_known_titles["titles"].str.split(",")
print("Person known titles cleaned")

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['project_movies']
movie_collection = db['movie_titles']

document = movie_collection.insert_one(movie_titles_df)




