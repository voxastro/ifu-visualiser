-- This script to upload tables to the DB.

-- First login under db_user
-- psql -p db_port -U db_user db_name
-------------------------------------------------------------------------------
-- Load table
\i upload_atlas.sql
\i upload_califa.sql
\i upload_sami.sql
\i upload_manga.sql


-- Create the main Cube table

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
    fov_fits        real[][],
    fov_ifu         real[][]
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

ALTER TABLE cube ADD COLUMN sami_inputcat_filler bigint REFERENCES sami_inputcat_filler(catid);
UPDATE cube AS c SET sami_inputcat_filler=t.catid FROM sami_inputcat_filler AS t WHERE c.sami_catid = t.catid;

ALTER TABLE cube ADD COLUMN sami_densitycat bigint REFERENCES sami_densitycat(catid);
UPDATE cube AS c SET sami_densitycat=t.catid FROM sami_densitycat AS t WHERE c.sami_catid = t.catid;

-- ALTER TABLE cube ADD COLUMN sami_starcat_clust bigint REFERENCES sami_starcat_clust(catid);
-- UPDATE cube AS c SET sami_starcat_clust=t.catid FROM sami_starcat_clust AS t WHERE c.sami_catid = t.catid;

ALTER TABLE cube ADD COLUMN sami_inputcat_clusters bigint REFERENCES sami_inputcat_clusters(catid);
UPDATE cube AS c SET sami_inputcat_clusters=t.catid FROM sami_inputcat_clusters AS t WHERE c.sami_catid = t.catid;

-------------------------------------------------------------------------------
-- First create many-to-many table
DROP TABLE IF EXISTS cube_sami_mgephotom_unreg CASCADE;
CREATE TABLE cube_sami_mgephotom_unreg (
  sami_mgephotom_unreg_id integer NOT NULL,
  cube_id integer NOT NULL,
  PRIMARY KEY (sami_mgephotom_unreg_id, cube_id),
  FOREIGN KEY (sami_mgephotom_unreg_id) REFERENCES sami_mgephotom_unreg(ind),
  FOREIGN KEY (cube_id) REFERENCES cube(cube_id)
);

INSERT INTO cube_sami_mgephotom_unreg
SELECT s.ind, c.cube_id
FROM
    sami_mgephotom_unreg AS s, cube AS c
WHERE
    s.catid = c.sami_catid;

ANALYZE cube_sami_mgephotom_unreg;
-------------------------------------------------------------------------------

ALTER TABLE sami_gaskin ADD COLUMN cube integer REFERENCES cube(cube_id);
UPDATE sami_gaskin AS t SET cube=c.cube_id FROM cube AS c WHERE c.sami_cubeidpub = t.cubeidpub;


ALTER TABLE cube ADD COLUMN manga_drp varchar(11) REFERENCES manga_drp(plateifu);
UPDATE cube AS c SET manga_drp=t.plateifu FROM manga_drp AS t WHERE c.manga_plateifu = t.plateifu;

ALTER TABLE cube OWNER TO ifu_user;

CREATE INDEX ON cube (q3c_ang2ipix(ra, dec));

CLUSTER cube_q3c_ang2ipix_idx ON cube;

ANALYZE cube;