export function getObjectById(state) {
  return (cube_id) => {
    return state.cubeset.filter((obj) => obj.cube_id == cube_id)[0]
  }
}
