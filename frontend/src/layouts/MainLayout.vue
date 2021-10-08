<template>
  <q-layout view="lHh LpR fff">
    <q-toolbar class="text-white shadow-3 toolbar">
      <router-link
        to="/"
        class="voxastro-font-logo text-h5 text-white"
        style="cursor: pointer; text-decoration: none"
      >
        <div class="row items-center">
          <img
            alt="IFU visualiser logo"
            src="~assets/logo_IFU.svg"
            style="width: 30px; height: 30px"
            class="q-mr-sm"
          />
          IFU Visualiser
        </div>
      </router-link>
      <!-- </q-toolbar-title> -->

      <!-- <SuperSearchInput
        v-if="
          $route.path.includes('data') |
            $route.path.includes('docs') |
            $route.path.includes('about')
        "
        input-style="font-size: 14px"
        dark
        dense
        standout
        color="grey-12"
        class="col-grow text-white q-mx-xl gt-sm"
        style="min-width: 350px"
      /> -->
      <q-space
        v-if="
          $route.path.includes('visualiser') |
            $route.path.includes('docs') |
            $route.path.includes('about')
        "
      />
      <q-space />
      <q-space class="lt-md" />

      <q-tabs v-model="tab" no-caps class="gt-xs">
        <q-route-tab to="/" exact name="home" label="Home"></q-route-tab>
        <q-route-tab
          :to="{ path: '/search', query: { q: queryString } }"
          name="search"
          label="Search"
        ></q-route-tab>
        <q-route-tab
          to="/visualiser"
          name="visualiser"
          label="Visualiser"
        ></q-route-tab>
        <q-route-tab to="/docs" name="docs" label="Docs"></q-route-tab>
        <q-route-tab to="/about" name="about" label="About"></q-route-tab>
      </q-tabs>
      <q-space class="lt-sm" />
      <q-btn
        dense
        flat
        round
        icon="menu"
        @click="toggleRightDrawer"
        class="lt-sm"
      />
    </q-toolbar>

    <q-drawer v-model="rightDrawerOpen" side="right" bordered :width="150">
      <q-item to="/" exact>
        <q-item-section>Home</q-item-section>
      </q-item>
      <q-item :to="{ path: '/search', query: { q: queryString } }">
        <q-item-section>Search</q-item-section>
      </q-item>
      <q-item to="/visualiser">
        <q-item-section>Visualiser</q-item-section>
      </q-item>
      <q-item to="/docs">
        <q-item-section>Docs</q-item-section>
      </q-item>
      <q-item to="/about">
        <q-item-section>About</q-item-section>
      </q-item>
    </q-drawer>

    <q-page-container>
      <q-page>
        <!-- <q-page-sticky expand position="top-left"> -->
        <router-view />
        <q-page-scroller
          position="bottom-right"
          :scroll-offset="150"
          :offset="[18, 18]"
        >
          <q-btn round icon="keyboard_arrow_up" color="primary" size="md" />
        </q-page-scroller>
      </q-page>
      <!-- </q-page-sticky> -->
    </q-page-container>

    <q-footer elevated>
      <div class="text-white footer row justify-center items-center">
        <div class="col text-center">
          &copy; 2021 by
          <!-- <router-link :to="{ name: 'about' }" class="text-white">the Team</router-link> -->
          <a href="about/" class="text-white">the Team</a>
        </div>
      </div>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'MainLayout',

  components: {
    // EssentialLink,
  },

  setup() {
    const store = useStore()
    const rightDrawerOpen = ref(false)
    const tab = ref('home')

    const queryString = computed(() => store.state.queryString)

    return {
      rightDrawerOpen,
      tab,
      queryString,
      toggleRightDrawer() {
        rightDrawerOpen.value = !rightDrawerOpen.value
      },
    }
  },
})
</script>

<style lang="scss">
.toolbar {
  padding: 0px 8.33vw;
  height: 50px;
  background: linear-gradient(45deg, #808588, #2c3e50);
  // background-position: center 0;
  // background-repeat: no-repeat;
  // background-size: cover;
  z-index: 1;
}

.footer {
  // padding: 0px 8.33vw;
  height: 40px;
  background: linear-gradient(45deg, #808588, #2c3e50);
  // background-position: center 0;
  // background-repeat: no-repeat;
  // background-size: cover;
  z-index: 1;
}
</style>
