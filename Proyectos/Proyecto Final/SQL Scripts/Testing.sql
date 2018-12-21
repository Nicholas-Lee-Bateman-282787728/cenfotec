with a as
(
SELECT * FROM vw_movie_ratings ORDER BY num_votes DESC, average_rating DESC LIMIT 250
)
SELECT max(num_votes),min(num_votes),avg(num_votes) FROM a;

SELECT count(1) from vw_movie_ratings;
SELECT count(1) from vw_movie_ratings where num_votes > 400000;
SELECT count(1) from vw_movie_ratings where num_votes > 650000;