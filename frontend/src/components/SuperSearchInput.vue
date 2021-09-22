<template>
  <q-form @submit="submitQuery">
    <q-input
      ref="queryInput"
      outlined
      autofocus
      standout
      v-bind="$attrs"
      :value="querySuggestion"
      type="search"
      @keyup="keyup"
      @keydown.9.prevent
      @keydown.38.prevent
      @keydown.40.prevent
      @keydown.13.prevent
      @input.native="input"
    >
      <q-menu
        v-model="showingMenu"
        no-parent-event
        no-focus
        fit
        ref="menu"
        max-height="250px"
      >
        <q-list dense style="min-width: 100px">
          <q-item
            v-for="op in optionsSelected"
            :key="op"
            v-close-popup
            :active="op == optionsSelected[menuSelectedPosition]"
            active-class="bg-deep-purple-1 text-grey-8"
            @mouseover="mouseover(op)"
          >
            <q-item-section>{{ op }}</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
      <template v-slot:append>
        <q-btn flat round @click="submitQuery"
          ><q-icon name="search" style="font-size: 24px;"
        /></q-btn>
      </template>
    </q-input>
  </q-form>
</template>

<script>
import Vuex from 'vuex'

const fullOptions = [
  // main table
  'r2id_spec',
  'survey',
  'ra_j2000',
  'dec_j2000',
  'z',
  'z_err',
  'z_q',
  'sdss_mjd',
  'sdss_plate',
  'sdss_fiberid',
  'twodf_seqnum',
  'sixdf_specid',
  'uzc_zname',
  'cfa_rfn',
  'hectospec_date',
  'hectospec_dataset',
  'hectospec_spec',
  'lamost_obsid',
  'lamost_planid',
  'lamost_obsdate',
  'lamost_lmjd',
  'lamost_spid',
  'lamost_fiberid',
  'lega_c_spectid',
  'deep2_objno',
  'deep3_objno',
  'wigglez_specfile',
  'gama_specid',
  'twodflens_target',
  'obj',
  // Obj Table
  'obj.r2id_obj',
  'obj.size_survey',
  'obj.objid_nsc',
  'obj.objid',
  'obj.ra_obj',
  'obj.dec_obj',
  'obj.amaj',
  'obj.ell',
  'obj.pa',
  // PhotAper Table
  'phot_aper.r2id_spec',
  'phot_aper.source',
  'phot_aper.aper_size',
  'phot_aper.fuv',
  'phot_aper.fuv_err',
  'phot_aper.kcorr_fuv',
  'phot_aper.nuv',
  'phot_aper.nuv_err',
  'phot_aper.kcorr_nuv',
  'phot_aper.u',
  'phot_aper.u_err',
  'phot_aper.kcorr_u',
  'phot_aper.g',
  'phot_aper.g_err',
  'phot_aper.kcorr_g',
  'phot_aper.r',
  'phot_aper.r_err',
  'phot_aper.kcorr_r',
  'phot_aper.i',
  'phot_aper.i_err',
  'phot_aper.kcorr_i',
  'phot_aper.z',
  'phot_aper.z_err',
  'phot_aper.kcorr_z',
  'phot_aper.y',
  'phot_aper.y_err',
  'phot_aper.kcorr_y',
  'phot_aper.j',
  'phot_aper.j_err',
  'phot_aper.kcorr_j',
  'phot_aper.h',
  'phot_aper.h_err',
  'phot_aper.kcorr_h',
  'phot_aper.k',
  'phot_aper.k_err',
  'phot_aper.kcorr_k',
  'phot_aper.w1',
  'phot_aper.w1_err',
  'phot_aper.kcorr_w1',
  'phot_aper.w2',
  'phot_aper.w2_err',
  'phot_aper.kcorr_w2',
  'phot_aper.w3',
  'phot_aper.w3_err',
  'phot_aper.kcorr_w3',
  'phot_aper.w4',
  'phot_aper.w4_err',
  'phot_aper.kcorr_w4',
  // PhotTot
  'obj.phot_tot.r2id_obj',
  'obj.phot_tot.source',
  'obj.phot_tot.mag_type',
  'obj.phot_tot.fuv',
  'obj.phot_tot.fuv_err',
  'obj.phot_tot.fuv_size',
  'obj.phot_tot.kcorr_fuv',
  'obj.phot_tot.nuv',
  'obj.phot_tot.nuv_err',
  'obj.phot_tot.nuv_size',
  'obj.phot_tot.kcorr_nuv',
  'obj.phot_tot.u',
  'obj.phot_tot.u_err',
  'obj.phot_tot.u_size',
  'obj.phot_tot.kcorr_u',
  'obj.phot_tot.g',
  'obj.phot_tot.g_err',
  'obj.phot_tot.g_size',
  'obj.phot_tot.kcorr_g',
  'obj.phot_tot.r',
  'obj.phot_tot.r_err',
  'obj.phot_tot.r_size',
  'obj.phot_tot.kcorr_r',
  'obj.phot_tot.i',
  'obj.phot_tot.i_err',
  'obj.phot_tot.i_size',
  'obj.phot_tot.kcorr_i',
  'obj.phot_tot.z',
  'obj.phot_tot.z_err',
  'obj.phot_tot.z_size',
  'obj.phot_tot.kcorr_z',
  'obj.phot_tot.y',
  'obj.phot_tot.y_err',
  'obj.phot_tot.y_size',
  'obj.phot_tot.kcorr_y',
  'obj.phot_tot.j',
  'obj.phot_tot.j_err',
  'obj.phot_tot.j_size',
  'obj.phot_tot.kcorr_j',
  'obj.phot_tot.h',
  'obj.phot_tot.h_err',
  'obj.phot_tot.h_size',
  'obj.phot_tot.kcorr_h',
  'obj.phot_tot.k',
  'obj.phot_tot.k_err',
  'obj.phot_tot.k_size',
  'obj.phot_tot.kcorr_k',
  'obj.phot_tot.w1',
  'obj.phot_tot.w1_err',
  'obj.phot_tot.w1_size',
  'obj.phot_tot.kcorr_w1',
  'obj.phot_tot.w2',
  'obj.phot_tot.w2_err',
  'obj.phot_tot.w2_size',
  'obj.phot_tot.kcorr_w2',
]

const analyseQueryString = (query, delimiter, cursorPosition) => {
  const query_splitted = query.split(delimiter)
  const string_tokens = query_splitted
    .map((v, i) => `${i}`.repeat(v.length))
    .join(delimiter)

  const string_indices = query_splitted
    .map((v, i) => [...Array(v.length).keys()].map(v => String(v)).join(''))
    .join(delimiter)

  const token_selected = string_tokens[cursorPosition - 1]
  const index_selected = string_indices[cursorPosition - 1]

  const token =
    typeof query_splitted[token_selected] === 'undefined'
      ? null
      : query_splitted[token_selected]

  return {
    token: token,
    token_selected: token_selected == ' ' ? null : Number(token_selected),
    index_selected: index_selected == ' ' ? null : Number(index_selected),
    query_splitted: query_splitted,
  }
}

export default {
  name: 'SuperSearchInput',
  data: function() {
    return {
      options: fullOptions,
      menuSelectedPosition: 0,
      showingMenu: false,
      token: null,
      queryTokens: null,
      queryTokenID: null,
      cursorPosition: 0,
      previousSuggestion: '',
      querySuggestion2: null,
      querySuggestion: null,
    }
  },
  beforeMount: function() {
    this.querySuggestion = this.queryString
  },
  computed: {
    queryString: {
      get() {
        return this.$store.state.queryString
      },
      set(value) {
        return this.$store.commit('setQueryString', value)
      },
    },
    ...Vuex.mapState(['tableStatus', 'tableData']),
    inputElement: function() {
      return this.$refs.queryInput.$refs.input
    },
    optionsSelected: function() {
      if (this.token === null) {
        return null
      } else {
        const needle = this.token.toLowerCase()
        // return fullOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
        return fullOptions.filter(v => v.toLowerCase().startsWith(needle))
      }
    },
    suggestion: function() {
      if (this.token === null) {
        return null
      } else {
        return this.optionsSelected.length > 0
          ? this.optionsSelected[this.menuSelectedPosition]
          : null
      }
    },
  },
  watch: {
    token() {
      if (this.token) {
        this.menuSelectedPosition = 0
      }
    },
    suggestion(newValue, oldValue) {
      this.previousSuggestion = oldValue

      if (this.suggestion) {
        const missingPart = this.suggestion.slice(this.token.length)
        const missingPartLast = this.previousSuggestion
          ? this.previousSuggestion.slice(this.token.length)
          : ''

        const q = analyseQueryString(
          this.querySuggestion,
          ' ',
          this.inputElement.selectionStart
        )

        this.inputElement.setRangeText(
          missingPart,
          this.inputElement.selectionStart,
          this.inputElement.selectionEnd,
          'select'
        )

        this.querySuggestion = this.inputElement.value
      }
    },
    queryString() {
      this.querySuggestion = this.queryString
      this.$forceUpdate()
      this.inputElement.focus()
    },
  },
  methods: {
    submitQuery() {
      if (this.tableStatus == 'loading') {
        console.log('Previous request is not finished yet!')
      } else {
        console.log('Submit Search Query', this.queryString)

        this.$store.dispatch('resolveQuery')
        // this.$store.dispatch('fetchTable')

        this.$router.push(
          {
            path: '/catalog',
            query: { q: this.queryString },
          },
          () => {}
        )
      }
    },

    analyseQuery() {
      const q = analyseQueryString(
        this.queryString,
        ' ',
        this.inputElement.selectionStart
      )

      this.token = q.token
      this.queryTokenID = q.token_selected
      this.queryTokens = q.query_splitted
    },

    mouseover(op) {
      this.menuSelectedPosition = this.optionsSelected.indexOf(op)
    },

    input(event) {
      this.queryString = event.target.value
      this.querySuggestion = event.target.value
      this.cursorPosition = this.inputElement.selectionStart
      console.log('kuku')
    },

    keyup(event) {
      this.analyseQuery()

      this.showingMenu = this.suggestion ? true : false

      // submit query
      if (event.key == 'Enter' && this.showingMenu === false) {
        this.submitQuery()
      }

      // before treat ArrowDown and ArrowDown we blocked keydown 38 and 40.
      // See used directives in the q-input

      // taping ArrowUp/ArrowDown we change selected option in the menu
      if (event.key == 'ArrowDown' && this.optionsSelected) {
        this.menuSelectedPosition =
          (this.menuSelectedPosition + 1) % this.optionsSelected.length
      }
      if (event.key == 'ArrowUp' && this.optionsSelected) {
        this.menuSelectedPosition =
          this.menuSelectedPosition == 0
            ? this.optionsSelected.length - 1
            : this.menuSelectedPosition - 1
      }

      const actionKeys = ['Enter', 'Tab']
      if (actionKeys.includes(event.key) && this.showingMenu) {
        this.inputElement.focus()
        this.inputElement.setSelectionRange(
          this.querySuggestion.length,
          this.querySuggestion.length
        )
        this.showingMenu = false
        this.queryString = this.querySuggestion
      }
    },
  },
}
</script>
