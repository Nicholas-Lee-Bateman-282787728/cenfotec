import pj_data_cleaning as p
import pandas as pd


titles = p.load_title_data()
genres = p.load_rating_data(titles)
rating = p.load_rating_data(titles)

titles_df = p.clean_movie_data(titles)
genres_df = p.clean_genre_data(genres)

rating_df = p.clean_rating_data(rating)
rating_df = rating_df[rating_df['num_votes'] > 3155]

genres_df = pd.merge(genres_df, titles_df, on='title_id', how='inner')
rating_df = pd.merge(rating_df, genres_df, on='title_id', how='inner')

groupby_genre = rating_df.groupby(['genres', 'year'])

print(groupby_genre)

# titles_raw[titles_raw['titleType'] == 'movie']

print(groupby_genre.describe())
print(groupby_genre.mean())
