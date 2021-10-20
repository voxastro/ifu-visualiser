About
===

# The Team

<q-item tag="a" href="https://www.linkedin.com/in/igorchilingarian">
            <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_IC.jpg" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">Igor Chilingarian</q-item-label>
              <q-item-label class="text-subtitle1"
                >Harvard-Smithsonian Center for Astrophysics / SAI
                MSU</q-item-label
              >
              <q-item-label class="text-subtitle2">Researcher</q-item-label>
            </q-item-section>
          </q-item>

TBW
# Query Language

## Basic syntax

On the [Search page](search/) it is possible to select spectral cubes using simple query language expression which mimics syntax of `WHERE` clause in SQL language. The language consists of arbitrary number of expressions combined together using `AND` or `OR` clauses. Expression usually has the following structure (square brackets mean optional clauses):

```
parameter operator value [AND | OR [NOT] expression] [, …]
```

Parameter is the name of any column in the database or simple arithmetical operation between two properties (`+ - * /` are supported). Full list of tables and columns see [here](#available-tables).


Operator can be any comparison operator from SQL-like languages:


- `=` tests equality
- `!=` tests non-equality
- `>` greater than (does not work for string parameters)
- `<` less than (does not work for string parameters)
- `>=` greater or equal than (does not work for string parameters)
- `<=` less or equal than (does not work for string parameters)

The following operators are also available:

- `~` non-strict equality (works for string and number parameters)
- `IN` checks whether the parameter is in the list
- `BETWEEN` select values from the range.

::: tip
Operators `AND, OR, IN, BETWEEN` are case insensitive.
:::

## Cone queries

Thanks to [q3c](https://github.com/segasai/q3c) PostgreSQL extension in the IFU visualiser you can perform Cone Search queries. The syntax is quite simple:
```
cone(RA, DEC, RADIUS)
```
where values of `RA, DEC, RADIUS` should be in degrees. Examples of Cone queries are shown in the [Query Example section](#cone-search-queries).


In addition to coordinate Cone queries, user can enter any astronomical object name or coordinate statement in the search query input form. Such query will be resolved through the [CDS Sesame Resolver service](https://cds.u-strasbg.fr/cgi-bin/Sesame). In case of successfully name/coordinates resolving the input string will be replaced by Cone statement with a standard radius of 0.015 degrees.

:::
For example, 

[`NGC 6173`](search?q=NGC+6173)

will be converted to

[`cone(247.437155, 40.811611, 0.015)`](search?q=cone(247.437155,+40.811611,+0.015))
:::



## Query examples

### Basic queries

:::
**Select SAMI survey cubes**

[`survey=sami`](search?q=survey=sami)
:::

:::
**Cube with given `cube_id` value**

[`cube_id=1234`](search?q=cube_id=1234)
:::

:::
**Cubes from all surveys except MaNGA**

Dispite of `String` type of `survey` column the quotas can be skipped in the query.
Both
[`survey != manga`](search?q=survey!=manga)
and
[`survey != 'manga'`](search?q=survey!='manga')
are valid queries.
:::

:::
**Declination greater than 45 degrees**

[`dec > 45`](search?q=dec>45)
:::

:::
**Non-strict equality selection**

[`survey ~ ami`](search?q=survey~ami)
:::

:::
**Non-strict equality might be applied for numeric fields too** 🤦
[`ra ~ 10.23`](search?q=ra~10.2)
:::

:::
**`IN` operator is used to select multiple cubes**

[`cube_id in (13,1966,5694)`](<search?q=cube_id+in+(13,1966,5694)>)

[`survey in (califa, atlas3d)`](<search?q=survey+in+(califa,+atlas3d)>)
:::

:::
**Right Accention in the given range**

[`ra BETWEEN 10 and 15`](search?q=ra+BETWEEN+10+and+15)

:::

### Simple math expressions

:::
**List of galaxies with g-r color between 0.9 and 1.0**

[`manga_drp.nsa_elpetro_absmag_g - manga_drp.nsa_elpetro_absmag_r BETWEEN  0.9 AND 1.0`](search?q=manga_drp.nsa_elpetro_absmag_g+-+manga_drp.nsa_elpetro_absmag_r+between++0.9+and+1.0)
:::


### Complex queries

Here are presented more complex queries using columns from related tables and multiple operators.

:::
Using MaNGA DRP table to select galaxies with elpetro effective radius 3 times bigger than Sersic R<sub>eff</sub>. This criteria selects bright core elliptical galaxies. Extra condition filters out invalid values in the `manga_drp` table.

[`manga_drp.nsa_elpetro_th50_r / manga_drp.nsa_sersic_th50 > 3 and manga_drp.nsa_elpetro_th50_r != -9999`](search?q=manga_drp.nsa_elpetro_th50_r+/+manga_drp.nsa_sersic_th50+>+3+and+manga_drp.nsa_elpetro_th50_r+!=+-9999)
:::


:::

[`atlas_morphkin.eps > 0.5 AND atlas_param.logre > 1.3 OR cube_id = 111`](search?q=atlas_morphkin.eps+>+0.5+AND+atlas_param.logre+>+1.3+OR+cube_id+=+111)

Note that the logical `AND` has a higher priority than `OR`.
:::


:::
Parentheses can help to combine logical operator as needed.

Following strange query returns 61 rows
[`dec < -31 OR survey=sami AND atlas_name=4551`](search?q=dec+<+-31+OR+survey=sami+AND+atlas_name=4551)

While parentheses dramatically change the number of lines to zero
[`(dec < -31 OR survey=sami) AND atlas_name=4551`](search?q=(dec+<+-31+OR+survey=sami)+AND+atlas_name=4551)

:::



### Cone search queries


:::
Simple Cone query around Virgo Cluster

[`cone(187, 13, 3)`](search?q=cone(187,+13,+3))
:::

::: warning
Note that harmless `+` makes query invalid!

[`cone(187, +13, 3)`](search?q=cone(187,+%2B13,+3))

:::


:::
`-` works much better

[`cone(10, -9, 2)`](search?q=cone(10,+-9,+2))
:::


:::
Cone conditions can be combined.

[`cone(195, 28, 0.5) OR  cone(10, -9, 1)`](search?q=cone(195,+28,+0.5)+OR++cone(10,+-9,+1))
:::


:::
And used with other logical conditions.
 
[`cone(195, 28, 1) and manga_drp.nsa_elpetro_absmag_g - manga_drp.nsa_elpetro_absmag_r BETWEEN 0.1 and 0.5`](search?q=cone(195,+28,+1)+and+manga_drp.nsa_elpetro_absmag_g+-+manga_drp.nsa_elpetro_absmag_r+BETWEEN+0.1+and+0.5)


In this example, the blue galaxies in the Coma cluster are selected. Since the color columns are taken from the MaNGA DRP table, only MaNGA cubes are shown.
:::



# Available tables

**TBW**

# Sources of spectral data

**TBW**