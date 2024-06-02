# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql

def connection():
    ''' User this function to create your connections '''    
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='srootpwd@271', db='movies') #update with your settings
    
    return con

def updateRank(rank1, rank2, movieTitle):
    # Create a new connection
    con = connection()
    cur = con.cursor()

    try:
        # Validate inputs
        rank1 = float(rank1)
        rank2 = float(rank2)
        
        if not (0 <= rank1 <= 10) or not (0 <= rank2 <= 10):
            return [("status",), ("error",),]
        
        # Check if the movie exists
        cur.execute("SELECT rank FROM movie WHERE title = %s", (movieTitle,))
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
        cur.execute("UPDATE movie SET rank = %s WHERE title = %s", (new_rank, movieTitle))
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

    print (actorId1, actorId2)

    return [("movieTitle", "colleagueOfActor1", "colleagueOfActor2", "actor1","actor2",),]

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
