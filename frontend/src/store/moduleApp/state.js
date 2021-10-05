export default function () {
  return {
    queryString: '',
    sesameStatus: null,
    sesameMessage: '',
    tableStatus: null,
    tableMessage: '',
    tableData: [],
    tablePagination: {
      sortBy: 'cube_id',
      descending: false,
      page: 1,
      rowsPerPage: 30,
      rowsNumber: 0,
    },
    schema: null,
    tableList: [],
    tableColumnsObject: [],
    tableColumnsTicked: [
      'cube.cube_id',
      'cube.ra',
      'cube.dec',
      'cube.survey',
      'cube.exptime',
    ],
    activityStream: [],
  }
}
