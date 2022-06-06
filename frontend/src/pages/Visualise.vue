<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-10 q-mt-md">
        <div class="text-h3 text-weight-light">Visualiser</div>
        <p class="text-body1 q-mt-xl">
          Unfortunately, there is currently only one way to select a cube to
          preview - using the
          <router-link to="/search">Search page</router-link>
          Please, go there to select interesting cube.
        </p>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'VisualiserPage',
})
</script>
