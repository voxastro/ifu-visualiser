<template>
  <!-- <div class="text-h4 text-weight-light">Cube ID {{ cube_id }}</div> -->
  <div class="q-mt-sm">
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
        <q-tab v-for="t in tableNamesCubeFirst" :name="t" :label="t" :key="t" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <!-- Main table with minor customizaitons -->
        <q-tab-panel name="cube">
          {{ tableColumnsObject['cube'].description }}

          <q-list dense style="max-height: 285px">
            <div
              v-for="col in tableColumnsObject['cube'].children"
              :key="col.key"
              class="inline-block q-px-sm"
            >
              <q-item-section v-if="col.label == 'ra'">
                <q-item-label caption>coordinates</q-item-label>
                <q-item-label>{{ cube.ra }} {{ cube.dec }} </q-item-label>
              </q-item-section>
              <q-item-section v-else-if="col.label !== 'dec'">
                <q-item-label caption>{{ col.label }}</q-item-label>
                <q-item-label>{{ replaceNull(cube[col.label]) }} </q-item-label>
              </q-item-section>
              <q-tooltip :delay="500" class="bg-grey-3 text-black">{{
                col.description
              }}</q-tooltip>
            </div>
          </q-list>
        </q-tab-panel>
        <q-tab-panel v-for="t in tableNamesCubeFirst" :name="t" :key="t">
          {{ tableColumnsObject[t].description }}
          <div v-if="Array.isArray(cube[t])">
            <q-list
              dense
              style="max-height: 285px"
              v-for="(tt, tt_idx) in cube[t]"
              :key="tt_idx"
            >
              <div
                v-for="col in tableColumnsObject[t].children"
                :key="col.label"
                class="inline-block q-px-sm"
              >
                <q-item-section>
                  <q-item-label caption>{{ col.label }}</q-item-label>
                  <q-item-label>{{ tt[col.label] }}</q-item-label>
                </q-item-section>
                <q-tooltip :delay="500" class="bg-grey-3 text-black">{{
                  col.description
                }}</q-tooltip>
              </div>
            </q-list>
          </div>
          <div v-else>
            <q-list dense style="max-height: 285px">
              <div
                v-for="col in tableColumnsObject[t].children"
                :key="col.label"
                class="inline-block q-px-sm"
              >
                <q-item-section>
                  <q-item-label caption>{{ col.label }}</q-item-label>
                  <q-item-label>{{ cube[t][col.label] }}</q-item-label>
                </q-item-section>
                <q-tooltip :delay="500" class="bg-grey-3 text-black">{{
                  col.description
                }}</q-tooltip>
              </div>
            </q-list>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </div>
</template>

<script>
import { defineComponent, computed, ref } from 'vue'
import { useStore } from 'vuex'

import { objectFlatten, omitColumnsColumnSettings } from 'src/utils.js'

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
      (a, v) => ({ ...a, [v.label]: v }),
      {}
    )

    // console.log('=============== DEBUUUUGGG ====================')
    // console.log(
    //   tableNames.map((e) => {
    //     console.log(
    //       e,
    //       e != 'cube' && cube.value[e],
    //       cube.value[e],
    //       Array.isArray(cube.value[e]),
    //       Array.isArray(cube.value[e]) && cube.value[e].length > 0
    //     )
    //     if (Array.isArray(cube.value[e]) && cube.value[e].length > 0) {
    //       console.log(cube.value[e], cube.value[e].length)
    //     }
    //   })
    // )

    const tableNamesCubeFirst = [
      'cube',
      ...tableNames.filter(
        (e) =>
          e != 'cube' &&
          (cube.value[e] ||
            (Array.isArray(cube.value[e]) && cube.value[e].length > 0))
      ),
    ]

    const replaceNull = (value) => {
      return value ? value : 'n/a'
    }

    const tab = ref('cube')
    const cubeFlat = cube.value ? objectFlatten(cube.value) : null

    return {
      cube,
      cubeFlat,
      tab,
      tableNamesCubeFirst,
      tableColumnsObject,
      replaceNull,
    }
  },
})
</script>
