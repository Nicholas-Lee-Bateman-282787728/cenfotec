import time
import sys
import pandas as pd
import sqlite3 as lite
import sys
#
# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 10)
# pd.set_option('display.width', 1000)
# pd.options.mode.chained_assignment = None  # default='warn'
#
const_path = r'C:\git\cenfotec\Proyectos\Proyecto Final\IMDB Datasets'
#
#
# titles_crew_raw = pd.read_csv(
#     const_path+r"\title.crew.tsv.gz"
#     , sep='\t'
#     , compression='gzip'
# )
#
# titles_raw = pd.read_csv(
#     const_path+r"\title.basics.tsv.gz"
#     , sep='\t'
#     , dtype={'startYear': object}
#     , compression='gzip'
# )
#
# movie_titles = titles_raw[titles_raw['titleType'] == 'movie']
#
# movie_crew_raw = pd.merge(titles_crew_raw, movie_titles, on='tconst', how='inner')
#
# movie_directors = movie_crew_raw[['tconst', 'directors']]
# movie_directors = movie_directors.replace(r'\N', 'N/A')
# movie_directors.columns = ['title_id', 'directors']
# movie_directors["directors"] = movie_directors["directors"].str.split(",")
#
# movie_directors_df = movie_directors.directors.apply(pd.Series)\
#     .merge(movie_directors, left_index=True, right_index=True)\
#     .drop(["directors"], axis=1)\
#     .melt(id_vars=['title_id'], value_name="directors")\
#     .drop("variable", axis=1)\
#     .dropna()\
#     .set_index('title_id')
#
# movie_writers = movie_crew_raw[['tconst', 'writers']]
# movie_writers = movie_writers.replace(r'\N', 'N/A')
# movie_writers.columns = ['title_id', 'writers']
# movie_writers["writers"] = movie_writers["writers"].str.split(",")
#
# movie_writers_df = movie_writers.writers.apply(pd.Series)\
#     .merge(movie_writers, left_index=True, right_index=True)\
#     .drop(["writers"], axis=1)\
#     .melt(id_vars=['title_id'], value_name="writers")\
#     .drop("variable", axis=1)\
#     .dropna()\
#     .set_index('title_id')
#
# print(movie_directors_df.head())
# print(movie_writers_df.head())

rating_raw = pd.read_csv(
    const_path + r"\title.ratings.tsv.gz"
    , sep='\t'
    , compression='gzip'
)

print(rating_raw.head())