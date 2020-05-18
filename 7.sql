SELECT rating, title
FROM ratings, movies
WHERE ratings.movie_id = movies.id AND movies.year = 2010
ORDER BY "rating", "title" DESC
