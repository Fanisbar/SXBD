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
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    try:
        float(rank1)
    except ValueError:
        return [("status",),("error",),]
    try:
        float(rank2)
    except ValueError:
        return [("status",),("error",),]

    print (rank1, rank2, movieTitle)

    return [("status",),("ok",),]


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
