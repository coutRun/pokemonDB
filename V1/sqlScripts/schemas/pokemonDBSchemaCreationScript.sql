--Schema creation script made on 11/16/2023

-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.collection_collection_number_seq;

CREATE SEQUENCE public.collection_collection_number_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 32767
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.pokedex_id_seq;

CREATE SEQUENCE public.pokedex_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 32767
	START 1
	CACHE 1
	NO CYCLE;-- public.pokedex definition

-- Drop table

-- DROP TABLE pokedex;

CREATE TABLE pokedex (
	dex_num int4 NULL,
	dex_name varchar(50) NULL,
	form varchar(50) NULL,
	type1 varchar(50) NULL,
	type2 varchar(50) NULL,
	total int4 NULL,
	hp int4 NULL,
	attack int4 NULL,
	defense int4 NULL,
	sp_atk int4 NULL,
	sp_def int4 NULL,
	speed int4 NULL,
	gen int4 NULL,
	dex_id int2 NOT NULL DEFAULT nextval('pokedex_id_seq'::regclass),
	CONSTRAINT pokedex_pk PRIMARY KEY (dex_id)
);


-- public.pkmn_coll definition

-- Drop table

-- DROP TABLE pkmn_coll;

CREATE TABLE pkmn_coll (
	pkmn_name varchar NOT NULL,
	lvl int2 NULL,
	iv numeric NULL,
	dex_id int2 NOT NULL,
	coll_num int2 NOT NULL,
	CONSTRAINT collection_pokedex_id_fkey FOREIGN KEY (dex_id) REFERENCES pokedex(dex_id)
);
CREATE UNIQUE INDEX collection_collection_number_idx ON public.pkmn_coll USING btree (coll_num);

-- Table Triggers

CREATE TRIGGER insert_coll_num_trigger AFTER INSERT ON
public.pkmn_coll FOR EACH ROW EXECUTE FUNCTION insert_coll_num();


-- public.pkmn_nicknames definition

-- Drop table

-- DROP TABLE pkmn_nicknames;

CREATE TABLE pkmn_nicknames (
	coll_num int2 NOT NULL,
	nickname varchar NULL DEFAULT ' '::character varying,
	CONSTRAINT pkmn_nicknames_pkey PRIMARY KEY (coll_num),
	CONSTRAINT pkmn_nicknames_coll_num_fkey FOREIGN KEY (coll_num) REFERENCES pkmn_coll(coll_num) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.pkmn_stats definition

-- Drop table

-- DROP TABLE pkmn_stats;

CREATE TABLE pkmn_stats (
	coll_num int2 NOT NULL,
	hp int2 NULL,
	hpiv int2 NULL,
	atk int2 NULL,
	atkiv int2 NULL,
	def int2 NULL,
	defiv int2 NULL,
	sp_atk int2 NULL,
	sp_atkiv int2 NULL,
	sp_def int2 NULL,
	sp_defiv int2 NULL,
	speed int2 NULL,
	speediv int2 NULL,
	CONSTRAINT pkmn_stats_pkey PRIMARY KEY (coll_num),
	CONSTRAINT pkmn_stats_coll_num_fkey FOREIGN KEY (coll_num) REFERENCES pkmn_coll(coll_num) ON DELETE CASCADE ON UPDATE CASCADE
);



CREATE OR REPLACE FUNCTION public.insert_coll_num()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	INSERT INTO
		pkmn_nicknames(coll_num)
		VALUES(NEW.coll_num);
	INSERT INTO
		pkmn_stats(coll_num)
		VALUES(NEW.coll_num);
			
			RETURN NEW;
END;
$function$
;