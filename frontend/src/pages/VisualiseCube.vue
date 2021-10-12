<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-10 q-mt-md">
        <div v-if="cube" class="row">
          <div class="col-auto q-mr-lg">
            <Aladin :ra="cube.ra" :dec="cube.dec" />
          </div>
          <div class="col">
            <CubeInfoPanel :cube_id="cube_id" />
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import Aladin from 'src/components/Aladin.vue'
import CubeInfoPanel from 'src/components/CubeInfoPanel.vue'

export default defineComponent({
  components: { Aladin, CubeInfoPanel },
  name: 'VisualiseCube',
  props: ['cube_id'],
  setup(props) {
    const store = useStore()
    const cube = computed(() => store.getters.getObjectById(props.cube_id))

    if (cube.value == null) {
      store.dispatch('fetchObject', props.cube_id)
    }

    return { cube }
  },
})
</script>
