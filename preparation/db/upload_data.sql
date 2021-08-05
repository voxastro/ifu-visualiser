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
    sami_catid      bigint,
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
-- Add Atlas3D table
-- http://www-astro.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt

DROP TABLE IF EXISTS atlas_sample CASCADE;

CREATE TABLE atlas_sample (
    atlas_name      varchar(32) PRIMARY KEY,
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

\copy atlas_sample FROM '../atlas3d/Cappellari2011a_Atlas3D_Paper1_Table3.txt' DELIMITER ',' CSV HEADER;

UPDATE atlas_sample SET atlas_name=REPLACE(atlas_name,' ','');
ALTER TABLE atlas_sample ADD COLUMN cube_id integer REFERENCES cube (cube_id);
UPDATE atlas_sample AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.atlas_name = c.atlas_name;

ALTER TABLE atlas_sample OWNER TO ifu_user;
ANALYZE atlas_sample;