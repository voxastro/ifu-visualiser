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

ALTER TABLE atlas_param OWNER TO ifu_user;
ANALYZE atlas_param;



-------------------------------------------------------------------------------
-- http://www-astro.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt

DROP TABLE IF EXISTS atlas_morphkin CASCADE;

CREATE TABLE atlas_morphkin (
    atlas_name      varchar(16) PRIMARY KEY,-- REFERENCES atlas_param (atlas_name),
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


ALTER TABLE atlas_morphkin OWNER TO ifu_user;
ANALYZE atlas_morphkin;
