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

ALTER TABLE califa_object OWNER TO ifu_user;
ANALYZE califa_object;