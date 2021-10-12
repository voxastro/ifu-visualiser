import { store } from 'quasar/wrappers'
import Vuex from 'vuex'
// import Vue from 'vue'

import moduleApp from './moduleApp'

// Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

const Store = new Vuex.Store({
  // modules: {
  //   moduleApp,
  // },
  ...moduleApp,

  // enable strict mode (adds overhead!)
  // for dev mode and --debug builds only
  strict: process.env.DEBUGGING,
})

export default store(function (/* { ssrContext } */) {
  Store.dispatch('loadSchema')
  return Store
})

export { Store }
