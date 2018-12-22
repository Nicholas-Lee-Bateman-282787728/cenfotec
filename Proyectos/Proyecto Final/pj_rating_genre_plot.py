import pandas as pd
import numpy as np
import sqlite3 as lite
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

print('Creating connection')
con = lite.connect('imdb_movies.db')
cur = con.cursor()

print('Executing Query')
query = 'SELECT cast(`year` as int) `year`' \
        '      , genres' \
        '      , avg(average_rating) `average_rating`' \
        ' FROM vw_movie_genres_ratings' \
        ' GROUP BY `year`,genres'
ratings_by_genre = pd.read_sql(sql=query, con=con)
group_ratings_by_genre = ratings_by_genre.groupby(['genres'])

print("plotting")

fig, axes = plt.subplots(3, 5, figsize=(15, 5))
for (group, data), ax in zip(group_ratings_by_genre, axes.flatten()):
        data.plot(x='year', y='average_rating', kind='line', ax=ax, title=group, color='green')
        ax.get_legend().remove()
        ax.set_xlabel('')

plt.subplots_adjust(left=0.125, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)
plt.suptitle("Movie Ratings by Genders Across Years")
plt.show()

print("closing connection")
cur.close()
con.close()
