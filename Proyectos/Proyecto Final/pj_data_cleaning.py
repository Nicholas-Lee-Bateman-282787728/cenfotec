import pandas as pd
import sqlite3 as lite
import sys
import datetime

const_path = r'C:\git\cenfotec\Proyectos\Proyecto Final\IMDB Datasets'

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None  # default='warn'

print("Loading titles data")
start_time = datetime.datetime.now()

titles_raw = pd.read_csv(
    const_path+r"\title.basics.tsv.gz"
    , sep='\t'
    , dtype={'startYear': object}
    , compression='gzip'
)

finish_time = datetime.datetime.now()
total_time = finish_time - start_time
print("Titles data loaded. Duration: ", str(total_time))

print("Loading Person Data"+str(datetime.datetime.now()))
person_raw = pd.read_csv(
    const_path+r"\name.basics.tsv.gz"
    , sep='\t'
    , compression='gzip'
)
print("Person data loaded"+str(datetime.datetime.now()))

print("Loading Rating data"+str(datetime.datetime.now()))
rating_raw = pd.read_csv(
    const_path + r"\title.ratings.tsv.gz"
    , sep='\t'
    , compression='gzip'
)
print("Rating data loaded"+str(datetime.datetime.now()))

print("Loading Movie Crew data"+str(datetime.datetime.now()))
titles_crew_raw = pd.read_csv(
    const_path + r"\title.crew.tsv.gz"
    , sep='\t'
    , compression='gzip'
)
print("Movie Crew data loaded"+str(datetime.datetime.now()))

print("Loading Title Principals data"+str(datetime.datetime.now()))
titles_principals_raw = pd.read_csv(
    const_path + r"\title.principals.tsv.gz"
    , sep='\t'
    , compression='gzip'
)
print("Title Principals data loaded"+str(datetime.datetime.now()))

print("Cleaning movie data"+str(datetime.datetime.now()))
movie_titles = titles_raw[titles_raw['titleType'] == 'movie']
movie_titles_df = movie_titles[['tconst', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes']]
movie_titles_df = movie_titles_df.replace(r'\N', 'N/A')
movie_titles_df.columns = ['title_id', 'movie_name', 'is_adult', 'year', 'runtime']
movie_titles_df = movie_titles_df.set_index('title_id')
print("Movie data cleaned"+str(datetime.datetime.now()))

print("Cleaning movie genre data"+str(datetime.datetime.now()))
movie_genres = movie_titles[['tconst', 'genres']]
movie_genres.columns = ['title_id', 'genres']
movie_genres = movie_genres.replace(r'\N', 'N/A')
movie_genres["genres"] = movie_genres["genres"].str.split(",")
print("Genre data cleaned"+str(datetime.datetime.now()))

print("Cleaning rating data"+str(datetime.datetime.now()))
rating_df = rating_raw.replace(r'\N', 'N/A')
rating_df = pd.merge(rating_df, movie_titles, on='tconst', how='inner')
rating_df = rating_df[['tconst', 'averageRating', 'numVotes']]
rating_df.columns = ['title_id', 'average_rating', 'num_votes']
rating_df = rating_df.set_index('title_id')
print("Movie rating cleaned"+str(datetime.datetime.now()))

print("Cleaning rating data"+str(datetime.datetime.now()))
title_principals = pd.merge(titles_principals_raw, movie_titles, on='tconst', how='inner')
title_principals_df = title_principals[['tconst', 'nconst', 'category', 'job']]
title_principals_df = title_principals_df.replace(r'\N', 'N/A')
title_principals_df.columns = ['title_id', 'person_id', 'category', 'job']
title_principals_df = title_principals_df.set_index('title_id')
print("Movie rating cleaned"+str(datetime.datetime.now()))

print("Cleaning person data"+str(datetime.datetime.now()))
person_df = person_raw.replace(r'\N', 'N/A')
person_df = person_df[person_df['deathYear'] == 'N/A']
person_data_df = person_df[['nconst', 'primaryName', 'birthYear']]
person_data_df.columns = ['person_id', 'name', 'birth_year']
person_data_df = person_data_df.set_index('person_id')
print("Person data cleaned"+str(datetime.datetime.now()))

movie_crew_raw = pd.merge(titles_crew_raw, movie_titles, on='tconst', how='inner')

movie_directors = movie_crew_raw[['tconst', 'directors']]
movie_directors = movie_directors.replace(r'\N', 'N/A')
movie_directors.columns = ['title_id', 'directors']
movie_directors["directors"] = movie_directors["directors"].str.split(",")

movie_directors_df = movie_directors.directors.apply(pd.Series)\
    .merge(movie_directors, left_index=True, right_index=True)\
    .drop(["directors"], axis=1)\
    .melt(id_vars=['title_id'], value_name="directors")\
    .drop("variable", axis=1)\
    .dropna()\
    .set_index('title_id')

movie_writers = movie_crew_raw[['tconst', 'writers']]
movie_writers = movie_writers.replace(r'\N', 'N/A')
movie_writers.columns = ['title_id', 'writers']
movie_writers["writers"] = movie_writers["writers"].str.split(",")

movie_writers_df = movie_writers.writers.apply(pd.Series)\
    .merge(movie_writers, left_index=True, right_index=True)\
    .drop(["writers"], axis=1)\
    .melt(id_vars=['title_id'], value_name="writers")\
    .drop("variable", axis=1)\
    .dropna()\
    .set_index('title_id')

print("Pivoting movie genre data"+str(datetime.datetime.now()))
movie_genres_df = movie_genres.genres.apply(pd.Series)\
    .merge(movie_genres, left_index=True, right_index=True)\
    .drop(["genres"], axis=1)\
    .melt(id_vars=['title_id'], value_name="genres")\
    .drop("variable", axis=1)\
    .dropna()\
    .set_index('title_id')
print("Movie genre data pivoted"+str(datetime.datetime.now()))

con = lite.connect('imdb_movies.db')
cur = con.cursor()

print("Creating tables"+str(datetime.datetime.now()))
with con:
    cur.execute("DROP TABLE IF EXISTS movie_titles")
    movie_titles_df.to_sql('movie_titles', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
with con:
    cur.execute("DROP TABLE IF EXISTS movie_genres")
    movie_genres_df.to_sql('movie_genres', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
with con:
    cur.execute("DROP TABLE IF EXISTS person_data")
    person_data_df.to_sql('person_data', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
with con:
    cur.execute("DROP TABLE IF EXISTS movie_rating")
    rating_df.to_sql('movie_rating', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
with con:
    cur.execute("DROP TABLE IF EXISTS movie_directors")
    movie_directors_df.to_sql('movie_directors', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
    cur.execute("DROP TABLE IF EXISTS movie_writers")
    movie_writers_df.to_sql('movie_writers', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
with con:
    cur.execute("DROP TABLE IF EXISTS movie_principals")
    title_principals_df.to_sql('movie_principals', con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)

print("Tables created, closing connection"+str(datetime.datetime.now()))
cur.close()
con.close()



