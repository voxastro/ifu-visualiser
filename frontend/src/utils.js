export function objectFlatten(obj) {
  let entries = []
  Object.entries(obj).forEach((key, value) => {
    console.log('DEBUG IN objectFlatten', key, value, typeof value)
  })
  return Object.fromEntries([])
}
