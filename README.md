# pokemonDB


## Database Notes:

Note: columns that contain id in their name indicates that the column is used to uniquely identify an entry.

### Tables:
pokedex
Columns:
dex_num
dex_name
form
type1
type2
total
hp
attack
defense
sp_atk
sp_def
speed
gen
dex_id

Note: In Pokemon, a pokemon's Pokedex Number is not unique if the pokemon has multiple forms. This is why dex_id is a necessary column to uniquely identify a pokedex entry. However, dex_num refers to the Pokemon's pokedex number.


pkmn_coll
Columns:
pkmn_name
lvl
iv
dex_id
coll_id

Note: coll_id refers to the pokemon's number. It uniquely identifies a pokemon in the collection.
(coll_id was previously named coll_num. It was renamed to indicate that it is a unique identifier, and to avoid confusion with a pokemon's pokedex number.)


pkmn_stats
Columns:
coll_id
hp
hpiv
atk
atkiv
def
defiv
sp_atk
sp_atkiv
sp_def
sp_defiv
speed
speediv


pkmn_nicknames
Columns:
coll_id
nickname
