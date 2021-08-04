## Extract Califa DR3 data from project [site](https://califaserv.caha.es/CALIFA_WEB/public_html/?q=content/califa-3rd-data-release)

Simply recursevely wget all all spectral cubes

```
wget -r ftp://anonymous@ftp.caha.es/CALIFA/reduced/*
```

Associated tables can be found [here](https://califaserv.caha.es/CALIFA_WEB/public_html/?q=content/dr3-tables)

```
wget -r ftp://ftp.caha.es/CALIFA/docs/DR3/*
```

For additional dataproducts, please, inspect `ftp://ftp.caha.es/CALIFA/`
