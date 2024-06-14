#1115202200071 - Παναγιώτης Κλαΐνος
#1115202200168 - Γεώργιος Σπύρου
#1115202200107 - Θεοφάνης Μπαρμπαρόσος

#1
SELECT 
    m.title, g.genre_name
FROM
    movie m,
    genre g,
    movie_has_genre mg,
    actor a,
    role r
WHERE
    g.genre_name = 'Comedy'
        AND g.genre_id = mg.genre_id
        AND m.movie_id = mg.movie_id
        AND a.last_name = 'Allen'
        AND a.actor_id = r.actor_id
        AND m.movie_id = r.movie_id;

#2
SELECT 
    d.last_name, m.title
FROM
    director d,
    movie_has_director md,
    actor a,
    role r,
    movie m
WHERE
    a.last_name = 'Allen'
        AND a.actor_id = r.actor_id
        AND m.movie_id = r.movie_id
        AND d.director_id = md.director_id
        AND m.movie_id = md.movie_id
        AND d.director_id IN (SELECT DISTINCT
            d.director_id
        FROM
            director d,
            movie_has_director md1,
            movie_has_director md2,
            genre g1,
            genre g2,
            movie_has_genre mg1,
            movie_has_genre mg2,
            movie m1,
            movie m2
        WHERE
            d.director_id = md1.director_id
                AND d.director_id = md2.director_id
                AND m1.movie_id = md1.movie_id
                AND m2.movie_id = md2.movie_id
                AND g1.genre_id = mg1.genre_id
                AND g2.genre_id = mg2.genre_id
                AND m1.movie_id = mg1.movie_id
                AND m2.movie_id = mg2.movie_id
                AND g1.genre_id != g2.genre_id);

#3
SELECT 
    a.last_name
FROM
    actor a
WHERE
    a.actor_id IN (SELECT 
            a.actor_id
        FROM
            actor a,
            role r,
            director d,
            movie_has_director md,
            movie m
        WHERE
            a.last_name = d.last_name
                AND a.actor_id = r.actor_id
                AND m.movie_id = r.movie_id
                AND d.director_id = md.director_id
                AND m.movie_id = md.movie_id)
        AND a.actor_id IN (SELECT 
            a.actor_id
        FROM
            actor a,
            role r,
            director d,
            movie_has_director md,
            movie_has_director md1,
            movie m,
            movie m1,
            movie_has_genre mg,
            movie_has_genre mg1,
            genre g,
            genre g1
        WHERE
            a.actor_id = r.actor_id
                AND m.movie_id = r.movie_id
                AND d.director_id = md.director_id
                AND m.movie_id = md.movie_id
                AND a.last_name != d.last_name
                AND md1.movie_id = m1.movie_id
                AND md1.director_id = d.director_id
                AND mg.movie_id = m.movie_id
                AND mg.genre_id = g.genre_id
                AND mg1.movie_id = m1.movie_id
                AND mg1.genre_id = g1.genre_id
                AND mg.genre_id != mg1.genre_id);

#4
SELECT DISTINCT 'yes' AS answer
WHERE EXISTS (
    SELECT m.movie_id
    FROM movie m,
    movie_has_genre mg,
    genre g
    WHERE
    mg.movie_id = m.movie_id
    AND mg.genre_id = g.genre_id
    AND g.genre_name = 'Drama'
    AND m.year = 1995
)

UNION

SELECT DISTINCT 'no' AS answer
WHERE NOT EXISTS (
    SELECT m.movie_id
    FROM movie m,
    movie_has_genre mg,
    genre g
    WHERE
    mg.movie_id = m.movie_id
    AND mg.genre_id = g.genre_id
    AND g.genre_name = 'Drama'
    AND m.year = 1995
);

#5
SELECT 
    d1.last_name AS director1, d2.last_name AS director2
FROM
    director d1,
    director d2,
    movie_has_director md1,
    movie_has_director md2,
    movie m
WHERE
    d1.director_id = md1.director_id
        AND m.movie_id = md1.movie_id
        AND d2.director_id = md2.director_id
        AND m.movie_id = md2.movie_id
        AND m.year >= 2000
        AND m.year <= 2006
        -- Για να εμφανίζεται το κάθε ζεύγος μόνο μία φορά --
        AND d1.director_id < d2.director_id
        AND d1.director_id IN (SELECT 
            d.director_id
        FROM
            director d
        WHERE
            (SELECT 
                    COUNT(DISTINCT mg.genre_id)
                FROM
                    movie_has_director md,
                    movie_has_genre mg
                WHERE
                    md.director_id = d.director_id
                        AND md.movie_id = mg.movie_id) >= 6)
        AND d2.director_id IN (SELECT 
            d.director_id
        FROM
            director d
        WHERE
            (SELECT 
                    COUNT(DISTINCT mg.genre_id)
                FROM
                    movie_has_director md,
                    movie_has_genre mg
                WHERE
                    md.director_id = d.director_id
                        AND md.movie_id = mg.movie_id) >= 6);

#6
SELECT 
    a.first_name,
    a.last_name,
    COUNT(DISTINCT md.director_id) AS num_directors
FROM
    actor a,
    role r,
    movie_has_director md
WHERE
    a.actor_id = r.actor_id
        AND r.movie_id = md.movie_id
        AND a.actor_id IN (SELECT 
            actor_id
        FROM
            role
        GROUP BY actor_id
        HAVING COUNT(DISTINCT movie_id) = 3)
GROUP BY a.actor_id , a.first_name , a.last_name;

#7
SELECT 
    g1.genre_id, COUNT(DISTINCT mhd.director_id) AS count
FROM
    genre g1,
    movie_has_genre mhg1,
    movie_has_director mhd
WHERE
    g1.genre_id IN (SELECT DISTINCT
            g.genre_id
        FROM
            movie m,
            genre g,
            movie_has_genre mhg
        WHERE
            m.movie_id = mhg.movie_id
                AND g.genre_id = mhg.genre_id
                AND (SELECT 
                    COUNT(mg.genre_id)
                FROM
                    movie_has_genre mg,
                    genre g_in
                WHERE
                    g_in.genre_id = mg.genre_id
                        AND m.movie_id = mg.movie_id) = 1)
        AND g1.genre_id = mhg1.genre_id
        AND mhg1.movie_id = mhd.movie_id
        GROUP BY g1.genre_id;

#8
SELECT actor_id
FROM actor
WHERE NOT EXISTS (
    SELECT genre_id
    FROM genre
    WHERE NOT EXISTS (
        SELECT movie_id
        FROM movie_has_genre
        WHERE movie_has_genre.genre_id = genre.genre_id
        AND movie_id IN (
            SELECT movie_id
            FROM role
            WHERE role.actor_id = actor.actor_id
        )
    )
);