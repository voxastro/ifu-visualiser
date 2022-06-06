<template>
  <div ref="aladinDiv" style="width: 400px; height: 400px; margin-bottom: -1px">
    <div class="fit relative-position">
      <div class="absolute-center">
        <q-spinner color="primary" size="3em" />
      </div>
    </div>
  </div>

  <q-btn-toggle
    v-model="survey"
    no-caps
    unelevated
    spread
    class="toggle"
    toggle-color="grey-7"
    text-color="grey-7"
    color="white"
    size="md"
    padding="1px 0px 1px 0px"
    style="width: 400px"
    :options="[
      { label: 'SDSS', value: 'P/SDSS9/color' },
      { label: 'PanSTARRS', value: 'P/PanSTARRS/DR1/color/z/zg/g' },
      { label: 'DECaLS3', value: 'P/DECaLS/DR3/color' },
      { label: 'DSS2', value: 'P/DSS2/color' },
      { label: 'DES', value: 'DES_DR2_color' },
    ]"
  />
  <q-btn-toggle
    v-model="survey"
    no-caps
    unelevated
    spread
    class="toggle"
    toggle-color="grey-7"
    text-color="grey-7"
    color="white"
    size="md"
    padding="1px 0px 1px 0px"
    style="width: 400px"
    :options="[
      { label: 'GALEX', value: 'P/GALEXGR6/AIS/color' },
      { label: '2MASS', value: 'P/2MASS/color' },
      { label: 'WISE', value: 'P/allWISE/color' },
      { label: 'XMM', value: 'P/XMM/PN/color' },
      { label: 'unWISE', value: 'unWISE_color' },
      { label: 'ZTF', value: 'CDS_P_ZTF_DR7_color' },
    ]"
  />
</template>

<script>
// Based on this
// https://github.com/cds-astro/aladin-lite-vue-component/blob/master/src/components/Viewer.vue

import {
  defineComponent,
  watch,
  ref,
  computed,
  onMounted,
  watchEffect,
} from 'vue'

export default defineComponent({
  name: 'AladinComp',
  props: {
    ra: { default: 10.0 },
    dec: { default: 15.0 },
    fov: { default: 1 / 60.0 },
    fov_arrays: Array,
    pointer: Object,
  },
  emits: ['aladinOnClick'],
  setup(props, context) {
    const aladinDiv = ref(null)
    const survey = ref('P/SDSS9/color')
    const aladinObj = ref(null)
    const aladinCatalog = ref(null)
    const aladinASourceFunc = ref(null)
    const aladinSourceList = ref([])

    const loadScriptIntoDOM = (bodyElement, url, onloadCallback) => {
      const scriptElement = document.createElement('script')
      scriptElement.setAttribute('src', url)
      scriptElement.async = false
      if (onloadCallback) {
        scriptElement.onload = onloadCallback
      }
      bodyElement.appendChild(scriptElement)
    }

    // const setImageSurvey = (bla) => {
    //   console.log('DEBUUUUG++++++++++++++++++++++++++++++', bla)
    //   this.aladin.setImageSurvey(this.survey)
    // }

    onMounted(() => {
      // Now the component is mounted we can load aladin lite.
      const bodyElement = document.getElementsByTagName('BODY')[0]

      // jQuery is a dependency for aladin-lite and therefore must be inserted in the DOM.
      loadScriptIntoDOM(
        bodyElement,
        'https://code.jquery.com/jquery-1.12.1.min.js'
      )
      // Setup Aladin
      loadScriptIntoDOM(
        bodyElement,
        'https://aladin.u-strasbg.fr/AladinLite/api/v2/beta/aladin.min.js',
        () => {
          // When the import has succeded we store the aladin js instance into its component
          aladinObj.value = A.aladin(aladinDiv.value, {
            survey: survey.value,
            fov: props.fov,
            target: `${props.ra} ${props.dec}`,
          })
          // var HiPSCat = A.catalogHiPS(
          //   'https://api.rcsed2.voxastro.org/hips/HiPSCat_rcsed_v2/',
          //   { color: 'red' }
          // )
          // this.aladin.addCatalog(HiPSCat)
          aladinObj.value.createImageSurvey(
            'DES_DR2_color',
            'DES DR2',
            'https://desportal.cosmology.illinois.edu/data/releases/y6a1_coadd/images/aladin/irg/',
            'equatorial',
            11,
            { imgFormat: 'png' }
          )
          aladinObj.value.createImageSurvey(
            'unWISE_color',
            'unWISE',
            'https://alasky.u-strasbg.fr/unWISE/color-W2-W1W2-W1/',
            'equatorial',
            8,
            { imgFormat: 'jpg' }
          )
          aladinObj.value.createImageSurvey(
            'CDS_P_ZTF_DR7_color',
            'ZTF',
            'https://alasky.u-strasbg.fr/ZTF/DR7/CDS_P_ZTF_DR7_color/',
            'equatorial',
            9,
            { imgFormat: 'png' }
          )

          // Plot region if provided
          if (props.fov_arrays) {
            let overlay = A.graphicOverlay({
              color: '#ee2345',
              lineWidth: 0.5,
            })
            aladinObj.value.addOverlay(overlay)
            props.fov_arrays.forEach((fov_array) => {
              overlay.add(A.polyline(fov_array))
            })
          }

          //   aladin.on('objectClicked', (object) =>
          //     aladin.$emit('aladinObjectClicked', object)
          //   )

          // on click event
          aladinObj.value.on('click', (object) => {
            context.emit('aladinOnClick', object)
          })

          // Catalog of sources. Used to show pointer
          aladinCatalog.value = A.catalog({ shape: 'plus', color: 'lightblue' })
          aladinObj.value.addCatalog(aladinCatalog.value)
          aladinASourceFunc.value = A.source
        }
      )
    })

    watchEffect(() => {
      if (aladinObj.value) {
        aladinObj.value.setImageSurvey(survey.value)
      }
    })

    watchEffect(() => {
      if (aladinCatalog.value) {
        // first check is there source in the list. If so, remove
        if (aladinSourceList.value.length > 0) {
          aladinCatalog.value.remove(aladinSourceList.value[0])
        }
        // add source into list
        aladinSourceList.value = props.pointer
          ? [aladinASourceFunc.value(props.pointer.ra, props.pointer.dec)]
          : []
        // upload source list to the catalog to be shown
        aladinCatalog.value.addSources(aladinSourceList.value)
      }
    })

    return { aladinDiv, survey }
  },
})
</script>

<style>
@import 'https://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.css';

.aladin-box {
  width: 100%;
  height: 100%;
  /* padding-bottom: 100%;
  position: relative; */
}
.toggle {
  border: 0 1px 1px 1px solid #e0e0e0;
  border-top-style: none;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  /* border-right-style: solid;
  border-bottom-style: dotted;
  border-left-style: solid; */
}
</style>
