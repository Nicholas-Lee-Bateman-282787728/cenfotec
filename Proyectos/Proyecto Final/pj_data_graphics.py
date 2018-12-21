import pandas as pd
import sqlite3 as lite

con = lite.connect('imdb_movies.db')
cur = con.cursor()

with con:
    test = pd.read_sql_table('')