// export function someGetter (/* state */) {
// }

export function getObjectById(state) {
  return (cube_id) => {
    console.log('Hi from getter', cube_id)
    return state.cubeset.filter((obj) => obj.cube_id == cube_id)
  }
}
