<template>
  <q-table
    :rows="tableDataResults"
    :rows-per-page-options="[10, 20, 30, 50, 70, 100, 200, 300, 400, 500]"
    v-model:pagination="tablePagination"
    :loading="tableStatus === 'loading'"
    @request="onRequest"
    dense
    binary-state-sort
    class="q-mb-xl"
  >
    <template v-slot:top>
      <div class="row fit justify-start">
        <q-list>
          <q-expansion-item
            expand-separator
            icon="settings"
            label="Table settings"
            dense
            popup
          >
            <TableSettingsColumnSelector />
          </q-expansion-item>
        </q-list>

        <q-tree
          :nodes="streamNodes"
          node-key="msg"
          label-key="msg"
          class="q-ml-lg"
        >
          <template v-slot:default-header="prop">
            <div class="row items-center">
              <q-icon
                :name="prop.node.icon"
                :color="prop.node.color"
                class="q-mr-sm"
              />
              {{ prop.node.msg }}
            </div>
          </template>
        </q-tree>
      </div>
    </template>
    <template v-slot:body-cell-cube_id="props">
      <q-td :props="props">
        <router-link :to="{ name: 'cube', params: { cube_id: props.value } }">{{
          props.value
        }}</router-link>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import TableSettingsColumnSelector from 'components/TableSettingsColumnSelector'

export default defineComponent({
  components: { TableSettingsColumnSelector },
  setup() {
    const store = useStore()

    const tableStatus = computed(() => store.state.tableStatus)
    const tableMessage = computed(() => store.state.tableMessage)
    const sesameStatus = computed(() => store.state.sesameStatus)
    const sesameMessage = computed(() => store.state.sesameMessage)
    const tableDataResults = computed(() => store.state.tableData.results)

    const tablePagination = computed({
      get() {
        return store.state.tablePagination
      },
      set(value) {
        store.commit('setTablePagination', value)
      },
    })

    onMounted(() => {
      if (tableStatus.value === null) {
        store.dispatch('fetchTable')
      }
    })

    const submitQuery = () => {
      store.dispatch('fetchTable')
    }

    const onRequest = (props) => {
      store.commit('setTablePagination', props.pagination)
      store.dispatch('fetchTable')
    }

    // convert stream to nodes
    const stream = computed(() => store.state.activityStream)

    const streamNodes = computed(() => {
      // const stream = store.state.activityStream
      const nodes = store.state.activityStream.map((item) => {
        const d = new Date(item.date)

        let meta
        if (item.status == 'error') {
          meta = { icon: 'error', color: 'negative' }
        } else if (item.status == 'unresolved') {
          meta = { icon: 'warning', color: 'warning' }
        } else if (item.status == 'loaded' || item.status == 'resolved') {
          meta = { icon: 'info', color: 'positive' }
        } else if (item.status == 'loading' || item.status == 'resolving') {
          meta = { icon: 'loop', color: 'grey-7' }
        }

        return {
          msg: `${d.toISOString().replace('T', ' ').replace('Z', '')} - ${
            item.msg
          }`,
          ...meta,
        }
      })

      const sn =
        nodes.length > 0
          ? [
              {
                ...nodes[0],
                msg: nodes[0].msg.split(' - ')[1],
                children: nodes.slice(1),
              },
            ]
          : []
      return sn
    })

    return {
      tableStatus,
      tableMessage,
      sesameStatus,
      sesameMessage,
      tableDataResults,
      tablePagination,
      stream,
      streamNodes,
      onRequest,
    }
  },
})
</script>
