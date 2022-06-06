<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-10 q-mt-md">
        <SearchInput class="q-mb-md q-mt-xl" input-style="font-size: 24px" />
        <SearchTableServer />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import SearchInput from 'components/SearchInput.vue'
import SearchTableServer from 'components/SearchTableServer.vue'

export default defineComponent({
  name: 'SearchPage',
  components: { SearchInput, SearchTableServer },
})
</script>
