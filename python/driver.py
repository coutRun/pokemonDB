
# This python project connects to the pokemondb database on localhost
# features:
# insert pokemon to collection
# search pokedex by dex_id
# select pokemon collection
# autofill functionality to speed up insertion process

import psycopg2
from pgFunctions import *
from functions import *

# Note: The only function this file defines is the main function
# all other functions are defined in functions.py and pgFunctions.py

# main
def main():
  connection = None
  try:
    connection = pgStartConnection(connection)
    crsr = connection.cursor()
        
    # initalized variables
    menuOption = None
    
    while menuOption != '0':
      print("Enter an option:\n1 = show collection\n2 = search pokedex for pokemon by name\n3 = insert pokemon to database\n4 = add basic stats\n5 = delete pokemon by collection number\n0 = quit")
      menuOption = input()
      
      #list all pokemon in the collection
      if menuOption == '1':
        coll = pgSelPkmnColl(crsr)
        printer(crsr,coll)
            
      # search pokedex by name
      if menuOption == '2':
        pkmnName = input("Enter pokemon name: ")
        searchResults = pgSelPokedexEntryByName(crsr,pkmnName)
        printer(crsr,searchResults)
                
      # insert pokemon into collection
      if menuOption == '3':
        pkmnCollData = readPkmnCollDataFromUser(crsr)
        pgInsPkmnColl(crsr,pkmnCollData)
      if menuOption == '4':
        pkmnStatsData = readPkmnStatsDataFromUser()
        pgUpdPkmnStats(crsr,pkmnStatsData)
      if menuOption == '5':
        pkmnCollNum = readPkmnCollNumFromUser()
        delPkmnByCollNum(crsr,pkmnCollNum)
                
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