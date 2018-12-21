import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

con = lite.connect('imdb_movies.db')
cur = con.cursor()

query = 'SELECT cast(year as int) `year`' \
        ',genres' \
        ',avg(average_rating) `average_rating` ' \
        'FROM vw_movie_genres_ratings ' \
        'WHERE `year` != "N/A"' \
        'GROUP BY year,genres ' \
        'ORDER BY `year`'
test = pd.read_sql(sql=query, con=con)

#test.plot(kind='scatter', x='year', y='average_rating')
test.plot(kind='bar',x='year',y='average_rating')
plt.show()

cur.close()
con.close()
