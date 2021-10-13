<template>
  <q-no-ssr>
    <div ref="plotly"></div>
  </q-no-ssr>
</template>

<script>
export default {
  name: 'Plotly',
  props: ['traces', 'layout', 'config'],
  data: function () {
    return {
      plt: null,
    }
  },
  computed: {
    plotlyPars: function () {
      return [this.traces, this.layout, this.config]
    },
  },
  watch: {
    plotlyPars: function (val) {
      if (this.plt !== null) {
        this.plt.newPlot(this.$refs.plotly, val[0], val[1], val[2])
      }
    },
  },
  mounted() {
    import('plotly.js-cartesian-dist-min').then((Plotly) => {
      this.plt = Plotly
      this.plt.newPlot(this.$refs.plotly, this.traces, this.layout, this.config)
    })
  },
}
</script>
