
import pandas
from pkmnCollEntryClass import PkmnCollEntry
from pkmnStatsEntryClass import PkmnStatsEntry
from pgFunctions import *
import csv

# All functions in the python project that do not access the database
# Note: although these functions can call other functions in pgFunctions,
# They should never access the database directly

def readPkmnCollDataFromUser(crsr):

  pkmnCollData = PkmnCollEntry()
  
  print("Enter pokemon collID, name, level, IV: ")
  pkmnCollInput = input().split()
  pkmnCollData.collID = pkmnCollInput[0]
  pkmnCollData.name = pkmnCollInput[1]
  pkmnCollData.level = pkmnCollInput[2]
  pkmnCollData.iv = pkmnCollInput[3]
  
  searchResults = pgSelPokedexEntryByName(crsr,pkmnCollData.name)
  # if there's only 1 search result, autofill dexID
  if len(searchResults) == 1:
    pkmnCollData.dexID = searchResults[0][0]
  #else print search results and ask for dexID
  else:
    printer(crsr,searchResults)
    pkmnCollData.dexID = input("Enter pokemon dexID: ")
  
  return pkmnCollData

def readPkmnStatsDataFromUser():
  
  pkmnStatsData = PkmnStatsEntry()
  
  print("Enter pokemon collID, HP, Atk, Def, Sp. Atk, Sp. Def, Speed: ")
  pkmnStatsInput = input().split()
  pkmnStatsData.collID = pkmnStatsInput[0]
  pkmnStatsData.hp = pkmnStatsInput[1]
  pkmnStatsData.attack = pkmnStatsInput[2]
  pkmnStatsData.defense = pkmnStatsInput[3]
  pkmnStatsData.spatk = pkmnStatsInput[4]
  pkmnStatsData.spdef = pkmnStatsInput[5]
  pkmnStatsData.speed = pkmnStatsInput[6]
  
  return pkmnStatsData
  
def readPkmnCollIDFromUser():
  collID = input("Enter the collID of the pokemon to be deleted: ")
  return collID
  
def delPkmnByCollID(crsr,collID):
  pkmnToBeDeleted = pgSelPkmnByCollID(crsr,collID)
  print("Deleting the following pokemon: ")
  printer(crsr,pkmnToBeDeleted)
  
  pgDelPkmn(crsr,collID)

def printer(crsr,res):
  cols = []
  for elt in crsr.description:
    cols.append(elt[0])
  df = pandas.DataFrame(data=res,columns=cols)
  df = df.to_string(index=False)
  print(df)
  return crsr,res

