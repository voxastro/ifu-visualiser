<template>
  <q-page>
    <div class="header">
      <div class="row justify-center items-center" style="height: 600px">
        <div class="col-7">
          <div class="row justify-center items-center">
            <img
              alt="IFU visualiser logo"
              src="~assets/logos/logo_IFU.svg"
              style="width: 80px; height: 80px"
              class="q-mr-lg"
            />
            <h2 class="voxastro-font-label text-center">IFU Visualiser</h2>
          </div>
          <div class="text-h4 text-weight-light text-center">
            A tool for visualization and exploration of spectroscopy IFU data
            from the MaNGA, SAMI, Califa, and Atlas3D galaxy surveys
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'LandingPage',
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
