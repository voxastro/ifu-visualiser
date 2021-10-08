-- This script to upload tables to the DB.

-- First login under db_user
-- psql -p db_port -U db_user db_name


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

-- ALTER TABLE atlas_param ADD COLUMN cube_id integer REFERENCES cube (cube_id);
-- UPDATE atlas_param AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.atlas_name = c.atlas_name;

ALTER TABLE atlas_param OWNER TO ifu_user;
ANALYZE atlas_param;




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

-- ALTER TABLE cube ADD CONSTRAINT cube_atlas_name_fkey FOREIGN KEY (atlas_name) REFERENCES atlas_morphkin(atlas_name);

-- ALTER TABLE atlas_morphkin ADD COLUMN cube_id integer REFERENCES cube (cube_id);
-- UPDATE atlas_morphkin AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.atlas_name = c.atlas_name;

ALTER TABLE atlas_morphkin OWNER TO ifu_user;
ANALYZE atlas_morphkin;




-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- Add CALIFA tables

DROP TABLE IF EXISTS califa_object CASCADE;

CREATE TABLE califa_object  (
    target_name	    varchar(23),
    califa_id	    integer PRIMARY KEY, 
    raj2000	        float(8),
    dej2000	        float(8),
    redshift        real,
    sdss_z          real,
    maj_axis        real,
    mstar           real,
    mstar_min       real,
    mstar_max       real,
    chi2            real,
    vmax_nocorr	    real,
    vmax_denscorr   real,
    magu            real,
    err_magu        real,
    u_ext           real,
    abs_u_min       real,
    abs_u_max       real,
    magg            real,
    err_magg        real,
    g_ext           real,
    abs_g_min       real,
    abs_g_max       real,
    magr            real,
    err_magr        real,
    r_ext           real,
    abs_r_min       real,
    abs_r_max       real,
    magi            real,
    err_magi        real,
    i_ext	        real,
    abs_i_min       real,
    abs_i_max       real,
    magz            real,
    err_magz        real,
    z_ext           real,
    abs_z_min       real,
    abs_z_max       real,
    hubtyp          varchar(16),
    minhubtyp       varchar(16),
    maxhubtyp       varchar(16),
    bar             varchar(16),
    flag_release_comb   boolean,
    flag_release_v1200  boolean,
    flag_release_v500   boolean,
    axis_ratio      real,
    position_angle  real,
    el_hlr          real,
    modmag_r        real
);


\copy califa_object FROM '../califa/califadr3.objects.csv' DELIMITER ',' CSV HEADER;

UPDATE califa_object SET target_name=REPLACE(target_name,' ','');


-- ALTER TABLE cube ADD CONSTRAINT cube_califa_object_fkey FOREIGN KEY (califa_id) REFERENCES califa_object(califa_id);

-- UPDATE califa_object AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.califaid = c.califa_id;
-- ALTER TABLE califa_object ADD COLUMN cube_id integer REFERENCES cube (cube_id);
-- UPDATE califa_object AS a SET cube_id=c.cube_id FROM cube AS c WHERE a.califaid = c.califa_id;

ALTER TABLE califa_object OWNER TO ifu_user;
ANALYZE califa_object;


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- Add SAMI tables

DROP TABLE IF EXISTS sami_cube_obs CASCADE;

CREATE TABLE sami_cube_obs  (
    ind             integer,
    cubeidpub       varchar(14)  PRIMARY KEY,
    cubeid          varchar(80),
    cubename        varchar(80),
    catid           bigint,
    cubefwhm        real,
    cubetexp        real,
    meantrans       real,
    isbest          boolean,
    catsource       integer,
    warnstar        integer,
    warnfill        integer,
    warnz           integer,
    warnmult        integer,
    warnakpc        integer,
    warnare         integer,
    warnamge        integer,
    warnsk2m        integer,
    warnsk4m        integer,
    warnsk4mhsn     integer,
    warnfcal        integer,
    warnfcbr        integer,
    warnskyb        integer,
    warnskyr        integer,
    warnsker        integer,
    warnwcs         integer,
    warnre          integer,
    warnskem        integer,
    warnemft        integer
);


\copy sami_cube_obs FROM '../sami/sami_dr3.CubeObs.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE sami_cube_obs DROP COLUMN ind;


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- Before (re)populate the table it has to be dropped
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
    sami_cubeidpub  varchar(32),
    califa_id       integer,
    califa_name     varchar(32),
    califa_cube     varchar(32),
    atlas_name      varchar(32)
);

\copy cube FROM 'table_cubes.csv' DELIMITER ',' CSV HEADER;

UPDATE cube SET atlas_name=REPLACE(atlas_name,' ','');

-- add reference columns
ALTER TABLE cube ADD COLUMN atlas_param varchar(32) REFERENCES atlas_param(atlas_name);
UPDATE cube AS c SET atlas_param=t.atlas_name FROM atlas_param AS t WHERE c.atlas_name = t.atlas_name;

ALTER TABLE cube ADD COLUMN atlas_morphkin varchar(32) REFERENCES atlas_morphkin(atlas_name);
UPDATE cube AS c SET atlas_morphkin=t.atlas_name FROM atlas_param AS t WHERE c.atlas_name = t.atlas_name;

ALTER TABLE cube ADD COLUMN califa_object integer REFERENCES califa_object(califa_id);
UPDATE cube AS c SET califa_object=t.califa_id FROM califa_object AS t WHERE c.califa_id = t.califa_id;

ALTER TABLE cube ADD COLUMN sami_cube_obs varchar(14) REFERENCES sami_cube_obs(cubeidpub);
UPDATE cube AS c SET sami_cube_obs=t.cubeidpub FROM sami_cube_obs AS t WHERE c.sami_cubeidpub = t.cubeidpub;

ALTER TABLE cube OWNER TO ifu_user;

CREATE INDEX ON cube (q3c_ang2ipix(ra, dec));

CLUSTER cube_q3c_ang2ipix_idx ON cube;

ANALYZE cube;