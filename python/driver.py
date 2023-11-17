
# This python file connects to the pokemondb database on localhost
# features:
# insert pokemon to collection
# search pokedex by dex_id
# select pokemon collection
# autofill functionality to speed up insertion process

import psycopg2
import os
import pandas

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


#psql related functions

def getPkmnColl(crsr):
    
  showColl = """SELECT coll_num,pkmn_name,lvl,iv,dex_id FROM pkmn_coll ORDER BY coll_num ASC;"""

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

def updatePkmnStats(crsr,collNum,hp,attack,defense,spatk,spdef,speed):
  updPkmnStats = """UPDATE pkmn_stats SET hp = %s, atk = %s, def = %s, sp_atk = %s, sp_def = %s, speed = %s WHERE coll_num = %s;"""
  crsr.execute(updPkmnStats,(hp,attack,defense,spatk,spdef,speed,collNum))


# Other functions
def printer(crsr,res):
  cols = []
  for elt in crsr.description:
    cols.append(elt[0])
  df = pandas.DataFrame(data=res,columns=cols)
  df = df.to_string(index=False)
  print(df)
  return crsr,res



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
    
    hp = None
    attack = None
    defense = None
    spatk = None
    spdef = None
    speed  = None
    
    while menuOption != '0':
      print("Enter an option:\n1 = show collection\n2 = search pokedex for pokemon by name\n3 = insert pokemon to database\n4 = add basic stats\n0 = quit")
      menuOption = input()
      
      #list all pokemon in the collection
      if menuOption == '1':
        coll = getPkmnColl(crsr)
        printer(crsr,coll)
            
      # search pokedex by name
      if menuOption == '2':
        name = input("Enter pokemon name: ")
        searchResults = getPokedexByName(crsr,name)
        printer(crsr,searchResults)
                
      # insert pokemon into collection
      if menuOption == '3':
        collNum = input("Enter pokemon collNum: ")
        name = input("Enter pokemon name: ")
        lvl = input("Enter pokemon level: ")
        iv = input("Enter pokemon iv: ")
        searchResults = getPokedexByName(crsr,name)
        # if there's only 1 search result, autofill dexID
        if len(searchResults) == 1:
          dexID = searchResults[0][0]
        #else print search results and ask for dexID
        else:
          printer(crsr,searchResults)
          dexID = input("Enter pokemon dexID: ")
        insertPkmnColl(crsr,name,lvl,iv,dexID,collNum)
      if menuOption == '4':
        collNum = input("Enter pokemon collNum: ")
        hp = input("HP:     ")
        attack = input("Atk:    ")
        defense = input("Def:    ")
        spatk = input("Sp Atk: ")
        spdef = input("Sp Def: ")
        speed = input("Speed:  ")
        updatePkmnStats(crsr,collNum,hp,attack,defense,spatk,spdef,speed)
                
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