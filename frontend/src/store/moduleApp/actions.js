import axios from 'axios'

export function someAction(/* context */) {}

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
  const url = `${process.env.URL_API}/api/cubes/?omit=spectrum&q=${queryClean}&page=${p.page}&page_size=${p.rowsPerPage}&sortby=${p.sortBy}&descending=${p.descending}`
  console.log('Requesting: ', url)
  axios
    .get(url)
    .then(({ data }) => {
      // First, expecting that query is param-search
      ctx.commit('setTableData', data)

      ctx.commit('setTablePagination', {
        ...ctx.state.tablePagination,
        rowsNumber: data.count,
      })
      // update columns table depending on type of query
      //   const cols = ctx.state.queryString.includes('cone')
      //     ? [...columns, columnDist]
      //     : columns
      //   ctx.commit('setTableColumns', cols)
      ctx.commit('setTableStatus', 'loaded')
      ctx.commit('setTableMessage', `${data.count} rows loaded`)
      ctx.commit('addRowStream', {
        msg: `${data.count} rows loaded.`,
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
