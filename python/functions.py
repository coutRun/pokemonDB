
import pandas
from pkmnCollEntryClass import PkmnCollEntry
from pkmnStatsEntryClass import PkmnStatsEntry
from pgFunctions import *


def readPkmnCollDataFromUser(crsr):

  pkmnCollData = PkmnCollEntry()
  
  print("Enter pokemon collNum, name, level, IV: ")
  pkmnCollInput = input().split()
  pkmnCollData.collNum = pkmnCollInput[0]
  pkmnCollData.name = pkmnCollInput[1]
  pkmnCollData.level = pkmnCollInput[2]
  pkmnCollData.iv = pkmnCollInput[3]
  
  searchResults = pgSelectPokedexEntryByName(crsr,pkmnCollData.name)
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
  
  print("Enter pokemon collNum, HP, Atk, Def, Sp. Atk, Sp. Def, Speed: ")
  pkmnStatsInput = input().split()
  pkmnStatsData.collNum = pkmnStatsInput[0]
  pkmnStatsData.hp = pkmnStatsInput[1]
  pkmnStatsData.attack = pkmnStatsInput[2]
  pkmnStatsData.defense = pkmnStatsInput[3]
  pkmnStatsData.spatk = pkmnStatsInput[4]
  pkmnStatsData.spdef = pkmnStatsInput[5]
  pkmnStatsData.speed = pkmnStatsInput[6]
  
  return pkmnStatsData
  
# Other functions
def printer(crsr,res):
  cols = []
  for elt in crsr.description:
    cols.append(elt[0])
  df = pandas.DataFrame(data=res,columns=cols)
  df = df.to_string(index=False)
  print(df)
  return crsr,res

