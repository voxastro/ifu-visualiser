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

DROP TABLE IF EXISTS sami_inputcat_filler CASCADE;

CREATE TABLE sami_inputcat_filler (
    ind             integer,
    catid           bigint PRIMARY KEY,
    ra_obj          real,
    dec_obj         real,
    z_spec          real,
    fillflag        integer
);

\copy sami_inputcat_filler FROM '../sami/sami_dr3.InputCatFiller.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE sami_inputcat_filler DROP COLUMN ind;


ANALYZE sami_inputcat_filler;

-------------------------------------------------------------------------------

DROP TABLE IF EXISTS sami_densitycat CASCADE;

CREATE TABLE sami_densitycat (
    ind                          integer,
    catid                        bigint PRIMARY KEY,
    surfacedensity               real,
    surfacedensity_err           real,
    completenesscorrection       real,
    areacorrection               real,
    surfacedensityflag           integer,
    surfacedensity_m19           real,
    surfacedensity_err_m19       real,
    completenesscorrection_m19   real,
    areacorrection_m19           real,
    surfacedensityflag_m19       integer
);

\copy sami_densitycat FROM '../sami/sami_dr3.DensityCatDR3.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE sami_densitycat DROP COLUMN ind;
UPDATE sami_densitycat SET surfacedensity=NULL WHERE surfacedensity='NaN';
UPDATE sami_densitycat SET surfacedensity_err=NULL WHERE surfacedensity_err='NaN';
UPDATE sami_densitycat SET completenesscorrection=NULL WHERE completenesscorrection='NaN';
UPDATE sami_densitycat SET areacorrection=NULL WHERE areacorrection='NaN';
UPDATE sami_densitycat SET surfacedensity_m19=NULL WHERE surfacedensity_m19='NaN';
UPDATE sami_densitycat SET surfacedensity_err_m19=NULL WHERE surfacedensity_err_m19='NaN';

ANALYZE sami_densitycat;


DROP TABLE IF EXISTS sami_inputcat_clusters CASCADE;

CREATE TABLE sami_inputcat_clusters (
    ind             integer,
    catid           bigint PRIMARY KEY,
    ra_obj          real,
    dec_obj         real,
    r_petro         real,
    r_auto          real,
    z_spec          real,
    m_r             real,
    r_e             real,
    mu_within_1re   real,
    mu_1re          real,
    mu_2re          real,
    ellip           real,
    pa              real,
    g_i             real,
    mstar           real,
    r_on_rtwo       real,
    v_on_sigma      real,
    is_mem          boolean,
    surv_sami       integer,
    bad_class       integer
);

\copy sami_inputcat_clusters FROM '../sami/sami_dr3.InputCatClustersDR3.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE sami_inputcat_clusters DROP COLUMN ind;
UPDATE sami_inputcat_clusters SET r_e=NULL WHERE r_e='NaN';
UPDATE sami_inputcat_clusters SET mu_within_1re=NULL WHERE mu_within_1re='NaN';
UPDATE sami_inputcat_clusters SET mu_1re=NULL WHERE mu_1re='NaN';
UPDATE sami_inputcat_clusters SET mu_2re=NULL WHERE mu_2re='NaN';
UPDATE sami_inputcat_clusters SET ellip=NULL WHERE ellip='NaN';
UPDATE sami_inputcat_clusters SET pa=NULL WHERE pa='NaN';

ANALYZE sami_inputcat_clusters;

-------------------------------------------------------------------------------

DROP TABLE IF EXISTS sami_mgephotom_unreg CASCADE;

CREATE TABLE sami_mgephotom_unreg (
    ind             integer PRIMARY KEY,
    catid           bigint,
    photometry      varchar(8),
    remge           real,
    mmge            real,
    rextinction     real,
    pamge           real,
    epsmge_re       real,
    epsmge_lw       real,
    dist2nneigh     real,
    chi2            real
);

\copy sami_mgephotom_unreg FROM '../sami/sami_dr3.MGEPhotomUnregDR3.csv' DELIMITER ',' CSV HEADER;
-- ALTER TABLE sami_mgephotom_unreg DROP COLUMN ind;
UPDATE sami_mgephotom_unreg SET remge=NULL WHERE remge='NaN';
UPDATE sami_mgephotom_unreg SET mmge=NULL WHERE mmge='NaN';
UPDATE sami_mgephotom_unreg SET pamge=NULL WHERE pamge='NaN';
UPDATE sami_mgephotom_unreg SET epsmge_re=NULL WHERE epsmge_re='NaN';
UPDATE sami_mgephotom_unreg SET epsmge_lw=NULL WHERE epsmge_lw='NaN';
UPDATE sami_mgephotom_unreg SET chi2=NULL WHERE chi2='NaN';

ANALYZE sami_mgephotom_unreg;

-------------------------------------------------------------------------------

DROP TABLE IF EXISTS sami_gaskin CASCADE;

CREATE TABLE sami_gaskin (
     ind                integer,
     cubeid             varchar(80),
     cubeidpub          varchar(15) PRIMARY KEY,
     cubename           varchar(80),
     catid              bigint,
     pa_gaskin          real,
     pa_gaskin_err      real
    );

\copy sami_gaskin FROM '../sami/sami_dr3.samiDR3gaskinPA.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE sami_gaskin DROP COLUMN ind;
UPDATE sami_gaskin SET pa_gaskin=NULL WHERE pa_gaskin='NaN';
UPDATE sami_gaskin SET pa_gaskin_err=NULL WHERE pa_gaskin_err='NaN';

ANALYZE sami_gaskin;
