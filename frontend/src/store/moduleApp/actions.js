import axios from 'axios'
import { omitColumnsColumnSettings, messages } from 'src/utils.js'

export function resolveSesameQuery(ctx) {
  console.log('Query Resolving....', ctx.state.queryString)
  ctx.commit('setSesameStatus', 'resolving')
  ctx.commit(
    'setSesameMessage',
    'Trying to resolve query as an object name in Sesame CDS Service.'
  )
  ctx.commit('addRowStream', {
    msg: `Trying to resolve query "${ctx.state.queryString}" as an object name in Sesame CDS Service.`,
    status: 'resolving',
  })

  // dirty hack to avoid Sesame error
  const queryClean = ctx.state.queryString.replace('+', '%2b')
  const ucds = `https://cds.unistra.fr/cgi-bin/nph-sesame/-ox/SVN?${queryClean}`

  axios
    .get(ucds)
    .then((response) => response.data)
    .then((str) => new window.DOMParser().parseFromString(str, 'text/xml'))
    .then((data) => {
      const e_ra = data.getElementsByTagName('jradeg')[0]
      const e_de = data.getElementsByTagName('jdedeg')[0]

      if (e_ra !== undefined && e_de !== undefined) {
        const numRa = Number(e_ra.textContent)
        const numDec = Number(e_de.textContent)
        const coneQuery = `cone(${numRa}, ${numDec}, 0.015)`

        // informational output
        ctx.commit('setSesameStatus', 'resolved')
        ctx.commit(
          'setSesameMessage',
          `Sesame CDS Service successfully resolved ${queryClean} as coordinates: ${numRa}, ${numDec}.`
        )
        ctx.commit('addRowStream', {
          msg: `Sesame CDS Service successfully resolved ${queryClean} as coordinates: ${numRa}, ${numDec}.`,
          status: 'resolved',
        })
        ctx.commit('setQueryString', coneQuery)
        console.log('Sesame successfully resolved query')
        console.log(e_ra.textContent, e_de.textContent)
        console.log(coneQuery)
        // repeat data fetchiing with cone syntaxes
        ctx.dispatch('fetchTable')
      } else {
        console.log('Sesame cannot resolve name query!!!')
        ctx.commit('setSesameStatus', 'unresolved')
        ctx.commit(
          'setSesameMessage',
          `Sesame CDS Service cannot resolve ${queryClean} as object name. Try to re-write query.`
        )
        ctx.commit('addRowStream', {
          msg: `Sesame CDS Service cannot resolve ${queryClean} as object name. Try to re-write query.`,
          status: 'unresolved',
        })
      }
    })
    .catch((error) => {
      console.log('Some problem with request to the Sesame Service at CDS!')
      console.error(error)
      ctx.commit('setSesameStatus', 'error')
      ctx.commit(
        'setSesameMessage',
        'There was some problem with request to the Sesame CDS Name resolver!'
      )
      ctx.commit('addRowStream', {
        msg: 'There was some problem with request to the Sesame CDS Name resolver!',
        status: 'error',
      })
    })
}

export function fetchTable(ctx) {
  ctx.commit('setTableStatus', 'loading')
  ctx.commit('setTableMessage', 'Retrieving data from API...')
  ctx.commit('addRowStream', {
    msg: `Retrieving data from API with "${ctx.state.queryString}" query string.`,
    status: 'loading',
  })

  const queryClean = ctx.state.queryString.replace('+', '%2b')

  const p = ctx.state.tablePagination
  const tableColumnsTicked = ctx.state.tableColumnsTicked
  const tableColumnsTickedStr = tableColumnsTicked
    .map((e) => e.replace('cube.', ''))
    .join()

  const url = `${process.env.URL_API}/api/cubes/?omit=spectrum&expand=~all&fields=${tableColumnsTickedStr}&q=${queryClean}&page=${p.page}&page_size=${p.rowsPerPage}&sortby=${p.sortBy}&descending=${p.descending}`
  console.log('Requesting: ', url)
  axios
    .get(url)
    .then(({ data }) => {
      const results = data.results

      const results_upd = results.reduce((res, row) => {
        let duplicatedFields = []

        const entries = tableColumnsTicked.map((column) => {
          const [table, field] = column.split('.')
          const key = table == 'cube' ? field : column

          // check nested columns and its length
          const nElementsInColumn =
            table == 'cube' ? 1 : row[table] != null ? row[table].length : null

          // if there is long column save this information
          if (nElementsInColumn > 1) {
            duplicatedFields.push({
              key: key,
              field: field,
              nvals: nElementsInColumn,
              vals: row[table],
            })
          }
          console.log('row', row)
          console.log('table', table)
          console.log('key', key)
          console.log('row[table]', row[table])
          console.log(
            'row[table] == []:',
            row[table] == Array([]),
            row[table]?.length == 0
          )
          const value =
            table == 'cube'
              ? row[key]
              : row[table] == null
              ? null
              : nElementsInColumn >= 1
              ? row[table][0][field] // for nested fields as array many=True in serializer
              : row[table][field] // for nested fields where many=False

          return [key, value]
        })

        const objectRow = Object.fromEntries(entries)
        res.push(objectRow)

        // expand output results by duplicated values
        console.log('duplicatedFields-->', duplicatedFields)
        duplicatedFields.forEach((dupfld) => {
          // skip first row which is already in res
          dupfld.vals.slice(1).forEach((v) => {
            const newObjectRow = { ...objectRow, [dupfld.key]: v[dupfld.field] }
            res.push(newObjectRow)
          })
        })

        return res
      }, [])

      ctx.commit('setTableData', { ...data, results: results_upd })

      ctx.commit('setTablePagination', {
        ...ctx.state.tablePagination,
        rowsNumber: data.count,
      })

      ctx.commit('setTableStatus', 'loaded')
      ctx.commit('setTableMessage', `${data.count} cubes found`)
      ctx.commit('addRowStream', {
        msg: `${data.count} cubes found`,
        status: 'loaded',
      })
    })
    .catch((error) => {
      // If does not work, try resolve query as Sesame
      console.error(`Something went wrong ${error}`)
      ctx.commit('setTableStatus', 'error')
      ctx.commit(
        'setTableMessage',
        `Something went wrong while loading the data: ${error}`
      )
      ctx.commit('addRowStream', {
        msg: `Something went wrong while loading the data: ${error}`,
        status: 'error',
      })
      ctx.dispatch('resolveSesameQuery')
    })
}

function parseSchema(schema) {
  const d = schema.definitions
  const tableObj = d
    ? Object.keys(d).map((key) => {
        const prop = d[key].properties
        return {
          label: d[key].table_name,
          key: d[key].table_name,
          description: d[key].description,
          children: Object.keys(prop)
            .filter((p) => !omitColumnsColumnSettings.includes(p))
            .map((p) => {
              return {
                label: p,
                key: `${d[key].table_name}.${p}`,
                description: prop[p].description,
              }
            }),
        }
      })
    : null
  return tableObj
}

export function loadSchema(ctx) {
  const schemaURL = `${process.env.URL_API}/api/swagger.json`
  axios
    .get(schemaURL)
    .then(({ data }) => {
      ctx.commit('setSchema', data)

      const tableObj = parseSchema(data)
      ctx.commit('setTableColumnsObject', tableObj)
    })
    .catch((error) => {
      console.error(error)
    })
}

export function fetchObject(ctx, cube_id) {
  const url = `${process.env.URL_API}/api/cubes/${cube_id}/?omit=spectrum&expand=~all`
  console.log(`Requesting object: ${cube_id}: ${url}`)
  axios
    .get(url)
    .then(({ data }) => {
      ctx.commit('addObjectCubeSet', data)
    })
    .catch((error) => {
      console.error(error)
    })
}

export function fetchSpectrum(ctx) {
  const cube_id = ctx.state.currentCube
  const ra = ctx.state.pointer.ra
  const dec = ctx.state.pointer.dec

  ctx.commit('setSelectedSpectrum', {
    status: 'loading',
    message: '',
    data: null,
  })
  const url = `${process.env.URL_API}/api/cubes/${cube_id}/?fields=spectrum&ra=${ra}&dec=${dec}`
  console.log(`Requesting spec: ${cube_id}: ${url}`)
  axios
    .get(url)
    .then(({ data }) => {
      ctx.commit('setSelectedSpectrum', {
        status: data.spectrum.status,
        message: data.spectrum.message,
        data: data.spectrum,
      })
    })
    .catch((error) => {
      // unpredictable error, likely on server side
      console.error(error.toJSON())

      ctx.commit('setSelectedSpectrum', {
        status: 'error',
        message: messages.serverProblem,
        data: null,
      })
    })
}
