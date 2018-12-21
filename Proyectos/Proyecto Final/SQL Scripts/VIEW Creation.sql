SELECT * FROM tbl_movie_directors;
SELECT * FROM tbl_movie_genres;
SELECT * FROM tbl_movie_principals;
SELECT * FROM tbl_movie_ratings;
SELECT * FROM tbl_movie_titles;
SELECT * FROM tbl_movie_writers;
SELECT * FROM tbl_person_data;

CREATE VIEW IF NOT EXISTS vw_director_data AS
SELECT DISTINCT
     pd.person_id
   , pd.name
   , pd.birth_year
FROM tbl_person_data pd
     JOIN tbl_movie_directors md
        ON pd.person_id = md.directors;
       
CREATE VIEW IF NOT EXISTS vw_writer_data AS
SELECT DISTINCT
     pd.person_id
   , pd.name
   , pd.birth_year
FROM tbl_person_data pd
     JOIN tbl_movie_writers mw
        ON pd.person_id = mw.writers;

DROP VIEW IF EXISTS vw_movie_ratings;
CREATE VIEW IF NOT EXISTS vw_movie_ratings AS
SELECT mt.title_id
     , mt.movie_name
     , mt.is_adult
     , mt.`year`
     , mt.runtime
     , mr.average_rating
     , mr.num_votes
FROM tbl_movie_titles mt
     JOIN tbl_movie_ratings mr
        ON mt.title_id = mr.title_id;

DROP VIEW IF EXISTS vw_movie_genres;
CREATE VIEW IF NOT EXISTS vw_movie_genres AS
SELECT mt.title_id
     , mt.movie_name
     , mt.is_adult
     , mt.`year`
     , mt.runtime
     , mg.genres
FROM tbl_movie_titles mt
     JOIN tbl_movie_genres mg
        ON mt.title_id = mg.title_id;
        
CREATE VIEW IF NOT EXISTS vw_movie_genres_ratings AS
SELECT mt.title_id
     , mt.movie_name
     , mt.is_adult
     , mt.`year`
     , mt.runtime
     , mr.average_rating
     , mr.num_votes
     , mg.genres
FROM tbl_movie_titles mt
     JOIN tbl_movie_ratings mr
        ON mt.title_id = mr.title_id
     JOIN tbl_movie_genres mg
        ON mt.title_id = mg.title_id;


DROP VIEW IF EXISTS vw_full_movie_data;
CREATE VIEW IF NOT EXISTS vw_full_movie_data AS
SELECT DISTINCT 
     mt.title_id
     , mt.movie_name
     , mt.is_adult
     , mt.`year`
     , mt.runtime
     , md.directors
     , COALESCE(vdd.name,'N/A') `director_name`
     , mw.writers
     , COALESCE(vwd.name,'N/A') `writer_name`
     , mr.average_rating
     , mr.num_votes
     , mg.genres
FROM tbl_movie_titles mt
     JOIN tbl_movie_directors md
        ON mt.title_id = md.title_id
     JOIN tbl_movie_writers mw 
        ON mt.title_id = mw.title_id
     JOIN tbl_movie_ratings mr 
        ON mt.title_id = mr.title_id
     JOIN tbl_movie_genres mg 
        ON mt.title_id = mg.title_id
     LEFT JOIN vw_director_data vdd
        ON vdd.person_id = md.directors
     LEFT JOIN vw_writer_data vwd
        ON vwd.person_id = mw.writers;

CREATE VIEW IF NOT EXISTS vw_movie_principals AS
SELECT mt.`title_id`
     , mt.`movie_name`
     , mt.`is_adult`
     , mt.`year`
     , mt.`runtime`
     , COALESCE(pd.`person_id`,'N/A') `person_id`
     , COALESCE(pd.`name`,'N/A') `name`
     , mp.`category`
FROM tbl_movie_titles mt
JOIN tbl_movie_principals mp ON mt.title_id = mp.title_id
LEFT JOIN tbl_person_data pd ON mp.person_id = pd.person_id;