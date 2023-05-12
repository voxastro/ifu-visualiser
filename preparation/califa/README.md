## Extract Califa DR3 data from project [site](https://califaserv.caha.es/CALIFA_WEB/public_html/?q=content/califa-3rd-data-release)

### Cubes

Simply recursevely wget all all spectral cubes

```
wget -r ftp://anonymous@ftp.caha.es/CALIFA/reduced/*
```

### Data tables

#### TAP

To extract complementary table for DB use following command:

```bash
stilts tapquery tapurl='http://dc.zah.uni-heidelberg.de/tap' adql='SELECT * FROM califadr3.objects' out=califadr3.objects.csv ofmt=csv
```

#### Other

Associated tables can be found [here](https://califaserv.caha.es/CALIFA_WEB/public_html/?q=content/dr3-tables)

```
wget -r ftp://ftp.caha.es/CALIFA/docs/DR3/*
```

For additional dataproducts, please, inspect `ftp://ftp.caha.es/CALIFA/`


## eCALIFA (UPD 11/05/2023)

To download all cubes in the eCALIFA release just dump out the page `http://ifs.astroscu.unam.mx/CALIFA/V500/v2.3/reduced_masked/` to the `list_eCALIFAv2.3.txt`.