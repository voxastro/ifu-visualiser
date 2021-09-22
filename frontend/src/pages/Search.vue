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
import SearchInput from 'components/SearchInput'
import SearchTableServer from 'components/SearchTableServer'

export default defineComponent({
  name: 'Search',
  components: { SearchInput, SearchTableServer },
})
</script>
