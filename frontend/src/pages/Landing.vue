<template>
  <q-page>
    <div class="header">
      <div class="row justify-center items-center" style="height: 600px">
        <div class="col-7">
          <h2 class="voxastro-font-label text-center">IFU Visualiser</h2>
          <div class="text-h4 text-weight-light text-center">
            A tool for visualization and exploration of spectroscopy IFU data
            from the MaNGA, SAMI, Califa, and Atlas3D galaxy surveys.
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Landing',
})
</script>

<style lang="scss">
.header {
  position: relative;
  top: -50px;
  background: linear-gradient(45deg, #808588, #2c3e50);
  background-position: center 0;
  background-repeat: no-repeat;
  background-size: cover;
  color: #fff;
}
</style>
