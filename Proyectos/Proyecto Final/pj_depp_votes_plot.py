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
query = 'SELECT mgr.title_id' \
        '     , cast(mgr.`year` as int) `year`' \
        '     , mgr.num_votes' \
        '     , mgr.genres' \
        ' FROM vw_movie_genres_ratings mgr' \
        '        JOIN tbl_movie_principals mp' \
        '                ON mgr.title_id = mp.title_id' \
        ' WHERE mp.person_id = "nm0000136" AND mp.category = "actor"' \
        ' ORDER BY `year`'
depp_movies_votes = pd.read_sql(sql=query, con=con)
group_depp_by_genre = depp_movies_votes.groupby(['genres'])

fig, axes = plt.subplots(2, 5, figsize=(15, 5))
for (group, data), ax in zip(group_depp_by_genre, axes.flatten()):
        data.plot(x='year', y='num_votes', kind='scatter', ax=ax, title=group, color='red')
        data.plot(x='year', y='num_votes', kind='line', ax=ax, title=group, color='red')
        ax.get_legend().remove()
        ax.set_xlabel('')

plt.subplots_adjust(left=0.125, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)
plt.suptitle("Johnny Depp Movie Votes Across Years")
plt.show()

print("closing connection")
cur.close()
con.close()
