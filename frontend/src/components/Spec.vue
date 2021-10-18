<template>
  <div class="relative-position">
    <q-banner
      v-if="selectedSpectrum.status == 'warning'"
      class="text-black bg-warning"
    >
      {{ selectedSpectrum.message }}
    </q-banner>
    <q-banner
      v-if="selectedSpectrum.status == 'error'"
      class="text-white bg-negative"
    >
      {{ selectedSpectrum.message }}
    </q-banner>
    <Plotly :traces="traces" :layout="layout" :config="config" />

    <q-inner-loading :showing="selectedSpectrum.status == 'loading'">
      <q-spinner color="primary" size="3em" :thickness="2" />
    </q-inner-loading>
  </div>
</template>

<script>
import { defineComponent, ref, computed, watchEffect } from 'vue'
import { useStore } from 'vuex'
import Plotly from 'src/components/Plotly.vue'

export default defineComponent({
  name: 'Spec',
  components: { Plotly },
  setup() {
    const store = useStore()
    const traces = ref([])
    const layout = ref(null)
    const config = ref(null)
    const selectedSpectrum = computed(() => store.state.selectedSpectrum)

    const plotSpectrum = (d) => {
      // const d = data.spectrum.data
      console.log('Start ploting spectrum.....', d)

      const yrange = d.spec[0]?.yrange
      d.spec.forEach((sp) => {
        traces.value = [
          ...traces.value,
          {
            x: sp.wave,
            y: sp.flux.map((v, i) => v - sp.error[i]),
            fill: 'none',
            line: { width: 0.3, color: 'grey' },
            hoverinfo: 'skip',
            showlegend: false,
          },
          {
            name: 'Error bar',
            x: sp.wave,
            y: sp.flux.map((v, i) => v + sp.error[i]),
            fill: 'tonexty',
            line: { width: 0.3, color: 'grey' },
            fillcolor: 'rgba(200, 200, 200, 0.5)',
            hoverinfo: 'skip',
          },
          {
            name: 'Flux',
            x: sp.wave,
            y: sp.flux,
            line: { width: 1, color: 'black' },
            hoverinfo: 'skip',
          },
        ]
      })

      //     // {
      //     //   // fake trace to make restframe
      //     //   name: 'Fake Restframed',
      //     //   x: d.wave.map((v) => v / (1.0 + d.V / 299792.45)),
      //     //   y: d.flux,
      //     //   type: 'lines',
      //     //   line: { color: 'black', width: 0.1 },
      //     //   name: 'Fake.',
      //     //   hoverinfo: 'none',
      //     //   showlegend: false,
      //     //   xaxis: 'x2',
      //     // },

      //   const shapes = d.masked.map((e, i) => ({
      //     type: 'rect',
      //     xref: 'x',
      //     yref: 'paper',
      //     layer: 'below',
      //     x0: e[0],
      //     y0: 0,
      //     x1: e[1],
      //     y1: 1,
      //     opacity: 0.5,
      //     fillcolor: 'rgb(255, 192, 203)',
      //     line: { width: 0 },
      //   }))

      layout.value = {
        showlegend: true,
        // legend: { x: 1, xanchor: 'right', y: 0.9 },
        legend: { orientation: 'h', x: 0, y: 1.13 },
        hovermode: 'closest',
        // shapes: shapes,
        autosize: true,
        xaxis: { title: 'Wavelength, A' },
        xaxis2: {
          title: 'Restframe Wavelength, A',
          overlaying: 'x',
          side: 'top',
        },
        // yaxis: { title: 'Flux', range: [...yrange] },
        yaxis: { title: 'Flux', range: null },
        margin: { l: 40, r: 0, b: 40, t: 40 },
      }

      config.value = { displaylogo: false, responsive: true }

      console.log('Finished ploting spectrum.....')
    }

    watchEffect(() => {
      if (selectedSpectrum.value.data) {
        plotSpectrum(selectedSpectrum.value.data)
      } else {
        traces.value = []
      }
    })

    return {
      selectedSpectrum,
      traces,
      layout,
      config,
    }
  },
})
</script>
