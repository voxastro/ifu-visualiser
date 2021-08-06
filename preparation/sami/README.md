## Extract SAMI DR3 data from https://datacentral.org.au/

First, inspect schema of the SAMI survey related tables https://datacentral.org.au/services/schema/#sami

Download `sami_dr3.CubeObs` (SAMI cube observations, quality and flagging catalogue) making query

```sql
SELECT * FROM sami_dr3.CubeObs
```

https://datacentral.org.au/services/query/ and save into csv file

`sami_dr3.CubeObs` contains calibration star cubes which we would like to ignore using `t['warnstar'] == 0`

`sami_prepare_urls_for_downloading_data.py` script generate commands to download all data products

Download all other related to SAMI DR3 survey tables

```sql
SELECT * FROM sami_dr3.IndexAperturesDR3
SELECT * FROM sami_dr3.samiDR3gaskinPA
SELECT * FROM sami_dr3.EmissionLine1compDR3
SELECT * FROM sami_dr3.SSPAperturesDR3
SELECT * FROM sami_dr3.samiDR3Stelkin
SELECT * FROM sami_dr3.MGEPhotomUnregDR3
SELECT * FROM sami_dr3.InputCatGAMADR3
SELECT * FROM sami_dr3.FstarCatClusters
SELECT * FROM sami_dr3.VisualMorphologyDR3
SELECT * FROM sami_dr3.DensityCatDR3
SELECT * FROM sami_dr3.InputCatClustersDR3
SELECT * FROM sami_dr3.InputCatFiller
```

Descriptions of tables and columns can be found on [Schema Browser page](https://datacentral.org.au/services/schema/#sami).
