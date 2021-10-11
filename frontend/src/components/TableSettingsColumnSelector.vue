<template>
  <div>
    <div class="row no-wrap q-pa-md">
      <div class="column">
        <div class="row">
          <div
            v-if="tableColumns && tableColumns.length > 0"
            class="text-h6 q-mb-md"
          >
            Columns to be displayed
          </div>
          <div class="q-ml-md">
            <q-btn
              color="white"
              text-color="black"
              icon="sync"
              no-caps
              dense
              label="Refresh table"
              @click="refetchTable"
            />
          </div>
        </div>
        <q-tree
          :nodes="tableColumns"
          node-key="key"
          label-key="label"
          children-key="children"
          v-model:ticked="tableColumnsTicked"
          tick-strategy="leaf"
          accordion
        >
          <template v-slot:default-header="prop">
            <div>
              <span class="text-weight-bold">{{ prop.node.label }} </span>
              <span class="text-weight-light q-ml-xs">{{
                prop.node.description
              }}</span>
            </div>
          </template>
        </q-tree>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, watch, ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { useQuery, useResult } from '@vue/apollo-composable'
import gql from 'graphql-tag'

export default defineComponent({
  name: 'TableSettingsColumnSelector',
  setup() {
    const store = useStore()

    const schema = computed(() => store.state.schema)
    if (schema.value == null) {
      store.dispatch('loadSchema')
    }

    const tableColumns = computed(() => store.state.tableColumnsObject)

    const tableColumnsTicked = computed({
      get() {
        return store.state.tableColumnsTicked
      },
      set(value) {
        store.commit('setTableColumnsTicked', value)
      },
    })

    const refetchTable = (target) => {
      store.dispatch('fetchTable')
    }

    return { schema, tableColumns, tableColumnsTicked, refetchTable }
  },
})
</script>
