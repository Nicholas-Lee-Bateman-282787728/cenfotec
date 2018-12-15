import time
import sys
import pandas as pd
import sqlite3 as lite
import sys

const_path = r'C:\git\cenfotec\Proyectos\Proyecto Final\IMDB Datasets'

toolbar_width = 40

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

for i in range(toolbar_width):
    time.sleep(0.1) # do real work here

    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)

    titles_raw = pd.read_csv(
        const_path + r"\title.basics.tsv.gz"
        , sep='\t'
        , dtype={'startYear': object}
        , compression='gzip'
    )
    person_raw = pd.read_csv(
        const_path + r"\name.basics.tsv.gz"
        , sep='\t'
        , compression='gzip'
    )
    person_raw = pd.read_csv(
        const_path + r"\name.basics.tsv.gz"
        , sep='\t'
        , compression='gzip'
    )

    movie_titles = titles_raw[titles_raw['titleType'] == 'movie']
    movie_titles_df = movie_titles[['tconst', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes']]
    movie_titles_df = movie_titles_df.replace(r'\N', 'N/A')
    movie_titles_df.columns = ['title_id', 'movie_name', 'is_adult', 'year', 'runtime']
    movie_titles_df = movie_titles_df.set_index('title_id')

    movie_genres = movie_titles[['tconst', 'genres']]
    movie_genres.columns = ['title_id', 'genres']
    movie_genres["genres"] = movie_genres["genres"].str.split(",")

    person_df = person_raw.replace(r'\N', 'N/A')
    person_df = person_df[person_df['deathYear'] == 'N/A']

    person_data_df = person_df[['nconst', 'primaryName', 'birthYear']]
    person_data_df.columns = ['person_id', 'name', 'birth_year']
    person_data_df.set_index('person_id')

    person_profession = person_df[['nconst', 'primaryProfession']]
    person_profession.columns = ['person_id', 'profession']
    person_profession["profession"] = person_profession["profession"].str.split(",")

    person_known_titles = person_df[['nconst', 'knownForTitles']]
    person_known_titles.columns = ['person_id', 'titles']
    person_known_titles["titles"] = person_known_titles["titles"].str.split(",")

    movie_genres_df = movie_genres.genres.apply(pd.Series) \
        .merge(movie_genres, left_index=True, right_index=True) \
        .drop(["genres"], axis=1) \
        .melt(id_vars=['title_id'], value_name="genres") \
        .drop("variable", axis=1) \
        .dropna() \
        .set_index('title_id')
    person_profession_df = person_profession.profession.apply(pd.Series) \
        .merge(person_profession, left_index=True, right_index=True) \
        .drop(["profession"], axis=1) \
        .melt(id_vars=['person_id'], value_name="profession") \
        .drop("variable", axis=1) \
        .dropna() \
        .set_index('person_id')
    person_known_titles_df = person_known_titles.titles.apply(pd.Series) \
        .merge(person_profession, left_index=True, right_index=True) \
        .drop(["titles"], axis=1) \
        .melt(id_vars=['person_id'], value_name="titles") \
        .drop("variable", axis=1) \
        .dropna() \
        .set_index('person_id')

    con = lite.connect('imdb_movies.db')
    cur = con.cursor()

    with con:
        cur.execute("DROP TABLE IF EXISTS movie_titles")
        movie_titles_df.to_sql('movie_titles', con, schema=None, if_exists='fail', index=True, index_label=None,
                               chunksize=None, dtype=None)
        cur.execute("DROP TABLE IF EXISTS movie_genres")
        movie_genres_df.to_sql('movie_genres', con, schema=None, if_exists='fail', index=True, index_label=None,
                               chunksize=None, dtype=None)
        cur.execute("DROP TABLE IF EXISTS person_data")
        person_data_df.to_sql('person_data', con, schema=None, if_exists='fail', index=True, index_label=None,
                              chunksize=None, dtype=None)
        cur.execute("DROP TABLE IF EXISTS person_profession")
        person_profession_df.to_sql('person_profession', con, schema=None, if_exists='fail', index=True,
                                    index_label=None, chunksize=None, dtype=None)
        cur.execute("DROP TABLE IF EXISTS person_known_titles")
        person_known_titles_df.to_sql('person_known_titles', con, schema=None, if_exists='fail', index=True,
                                      index_label=None, chunksize=None, dtype=None)

    cur.close()
    con.close()

    # update the bar
    sys.stdout.write("-")
    sys.stdout.flush()

sys.stdout.write("\n")