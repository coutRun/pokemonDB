
# This python file connects to the pokemondb database on localhost
# features:
# insert pokemon to collection
# search pokedex by dex_id
# select pokemon collection
# autofill functionality to speed up insertion process

import psycopg2
import os


def startConnection(connection):
        # sensitive information is stored as environment variables
    connection = psycopg2.connect(
        host=os.getenv("PSQLPKMNHOST"),
        port=os.getenv("PSQLPKMNPORT"),
        database=os.getenv("PSQLPKMNDATABASE"),
        user=os.getenv("PSQLPKMNUSER"),
        password=os.getenv("PSQLPKMNPASSWORD")
    )
    return connection

def getPkmnColl(crsr):
    
    showColl = """SELECT * FROM pkmn_coll;"""

    crsr.execute(showColl)
    pkmnColl = crsr.fetchall()
    return pkmnColl

def getPokedexByName(crsr,name):
    
    lookupDex = """SELECT dex_id,form,type1,type2,form FROM pokedex WHERE dex_name = %s;"""

    crsr.execute(lookupDex,[name])
    searchResults = crsr.fetchall()
    return searchResults

def insertPkmnColl(crsr,name,lvl,iv,dexID,collNum):
    insPkmn = """INSERT INTO pkmn_coll (pkmn_name,lvl,iv,dex_id,coll_num) VALUES (%s,%s,%s,%s,%s);"""
    crsr.execute(insPkmn,(name,lvl,iv,dexID,collNum))

def printer(res):
    print("-------------------------")
    for i in res:
        print(i)
    print("-------------------------")
    return res

# main
def main():
    connection = None
    try:
        connection = startConnection(connection)
        crsr = connection.cursor()
        
        # prepared statements
        
        # initalized variables
        menuOption = None
        name = None
        lvl = None
        iv = None
        dexID = None
        collNum = None
        
        while menuOption != 'q':
            print("Enter an option:\nc = show collection\ns = search pokedex for pokemon by name\ni = insert pokemon to database\nq = quit")
            menuOption = input()
            
            #list all pokemon in the collection
            if menuOption == 'c':
                coll = getPkmnColl(crsr)
                printer(coll)
            
            # search pokedex by name
            if menuOption == 's':
                name = input("Enter pokemon name: ")
                searchResults = getPokedexByName(crsr,name)
                printer(searchResults)
                
            # insert pokemon into collection
            if menuOption == 'i':
                name = input("Enter pokemon name: ")
                lvl = input("Enter pokemon level: ")
                iv = input("Enter pokemon iv: ")
                searchResults = getPokedexByName(crsr,name)
                # if there's only 1 search result, autofill dexID
                if len(searchResults) == 1:
                    dexID = searchResults[0][0]
                #else print search results and ask for dexID
                else:
                    printer(searchResults)
                    dexID = input("Enter pokemon dexID: ")
                # autofill colNum if it isn't this session's first insert
                if collNum != None:
                    collNum = str(int(collNum) + 1)
                else:
                    collNum = input("Enter pokemon collNum: ")
                insertPkmnColl(crsr,name,lvl,iv,dexID,collNum)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            # commit changes to pokemondb
            connection.commit()
            connection.close()
            print("Database connection terminated.")

if __name__=="__main__":
    main()