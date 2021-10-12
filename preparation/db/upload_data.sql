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
ANALYZE sami_cube_obs;

-------------------------------------------------------------------------------
DROP TABLE IF EXISTS sami_inputcat_gama CASCADE;

CREATE TABLE sami_inputcat_gama (
    ind             integer,
    catid           bigint PRIMARY KEY,
    ra_obj          real,
    dec_obj         real,
    ra_ifu          real,
    dec_ifu         real,
    r_petro         real,
    r_auto          real,
    z_tonry         real,
    z_spec          real,
    m_r             real,
    r_e             real,
    mu_within_1re   real,
    mu_1re          real,
    mu_2re          real,
    ellip           real,
    pa              real,
    mstar           real,
    g_i             real,
    a_g             real,
    surv_sami       integer,
    bad_class       integer
);

\copy sami_inputcat_gama FROM '../sami/sami_dr3.InputCatGAMADR3.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE sami_inputcat_gama DROP COLUMN ind;
UPDATE sami_inputcat_gama SET m_r=NULL WHERE m_r='NaN';
UPDATE sami_inputcat_gama SET r_e=NULL WHERE r_e='NaN';
UPDATE sami_inputcat_gama SET mu_within_1re=NULL WHERE mu_within_1re='NaN';
UPDATE sami_inputcat_gama SET mu_1re=NULL WHERE mu_1re='NaN';
UPDATE sami_inputcat_gama SET mu_2re=NULL WHERE mu_2re='NaN';
UPDATE sami_inputcat_gama SET ellip=NULL WHERE ellip='NaN';
UPDATE sami_inputcat_gama SET pa=NULL WHERE pa='NaN';

ANALYZE sami_inputcat_gama;



-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- Add MaNGA tables

DROP TABLE IF EXISTS manga_drp CASCADE;

CREATE TABLE manga_drp (
    plate           integer,
    ifudsgn         integer,
    plateifu        varchar(11) PRIMARY KEY,
    mangaid         varchar(11),
    versdrp2        varchar(6),
    versdrp3        varchar(6),
    verscore        varchar(6),
    versutil        varchar(7),
    versprim        varchar(4),
    platetyp        varchar(14),
    srvymode        varchar(12),
    objra           real,
    objdec          real,
    ifuglon         real,
    ifuglat         real,
    ifura           real,
    ifudec          real,
    ebvgal          real,
    nexp            integer,
    exptime         real,
    drp3qual        integer,
    bluesn2         real,
    redsn2          real,
    harname         varchar(35),
    frlplug         integer,
    cartid          varchar(30),
    designid        integer,
    cenra           real,
    cendec          real,
    airmsmin        real,
    airmsmed        real,
    airmsmax        real,
    seemin          real,
    seemed          real,
    seemax          real,
    transmin        real,
    transmed        real,
    transmax        real,
    mjdmin          bigint,
    mjdmed          bigint,
    mjdmax          bigint,
    gfwhm           real,
    rfwhm           real,
    ifwhm           real,
    zfwhm           real,
    mngtarg1        integer,
    mngtarg2        integer,
    mngtarg3        integer,
    catidnum        integer,
    plttarg         varchar(30),
    manga_tileid    integer,
    nsa_iauname     varchar(19),
    ifudesignsize   integer,
    ifutargetsize   integer,
    ifudesignwrongsize  integer,
    z               real,
    zmin            real,
    zmax            real,
    szmin           real,
    szmax           real,
    ezmin           real,
    ezmax           real,
    probs           real,
    pweight         real,
    psweight        real,
    psrweight       real,
    sweight         real,
    srweight        real,
    eweight         real,
    esweight        real,
    esrweight       real,
    nsa_field       integer,
    nsa_run         integer,
    nsa_camcol      integer,
    nsa_version     varchar(6),
    nsa_nsaid       integer,
    nsa_nsaid_v1b   integer,
    nsa_z           real,
    nsa_zdist       real,
    nsa_sersic_absmag_f     real,
    nsa_sersic_absmag_n     real,
    nsa_sersic_absmag_u     real,
    nsa_sersic_absmag_g     real,
    nsa_sersic_absmag_r     real,
    nsa_sersic_absmag_i     real,
    nsa_sersic_absmag_z     real,
    nsa_elpetro_absmag_f    real,
    nsa_elpetro_absmag_n    real,
    nsa_elpetro_absmag_u    real,
    nsa_elpetro_absmag_g    real,
    nsa_elpetro_absmag_r    real,
    nsa_elpetro_absmag_i    real,
    nsa_elpetro_absmag_z    real,
    nsa_elpetro_amivar_f    real,
    nsa_elpetro_amivar_n    real,
    nsa_elpetro_amivar_u    real,
    nsa_elpetro_amivar_g    real,
    nsa_elpetro_amivar_r    real,
    nsa_elpetro_amivar_i    real,
    nsa_elpetro_amivar_z    real,
    nsa_sersic_mass         real,
    nsa_elpetro_mass        real,
    nsa_elpetro_ba          real,
    nsa_elpetro_phi         real,
    nsa_extinction_f        real,
    nsa_extinction_n        real,
    nsa_extinction_u        real,
    nsa_extinction_g        real,
    nsa_extinction_r        real,
    nsa_extinction_i        real,
    nsa_extinction_z        real,
    nsa_elpetro_th50_r      real,
    nsa_petro_th50          real,
    nsa_petro_flux_f        real,
    nsa_petro_flux_n        real,
    nsa_petro_flux_u        real,
    nsa_petro_flux_g        real,
    nsa_petro_flux_r        real,
    nsa_petro_flux_i        real,
    nsa_petro_flux_z        real,
    nsa_petro_flux_ivar_f   real,
    nsa_petro_flux_ivar_n   real,
    nsa_petro_flux_ivar_u   real,
    nsa_petro_flux_ivar_g   real,
    nsa_petro_flux_ivar_r   real,
    nsa_petro_flux_ivar_i   real,
    nsa_petro_flux_ivar_z   real,
    nsa_elpetro_flux_f      real,
    nsa_elpetro_flux_n      real,
    nsa_elpetro_flux_u      real,
    nsa_elpetro_flux_g      real,
    nsa_elpetro_flux_r      real,
    nsa_elpetro_flux_i      real,
    nsa_elpetro_flux_z      real,
    nsa_elpetro_flux_ivar_f real,
    nsa_elpetro_flux_ivar_n real,
    nsa_elpetro_flux_ivar_u real,
    nsa_elpetro_flux_ivar_g real,
    nsa_elpetro_flux_ivar_r real,
    nsa_elpetro_flux_ivar_i real,
    nsa_elpetro_flux_ivar_z real,
    nsa_sersic_ba           real,
    nsa_sersic_n            real,
    nsa_sersic_phi          real,
    nsa_sersic_th50         real,
    nsa_sersic_flux_f       real,
    nsa_sersic_flux_n       real,
    nsa_sersic_flux_u       real,
    nsa_sersic_flux_g       real,
    nsa_sersic_flux_r       real,
    nsa_sersic_flux_i       real,
    nsa_sersic_flux_z       real,
    nsa_sersic_flux_ivar_f  real,
    nsa_sersic_flux_ivar_n  real,
    nsa_sersic_flux_ivar_u  real,
    nsa_sersic_flux_ivar_g  real,
    nsa_sersic_flux_ivar_r  real,
    nsa_sersic_flux_ivar_i  real,
    nsa_sersic_flux_ivar_z  real
);
\copy manga_drp FROM '../manga/drpall-v2_4_3.csv' DELIMITER ',' CSV HEADER;
-- ALTER TABLE manga_drp DROP COLUMN ind;

ANALYZE manga_drp;



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
    manga_id        varchar(11),
    manga_plateifu  varchar(11),
    sami_catid      bigint,
    sami_cubeidpub  varchar(32),
    califa_id       integer,
    califa_name     varchar(32),
    califa_cube     varchar(32),
    atlas_name      varchar(32),
    fov_fits        real[][]
);

\copy cube FROM 'table_cubes.csv' DELIMITER ',' CSV HEADER;

UPDATE cube SET atlas_name=REPLACE(atlas_name,' ','');
UPDATE cube SET exptime=NULL WHERE exptime='NaN';

-- add reference columns
ALTER TABLE cube ADD COLUMN atlas_param varchar(32) REFERENCES atlas_param(atlas_name);
UPDATE cube AS c SET atlas_param=t.atlas_name FROM atlas_param AS t WHERE c.atlas_name = t.atlas_name;

ALTER TABLE cube ADD COLUMN atlas_morphkin varchar(32) REFERENCES atlas_morphkin(atlas_name);
UPDATE cube AS c SET atlas_morphkin=t.atlas_name FROM atlas_param AS t WHERE c.atlas_name = t.atlas_name;

ALTER TABLE cube ADD COLUMN califa_object integer REFERENCES califa_object(califa_id);
UPDATE cube AS c SET califa_object=t.califa_id FROM califa_object AS t WHERE c.califa_id = t.califa_id;

ALTER TABLE cube ADD COLUMN sami_cube_obs varchar(14) REFERENCES sami_cube_obs(cubeidpub);
UPDATE cube AS c SET sami_cube_obs=t.cubeidpub FROM sami_cube_obs AS t WHERE c.sami_cubeidpub = t.cubeidpub;

ALTER TABLE cube ADD COLUMN sami_inputcat_gama bigint REFERENCES sami_inputcat_gama(catid);
UPDATE cube AS c SET sami_inputcat_gama=t.catid FROM sami_inputcat_gama AS t WHERE c.sami_catid = t.catid;

ALTER TABLE cube ADD COLUMN manga_drp varchar(11) REFERENCES manga_drp(plateifu);
UPDATE cube AS c SET manga_drp=t.plateifu FROM manga_drp AS t WHERE c.manga_plateifu = t.plateifu;

ALTER TABLE cube OWNER TO ifu_user;

CREATE INDEX ON cube (q3c_ang2ipix(ra, dec));

CLUSTER cube_q3c_ang2ipix_idx ON cube;

ANALYZE cube;