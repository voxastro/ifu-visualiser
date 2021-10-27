<template>
  <div v-if="tableColumnsSorted" class="q-pa-md q-gutter-sm">
    <div v-for="t in tableColumnsSorted" :key="t.label">
      <h2
        :id="t.label"
        :ref="t.label"
        :name="t.label"
        class="
          q-markdown--heading
          q-markdown--heading-h1
          q-markdown--heading--anchor-link
        "
      >
        <a
          :href="`/docs#${t.label}`"
          aria-hidden="true"
          class="q-markdown--link q-markdown--link-local"
          >{{ t.label }}</a
        >
      </h2>
      <p>{{ t.description }}</p>
      <table class="q-markdown--table">
        <thead>
          <tr>
            <th>Field</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="f in t.children" :key="`${t.label}.${f.label}`">
            <td>
              <b>{{ f.label }}</b>
            </td>
            <td>{{ f.description }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, defineComponent, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'DocsTablesInfo',
  setup() {
    const store = useStore()
    const schema = computed(() => store.state.schema)
    const tableColumns = computed(() => store.state.tableColumnsObject)
    // const tocData = ref([])
    // const toc = ref([])

    const tableColumnsSorted = [
      ...tableColumns.value.filter((e) => e.label == 'cube'),
      ...tableColumns.value.filter((e) => e.label != 'cube'),
    ]

    return { tableColumns, tableColumnsSorted }
  },
})
</script>
