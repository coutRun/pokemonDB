import os
import psycopg2
from pkmnCollEntryClass import PkmnCollEntry
from pkmnStatsEntryClass import PkmnStatsEntry

# Postgres related functions
# Note: These are the only functions in the python program that access the database
# Accessing the database is their primary purpose
# User input, input validation, etc are to be handled by functions in functions.py

def pgStartConnection(connection):
  # sensitive information is stored as environment variables
  connection = psycopg2.connect(
    host=os.getenv("PSQLPKMNHOST"),
    port=os.getenv("PSQLPKMNPORT"),
    database=os.getenv("PSQLPKMNDATABASE"),
    user=os.getenv("PSQLPKMNUSER"),
    password=os.getenv("PSQLPKMNPASSWORD")
  )
  return connection


def pgSelPkmnColl(crsr):
    
  showColl = """SELECT coll_num,pkmn_name,lvl,iv,dex_id FROM pkmn_coll ORDER BY coll_num ASC;"""

  crsr.execute(showColl)
  pkmnColl = crsr.fetchall()
  return pkmnColl

def pgSelPokedexEntryByName(crsr,pkmnName):
    
  lookupDex = """SELECT dex_id,form,type1,type2,form FROM pokedex WHERE dex_name = %s;"""

  crsr.execute(lookupDex,[pkmnName])
  searchResults = crsr.fetchall()
  return searchResults

def pgInsPkmnColl(crsr,pkmnCollData:PkmnCollEntry):
  insPkmn = """INSERT INTO pkmn_coll (pkmn_name,lvl,iv,dex_id,coll_num) VALUES (%s,%s,%s,%s,%s);"""
  crsr.execute(insPkmn,(pkmnCollData.name,pkmnCollData.level,pkmnCollData.iv,pkmnCollData.dexID,pkmnCollData.collNum))

def pgUpdPkmnStats(crsr,pkmnStatsData:PkmnStatsEntry):
  updPkmnStats = """UPDATE pkmn_stats SET hp = %s, atk = %s, def = %s, sp_atk = %s, sp_def = %s, speed = %s WHERE coll_num = %s;"""
  crsr.execute(updPkmnStats,(pkmnStatsData.hp,pkmnStatsData.attack,pkmnStatsData.defense,pkmnStatsData.spatk,pkmnStatsData.spdef,pkmnStatsData.speed,pkmnStatsData.collNum))

def pgSelPkmnByCollNum(crsr,collNum):
    selectPkmn = """SELECT * FROM pkmn_coll WHERE coll_num = %s"""
    crsr.execute(selectPkmn,[collNum])
    selectedPkmn = crsr.fetchall()
    return selectedPkmn

def pgDelPkmn(crsr,collNum):
  deletePkmn = """DELETE FROM pkmn_coll WHERE coll_num = %s"""
  crsr.execute(deletePkmn,[collNum])

