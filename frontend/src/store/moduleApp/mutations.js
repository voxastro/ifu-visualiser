import { Notify } from 'quasar'

export function setQueryString(state, value) {
  state.queryString = value
}

export function setSesameStatus(state, value) {
  state.sesameStatus = value
}

export function setSesameMessage(state, value) {
  state.sesameMessage = value
}

export function setTableStatus(state, value) {
  state.tableStatus = value
}

export function setTableMessage(state, value) {
  state.tableMessage = value
}

export function setTableData(state, value) {
  state.tableData = value
}

export function setTablePagination(state, paginationObject) {
  state.tablePagination = paginationObject
}

export function addRowStream(state, { msg, status }) {
  let meta

  if ((status == 'loading') | (status == 'resolving')) {
    meta = { type: 'info', color: 'grey-7' }
  } else if ((status == 'loaded') | (status == 'resolved')) {
    meta = { type: 'positive' }
  } else if (status == 'unresolved') {
    meta = { type: 'warning' }
  } else if (status == 'error') {
    meta = { type: 'negative' }
  }

  // if (status == 'unresolved' || status == 'error') {
  //   Notify.create({
  //     message: msg,
  //     position: 'top-right',
  //     ...meta,
  //   })
  // }

  state.activityStream = [
    { date: Date.now(), msg: msg, status: status },
    ...state.activityStream,
  ]
}

export function resetActivityStream(state) {
  state.activityStream = []
}

export function setSchema(state, schema) {
  state.schema = schema
}

export function setTableList(state, tableList) {
  state.tableList = tableList
}

export function setTableColumnsObject(state, columnsObject) {
  state.tableColumnsObject = columnsObject
}

export function setTableColumnsTicked(state, ticked) {
  state.tableColumnsTicked = ticked
}

export function addObjectCubeSet(state, object) {
  state.cubeset = [...state.cubeset, object]
}

export function setPointer(state, pointer) {
  state.pointer = pointer
}

export function setSelectedSpectrum(state, data) {
  state.selectedSpectrum = data
}

export function setCurrentCube(state, cube_id) {
  state.currentCube = cube_id
}
