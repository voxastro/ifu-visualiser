## Extract SAMI DR3 data from https://datacentral.org.au/

First, inspect schema of the SAMI survey related tables https://datacentral.org.au/services/schema/#sami

Download `sami_dr3.CubeObs` (SAMI cube observations, quality and flagging catalogue) making query

```sql
SELECT * FROM sami_dr3.CubeObs
```

https://datacentral.org.au/services/query/ and save into csv file

`sami_dr3.CubeObs` contains calibration star cubes which we would like to ignore using `t['warnstar'] == 0`

`sami_prepare_urls_for_downloading_data.py` script generate commands to download all data products
