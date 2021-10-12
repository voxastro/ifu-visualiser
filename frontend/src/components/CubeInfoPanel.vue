<template>
  <div>
    <div class="text-h4 text-weight-light">Cube ID {{ cube_id }}</div>
    <div>
      <q-card>
        <q-tabs
          v-model="tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="left"
          narrow-indicator
          :breakpoint="0"
        >
          <q-tab
            v-for="t in tableNamesCubeFirst"
            :name="t"
            :label="t"
            :key="t"
          />
          <!-- <q-tab name="mails" label="Mails" />
          <q-tab name="alarms" label="Alarms" />
          <q-tab name="movies" label="Movies" /> -->
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel v-for="t in tableNamesCubeFirst" :name="t" :key="t">
            <div class="text-h6">{{ t }}</div>
            {{ tableColumnsObject[t].description }}
            <q-list bordered class="q-mb-md full-height">
              <q-item
                v-for="(value, name) in tableColumnsObject[t].children"
                :key="name"
                class="inline-block"
              >
                <q-item-section>
                  <q-item-label caption>{{ name }}</q-item-label>
                  <q-item-label>{{ value }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed, ref } from 'vue'
import { useStore } from 'vuex'

import { objectFlatten } from 'src/utils.js'

export default defineComponent({
  name: 'CubeInfoPanel',
  props: ['cube_id'],
  setup(props) {
    const store = useStore()
    const cube = computed(() => store.getters.getObjectById(props.cube_id))

    if (cube.value == null) {
      store.dispatch('fetchObject', props.cube_id)
    }

    const tableColumnsList = computed(() => store.state.tableColumnsObject)
    const tableNames = tableColumnsList.value.map((e) => e.label)
    const tableColumnsObject = tableColumnsList.value.reduce(
      (a, v) => ({
        ...a,
        [v.label]: v,
      }),
      {}
    )
    const tableNamesCubeFirst = [
      'cube',
      ...tableNames.filter((e) => e != 'cube'),
    ]

    console.log(
      '---------------------------------=',
      tableColumnsObject,
      tableColumnsList.value
    )
    // const tableNames = Object.keys(columnsObject?.value)

    const tab = ref('cube')
    const cubeFlat = cube.value ? objectFlatten(cube.value) : null

    return { cube, cubeFlat, tab, tableNamesCubeFirst, tableColumnsObject }
  },
})
</script>
