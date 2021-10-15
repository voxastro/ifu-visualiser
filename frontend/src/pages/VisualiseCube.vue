<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-10 q-mt-md">
        <div v-if="cube" class="row">
          <div class="col-12">
            <CubeInfoPanel :cube_id="cube_id" />
          </div>
          <div class="col-12 q-mt-md">
            <div class="row">
              <div class="col-auto q-mr-lg">
                <Aladin
                  :ra="cube.ra"
                  :dec="cube.dec"
                  :fov_arrays="fov_arrays"
                  :pointer="pointer"
                  @aladinOnClick="setPointerCoordinates"
                />
              </div>
              <div class="col full-width" style="min-width: 400px">
                <Spec />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, computed, watch, watchEffect } from 'vue'
import { useStore } from 'vuex'
import Aladin from 'src/components/Aladin.vue'
import CubeInfoPanel from 'src/components/CubeInfoPanel.vue'
import Spec from 'src/components/Spec.vue'

export default defineComponent({
  components: { Aladin, CubeInfoPanel, Spec },
  name: 'VisualiseCube',
  props: ['cube_id'],
  setup(props) {
    const store = useStore()
    const cube = computed(() => store.getters.getObjectById(props.cube_id))
    const fov_arrays = computed(() => {
      const cub = store.getters.getObjectById(props.cube_id)
      const ffov = [...cub.fov_fits, cub.fov_fits[0]]
      return cub.fov_ifu ? [ffov, cub.fov_ifu] : [ffov]
    })

    const pointer = computed(() => store.state.pointer)

    watchEffect(() => {
      // when cube will be loaded, setup pointer to the cube center
      if (cube.value) {
        store.commit('setPointer', { ra: cube.value.ra, dec: cube.value.dec })
      }
    })

    if (cube.value == null) {
      store.dispatch('fetchObject', props.cube_id)
    }

    const setPointerCoordinates = (obj) => {
      if (!obj.isDragging) {
        store.commit('setPointer', { ra: obj.ra, dec: obj.dec })
        // store.dispatch('fetchSpectrum')
      }
    }

    // add store watcher which used to
    store.watch(
      () => store.state.pointer,
      (pointer) => {
        store.dispatch('fetchSpectrum')
      }
    )

    store.commit('setCurrentCube', props.cube_id)

    return { cube, fov_arrays, pointer, setPointerCoordinates }
  },
})
</script>
