# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql

def connection():
    ''' User this function to create your connections '''    
    con = pymysql.connect(host='127.0.0.1', port=3306, user='', passwd='', db='movies') #update with your settings
    
    return con

def updateRank(rank1, rank2, movieTitle):
    # Create a new connection
    con = connection()
    cur = con.cursor()

    try:
        # Validate inputs
        try:
            rank1 = float(rank1)
        except:
            return [("status",), ("error", "Rank1 must be a double from 0 to 10"),]
        
        try:
            rank2 = float(rank2)
        except:
            return [("status",), ("error", "Rank2 must be a double from 0 to 10"),]
        
        if not (0 <= rank1 <= 10):
            return [("status",), ("error", "Rank1 must be a double from 0 to 10"),]
        
        if not (0 <= rank2 <= 10):
            return [("status",), ("error", "Rank2 must be a double from 0 to 10"),]
        
        # Check if the movie exists
        cur.execute("SELECT m.`rank` FROM movie m WHERE title = %s", (movieTitle,))
        results = cur.fetchall()

        if len(results) == 0:
            return [("status",), ("error", "Movie not found"),]
        elif len(results) > 1:
            return [("status",), ("error", "Multiple movies found"),]
        
        current_rank = results[0][0]

        # Calculate the new rank
        if current_rank is None:
            new_rank = (rank1 + rank2) / 2
        else:
            new_rank = (current_rank + rank1 + rank2) / 3
        
        # Update the rank in the database
        cur.execute("UPDATE movie SET `rank` = %s WHERE title = %s", (new_rank, movieTitle))
        con.commit()
        return [("status",), ("ok",),]
    
    except Exception as e:
        con.rollback()
        return [("status",), ("error", str(e)),]
    finally:
        cur.close()
        con.close()


def colleaguesOfColleagues(actorId1, actorId2):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    try:
        #Check if actor id's are integers
        try:
            actorId1 = float(actorId1)
            actorId2 = float(actorId2)
        except:
            return [("status",), ("error", "The actor Id's must be integers"),]

        #Check if actor id's exist
        cur.execute("SELECT a.`actor_id` FROM actor a WHERE a.actor_id = %s", actorId1)
        results = cur.fetchall()
        if len(results) == 0:
            return [("status",), ("error", "Actor Id 1 does not exist"),]
        
        cur.execute("SELECT a.`actor_id` FROM actor a WHERE a.actor_id = %s", actorId2)
        results = cur.fetchall()
        if len(results) == 0:
            return [("status",), ("error", "Actor Id 2 does not exist"),]

        #Check if actor id's are different
        if actorId1 == actorId2:
            return [("status",), ("error", "The actor Id's must be different"),]
        
        #Find colleagues of actorId1
        cur.execute("""SELECT 
                            r1.actor_id
                        FROM
                            movie m,
                            role r1,
                            role r2
                        WHERE
                            r2.actor_id = %s
                            AND r2.movie_id = m.movie_id
                            AND r1.movie_id = m.movie_id
                            AND r1.actor_id != r2.actor_id;""", actorId1)
        results = cur.fetchall()

        colleagues1 = []
        for row in results:
            colleagues1.append(row[0])
        if actorId2 in colleagues1:
            colleagues1.remove(actorId2)

        #Find colleagues of actorId2
        cur.execute("""SELECT 
                            r1.actor_id
                        FROM
                            movie m,
                            role r1,
                            role r2
                        WHERE
                            r2.actor_id = %s
                            AND r2.movie_id = m.movie_id
                            AND r1.movie_id = m.movie_id;""", actorId2)
        results = cur.fetchall()

        colleagues2 = []
        for row in results:
            colleagues2.append(row[0])
        if actorId1 in colleagues2:
            colleagues2.remove(actorId1)
        
        #Find colleagues of colleagues
        final = [("Movies", "Actor c", "Actor d", "Actor a", "Actor b")]
        for coll1 in colleagues1:
            for coll2 in colleagues2:
                if coll1 != coll2:
                    cur.execute("""SELECT 
                                        m.title
                                    FROM
                                        movie m,
                                        role r1,
                                        role r2
                                    WHERE
                                        r1.actor_id = %s
                                        AND r2.actor_id = %s
                                        AND r1.movie_id = m.movie_id
                                        AND r2.movie_id = m.movie_id;""", (coll1, coll2))
                    results = cur.fetchall()
                    if len(results) > 0:
                        movies = list(results[0])
                        movies_str = ""
                        counter = 1
                        for movie in movies:
                            movies_str += movie
                            if counter != len(movies):
                                movies_str += ", "
                                counter += 1
                        final.append((movies_str, coll1, coll2, int(actorId1), int(actorId2)))
                    
        
    except Exception as e:
        con.rollback()
        return [("status",), ("error", str(e)),]
    finally:
        cur.close()
        con.close()
        return final

def actorPairs(actorId):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    print (actorId)

    return [("actorId",),]

def selectTopNactors(n):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    print (n)

    return [("genreName", "actorId", "numberOfMovies"),]

def traceActorInfluence(actorId):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()


    return [("influencedActorId",),]
