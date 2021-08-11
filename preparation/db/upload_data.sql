-- This script to upload tables to the DB.

-- First login under db_user
-- psql -p db_port -U db_user db_name


-- Before (re)populate the table it have to be dropped
DROP TABLE IF EXISTS cube CASCADE;

CREATE TABLE cube (
    cube_id         integer PRIMARY KEY,
    ra              float(8),
    dec             float(8),
    survey          varchar(32),
    filename        varchar(64),
    exptime         real,
    manga_id        varchar(32),
    manga_plateifu  varchar(32),
    sami_catid      varchar(32),
    sami_cube       varchar(32),
    califa_id       integer,
    califa_name     varchar(32),
    califa_cube     varchar(32),
    atlas_name      varchar(32)
);

\copy cube FROM 'table_cubes.csv' DELIMITER ',' CSV HEADER;

ALTER TABLE cube OWNER TO ifu_user;

CREATE INDEX ON cube (q3c_ang2ipix(ra, dec));

CLUSTER cube_q3c_ang2ipix_idx ON cube;

ANALYZE cube;

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- Add Atlas3D tables

-- http://www-astro.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt

DROP TABLE IF EXISTS atlas_param CASCADE;

CREATE TABLE atlas_param (
    atlas_name      varchar(16) PRIMARY KEY,
    ra              float(8),
    dec             float(8),
    sbf             integer,
    nedd            integer,
    virgo           boolean,
    vhel            real,
    d               real,
    m_k             real,
    a_b             real,
    type            real,
    logRe           real
);

\copy atlas_param FROM '../atlas3d/Cappellari2011a_Atlas3D_Paper1_Table3.txt' DELIMITER ',' CSV HEADER;

UPDATE atlas_param SET atlas_name=REPLACE(atlas_name,' ','');
ALTER TABLE atlas_param ADD COLUMN cube_id integer REFERENCES cube (cube_id);
UPDATE atlas_param AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.atlas_name = c.atlas_name;

ALTER TABLE atlas_param OWNER TO ifu_user;
ANALYZE atlas_param;




-- http://www-astro.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt

DROP TABLE IF EXISTS atlas_morphkin CASCADE;

CREATE TABLE atlas_morphkin (
    atlas_name      varchar(16) PRIMARY KEY REFERENCES atlas_param (atlas_name),
    pa_phot         real,
    e_PAphot        real,
    eps             real,
    e_eps           real,
    pa_kin          real,
    e_pa_kin        real,
    psi             real,
    k51             real,
    e_k51           real,
    max_k1          real,
    morph           varchar(16),
    dust            varchar(16),
    kin_struct      varchar(16),
    kin_group       varchar(16)
);

\copy atlas_morphkin FROM '../atlas3d/Krajnovic2011_Atlas3D_Paper2_TableD1.txt' DELIMITER ',' CSV HEADER;

UPDATE atlas_morphkin SET atlas_name=REPLACE(atlas_name,' ','');
UPDATE atlas_morphkin SET morph=REPLACE(morph,' ','');
UPDATE atlas_morphkin SET dust=REPLACE(dust,' ','');
UPDATE atlas_morphkin SET kin_struct=REPLACE(kin_struct,' ','');
UPDATE atlas_morphkin SET kin_group=REPLACE(kin_group,' ','');

ALTER TABLE atlas_morphkin ADD COLUMN cube_id integer REFERENCES cube (cube_id);
UPDATE atlas_morphkin AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.atlas_name = c.atlas_name;

ALTER TABLE atlas_morphkin OWNER TO ifu_user;
ANALYZE atlas_morphkin;