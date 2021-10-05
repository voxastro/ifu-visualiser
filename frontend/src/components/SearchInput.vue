<template>
  <q-form @submit="submitQuery">
    <q-input
      outlined
      autofocus
      standout
      type="search"
      v-bind="$attrs"
      v-model="queryString"
    >
      <template v-slot:append>
        <q-btn flat round @click="submitQuery"
          ><q-icon name="search" style="font-size: 24px"
        /></q-btn>
      </template>
    </q-input>
  </q-form>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

export default defineComponent({
  name: 'SearchInput',
  setup() {
    const store = useStore()
    const router = useRouter()
    const tableStatus = computed(() => store.state.tableStatus)

    const queryString = computed({
      get() {
        return store.state.queryString
      },
      set(value) {
        store.commit('setQueryString', value)
      },
    })

    const submitQuery = () => {
      if (tableStatus.value == 'loading') {
        console.log('Previous request is not finished yet!')
      } else {
        // Before requesting data, reset all messages
        store.commit('setTableMessage', '')
        store.commit('setTableStatus', null)
        store.commit('setSesameStatus', null)
        store.commit('setSesameMessage', '')
        // Now time for requesting data
        store.dispatch('fetchTable')
        // store.dispatch('makeQuery')

        router.push(
          {
            path: '/search',
            query: { q: queryString.value },
          },
          () => {}
        )
      }
    }

    return {
      queryString,
      submitQuery,
    }
  },
})
</script>
