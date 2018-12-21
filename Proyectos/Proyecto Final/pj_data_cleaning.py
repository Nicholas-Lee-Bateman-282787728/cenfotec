import pandas as pd
import sqlite3 as lite

const_path = r'C:\git\cenfotec\Proyectos\Proyecto Final\IMDB Datasets'

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None  # default='warn'


def load_title_data():
    print("Loading titles data")
    titles_raw = pd.read_csv(
        const_path+r"\title.basics.tsv.gz"
        , sep='\t'
        , dtype={'startYear': object}
        , compression='gzip'
    )
    movie_titles = titles_raw[titles_raw['titleType'] == 'movie']
    print("Titles data loaded")
    return movie_titles


def load_person_data():
    print("Loading Person Data")
    person_raw = pd.read_csv(
        const_path+r"\name.basics.tsv.gz"
        , sep='\t'
        , compression='gzip'
    )
    print("Person data loaded")
    return person_raw


def load_rating_data(movie_titles):
    print("Loading Rating data")
    rating_raw = pd.read_csv(
        const_path + r"\title.ratings.tsv.gz"
        , sep='\t'
        , compression='gzip'
    )
    rating_df = pd.merge(rating_raw, movie_titles, on='tconst', how='inner')
    print("Rating data loaded")
    return rating_df


def load_crew_data(movie_titles):
    print("Loading Movie Crew data")
    titles_crew_raw = pd.read_csv(
        const_path + r"\title.crew.tsv.gz"
        , sep='\t'
        , compression='gzip'
    )
    movie_crew_raw = pd.merge(titles_crew_raw, movie_titles, on='tconst', how='inner')
    print("Movie Crew data loaded")
    return movie_crew_raw


def load_principals_data(movie_titles):
    print("Loading Title Principals data")
    titles_principals_raw = pd.read_csv(
        const_path + r"\title.principals.tsv.gz"
        , sep='\t'
        , compression='gzip'
    )
    print("Title Principals data loaded")
    titles_principals_raw = pd.merge(titles_principals_raw, movie_titles, on='tconst', how='inner')
    return titles_principals_raw


def clean_movie_data(movie_titles):
    print("Cleaning movie data")
    movie_titles_df = movie_titles[['tconst', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes']]
    movie_titles_df = movie_titles_df.replace(r'\N', 'N/A')
    movie_titles_df.columns = ['title_id', 'movie_name', 'is_adult', 'year', 'runtime']
    movie_titles_df = movie_titles_df.set_index('title_id')
    print("Movie data cleaned")
    return movie_titles_df


def clean_genre_data(movie_titles):
    print("Cleaning movie genre data")
    movie_genres = movie_titles[['tconst', 'genres']]
    movie_genres.columns = ['title_id', 'genres']
    movie_genres = movie_genres.replace(r'\N', 'N/A')
    movie_genres["genres"] = movie_genres["genres"].str.split(",")[0]
    movie_genres_df = movie_genres
    # print("Pivoting movie genre data")
    # movie_genres_df = movie_genres.genres.apply(pd.Series) \
    #     .merge(movie_genres, left_index=True, right_index=True) \
    #     .drop(["genres"], axis=1) \
    #     .melt(id_vars=['title_id'], value_name="genres") \
    #     .drop("variable", axis=1) \
    #     .dropna() \
    #     .set_index('title_id')
    # print("Movie genre data pivoted")
    print("Genre data cleaned")
    return movie_genres_df


def clean_rating_data(rating_df):
    print("Cleaning rating data")
    rating_df = rating_df.replace(r'\N', 'N/A')
    rating_df = rating_df[['tconst', 'averageRating', 'numVotes']]
    rating_df.columns = ['title_id', 'average_rating', 'num_votes']
    rating_df = rating_df.set_index('title_id')
    print("Movie rating cleaned")
    return rating_df


def clean_principals_data(title_principals):
    print("Cleaning titles principals data")
    title_principals_df = title_principals[['tconst', 'nconst', 'category', 'job']]
    title_principals_df = title_principals_df.replace(r'\N', 'N/A')
    title_principals_df.columns = ['title_id', 'person_id', 'category', 'job']
    title_principals_df = title_principals_df.set_index('title_id')
    print("Movie titles principals cleaned")
    return title_principals_df


def clean_person_data(person_raw):
    print("Cleaning person data")
    person_df = person_raw.replace(r'\N', 'N/A')
    person_df = person_df[person_df['deathYear'] == 'N/A']
    person_data_df = person_df[['nconst', 'primaryName', 'birthYear']]
    person_data_df.columns = ['person_id', 'name', 'birth_year']
    person_data_df = person_data_df.set_index('person_id')
    print("Person data cleaned")
    return person_data_df


def clean_directors_data(movie_crew_raw):
    print("Cleaning directors data")
    movie_directors = movie_crew_raw[['tconst', 'directors']]
    movie_directors = movie_directors.replace(r'\N', 'N/A')
    movie_directors.columns = ['title_id', 'directors']
    movie_directors["directors"] = movie_directors["directors"].str.split(",")
    print("Pivoting directors data")
    movie_directors_df = movie_directors.directors.apply(pd.Series)\
        .merge(movie_directors, left_index=True, right_index=True)\
        .drop(["directors"], axis=1)\
        .melt(id_vars=['title_id'], value_name="directors")\
        .drop("variable", axis=1)\
        .dropna()\
        .set_index('title_id')
    print("Directors data pivoted")
    print("Directors data cleaned")
    return movie_directors_df


def clean_writers_data(movie_crew_raw):
    print("Cleaning writers data")
    movie_writers = movie_crew_raw[['tconst', 'writers']]
    movie_writers = movie_writers.replace(r'\N', 'N/A')
    movie_writers.columns = ['title_id', 'writers']
    movie_writers["writers"] = movie_writers["writers"].str.split(",")
    print("Pivoting Writers data")
    movie_writers_df = movie_writers.writers.apply(pd.Series)\
        .merge(movie_writers, left_index=True, right_index=True)\
        .drop(["writers"], axis=1)\
        .melt(id_vars=['title_id'], value_name="writers")\
        .drop("variable", axis=1)\
        .dropna()\
        .set_index('title_id')
    print("Writers data pivoted")
    print("Writers data cleaned")
    return movie_writers_df


def load_tables(con, cur, movie_titles_df, movie_genres_df, person_data_df, rating_df,
                movie_directors_df, movie_writers_df, title_principals_df):
    print("Creating tables")
    with con:
        cur.execute("DROP TABLE IF EXISTS movie_titles")
        movie_titles_df.to_sql('movie_titles'
                               , con=con
                               , schema=None
                               , if_exists='fail'
                               , index=True
                               , index_label=None
                               , chunksize=None
                               , dtype=None)
        cur.execute("DROP TABLE IF EXISTS movie_genres")
        movie_genres_df.to_sql('movie_genres'
                               , con=con
                               , schema=None
                               , if_exists='fail'
                               , index=True
                               , index_label=None
                               , chunksize=None
                               , dtype=None)
        cur.execute("DROP TABLE IF EXISTS person_data")
        person_data_df.to_sql('person_data'
                              , con=con
                              , schema=None
                              , if_exists='fail'
                              , index=True
                              , index_label=None
                              , chunksize=None
                              , dtype=None)
        cur.execute("DROP TABLE IF EXISTS movie_rating")
        rating_df.to_sql('movie_rating'
                         , con=con
                         , schema=None
                         , if_exists='fail'
                         , index=True
                         , index_label=None
                         , chunksize=None
                         , dtype=None)
        cur.execute("DROP TABLE IF EXISTS movie_directors")
        movie_directors_df.to_sql('movie_directors'
                                  , con=con
                                  , schema=None
                                  , if_exists='fail'
                                  , index=True
                                  , index_label=None
                                  , chunksize=None
                                  , dtype=None)
        cur.execute("DROP TABLE IF EXISTS movie_writers")
        movie_writers_df.to_sql('movie_writers'
                                , con=con
                                , schema=None
                                , if_exists='fail'
                                , index=True
                                , index_label=None
                                , chunksize=None
                                , dtype=None)
        cur.execute("DROP TABLE IF EXISTS movie_principals")
        title_principals_df.to_sql('movie_principals'
                                   , con=con
                                   , schema=None
                                   , if_exists='fail'
                                   , index=True
                                   , index_label=None
                                   , chunksize=None
                                   , dtype=None)
    print("Tables created, closing connection")

def main():
    con = lite.connect('imdb_movies.db')
    cur = con.cursor()
    movie_data = load_title_data()
    person_data = load_person_data()
    rating_data = load_rating_data(movie_titles=movie_data)
    crew_data = load_crew_data(movie_titles=movie_data)
    principals_data = load_principals_data(movie_titles=movie_data)
    movie_data_df = clean_movie_data(movie_titles=movie_data)
    movie_genres_df = clean_genre_data(movie_titles=movie_data)
    person_data_df = clean_person_data(person_raw=person_data)
    rating_data_df = clean_rating_data(rating_df=rating_data)
    directors_data_df = clean_directors_data(movie_crew_raw=crew_data)
    writers_data_df = clean_writers_data(movie_crew_raw=crew_data)
    principals_data_df = clean_principals_data(title_principals=principals_data)
    load_tables(con=con,
                cur=cur,
                movie_titles_df=movie_data_df,
                movie_genres_df=movie_genres_df,
                person_data_df=person_data_df,
                rating_df=rating_data_df,
                movie_directors_df=directors_data_df,
                movie_writers_df=writers_data_df,
                title_principals_df=principals_data_df)
    cur.close()
    con.close()


if __name__ == '__main__':
    main()
