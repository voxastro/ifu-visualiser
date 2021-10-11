<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-10 q-mt-md">
        <div class="text-h3 text-weight-light">Cube ID {{ cube_id }}</div>
        {{ objData }}
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'VisualiseCube',
  props: ['cube_id'],
  setup(props) {
    const store = useStore()
    const objData = computed(() => store.getters.getObjectById(props.cube_id))
    store.dispatch('fetchObject', props.cube_id)
    return { objData }
  },
})
</script>
