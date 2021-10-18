export function objectFlatten(obj) {
  let entries = []
  Object.entries(obj).forEach((key, value) => {})
  return Object.fromEntries([])
}

export const omitColumnsColumnSettings = ['spectrum', 'fov_fits', 'fov_ifu']

export const messages = {
  serverProblem:
    'Something went wrong on the server side! Please contact admin@voxastro.org.',
}
